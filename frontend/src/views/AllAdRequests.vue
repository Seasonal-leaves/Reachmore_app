<template>
    <div class="container mt-5">
      <h1 class="text-center">All Ad Requests</h1>
      <div v-if="adRequests.length === 0" class="text-center">
        <p>No ad requests found.</p>
      </div>
      <div v-else class="row">
        <div v-for="adRequest in adRequests" :key="adRequest.id" class="col-md-6 mb-4">
          <div class="card h-100">
            <div class="card-body">
              <h5 class="card-title">Ad Request for {{ adRequest.campaign_name }}</h5>
              <p><strong>Influencer:</strong> {{ adRequest.influencer_name }}</p>
              <p><strong>Requirements:</strong> {{ adRequest.requirements }}</p>
              <p><strong>Messages:</strong> {{ adRequest.messages || 'No messages' }}</p>
              <p><strong>Payment:</strong> ₹{{ adRequest.payment_amount }}</p>
              <p><strong>Status:</strong> {{ adRequest.status }}</p>
              <div>
  <button
    v-if="isSponsor && adRequest.status === 'Pending'"
    @click="openUpdateAdRequestModal(adRequest)"
    class="btn btn-warning btn-sm"
  >
    Update Ad Request
  </button>
</div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- Update Ad Request Modal -->
<div v-if="showUpdateAdRequestModal" class="modal-backdrop">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Update Ad Request</h5>
        <button type="button" class="btn-close" @click="closeUpdateAdRequestModal"></button>
      </div>
      <div class="modal-body">
        <div class="mb-3">
          <label for="requirements" class="form-label">Requirements</label>
          <textarea
            v-model="adRequestRequirements"
            class="form-control"
            id="requirements"
            placeholder="Enter updated requirements"
          ></textarea>
        </div>
        <div class="mb-3">
          <label for="paymentAmount" class="form-label">Payment Amount</label>
          <input
            type="number"
            v-model="paymentAmount"
            class="form-control"
            id="paymentAmount"
            placeholder="Enter updated payment amount"
          />
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn btn-secondary" @click="closeUpdateAdRequestModal">Close</button>
        <button class="btn btn-success" @click="submitUpdateAdRequest">Save Changes</button>
      </div>
    </div>
  </div>
</div>

  </template>
  
  <script setup>
  import { ref, computed, onMounted } from "vue";
  import { useAuthStore } from "@/stores/auth_store";
  import { useMessageStore } from "@/stores/messageStore";
  
  const authStore = useAuthStore();
  const messageStore = useMessageStore();
  const isSponsor = computed(() => authStore.isSponsor());
  const adRequests = ref([]);
  const paymentAmount = ref(null);
  const adRequestRequirements = ref("");
  const showUpdateAdRequestModal = ref(false);
const selectedAdRequestId = ref(null);
  // Fetch all ad requests
  async function fetchAdRequests() {
    try {
      const response = await fetch(
        `${authStore.getBackendServerURL()}/sponsor/view-adrequest`,
        {
          headers: {
            "Content-Type": "application/json",
            "Authentication-Token": authStore.getAuthToken(),
          },
        }
      );
  
      const data = await response.json();
      if (response.ok) {
        adRequests.value = data.ad_requests;
      } else {
        messageStore.setFlashMessage(data.message || "Failed to fetch ad requests.", "error");
      }
    } catch (error) {
      console.error("Error fetching ad requests:", error);
      messageStore.setFlashMessage("An error occurred while fetching ad requests.", "error");
    }
  }
  // Open Update Modal
function openUpdateAdRequestModal(adRequest) {
  selectedAdRequestId.value = adRequest.id;
  adRequestRequirements.value = adRequest.requirements;
  paymentAmount.value = adRequest.payment_amount;
  showUpdateAdRequestModal.value = true;
}

// Close Update Modal
function closeUpdateAdRequestModal() {
  showUpdateAdRequestModal.value = false;
  selectedAdRequestId.value = null;
  adRequestRequirements.value = "";
  paymentAmount.value = null;
}

// Submit Updated Ad Request
async function submitUpdateAdRequest() {
  try {
    await updateAdRequest(selectedAdRequestId.value); // Call the update function
    closeUpdateAdRequestModal(); // Close the modal
  } catch (error) {
    console.error("Error submitting updated ad request:", error);
  }
}
async function updateAdRequest(adRequestId) {
  try {
    const payload = {
      requirements: adRequestRequirements.value,
      payment_amount: parseFloat(paymentAmount.value),
    };
    const response = await fetch(
      `${authStore.getBackendServerURL()}/sponsor/update-adrequest/${adRequestId}`,
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": authStore.getAuthToken(),
        },
        body: JSON.stringify(payload),
      }
    );
    const data = await response.json();
    if (response.ok) {
      messageStore.setFlashMessage(data.message, "success");
      fetchAdRequests(); // Refresh ad requests
    } else {
      messageStore.setFlashMessage(data.message || "Failed to update ad request.", "error");
    }
  } catch (error) {
    console.error("Error updating ad request:", error);
    messageStore.setFlashMessage("An error occurred while updating ad request.", "error");
  }
}

  onMounted(fetchAdRequests);
  </script>
  