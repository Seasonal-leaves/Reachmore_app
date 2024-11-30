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
          <div class="card h-100">
            <div class="card-body">
              <h5 class="card-title">{{ adRequest.influencer_name }}</h5>
              <p class="card-text"><strong>Requirements:</strong> {{ adRequest.requirements }}</p>
              <p class="card-text"><strong>Payment:</strong> ₹{{ adRequest.payment_amount }}</p>
              <p class="card-text"><strong>Status:</strong> {{ adRequest.status }}</p>
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
  