<template>
<div
  v-for="campaign in flaggedCampaigns"
  :key="campaign.id"
  class="col-md-6 mb-4"
>
  <div class="card h-100">
    <div class="card-body">
      <h5 class="card-title">{{ campaign.name }}</h5>
      <p class="card-text"><strong>ID:</strong> {{ campaign.id }}</p> <!-- Debugging -->
      <p class="card-text"><strong>Description:</strong> {{ campaign.description }}</p>
      <p class="card-text"><strong>Reason for Flagging:</strong> {{ campaign.reason }}</p>
      <p class="card-text"><strong>Start Date:</strong> {{ formatDate(campaign.start_date) }}</p>
      <p class="card-text">
        <strong>End Date:</strong> 
        {{ campaign.end_date ? formatDate(campaign.end_date) : "Ongoing" }}
      </p>
      <p class="card-text"><strong>Budget:</strong> ₹{{ campaign.budget }}</p>
      <p class="card-text"><strong>Visibility:</strong> {{ campaign.visibility }}</p>
      <p class="card-text"><strong>Goals:</strong> {{ campaign.goals }}</p>
      <p class="card-text"><strong>Flag ID:</strong> {{ campaign.flag_id }}</p> 
      <!-- Edit Campaign Button -->
      <button
        v-if="isSponsor"
        class="btn btn-secondary mt-2"
        @click="editCampaign(campaign.id)"
      >
        Edit Campaign
      </button>
    <!-- Update Resolve Flag Button -->

<button
v-if="isAdmin"
  class="btn btn-success mt-2"
  @click="resolveFlag(campaign.flag_id)"
>
  Resolve Flag
</button>
    </div>
  </div>
</div>

  </template>
  
  <script setup>
  import { ref, onMounted, computed } from "vue";
  import { useAuthStore } from "@/stores/auth_store";
  import { useRouter } from "vue-router";
  import { useMessageStore } from "@/stores/messageStore";
  
  const authStore = useAuthStore();
  const messageStore = useMessageStore();
  const router = useRouter();
  
  const flaggedCampaigns = ref([]);
  const isSponsor = computed(() => authStore.isSponsor());
  const isAdmin = computed(() => authStore.isAdmin());
  
  // Redirect if user is not admin or sponsor
  if (!authStore.isAdminOrSponsor()) {
    router.push("/unauthorized");
  }
  
  // Format date for display
  function formatDate(dateString) {
    const options = { year: "numeric", month: "long", day: "numeric" };
    return new Date(dateString).toLocaleDateString(undefined, options);
  }
  
  // Fetch flagged campaigns
  async function fetchFlaggedCampaigns() {
  try {
    const response = await fetch(`${authStore.getBackendServerURL()}/flagged-campaigns`, {
      headers: {
        "Content-Type": "application/json",
        "Authentication-Token": authStore.getAuthToken(),
      },
    });

    const data = await response.json();
    if (response.ok) {
      console.log("API Response for Flagged Campaigns:", data); // Debugging
      flaggedCampaigns.value = data.flagged_campaigns.map((campaign) => ({
        id: campaign.id,
        name: campaign.name,
        description: campaign.description,
        reason: campaign.reason,
        start_date: campaign.start_date,
        end_date: campaign.end_date,
        budget: campaign.budget,
        visibility: campaign.visibility,
        goals: campaign.goals,
        flag_id : campaign.flag_id,
      }));
    } else {
      messageStore.setFlashMessage(data.message || "Failed to fetch flagged campaigns.", "error");
    }
  } catch (error) {
    console.error("Error fetching flagged campaigns:", error);
    messageStore.setFlashMessage("An error occurred while fetching flagged campaigns.", "error");
  }
}



function editCampaign(campaignId) {
  if (!campaignId) {
    console.error("No campaign ID provided for editing.");
    messageStore.setFlashMessage("Invalid campaign ID. Cannot navigate.", "error");
    return;
  }

  console.log("Navigating to:", `/sponsor/edit-campaign/${campaignId}`); // Debugging

  router.push(`/sponsor/edit-campaign/${campaignId}`)
    .then(() => {
      console.log("Navigation successful.");
    })
    .catch((error) => {
      console.error("Failed to navigate:", error);
      messageStore.setFlashMessage("Failed to navigate to the edit campaign page.", "error");
    });
}
async function resolveFlag(flagId) {
    if (!flagId) {
    console.error("No flag ID provided for resolving.");
    return;
  }
  try {
    const response = await fetch(
      `${authStore.getBackendServerURL()}/admin/resolve-flag/${flagId}`,
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": authStore.getAuthToken(),
        },
      }
    );

    const data = await response.json();
    if (response.ok) {
      messageStore.setFlashMessage(data.message, "success");
      fetchFlaggedCampaigns(); // Refresh the flagged campaigns list
    } else {
      messageStore.setFlashMessage(data.message || "Failed to resolve flag.", "error");
    }
  } catch (error) {
    console.error("Error resolving flag:", error);
    messageStore.setFlashMessage("An error occurred while resolving the flag.", "error");
  }
}


  onMounted(() => {
    fetchFlaggedCampaigns();
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
  </style>
  