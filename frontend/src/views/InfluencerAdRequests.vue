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
  
              <!-- Action Buttons -->
              <div v-if="adRequest.status === 'Pending' || adRequest.status === 'Negotiated'" class="d-flex gap-2">
                <button class="btn btn-success" @click="respondToAdRequest(adRequest.ad_request_id, 'Accepted')">
                  Accept
                </button>
                <button class="btn btn-danger" @click="respondToAdRequest(adRequest.ad_request_id, 'Rejected')">
                  Reject
                </button>
                <button class="btn btn-warning" @click="openNegotiateModal(adRequest)">
                  Negotiate
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Negotiate Modal -->
      <div
        class="modal fade"
        id="negotiateModal"
        tabindex="-1"
        aria-labelledby="negotiateModalLabel"
        aria-hidden="true"
      >
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="negotiateModalLabel">Negotiate Ad Request</h5>
              <button
                type="button"
                class="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div class="modal-body">
              <label for="negotiatePayment" class="form-label">Proposed Payment</label>
              <input
                type="number"
                v-model="negotiatedPayment"
                class="form-control"
                id="negotiatePayment"
                placeholder="Enter proposed payment amount"
              />
              <label for="negotiateMessage" class="form-label mt-3">Message</label>
              <textarea
                v-model="negotiateMessage"
                class="form-control"
                id="negotiateMessage"
                placeholder="Add a message for negotiation (optional)"
              ></textarea>
            </div>
            <div class="modal-footer">
              <button class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
              <button class="btn btn-primary" @click="submitNegotiation">Submit</button>
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
  const negotiateModal = ref(null);
  const negotiatedPayment = ref(null);
  const negotiateMessage = ref("");
  let selectedAdRequest = ref(null);
  
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
  
  // Respond to ad request
  async function respondToAdRequest(adRequestId, status) {
    try {
      const response = await fetch(`${authStore.getBackendServerURL()}/influencer/respond-adrequest/${adRequestId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": authStore.getAuthToken(),
        },
        body: JSON.stringify({ status }),
      });
  
      const data = await response.json();
      if (response.ok) {
        messageStore.setFlashMessage(data.message, "success");
        fetchAdRequests(); // Refresh the ad requests list
      } else {
        messageStore.setFlashMessage(data.message || "Failed to respond to ad request.", "error");
      }
    } catch (error) {
      console.error("Error responding to ad request:", error);
      messageStore.setFlashMessage("An error occurred while responding to ad request.", "error");
    }
  }
  
  // Open negotiation modal
  function openNegotiateModal(adRequest) {
    selectedAdRequest.value = adRequest;
    negotiatedPayment.value = adRequest.payment_amount; // Default to current payment amount
    const modalElement = document.getElementById("negotiateModal");
    negotiateModal.value = new bootstrap.Modal(modalElement);
    negotiateModal.value.show();
  }
  
  // Submit negotiation
  async function submitNegotiation() {
    try {
      const payload = {
        status: "Negotiated",
        payment_amount: negotiatedPayment.value,
        message: negotiateMessage.value,
      };
  
      const response = await fetch(
        `${authStore.getBackendServerURL()}/influencer/respond-adrequest/${selectedAdRequest.value.ad_request_id}`,
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
        negotiateModal.value.hide(); // Close the modal
        fetchAdRequests(); // Refresh the ad requests list
      } else {
        messageStore.setFlashMessage(data.message || "Failed to negotiate ad request.", "error");
      }
    } catch (error) {
      console.error("Error submitting negotiation:", error);
      messageStore.setFlashMessage("An error occurred while negotiating ad request.", "error");
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
  