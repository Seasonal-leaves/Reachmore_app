<template>
    <div class="container mt-5">
      <h1 class="text-center mb-4">{{ isAuthenticated ? "All Campaigns" : "Welcome to Reachmore!" }}</h1>
  
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
  
      <div v-else>
        <div v-if="campaigns.length === 0" class="text-center">
          <p>No campaigns available.</p>
        </div>
        <div v-else>
          <div class="row">
            <div
              v-for="campaign in campaigns"
              :key="campaign.id"
              class="col-md-4 mb-4"
            >
              <div class="card">
                <div class="card-body">
                  <h5 class="card-title">{{ campaign.name }}</h5>
                  <p class="card-text">{{ campaign.description }}</p>
                  <p class="card-text"><small class="text-muted">Start Date: {{ campaign.start_date }}</small></p>
                  <p class="card-text"><small class="text-muted">Budget: ₹{{ campaign.budget }}</small></p>
                      <!-- Sponsor Button -->

                      <button
        v-if="isSponsor"
        @click="confirmDelete(campaign.id)"
        class="btn btn-danger btn-sm position-absolute top-0 end-0"
        title="Delete Campaign"
      >
        🗑️
      </button>

                      <button
  v-if="isSponsor"
  class="btn btn-secondary mt-2"
  @click="editCampaign(campaign.id)"
>
  Edit Campaign
</button>
                <button
                  v-if="isSponsor"
                  @click="createAdRequest(campaign.id)"
                  class="btn btn-primary"
                >
                  Create Ad Request
                </button>
                <!-- Influencer Button -->
                <button
                  v-if="isInfluencer"
                  @click="makeAdRequest(campaign.id)"
                  class="btn btn-outline-success"
                >
                  Make Ad Request
                </button>
                </div>
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
        <button type="button" class="btn-close" @click="closeDeleteModal" aria-label="Close"></button>
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


  </template>
  
  <script setup>
  import { ref, onMounted, computed } from "vue";
  import { useAuthStore } from "@/stores/auth_store";
  import { useMessageStore } from "@/stores/messageStore";
  import { useRouter } from 'vue-router';

const router = useRouter();
  const authStore = useAuthStore();
  const messageStore = useMessageStore();
  
  // Reactive values
  const isAuthenticated = computed(() => authStore.isAuthenticated);
  const isSponsor = computed(() => authStore.isSponsor());
  const isInfluencer = computed(() => authStore.isInfluencer());
  const campaigns = ref([]);
  
// State for delete modal
const showDeleteModal = ref(false);
const campaignToDelete = ref(null);

  // Fetch campaigns on mount
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

  function confirmDelete(campaignId) {
  campaignToDelete.value = campaignId;
  showDeleteModal.value = true;
}
  
async function deleteCampaign() {
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
      fetchCampaigns(); // Refresh the campaigns list
      closeDeleteModal();
    } else {
      messageStore.setFlashMessage(data.message || "Failed to delete campaign.", "error");
    }
  } catch (error) {
    console.error("Error deleting campaign:", error);
    messageStore.setFlashMessage("An error occurred while deleting the campaign.", "error");
  }
}

function closeDeleteModal() {
  showDeleteModal.value = false;
  campaignToDelete.value = null;
}
  function createAdRequest(campaignId) {
    // Add logic to handle creating ad requests
    console.log("Creating ad request for campaign:", campaignId);
  }

  function editCampaign(campaignId) {
  router.push(`/sponsor/edit-campaign/${campaignId}`);
}
  
  onMounted(() => {
    if (isAuthenticated.value) {
      fetchCampaigns();
    }
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
  