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
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from "vue";
  import { useAuthStore } from "@/stores/auth_store";
  import { useMessageStore } from "@/stores/messageStore";
  
  const authStore = useAuthStore();
  const messageStore = useMessageStore();
  
  const adRequests = ref([]);
  
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
  
  onMounted(fetchAdRequests);
  </script>
  