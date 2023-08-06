#include <absl/memory/memory.h>
#include <synapse_api.h>

#include "hccl_integration.h"
#include "hccl_operations.h"

namespace horovod {
namespace common {

OrderingGroup&
OrderedOpContext::GetOrderingGroup(std::set<int> ordering_indices,
                                   std::vector<int32_t> device_map) {
  if (ordering_groups_.end() == ordering_groups_.find(ordering_indices)) {
    OrderingGroup ordering_group(ordering_indices.size(), device_map);
    ordering_groups_.emplace(
        std::make_pair(ordering_indices, std::move(ordering_group)));
  }
  return ordering_groups_.at(ordering_indices);
}

void OrderingGroup::CreateQueueItem(OrderingQueueKey new_key) {
  auto item = std::make_shared<OrderingQueueItem>(new_key);
  LOG(TRACE) << "Adding empty order index entry " << new_key.first;
  HCCL_OP_ASSERT(ordering_queue_items_.end() ==
                 ordering_queue_items_.find(new_key.first));
  ordering_queue_items_[new_key.first] = item;
  HCCL_OP_ASSERT(ordering_queue_.end() == ordering_queue_.find(new_key));
  ordering_queue_[new_key] = item;
}

void OrderingGroup::FillQueueItem(int64_t order_index,
                                  TensorTableEntry&& entry) {
  LOG(DEBUG) << "Filling empty order index entry " << order_index;
  ordering_queue_items_[order_index]->tensor_entry = std::move(entry);
  ordering_queue_items_[order_index]->ready = true;
  ordering_queue_items_[order_index]->sent = false;
}

void OrderedOpContext::RemoveOrderingGroupIfCompleted(std::set<int> indices) {
  if (ordering_groups_.at(indices).group_completed()) {
    ordering_groups_.erase(indices);
  }
}

void OrderingGroup::AddEntry(TensorTableEntry& entry) {

  int64_t order_index = entry.order_index;
  int64_t execution_order;

  // TODO: group should be stored per device list
  if (0 == ordering_queue_.size()) {
    for (int64_t new_order_index : entry.group_order_indices) {
      hcclResult_t hcclx_result{
          hcclxGetExecutionOrder(new_order_index, &execution_order)};
      HCCL_OP_ASSERT(hcclSuccess == hcclx_result);
      OrderingQueueKey new_key;
      new_key.first = new_order_index;
      new_key.second = execution_order;
      LOG(TRACE) << "Execution order for order_index " << new_order_index
                 << " is " << execution_order;
      CreateQueueItem(new_key);
    }
  }

  FillQueueItem(order_index, std::move(entry));
}

std::vector<TensorTableEntry> OrderingGroup::GetEntriesToSchedule() {
  LOG(TRACE) << __PRETTY_FUNCTION__;
  std::vector<TensorTableEntry> entries;

  LOG(TRACE) << "Ordering queue size is: " << ordering_queue_.size();

  for (auto const& queue_iter : ordering_queue_) {
    OrderingQueueKey key = queue_iter.first;
    std::shared_ptr<OrderingQueueItem> item = queue_iter.second;

    if (!item->ready) {
      LOG(INFO) << "Waiting for item with order index " << key.first
                << " execution order " << key.second;
      break;
    }

    if (item->sent) {
      LOG(TRACE) << "Continuing...";
      continue;
    }

    entries.push_back(item->tensor_entry);

    item->sent = true;
    queue_items_sent_++;
    LOG(INFO) << "Marking as sent. order index: " << key.first
              << " exec order: " << key.second;
  }

  return entries;
}

std::vector<TensorTableEntry> OrderingGroup::GetEntriesToFinalize() {
  LOG(TRACE) << __PRETTY_FUNCTION__;
  std::vector<TensorTableEntry> entries;

  for (auto const& queue_iter : ordering_queue_) {
    OrderingQueueKey key = queue_iter.first;
    std::shared_ptr<OrderingQueueItem> item = queue_iter.second;

    if (false == item->sent) {
      break;
    }

    if (true == item->finalized) {
      continue;
    }

    entries.push_back(std::move(item->tensor_entry));
    LOG(INFO) << "Finalizng order index: " << key.first
              << " exec order: " << key.second;
    item->finalized = true;
  }

  return entries;
}

Status HCCLSignaledAllreduce::Execute(std::vector<TensorTableEntry>& entries,
                                      const Response& response) {
  auto& timeline = global_state_->timeline;

  timeline.ActivityStartAll(entries, HCCL_REORDERING);

  HCCL_OP_ASSERT(entries.size() == 1);

  auto entry = entries[0];
  std::set<int> indices = entry.group_order_indices;
  Status hvd_status{Status::InProgress()};

  {
    auto& ordering_group{
        ordered_op_context_.GetOrderingGroup(indices, response.devices())};
    ordering_group.AddEntry(entry);
    entries.clear();

    std::vector<TensorTableEntry> entries_to_schedule{
        ordering_group.GetEntriesToSchedule()};

    if (entries_to_schedule.size() > 0) {
      timeline.ActivityEndAll(entries_to_schedule);
      ScheduleAllreduce(entries_to_schedule, ordering_group.device_map());
      entries = ordering_group.GetEntriesToFinalize();
      if (entries.size() > 0) {
        hvd_status = op_context_.FinalizeDeviceQueue(entries);
      }
    }
  }
  ordered_op_context_.RemoveOrderingGroupIfCompleted(indices);
  return hvd_status;
}

void HCCLSignaledAllreduce::ScheduleAllreduce(
    std::vector<TensorTableEntry>& entries, std::vector<int32_t>& device_map) {
  LOG(TRACE) << "Entry " << __PRETTY_FUNCTION__;

  op_context_.InitCommunicator(entries, device_map);
  auto& timeline = global_state_->timeline;
  timeline.ActivityStartAll(entries, HCCL_ALLREDUCE);

  for (auto& entry : entries) {
    op_context_.InitDeviceQueue({entry}, op_context_.collective_stream());
    void* input_address;
    void* output_address;
    hcclResult_t hccl_result{hcclSuccess};

    hccl_result = hcclxLockDeviceAddress(
        const_cast<void*>(entry.tensor->data()), &input_address);
    HCCL_OP_ASSERT(hcclSuccess == hccl_result);
    hccl_result = hcclxLockDeviceAddress(
        const_cast<void*>(entry.output->data()), &output_address);
    HCCL_OP_ASSERT(hcclSuccess == hccl_result);

    hccl_result =
        hcclAllReduce(input_address, output_address,
                      (size_t)entry.tensor->shape().num_elements(),
                      GetHCCLDataType(entry.tensor->dtype()), hcclSum,
                      *op_context_.hccl_comm_, op_context_.collective_stream());

    hccl_result = hcclxUnlockDeviceAddress(input_address);
    HCCL_OP_ASSERT(hcclSuccess == hccl_result);
    hccl_result = hcclxUnlockDeviceAddress(output_address);
    HCCL_OP_ASSERT(hcclSuccess == hccl_result);
  }
}

bool HCCLSignaledAllreduce::Enabled(
    const ParameterManager& param_manager,
    const std::vector<TensorTableEntry>& entries,
    const Response& response) const {
  bool is_enabled = (entries[0].device != CPU_DEVICE_ID);
  LOG(TRACE) << "HCCLAllreduce is " << (is_enabled ? "enabled" : "disabled")
             << " for device: " << entries[0].device;
  return is_enabled;
}

} // namespace common
} // namespace horovod
