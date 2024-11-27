<template>
    <div class="container mt-5">
      <h2 class="text-center">Update Profile</h2>
      <form @submit.prevent="updateProfile" class="w-50 mx-auto">
        <div class="mb-3">
          <label for="username" class="form-label">Username</label>
          <input
            type="text"
            v-model="username"
            class="form-control"
            id="username"
            placeholder="Enter your username"
            required
          />
        </div>
  
        <div v-if="isSponsor" class="mb-3">
          <label for="company_name" class="form-label">Company Name</label>
          <input
            type="text"
            v-model="company_name"
            class="form-control"
            id="company_name"
            placeholder="Enter company name"
          />
        </div>
        <div v-if="isSponsor" class="mb-3">
          <label for="industry" class="form-label">Industry</label>
          <input
            type="text"
            v-model="industry"
            class="form-control"
            id="industry"
            placeholder="Enter industry"
          />
        </div>
        <div v-if="isSponsor" class="mb-3">
          <label for="budget" class="form-label">Budget</label>
          <input
            type="number"
            v-model="budget"
            class="form-control"
            id="budget"
            placeholder="Enter budget"
          />
        </div>
  
        <div v-if="isInfluencer" class="mb-3">
          <label for="category" class="form-label">Category</label>
          <input
            type="text"
            v-model="category"
            class="form-control"
            id="category"
            placeholder="Enter category"
          />
        </div>
        <div v-if="isInfluencer" class="mb-3">
          <label for="niche" class="form-label">Niche</label>
          <input
            type="text"
            v-model="niche"
            class="form-control"
            id="niche"
            placeholder="Enter niche"
          />
        </div>
        <div v-if="isInfluencer" class="mb-3">
          <label for="reach" class="form-label">Reach</label>
          <input
            type="number"
            v-model="reach"
            class="form-control"
            id="reach"
            placeholder="Enter your reach"
          />
        </div>
  
        <div class="text-center">
          <button type="submit" class="btn btn-primary w-100">Update Profile</button>
        </div>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  import { useAuthStore } from '@/stores/auth_store';
  import { useMessageStore } from '@/stores/messageStore';
  
  const authStore = useAuthStore();
  const messageStore = useMessageStore();
  const router = useRouter();
  
  const userDetails = JSON.parse(authStore.getUserDetails());
  const username = ref(userDetails.username || '');
  const company_name = ref(userDetails.company_name || '');
  const industry = ref(userDetails.industry || '');
  const budget = ref(userDetails.budget || '');
  const category = ref(userDetails.category || '');
  const niche = ref(userDetails.niche || '');
  const reach = ref(userDetails.reach || '');
  
  const isSponsor = userDetails.roles.includes('sponsor');
  const isInfluencer = userDetails.roles.includes('influencer');
  
  async function updateProfile() {
    const payload = {
      username: username.value,
      ...(isSponsor && { company_name: company_name.value, industry: industry.value, budget: budget.value }),
      ...(isInfluencer && { category: category.value, niche: niche.value, reach: reach.value }),
    };
  
    try {
      const response = await fetch(`${authStore.getBackendServerURL()}/user/update-profile`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': authStore.getAuthToken(),
        },
        body: JSON.stringify(payload),
      });
  
      const data = await response.json();
      if (response.ok) {
        messageStore.setFlashMessage(data.message || 'Profile updated successfully!', 'success');
        authStore.setUserDetails({ ...userDetails, ...payload });
        router.push('/');
      } else {
        messageStore.setFlashMessage(data.message || 'Profile update failed.', 'error');
      }
    } catch (error) {
      messageStore.setFlashMessage('An error occurred while updating your profile.', 'error');
      console.error('Update Profile Error:', error);
    }
  }
  </script>
  