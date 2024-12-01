<template>
    <div class="container mt-5">
      <h1 class="text-center mb-4">Flagged Users</h1>
      <div v-if="flaggedUsers.length === 0" class="text-center">
        <p>No flagged users at the moment.</p>
      </div>
      <div v-else class="row">
        <div
          v-for="user in flaggedUsers"
          :key="user.flag_id"
          class="col-md-6 mb-4"
        >
          <div class="card h-100">
            <div class="card-body">
              <h5 class="card-title">{{ user.username }}</h5>
              <p class="card-text"><strong>User ID:</strong> {{ user.user_id }}</p>
              <p class="card-text"><strong>Reason:</strong> {{ user.reason }}</p>
              <p class="card-text">
                <strong>Flagged On:</strong> {{ formatDate(user.timestamp) }}
              </p>
              <p class="card-text"><strong>Status:</strong> {{ user.status }}</p>
                   <!-- Resolve Flag Button -->
            <button
              class="btn btn-success mt-2"
              @click="resolveFlag(user.flag_id)"
            >
              Resolve Flag
            </button>
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
  import { useRouter } from "vue-router";
  
  const authStore = useAuthStore();
  const messageStore = useMessageStore();
  const router = useRouter();
  
  const flaggedUsers = ref([]);
  
  // Redirect if user is not admin
  if (!authStore.isAdmin()) {
    router.push("/unauthorized");
  }
  
  // Format date for display
  function formatDate(dateString) {
    const options = { year: "numeric", month: "long", day: "numeric" };
    return new Date(dateString).toLocaleDateString(undefined, options);
  }
  
  // Fetch flagged users
  async function fetchFlaggedUsers() {
    try {
      const response = await fetch(
        `${authStore.getBackendServerURL()}/admin/flagged-users`,
        {
          headers: {
            "Content-Type": "application/json",
            "Authentication-Token": authStore.getAuthToken(),
          },
        }
      );
  
      const data = await response.json();
      if (response.ok) {
        flaggedUsers.value = data.flagged_users;
      } else {
        messageStore.setFlashMessage(
          data.message || "Failed to fetch flagged users.",
          "error"
        );
      }
    } catch (error) {
      console.error("Error fetching flagged users:", error);
      messageStore.setFlashMessage(
        "An error occurred while fetching flagged users.",
        "error"
      );
    }
  }
  async function resolveFlag(flagId) {
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
      fetchFlaggedUsers(); // Refresh the flagged users list
    } else {
      messageStore.setFlashMessage(data.message || "Failed to resolve flag.", "error");
    }
  } catch (error) {
    console.error("Error resolving flag:", error);
    messageStore.setFlashMessage("An error occurred while resolving the flag.", "error");
  }
}

  onMounted(() => {
    fetchFlaggedUsers();
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
  