<template>
    <div class="container mt-5">
      <h2 class="text-center">Edit Campaign</h2>
      <form @submit.prevent="updateCampaign" class="w-50 mx-auto">
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
        <div class="mb-3">
          <label for="end_date" class="form-label">End Date</label>
          <input
            type="date"
            v-model="end_date"
            class="form-control"
            id="end_date"
          />
        </div>
        <div class="mb-3">
          <label for="budget" class="form-label">Budget</label>
          <input
            type="number"
            v-model="budget"
            class="form-control"
            id="budget"
            placeholder="Enter campaign budget"
            required
          />
        </div>
        <div class="mb-3">
          <label for="visibility" class="form-label">Visibility</label>
          <select v-model="visibility" class="form-select" id="visibility" required>
            <option value="public">Public</option>
            <option value="private">Private</option>
          </select>
        </div>
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
        <div class="text-center">
          <button type="submit" class="btn btn-primary w-100">Save Changes</button>
        </div>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import { useRouter, useRoute } from 'vue-router';
  import { useAuthStore } from '@/stores/auth_store';
  import { useMessageStore } from '@/stores/messageStore';
  
  const authStore = useAuthStore();
  const messageStore = useMessageStore();
  const router = useRouter();
  const route = useRoute();
  
  const campaignId = route.params.campaignId;
  const name = ref('');
  const description = ref('');
  const start_date = ref('');
  const end_date = ref('');
  const budget = ref('');
  const visibility = ref('');
  const goals = ref('');
  
  // Helper to format date
  function formatDateForInput(dateString) {
    if (!dateString) return null;
    const date = new Date(dateString);
    return date.toISOString().split('T')[0];
  }
  
  // Load campaign details
  onMounted(async () => {
    try {
      const response = await fetch(
        `${authStore.getBackendServerURL()}/view-campaign?id=${campaignId}`,
        {
          headers: {
            'Authentication-Token': authStore.getAuthToken(),
          },
        }
      );
      const data = await response.json();
      const campaign = data.campaigns[0];
      name.value = campaign.name;
      description.value = campaign.description;
      start_date.value = formatDateForInput(campaign.start_date);
      end_date.value = formatDateForInput(campaign.end_date);
      budget.value = campaign.budget;
      visibility.value = campaign.visibility;
      goals.value = campaign.goals;
    } catch (error) {
      console.error('Error loading campaign details:', error);
      messageStore.setFlashMessage('Failed to load campaign details.', 'error');
    }
  });
  
  // Update campaign details
  async function updateCampaign() {
    try {
      const payload = {
        name: name.value,
        description: description.value,
        start_date: start_date.value,
        end_date: end_date.value,
        budget: budget.value,
        visibility: visibility.value,
        goals: goals.value,
      };
      const response = await fetch(
        `${authStore.getBackendServerURL()}/sponsor/update-campaign/${campaignId}`,
        {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': authStore.getAuthToken(),
          },
          body: JSON.stringify(payload),
        }
      );
      const data = await response.json();
      if (response.ok) {
        messageStore.setFlashMessage(data.message, 'success');
        router.push('/');
      } else {
        messageStore.setFlashMessage(data.message, 'error');
      }
    } catch (error) {
      messageStore.setFlashMessage('Failed to update campaign. Please try again.', 'error');
      console.error('Error updating campaign:', error);
    }
  }
  </script>
  