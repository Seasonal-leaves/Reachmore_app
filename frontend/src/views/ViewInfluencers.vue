<template>
    <div class="container mt-5">
      <h1 class="text-center mb-4">Available Influencers</h1>
  
      <!-- Search Bar -->
      <div class="row mb-4">
        <div class="col-md-12">
          <input
            type="text"
            v-model="searchQuery"
            class="form-control"
            placeholder="Search influencers by username, niche, category, or minimum reach..."
          />
        </div>
      </div>
  
      <!-- Influencer Results -->
      <div v-if="filteredInfluencers.length === 0" class="text-center">
        <p>No influencers match your search criteria.</p>
      </div>
      <div v-else class="row">
        <div
          v-for="influencer in filteredInfluencers"
          :key="influencer.user_id"
          class="col-md-4 mb-4"
        >
          <div class="card h-100">
            <div class="card-body">
              <h5 class="card-title">{{ influencer.username }}</h5>
              <p class="card-text"><strong>ID:</strong> {{ influencer.user_id }}</p>
              <p class="card-text"><strong>Email:</strong> {{ influencer.email }}</p>
              <p class="card-text"><strong>Niche:</strong> {{ influencer.niche }}</p>
              <p class="card-text"><strong>Category:</strong> {{ influencer.category }}</p>
              <p class="card-text"><strong>Reach:</strong> {{ influencer.reach }}</p>
              <!-- Create AdRequest Button -->
              <button
                class="btn btn-primary mt-3"
                @click="openAdRequestModal(influencer)"
              >
                Create AdRequest
              </button>
            </div>
          </div>
        </div>
      </div>
  
      <!-- AdRequest Modal -->
      <div
        class="modal fade"
        tabindex="-1"
        id="adRequestModal"
        aria-labelledby="adRequestModalLabel"
        aria-hidden="true"
      >
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="adRequestModalLabel">
                Create AdRequest for {{ selectedInfluencer?.username }}
              </h5>
              <button
                type="button"
                class="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="createAdRequest">
                <div class="mb-3">
                  <label for="campaignSelect" class="form-label">Select Campaign</label>
                  <select
                    id="campaignSelect"
                    v-model="selectedCampaignId"
                    class="form-select"
                    required
                  >
                    <option value="" disabled>Select a campaign</option>
                    <option
                      v-for="campaign in campaigns"
                      :key="campaign.id"
                      :value="campaign.id"
                    >
                      {{ campaign.name }}
                    </option>
                  </select>
                </div>
                <div class="mb-3">
                  <label for="requirements" class="form-label">Requirements</label>
                  <textarea
                    id="requirements"
                    v-model="adRequestRequirements"
                    class="form-control"
                    rows="3"
                    required
                  ></textarea>
                </div>
                <div class="mb-3">
                  <label for="paymentAmount" class="form-label">Payment Amount</label>
                  <input
                    type="number"
                    id="paymentAmount"
                    v-model="paymentAmount"
                    class="form-control"
                    min="1"
                    required
                  />
                </div>
                <div class="text-center">
                  <button type="submit" class="btn btn-success w-100">Submit</button>
                </div>
              </form>
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
  
  const authStore = useAuthStore();
  const messageStore = useMessageStore();
  const influencers = ref([]);
  const campaigns = ref([]);
  const searchQuery = ref("");
  
  // Modal state
  const selectedInfluencer = ref(null);
  const selectedCampaignId = ref(null);
  const adRequestRequirements = ref("");
  const paymentAmount = ref("");
  
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
        messageStore.setFlashMessage(
          data.message || "Failed to fetch influencers.",
          "error"
        );
      }
    } catch (error) {
      console.error("Error fetching influencers:", error);
      messageStore.setFlashMessage(
        "An error occurred while fetching influencers.",
        "error"
      );
    }
  }
  
  // Fetch campaigns
  async function fetchCampaigns() {
    try {
      const response = await fetch(
        `${authStore.getBackendServerURL()}/view-campaign`,
        {
          headers: {
            "Content-Type": "application/json",
            "Authentication-Token": authStore.getAuthToken(),
          },
        }
      );
      const data = await response.json();
      if (response.ok) {
        campaigns.value = data.campaigns;
      } else {
        messageStore.setFlashMessage(
          data.message || "Failed to fetch campaigns.",
          "error"
        );
      }
    } catch (error) {
      console.error("Error fetching campaigns:", error);
      messageStore.setFlashMessage(
        "An error occurred while fetching campaigns.",
        "error"
      );
    }
  }
  
  // Computed property for filtering influencers
  const filteredInfluencers = computed(() => {
    if (!searchQuery.value) {
      return influencers.value;
    }
    const numericQuery = parseInt(searchQuery.value, 10);
    if (!isNaN(numericQuery)) {
      return influencers.value.filter(
        (influencer) => influencer.reach >= numericQuery
      );
    } else {
      return influencers.value.filter(
        (influencer) =>
          influencer.username.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
          (influencer.niche &&
            influencer.niche.toLowerCase().includes(searchQuery.value.toLowerCase())) ||
          (influencer.category &&
            influencer.category.toLowerCase().includes(searchQuery.value.toLowerCase()))
      );
    }
  });
  
  // Open modal and set selected influencer
  function openAdRequestModal(influencer) {
    selectedInfluencer.value = influencer;
    selectedCampaignId.value = null;
    adRequestRequirements.value = "";
    paymentAmount.value = "";
    new bootstrap.Modal(document.getElementById("adRequestModal")).show();
  }
  
  
  async function createAdRequest() {
  try {
    const payload = {
      campaign_id: selectedCampaignId.value,
      influencer_id: selectedInfluencer.value.user_id,
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

      // Close the modal after successful submission
      const modalElement = document.getElementById("adRequestModal");
      const bootstrapModal = bootstrap.Modal.getInstance(modalElement);
      if (bootstrapModal) {
        bootstrapModal.hide();
      }
    } else {
      messageStore.setFlashMessage(data.message || "Failed to create AdRequest.", "error");
    }
  } catch (error) {
    console.error("Error creating AdRequest:", error);
    messageStore.setFlashMessage("An error occurred while creating AdRequest.", "error");
  }
}

  
  onMounted(() => {
    fetchInfluencers();
    fetchCampaigns();
  });
  </script>
  
  <style>
  .card {
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  .card-title {
    font-size: 1.25rem;
    font-weight: bold;
  }
  .card-text {
    margin-bottom: 0.5rem;
  }
  .form-control {
    margin-bottom: 1rem;
  }
  </style>
  