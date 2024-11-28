<template>
    <div class="container mt-5">
      <h2 class="text-center">Create Campaign</h2>
      <form @submit.prevent="createCampaign" class="w-50 mx-auto">
        <!-- Campaign Name -->
        <div class="mb-3">
          <label for="name" class="form-label">Campaign Name</label>
          <input
            type="text"
            v-model="name"
            class="form-control"
            id="name"
            placeholder="Enter campaign name"
            required
          />
        </div>
  
        <!-- Description -->
        <div class="mb-3">
          <label for="description" class="form-label">Description</label>
          <textarea
            v-model="description"
            class="form-control"
            id="description"
            placeholder="Enter campaign description"
            rows="3"
          ></textarea>
        </div>
  
        <!-- Start Date -->
        <div class="mb-3">
          <label for="start_date" class="form-label">Start Date</label>
          <input
            type="date"
            v-model="start_date"
            class="form-control"
            id="start_date"
            required
          />
        </div>
  
        <!-- End Date -->
        <div class="mb-3">
          <label for="end_date" class="form-label">End Date</label>
          <input
            type="date"
            v-model="end_date"
            class="form-control"
            id="end_date"
          />
        </div>
  
        <!-- Budget -->
        <div class="mb-3">
          <label for="budget" class="form-label">Budget</label>
          <input
            type="number"
            v-model="budget"
            class="form-control"
            id="budget"
            placeholder="Enter budget"
            min="1"
            required
          />
        </div>
  
        <!-- Visibility -->
        <div class="mb-3">
          <label for="visibility" class="form-label">Visibility</label>
          <select v-model="visibility" class="form-select" id="visibility" required>
            <option value="public">Public</option>
            <option value="private">Private</option>
          </select>
        </div>
  
        <!-- Goals -->
        <div class="mb-3">
          <label for="goals" class="form-label">Goals</label>
          <textarea
            v-model="goals"
            class="form-control"
            id="goals"
            placeholder="Enter campaign goals"
            rows="3"
          ></textarea>
        </div>
  
        <!-- Submit Button -->
        <div class="text-center">
          <button type="submit" class="btn btn-primary w-100" :disabled="isSubmitting">
            Create Campaign
          </button>
        </div>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref } from "vue";
  import { useRouter } from "vue-router";
  import { useAuthStore } from "@/stores/auth_store";
  import { useMessageStore } from "@/stores/messageStore";
  
  // Stores and State
  const authStore = useAuthStore();
  const messageStore = useMessageStore();
  const router = useRouter();
  
  // Campaign Form Data
  const name = ref("");
  const description = ref("");
  const start_date = ref("");
  const end_date = ref("");
  const budget = ref("");
  const visibility = ref("public");
  const goals = ref("");
  
  // Form State
  const isSubmitting = ref(false);
  
  // Methods
  async function createCampaign() {
    isSubmitting.value = true;
  
    const payload = {
      name: name.value,
      description: description.value,
      start_date: start_date.value,
      end_date: end_date.value || null, // Optional field
      budget: budget.value,
      visibility: visibility.value,
      goals: goals.value,
    };
  
    try {
      const response = await fetch(`${authStore.getBackendServerURL()}/sponsor/create-campaign`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": authStore.getAuthToken(),
        },
        body: JSON.stringify(payload),
      });
  
      const data = await response.json();
  
      if (response.ok) {
        messageStore.setFlashMessage(data.message || "Campaign created successfully!", "success");
        router.push("/sponsor/view-campaigns"); // Redirect to campaigns page after success
      } else {
        messageStore.setFlashMessage(data.message || "Failed to create campaign.", "error");
      }
    } catch (error) {
      messageStore.setFlashMessage("An error occurred while creating the campaign.", "error");
      console.error(error);
    } finally {
      isSubmitting.value = false;
    }
  }
  </script>
  