<template>
    <div class="container mt-5">
      <h1 class="text-center mb-4">{{ campaignName }} - Ad Requests</h1>
  
      <!-- Create Ad Request Button -->
      <button
        v-if="isSponsor"
        @click="openAdRequestModal"
        class="btn btn-primary mb-4"
      >
        Create Ad Request
      </button>
  
      <!-- Ad Requests List -->
      <div v-if="adRequests.length === 0" class="text-center">
        <p>No ad requests for this campaign.</p>
      </div>
      <div v-else class="row">
        <div
          v-for="adRequest in adRequests"
          :key="adRequest.id"
          class="col-md-6 mb-4"
        >
        <div class="card h-100 position-relative">
    <div class="card-body">
      <!-- Delete Button at Top Right -->
      <button
        v-if="adRequest.status === 'Pending' || adRequest.status === 'Negotiated' || adRequest.status === 'Rejected'"
        @click="confirmDeleteAdRequest(adRequest.id)"
        class="btn btn-danger btn-sm position-absolute top-0 end-0"
        title="Delete Ad Request"
      >
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
  <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
  <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
</svg>
    
    </button>
              <h5 class="card-title">{{ adRequest.influencer_name }}</h5>
              <p class="card-text"><strong>Requirements:</strong> {{ adRequest.requirements }}</p>
              <p class="card-text"><strong>Payment:</strong> ₹{{ adRequest.payment_amount }}</p>
              <p class="card-text"><strong>Status:</strong> {{ adRequest.status }}</p>
              <!-- Update details button -->
<div>
  <button
    v-if="isSponsor && adRequest.status === 'Pending'"
    @click="openUpdateAdRequestModal(adRequest)"
    class="btn btn-warning btn-sm"
  >
    Update Ad Request
  </button>
  <button
      v-if="adRequest.status === 'Negotiated'"
      class="btn btn-success me-2"
      @click="respondToAdRequest(adRequest.id, 'Accepted')"
    >
      Accept
    </button>
    <button
      v-if="adRequest.status === 'Negotiated'"
      class="btn btn-danger me-2"
      @click="respondToAdRequest(adRequest.id, 'Rejected')"
    >
      Reject
    </button>
    <button
      v-if="adRequest.status === 'Negotiated'"
      class="btn btn-warning"
      @click="openNegotiateModal(adRequest)"
    >
      Negotiate
    </button>
</div>

            </div>
          </div>
        </div>
      </div>
  
      <!-- Ad Request Modal -->
      <div v-if="showAdRequestModal" class="modal-backdrop">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Create Ad Request</h5>
              <button type="button" class="btn-close" @click="closeAdRequestModal"></button>
            </div>
            <div class="modal-body">
              <!-- Search Bar -->
              <input
                type="text"
                v-model="searchQuery"
                class="form-control mb-3"
                placeholder="Search influencers..."
              />
  
              <!-- Influencer Dropdown -->
              <select
                v-model="selectedInfluencerId"
                class="form-select mb-3"
              >
                <option
                  v-for="influencer in filteredInfluencers"
                  :key="influencer.user_id"
                  :value="influencer.user_id"
                >
                  {{ influencer.username }}
                </option>
              </select>
  
              <!-- Additional Fields -->
              <div class="mb-3">
                <label for="requirements" class="form-label">Requirements</label>
                <textarea
                  v-model="adRequestRequirements"
                  class="form-control"
                  id="requirements"
                  placeholder="Enter ad request requirements"
                ></textarea>
              </div>
              <div class="mb-3">
                <label for="paymentAmount" class="form-label">Payment Amount</label>
                <input
                  type="number"
                  v-model="paymentAmount"
                  class="form-control"
                  id="paymentAmount"
                  placeholder="Enter payment amount"
                />
              </div>
            </div>
            <div class="modal-footer">
              <button class="btn btn-secondary" @click="closeAdRequestModal">Close</button>
              <button class="btn btn-primary" @click="createAdRequest">Submit Ad Request</button>
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

<!-- Negotiate modal -->
<div v-if="showNegotiateModal" class="modal-backdrop">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Negotiate Ad Request</h5>
        <button type="button" class="btn-close" @click="closeNegotiateModal"></button>
      </div>
      <div class="modal-body">
        <div class="mb-3">
          <label for="negotiationMessage" class="form-label">Message</label>
          <textarea
            v-model="negotiationMessage"
            class="form-control"
            id="negotiationMessage"
            placeholder="Enter negotiation message"
          ></textarea>
        </div>
        <div class="mb-3">
          <label for="negotiationAmount" class="form-label">Payment Amount</label>
          <input
            type="number"
            v-model="negotiationAmount"
            class="form-control"
            id="negotiationAmount"
            placeholder="Enter new payment amount"
          />
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn btn-secondary" @click="closeNegotiateModal">Close</button>
        <button class="btn btn-primary" @click="submitNegotiation">Submit</button>
      </div>
    </div>
  </div>
</div>

  </template>
  
  <script setup>
  import { ref, computed, onMounted } from "vue";
  import { useAuthStore } from "@/stores/auth_store";
  import { useMessageStore } from "@/stores/messageStore";
  import { useRoute } from "vue-router";
  
  // Store references
  const authStore = useAuthStore();
  const messageStore = useMessageStore();
  const route = useRoute();
  
  // Reactive data
  const campaignId = route.params.campaignId;
  const campaignName = ref("");
  const adRequests = ref([]);
  const influencers = ref([]);
  const searchQuery = ref("");
  const selectedInfluencerId = ref(null);
  const adRequestRequirements = ref("");
  const paymentAmount = ref(null);
  const showAdRequestModal = ref(false);
  const showUpdateAdRequestModal = ref(false);
const selectedAdRequestId = ref(null);
const showDeleteModal = ref(false);
const adRequestToDelete = ref(null);
const showNegotiateModal = ref(false);
const negotiationMessage = ref('');
const negotiationAmount = ref(null);
  // Computed properties
  const isSponsor = computed(() => authStore.isSponsor());
  const filteredInfluencers = computed(() => {
    if (!searchQuery.value) return influencers.value;
    return influencers.value.filter((influencer) =>
      influencer.username.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
  });
  
  // Fetch campaign ad requests
  async function fetchCampaignAdRequests() {
  try {
    const response = await fetch(
      `${authStore.getBackendServerURL()}/sponsor/view-adrequest?campaign_id=${campaignId}`,
      {
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": authStore.getAuthToken(),
        },
      }
    );
    const data = await response.json();
    if (response.ok) {
      // Update campaign name from the first ad request (all ad requests belong to the same campaign)
      campaignName.value = data.ad_requests[0]?.campaign_name || "Campaign";
      adRequests.value = data.ad_requests.map((request) => ({
        ...request,
        influencer_name: request.influencer_name || "Unknown",
      }));
    } else {
      messageStore.setFlashMessage(data.message || "Failed to fetch ad requests.", "error");
    }
  } catch (error) {
    console.error("Error fetching ad requests:", error);
    messageStore.setFlashMessage("An error occurred while fetching ad requests.", "error");
  }
}

  // Fetch influencers
  async function fetchInfluencers() {
    try {
      const response = await fetch(
        `${authStore.getBackendServerURL()}/sponsor/influencers`,
        {
          headers: {
            "Content-Type": "application/json",
            "Authentication-Token": authStore.getAuthToken(),
          },
        }
      );
      const data = await response.json();
      if (response.ok) {
        influencers.value = data.influencers;
      } else {
        messageStore.setFlashMessage(data.message || "Failed to fetch influencers.", "error");
      }
    } catch (error) {
      console.error("Error fetching influencers:", error);
      messageStore.setFlashMessage("An error occurred while fetching influencers.", "error");
    }
  }
  
  // Modal actions
  function openAdRequestModal() {
    showAdRequestModal.value = true;
  }
  function closeAdRequestModal() {
    showAdRequestModal.value = false;
    selectedInfluencerId.value = null;
    adRequestRequirements.value = "";
    paymentAmount.value = null;
  }
  
  // Create ad request
  async function createAdRequest() {
    try {
      const payload = {
        campaign_id: campaignId,
        influencer_id: selectedInfluencerId.value,
        requirements: adRequestRequirements.value,
        payment_amount: parseFloat(paymentAmount.value),
      };
      const response = await fetch(
        `${authStore.getBackendServerURL()}/sponsor/create-adrequest`,
        {
          method: "POST",
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
        closeAdRequestModal();
        fetchCampaignAdRequests(); // Refresh ad requests
      } else {
        messageStore.setFlashMessage(data.message || "Failed to create ad request.", "error");
      }
    } catch (error) {
      console.error("Error creating ad request:", error);
      messageStore.setFlashMessage("An error occurred while creating ad request.", "error");
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
      fetchCampaignAdRequests(); // Refresh ad requests
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
      fetchCampaignAdRequests(); // Refresh the ad requests list
      closeDeleteModal();
    } else {
      messageStore.setFlashMessage(data.message || "Failed to delete ad request.", "error");
    }
  } catch (error) {
    console.error("Error deleting ad request:", error);
    messageStore.setFlashMessage("An error occurred while deleting the ad request.", "error");
  }
}
// Open negotiation modal
function openNegotiateModal(adRequest) {
  selectedAdRequestId.value = adRequest.id;
  negotiationMessage.value = adRequest.messages || '';
  negotiationAmount.value = adRequest.payment_amount;
  showNegotiateModal.value = true;
}

// Close negotiation modal
function closeNegotiateModal() {
  showNegotiateModal.value = false;
  negotiationMessage.value = '';
  negotiationAmount.value = null;
}

// Respond to ad request
async function respondToAdRequest(adRequestId, status) {
  try {
    const payload = { status };
    const response = await fetch(
      `${authStore.getBackendServerURL()}/sponsor/respond-negotiation/${adRequestId}`,
      {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': authStore.getAuthToken(),
        },
        body: JSON.stringify(payload),
      }
    );
    const data = await response.json();
    if (response.ok) {
      messageStore.setFlashMessage(data.message, 'success');
      fetchCampaignAdRequests(); // Refresh the ad requests
    } else {
      messageStore.setFlashMessage(data.message || 'Failed to respond to ad request.', 'error');
    }
  } catch (error) {
    console.error('Error responding to ad request:', error);
    messageStore.setFlashMessage('An error occurred while responding to the ad request.', 'error');
  }
}

// Submit negotiation
async function submitNegotiation() {
  try {
    const payload = {
      status: 'Negotiated',
      payment_amount: parseFloat(negotiationAmount.value),
      message: negotiationMessage.value,
    };
    const response = await fetch(
      `${authStore.getBackendServerURL()}/sponsor/respond-negotiation/${selectedAdRequestId.value}`,
      {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': authStore.getAuthToken(),
        },
        body: JSON.stringify(payload),
      }
    );
    const data = await response.json();
    if (response.ok) {
      messageStore.setFlashMessage(data.message, 'success');
      closeNegotiateModal();
      fetchCampaignAdRequests(); // Refresh the ad requests
    } else {
      messageStore.setFlashMessage(data.message || 'Failed to negotiate.', 'error');
    }
  } catch (error) {
    console.error('Error submitting negotiation:', error);
    messageStore.setFlashMessage('An error occurred while negotiating.', 'error');
  }
}
  
  // Lifecycle hooks
  onMounted(() => {
    fetchCampaignAdRequests();
    fetchInfluencers();
  });
  </script>
  
  <style>
  .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1050;
  }
  
  .modal-dialog {
    width: 90%;
    max-width: 500px;
  }
  </style>
  