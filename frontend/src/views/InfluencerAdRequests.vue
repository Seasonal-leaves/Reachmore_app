<template>
    <div class="container mt-5">
      <h1 class="text-center mb-4">My Ad Requests</h1>
      <div v-if="adRequests.length === 0" class="text-center">
        <p>You have no ad requests at the moment.</p>
      </div>
      <div v-else class="row">
        <div
          v-for="adRequest in adRequests"
          :key="adRequest.ad_request_id"
          class="col-md-6 mb-4"
        >
          <div class="card h-100">
            <div class="card-body">
              <h5 class="card-title">{{ adRequest.campaign_name }}</h5>
              <p class="card-text"><strong>Description:</strong> {{ adRequest.campaign_description }}</p>
              <p class="card-text"><strong>Requirements:</strong> {{ adRequest.requirements }}</p>
              <p class="card-text"><strong>Messages:</strong> {{ adRequest.messages || 'No messages' }}</p>
              <p class="card-text"><strong>Payment:</strong> ₹{{ adRequest.payment_amount }}</p>
              <p class="card-text"><strong>Status:</strong> {{ adRequest.status }}</p>
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
  
  // Fetch ad requests for the logged-in influencer
  async function fetchAdRequests() {
    try {
      const response = await fetch(
        `${authStore.getBackendServerURL()}/influencer/ad-requests`,
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
  
  onMounted(() => {
    fetchAdRequests();
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
  