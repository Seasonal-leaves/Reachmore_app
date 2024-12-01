<template>
    <div class="container mt-5">
      <h1 class="text-center mb-4">User Management</h1>
  
      <!-- Search Bar -->
      <div class="row mb-4">
        <div class="col-md-12">
          <input
            type="text"
            v-model="searchQuery"
            class="form-control"
            placeholder="Search users by username, niche, category, company name..."
          />
        </div>
      </div>
  
      <!-- Grouped User Lists -->
      <div>
        <!-- Influencers Section -->
        <h3 class="text-center mb-4">Influencers</h3>
        <div v-if="filteredInfluencers.length === 0" class="text-center">
          <p>No influencers match your search criteria.</p>
        </div>
        <div v-else class="row">
          <div
            v-for="user in filteredInfluencers"
            :key="user.id"
            class="col-md-4 mb-4"
          >
            <div class="card h-100">
              <div class="card-body">
                <h5 class="card-title">{{ user.username }}</h5>
                <p class="card-text"><strong>Email:</strong> {{ user.email }}</p>
                <p class="card-text"><strong>Niche:</strong> {{ user.niche || 'N/A' }}</p>
                <p class="card-text"><strong>Category:</strong> {{ user.category || 'N/A' }}</p>
                <p class="card-text"><strong>Reach:</strong> {{ user.reach || 'N/A' }}</p>
                <button
  class="btn btn-danger btn-sm"
  @click="openFlagModal(user.id, null)" 

>
  Flag Influencer
</button>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Sponsors Section -->
        <h3 class="text-center mb-4">Sponsors</h3>
        <div v-if="filteredSponsors.length === 0" class="text-center">
          <p>No sponsors match your search criteria.</p>
        </div>
        <div v-else class="row">
          <div
            v-for="user in filteredSponsors"
            :key="user.id"
            class="col-md-4 mb-4"
          >
            <div class="card h-100">
              <div class="card-body">
                <h5 class="card-title">{{ user.username }}</h5>
                <p class="card-text"><strong>Email:</strong> {{ user.email }}</p>
                <p class="card-text"><strong>Company Name:</strong> {{ user.company_name || 'N/A' }}</p>
                <p class="card-text"><strong>Industry:</strong> {{ user.industry || 'N/A' }}</p>
                <p class="card-text"><strong>Budget:</strong> ₹{{ user.budget || 'N/A' }}</p>
                <p class="card-text">
                  <strong>Status:</strong>
                  {{ user.is_approved ? 'Approved' : 'Pending Approval' }}
                </p>
                <button
  class="btn btn-danger btn-sm"
  @click="openFlagModal(user.id, null)" 
>
  Flag Sponsor
</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
<!-- Flag Modal -->
<div v-if="showFlagModal" class="modal-backdrop">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Flag {{ flaggedUserId ? 'User' : 'Campaign' }}</h5>
        <button type="button" class="btn-close" @click="closeFlagModal"></button>
      </div>
      <div class="modal-body">
        <div class="mb-3">
          <label for="reason" class="form-label">Reason for Flagging</label>
          <textarea
            id="reason"
            v-model="flagReason"
            class="form-control"
            placeholder="Enter the reason for flagging"
            rows="3"
            required
          ></textarea>
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn btn-secondary" @click="closeFlagModal">Cancel</button>
        <button class="btn btn-danger" @click="submitFlag">Flag</button>
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

const usersByRole = ref({ influencers: [], sponsors: [] });
const searchQuery = ref("");
const showFlagModal = ref(false);
const flagReason = ref("");
const flaggedUserId = ref(null);

// Fetch users grouped by roles
async function fetchUsersByRole() {
  try {
    const response = await fetch(`${authStore.getBackendServerURL()}/admin/user-management`, {
      headers: {
        "Content-Type": "application/json",
        "Authentication-Token": authStore.getAuthToken(),
      },
    });
    const data = await response.json();
    if (response.ok) {
      usersByRole.value = data.users_by_role;
    } else {
      messageStore.setFlashMessage(data.message || "Failed to fetch users.", "error");
    }
  } catch (error) {
    console.error("Error fetching user management data:", error);
    messageStore.setFlashMessage("An error occurred while fetching users.", "error");
  }
}

// Computed properties for filtering users
const filteredInfluencers = computed(() => {
  if (!searchQuery.value) return usersByRole.value.influencers;

  const query = searchQuery.value.toLowerCase();
  return usersByRole.value.influencers.filter(
    (user) =>
      user.username.toLowerCase().includes(query) ||
      (user.niche && user.niche.toLowerCase().includes(query)) ||
      (user.category && user.category.toLowerCase().includes(query))
  );
});

const filteredSponsors = computed(() => {
  if (!searchQuery.value) return usersByRole.value.sponsors;

  const query = searchQuery.value.toLowerCase();
  return usersByRole.value.sponsors.filter(
    (user) =>
      user.username.toLowerCase().includes(query) ||
      (user.company_name && user.company_name.toLowerCase().includes(query)) ||
      (user.industry && user.industry.toLowerCase().includes(query))
  );
});

// Open the flag modal
function openFlagModal(userId, campaignId) {
  flaggedUserId.value = userId;
//   flaggedCampaignId.value = campaignId;
  flagReason.value = "";
  showFlagModal.value = true;
}

// Close the flag modal
function closeFlagModal() {
  flaggedUserId.value = null;
//   flaggedCampaignId.value = null;
  flagReason.value = "";
  showFlagModal.value = false;
}

// Submit the flag
async function submitFlag() {
  if (!flagReason.value.trim()) {
    messageStore.setFlashMessage("Reason is required to flag.", "error");
    return;
  }

  const payload = {
    flagged_user_id: flaggedUserId.value,
    // flagged_campaign_id: flaggedCampaignId.value,
    reason: flagReason.value.trim(),
  };

  try {
    const response = await fetch(`${authStore.getBackendServerURL()}/admin/flag`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authentication-Token": authStore.getAuthToken(),
      },
      body: JSON.stringify(payload),
    });

    const data = await response.json();
    if (response.ok) {
      messageStore.setFlashMessage(data.message, "success");
      fetchUsersByRole();
      closeFlagModal();
    } else {
      messageStore.setFlashMessage(data.message || "Failed to flag the entity.", "error");
    }
  } catch (error) {
    console.error("Error flagging entity:", error);
    messageStore.setFlashMessage("An error occurred while flagging.", "error");
  }
}
// Fetch users on mount
onMounted(() => {
  fetchUsersByRole();
});
</script>
  