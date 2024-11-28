<template>
    <div class="container mt-5">
      <h2 class="text-center">Pending Sponsor Approvals</h2>
      <div v-if="isLoading" class="text-center">
        <p>Loading pending approvals...</p>
      </div>
      <div v-if="error" class="alert alert-danger">
        {{ error }}
      </div>
      <table v-if="pendingSponsors.length" class="table table-striped">
        <thead>
          <tr>
            <th>Username</th>
            <th>Email</th>
            <th>Company Name</th>
            <th>Industry</th>
            <th>Budget</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="sponsor in pendingSponsors" :key="sponsor.user_id">
            <td>{{ sponsor.username }}</td>
            <td>{{ sponsor.email }}</td>
            <td>{{ sponsor.company_name }}</td>
            <td>{{ sponsor.industry }}</td>
            <td>{{ sponsor.budget }}</td>
            <td>
              <button
                class="btn btn-success btn-sm me-2"
                @click="approveSponsor(sponsor.user_id)"
              >
                Approve
              </button>
              <button
                class="btn btn-danger btn-sm"
                @click="deleteSponsor(sponsor.user_id)"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else-if="!isLoading" class="text-center">
        <p>No pending approvals.</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from "vue";
  import { useAuthStore } from "@/stores/auth_store";
  import { useMessageStore } from "@/stores/messageStore";
  
  const authStore = useAuthStore();
  const messageStore = useMessageStore();
  
  const pendingSponsors = ref([]);
  const isLoading = ref(true);
  const error = ref("");
  
  async function fetchPendingApprovals() {
    try {
      isLoading.value = true;
      error.value = "";
  
      const response = await fetch(`${authStore.getBackendServerURL()}/admin/pending-approvals`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": authStore.getAuthToken(),
        },
      });
  
      const data = await response.json();
  
      if (response.ok) {
        pendingSponsors.value = data.pending_sponsors;
      } else {
        error.value = data.message || "Failed to fetch pending approvals.";
      }
    } catch (err) {
      error.value = "An error occurred while fetching pending approvals.";
    } finally {
      isLoading.value = false;
    }
  }
  
  async function approveSponsor(sponsorId) {
    try {
      const response = await fetch(`${authStore.getBackendServerURL()}/admin/approve-sponsor/${sponsorId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": authStore.getAuthToken(),
        },
      });
  
      const data = await response.json();
  
      if (response.ok) {
        messageStore.setFlashMessage(data.message, "success");
        pendingSponsors.value = pendingSponsors.value.filter((sponsor) => sponsor.user_id !== sponsorId);
      } else {
        messageStore.setFlashMessage(data.message || "Failed to approve sponsor.", "error");
      }
    } catch (err) {
      messageStore.setFlashMessage("An error occurred while approving the sponsor.", "error");
    }
  }
  
  async function deleteSponsor(sponsorId) {
    try {
      const response = await fetch(`${authStore.getBackendServerURL()}/admin/approve-sponsor/${sponsorId}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": authStore.getAuthToken(),
        },
      });
  
      const data = await response.json();
  
      if (response.ok) {
        messageStore.setFlashMessage(data.message, "success");
        pendingSponsors.value = pendingSponsors.value.filter((sponsor) => sponsor.user_id !== sponsorId);
      } else {
        messageStore.setFlashMessage(data.message || "Failed to delete sponsor.", "error");
      }
    } catch (err) {
      messageStore.setFlashMessage("An error occurred while deleting the sponsor.", "error");
    }
  }
  
  onMounted(fetchPendingApprovals);
  </script>
  