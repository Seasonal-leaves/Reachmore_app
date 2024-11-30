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
    <!-- Delete Button at Top Right -->
    <button
        v-if="adRequest.status === 'Pending' || adRequest.status === 'Negotiated'"
        @click="confirmDeleteAdRequest(adRequest.id)"
        class="btn btn-danger btn-sm position-absolute top-0 end-0"
        title="Delete Ad Request"
      >
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
  <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
  <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
</svg>
    
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
<div v-if="showDeleteModal" class="modal-backdrop">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Confirm Delete</h5>
        <button type="button" class="btn-close" @click="closeDeleteModal"></button>
      </div>
      <div class="modal-body">
        <p>Are you sure you want to delete this ad request? This action is irreversible.</p>
      </div>
      <div class="modal-footer">
        <button class="btn btn-danger" @click="deleteAdRequest">Confirm Delete</button>
        <button class="btn btn-secondary" @click="closeDeleteModal">Cancel</button>
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
const showDeleteModal = ref(false);
const adRequestToDelete = ref(null);
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
// Open Delete Modal
function confirmDeleteAdRequest(adRequestId) {
  adRequestToDelete.value = adRequestId;
  showDeleteModal.value = true;
}

// Close Delete Modal
function closeDeleteModal() {
  showDeleteModal.value = false;
  adRequestToDelete.value = null;
}

// Delete Ad Request
async function deleteAdRequest() {
  try {
    const response = await fetch(
      `${authStore.getBackendServerURL()}/sponsor/delete-adrequest/${adRequestToDelete.value}`,
      {
        method: "DELETE",
        headers: {
          "Authentication-Token": authStore.getAuthToken(),
        },
      }
    );
    const data = await response.json();
    if (response.ok) {
      messageStore.setFlashMessage(data.message, "success");
      fetchAdRequests(); // Refresh the ad requests list
      closeDeleteModal();
    } else {
      messageStore.setFlashMessage(data.message || "Failed to delete ad request.", "error");
    }
  } catch (error) {
    console.error("Error deleting ad request:", error);
    messageStore.setFlashMessage("An error occurred while deleting the ad request.", "error");
  }
}


  onMounted(fetchAdRequests);
  </script>
  