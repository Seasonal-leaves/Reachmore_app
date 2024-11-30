<template>
    <div class="container mt-5">
      <h1 class="text-center mb-4">{{ isAuthenticated ? "All Campaigns" : "Welcome to Reachmore!" }}</h1>
  
      <!-- Welcome Section for Unauthenticated Users -->
      <div v-if="!isAuthenticated" class="text-center">
        <p class="lead">
          Looking to grow your reach or make your brand the next big thing? Join <strong>Reachmore</strong> today!
        </p>
        <p>
          🧑‍🎤 <strong>Influencers:</strong> Get exciting ad campaigns and monetize your social media presence.<br />
          🏢 <strong>Sponsors:</strong> Collaborate with top influencers to showcase your brand to the right audience.
        </p>
        <p class="fst-italic">
          "Where sponsors and influencers meet to create magic! 🌟"
        </p>
        <router-link to="/register" class="btn btn-primary mx-2">Get Started</router-link>
        <router-link to="/login" class="btn btn-outline-secondary mx-2">Log In</router-link>
      </div>
  
      <!-- Campaign List -->

      
      <div v-else>
        <div class="container mt-5">
  <!-- <h1 class="text-center mb-4">All Campaigns</h1> -->

  <!-- Search Bar -->
  <div class="row mb-4">
    <div class="col-md-12">
      <input
        type="text"
        v-model="campaignsearchQuery"
        class="form-control"
        placeholder="Search campaigns by name, description, visibility, or minimum budget..."
      />
    </div>
  </div>



         <!-- Campaign Results -->
  <div v-if="filteredCampaigns.length === 0" class="text-center">
    <p>No campaigns match your search criteria.</p>
  </div>
  <div v-else class="row">
    <div
      v-for="campaign in filteredCampaigns"
      :key="campaign.id"
      class="col-md-4 mb-4"
    >
              <div class="card">
                <div class="card-body">
                  <h5 class="card-title">{{ campaign.name }}</h5>
                  <p class="card-text">{{ campaign.description }}</p>
                  <p class="card-text"><small class="text-muted">Start Date: {{ campaign.start_date }}</small></p>
                  <p class="card-text"><small class="text-muted">Budget: ₹{{ campaign.budget }}</small></p>
  
                <!-- Influencer Button -->
<button
  v-if="isInfluencer"
  @click="openInfluencerAdRequestModal(campaign.id)"
  class="btn btn-outline-success"
>
  Make Ad Request
</button>
                  <!-- Edit Campaign Button -->
                  <button
                    v-if="isSponsor"
                    class="btn btn-secondary mt-2"
                    @click="editCampaign(campaign.id)"
                  >
                    Edit Campaign
                  </button>
  
                  <!-- Delete Campaign Button -->
                  <button
                    v-if="isSponsor"
                    @click="confirmDelete(campaign.id)"
                    class="btn btn-danger btn-sm position-absolute top-0 end-0"
                    title="Delete Campaign"
                  >
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
  <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
  <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
</svg>
                  </button>
                  <button
  v-if="isSponsor"
  @click="viewCampaignAdRequests(campaign.id)"
  class="btn btn-outline-info mt-2"
>
  View Details
</button>
                  <!-- Create Ad Request Button -->
                  <button
                    v-if="isSponsor"
                    @click="openAdRequestModal(campaign.id)"
                    class="btn btn-primary"
                  >
                    Create Ad Request
                  </button>
                </div>
              </div>
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
        <p>Are you sure you want to delete this campaign? This action is irreversible.</p>
      </div>
      <div class="modal-footer">
        <button class="btn btn-danger" @click="deleteCampaign">Confirm Delete</button>
        <button class="btn btn-secondary" @click="closeDeleteModal">Go Back</button>
      </div>
    </div>
  </div>
</div>

      <!-- AdRequest Modal -->
      <div
        class="modal fade"
        id="adRequestModal"
        tabindex="-1"
        aria-labelledby="adRequestModalLabel"
        aria-hidden="true"
      >
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="adRequestModalLabel">Create Ad Request</h5>
              <button
                type="button"
                class="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div class="modal-body">
              <!-- Search Bar -->
              <input
                type="text"
                v-model="searchQuery"
                class="form-control mb-3"
                placeholder="Search influencers by name..."
              />
  
              <!-- Influencer Dropdown -->
              <select
                v-model="selectedInfluencerId"
                class="form-select mb-3"
              >
                <option v-for="influencer in filteredInfluencers" :key="influencer.user_id" :value="influencer.user_id">
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
              <button
                type="button"
                class="btn btn-secondary"
                data-bs-dismiss="modal"
              >
                Close
              </button>
              <button
                type="button"
                class="btn btn-primary"
                @click="createAdRequest"
              >
                Submit Ad Request
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
<!-- Influencer Modal -->
<div
  v-if="showInfluencerAdRequestModal"
  id="adRequestModalForInfluencer"
  class="modal-backdrop"
>
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Make Ad Request (Influencer)</h5>
        <button type="button" class="btn-close" @click="closeInfluencerAdRequestModal"></button>
      </div>
      <div class="modal-body">
        <!-- Influencer-specific ad request form -->
        <p>Form for influencers to make ad requests...</p>
        <!-- Requirements -->
        <div class="mb-3">
              <label for="requirements" class="form-label">Requirements</label>
              <textarea
                v-model="influencerAdRequestRequirements"
                class="form-control"
                id="requirements"
                placeholder="Enter ad request requirements"
              ></textarea>
            </div>
            <!-- Payment Amount -->
            <div class="mb-3">
              <label for="paymentAmount" class="form-label">Payment Amount</label>
              <input
                type="number"
                v-model="influencerPaymentAmount"
                class="form-control"
                id="paymentAmount"
                placeholder="Enter payment amount"
              />
            
          </div>
      </div>
      <div class="modal-footer">
        <button class="btn btn-secondary" @click="closeInfluencerAdRequestModal">Close</button>
        <button class="btn btn-success" @click="submitInfluencerAdRequest">Submit</button>
      </div>
    </div>
  </div>
</div>
     

  </template>
  
  <script setup>
  import { ref, onMounted, computed } from "vue";
  import { useAuthStore } from "@/stores/auth_store";
  import { useMessageStore } from "@/stores/messageStore";
  import { useRouter } from "vue-router";
  
  const router = useRouter();
  const authStore = useAuthStore();
  const messageStore = useMessageStore();
  
  const campaigns = ref([]);
  const influencers = ref([]);
  const campaignsearchQuery = ref("");
  const searchQuery = ref("");
  const selectedInfluencerId = ref(null);
  const showInfluencerAdRequestModal = ref(false);
  const selectedCampaignIdForInfluencer = ref(null);
  const influencerAdRequestRequirements = ref("");
const influencerPaymentAmount = ref(null);
  const adRequestRequirements = ref("");
  const paymentAmount = ref(null);
  const selectedCampaignId = ref(null);
  const showDeleteModal = ref(false);
const campaignToDelete = ref(null);
  
  const isAuthenticated = computed(() => authStore.isAuthenticated);
  const isSponsor = computed(() => authStore.isSponsor());
  const isInfluencer = computed(() => authStore.isInfluencer());
  const filteredInfluencers = computed(() => {
    if (!searchQuery.value) return influencers.value;
    return influencers.value.filter((influencer) =>
      influencer.username.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
  });
  
  // Fetch data
  async function fetchCampaigns() {
    try {
      const response = await fetch(`${authStore.getBackendServerURL()}/view-campaign`, {
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": authStore.getAuthToken(),
        },
      });
      const data = await response.json();
      if (response.ok) {
        campaigns.value = data.campaigns;
      } else {
        messageStore.setFlashMessage(data.message || "Failed to fetch campaigns.", "error");
      }
    } catch (error) {
      console.error("Error fetching campaigns:", error);
      messageStore.setFlashMessage("An error occurred while fetching campaigns.", "error");
    }
  }

  // Computed property for filtered campaigns
const filteredCampaigns = computed(() => {
  if (!campaignsearchQuery.value) {
    return campaigns.value;
  }

  const numericQuery = parseInt(campaignsearchQuery.value, 10);

  if (!isNaN(numericQuery)) {
    // Filter campaigns by minimum budget
    return campaigns.value.filter((campaign) => campaign.budget >= numericQuery);
  } else {
    // Filter campaigns by name, description, or visibility
    return campaigns.value.filter(
      (campaign) =>
        campaign.name.toLowerCase().includes(campaignsearchQuery.value.toLowerCase()) ||
        (campaign.description &&
          campaign.description.toLowerCase().includes(campaignsearchQuery.value.toLowerCase())) ||
        (campaign.visibility &&
          campaign.visibility.toLowerCase().includes(campaignsearchQuery.value.toLowerCase()))
    );
  }
});

  
  async function fetchInfluencers() {
    if (!authStore.isSponsor()) {
    // Do not fetch influencers if the user is not a sponsor
    return;
  }

    try {
      const response = await fetch(`${authStore.getBackendServerURL()}/sponsor/influencers`, {
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": authStore.getAuthToken(),
        },
      });
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
  
  // Edit Campaign
  function editCampaign(campaignId) {
    router.push(`/sponsor/edit-campaign/${campaignId}`);
  }
  
// Confirm delete modal
function confirmDelete(campaignId) {
  campaignToDelete.value = campaignId;
  showDeleteModal.value = true;
}
  
function closeDeleteModal() {
  campaignToDelete.value = null;
  showDeleteModal.value = false;
}
 
  
// Delete campaign
async function deleteCampaign() {
  if (!campaignToDelete.value) return;

  try {
    const response = await fetch(
      `${authStore.getBackendServerURL()}/sponsor/delete-campaign/${campaignToDelete.value}`,
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
      closeDeleteModal();
      fetchCampaigns(); // Refresh the campaigns after deletion
    } else {
      messageStore.setFlashMessage(data.message || "Failed to delete campaign.", "error");
    }
  } catch (error) {
    console.error("Error deleting campaign:", error);
    messageStore.setFlashMessage("An error occurred while deleting the campaign.", "error");
  }
}

  
  
  // Open AdRequest Modal
  function openAdRequestModal(campaignId) {
    selectedCampaignId.value = campaignId;
    const modal = new bootstrap.Modal(document.getElementById("adRequestModal"));
    modal.show();
  }
  function viewCampaignAdRequests(campaignId) {
  router.push({ path: `/sponsor/adrequests/${campaignId}` });
}
  // Create AdRequest
  async function createAdRequest() {
    try {
      const payload = {
        campaign_id: selectedCampaignId.value,
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
        const modal = bootstrap.Modal.getInstance(document.getElementById("adRequestModal"));
        if (modal) modal.hide();
      } else {
        messageStore.setFlashMessage(data.message || "Failed to create AdRequest.", "error");
      }
    } catch (error) {
      console.error("Error creating AdRequest:", error);
      messageStore.setFlashMessage("An error occurred while creating AdRequest.", "error");
    }
  }
  // Open Influencer Ad Request Modal
function openInfluencerAdRequestModal(campaignId) {
  selectedCampaignIdForInfluencer.value = campaignId;
  showInfluencerAdRequestModal.value = true;
}// Close Influencer Ad Request Modal
function closeInfluencerAdRequestModal() {
  showInfluencerAdRequestModal.value = false;
  influencerAdRequestRequirements.value = "";
  influencerPaymentAmount.value = null;
}

// Submit Influencer Ad Request
async function submitInfluencerAdRequest() {
  try {
    const payload = {
      requirements: influencerAdRequestRequirements.value,
      payment_amount: parseFloat(influencerPaymentAmount.value),
    };

    const response = await fetch(
      `${authStore.getBackendServerURL()}/influencer/create-adrequest/${selectedCampaignIdForInfluencer.value}`,
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
      showInfluencerAdRequestModal.value = false; // Close the modal
    } else {
      messageStore.setFlashMessage(data.message || "Failed to create AdRequest.", "error");
    }
  } catch (error) {
    console.error("Error creating Influencer AdRequest:", error);
    messageStore.setFlashMessage("An error occurred while creating AdRequest.", "error");
  }
}
  onMounted(() => {
    fetchCampaigns();
    fetchInfluencers();
  });
  </script>
  
  <style>
  .text-center {
    margin-top: 20px;
  }
  
  .fst-italic {
    font-style: italic;
  }
  
  .btn {
    margin-top: 10px;
  }
  
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
  
  .modal-content {
    background-color: #fff;
    border-radius: 5px;
    padding: 20px;
  }
  </style>
  