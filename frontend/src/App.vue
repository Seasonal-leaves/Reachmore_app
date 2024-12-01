<script setup>
import { RouterLink, RouterView } from 'vue-router';
import { computed } from 'vue';
import { useMessageStore } from './stores/messageStore';
import { useAuthStore } from './stores/auth_store';

// Stores
const authStore = useAuthStore();
const messageStore = useMessageStore();

// Computed properties
const isAuthenticated = computed(() => authStore.isAuthenticated);
const userDetails = computed(() => {
    try {
        return isAuthenticated.value ? JSON.parse(authStore.getUserDetails() || '{}') : {};
    } catch (error) {
        console.error('Error parsing userDetails in App.vue:', error);
        return {}; // Fallback to an empty object
    }
});
const message = computed(() => messageStore.getFlashMessage());

// Role-based access
const isAdmin = computed(() => isAuthenticated.value && userDetails.value?.roles?.includes('admin'));
const isSponsor = computed(() => isAuthenticated.value && userDetails.value?.roles?.includes('sponsor'));
const isInfluencer = computed(() => isAuthenticated.value && userDetails.value?.roles?.includes('influencer'));

// Logout function
function logout() {
    fetch(`${authStore.getBackendServerURL()}/logout`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': authStore.getAuthToken(),
            'Access-Control-Allow-Origin': '*',
        },
    })
        .then((response) => response.json())
        .then((data) => {
            messageStore.setFlashMessage(data.message || 'You have been logged out.');
            authStore.removeAuthenticatedUser();
        })
        .catch(() => {
            messageStore.setFlashMessage('Logout failed. Please try again.');
        });
}
</script>

<template>
  <!-- Navbar -->
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
      <RouterLink to="/" class="navbar-brand">Reachmore</RouterLink>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <!-- Left Navbar -->
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <!-- Logged-out state -->
          <li v-if="!isAuthenticated" class="nav-item">
            <RouterLink to="/login" class="nav-link">Login</RouterLink>
          </li>
          <li v-if="!isAuthenticated" class="nav-item">
            <RouterLink to="/register" class="nav-link">Register</RouterLink>
          </li>

          <!-- Admin Links -->
          <template v-if="isAdmin">
            <router-link to="/admin/user-management" class="nav-link">
              User Management
            </router-link>
            <li class="nav-item">
              <RouterLink to="/admin/dashboard" class="nav-link">Admin Dashboard</RouterLink>
            </li>
            <li class="nav-item">
  <router-link
    to="/admin/flagged-users"
    class="nav-link"
    v-if="authStore.isAdmin()"
  >
    Flagged Users
  </router-link>
</li>

            <li class="nav-item">
              <RouterLink to="/admin/flags" class="nav-link">Manage Flags</RouterLink>
            </li>
            <li class="nav-item">
  <RouterLink to="/admin/pending-approvals" class="nav-link">Pending Approvals</RouterLink>
</li>
          </template>

          <!-- Sponsor Links -->
          <template v-if="isSponsor">
            <li class="nav-item">
              <RouterLink to="/sponsor/create-campaign" class="nav-link">Create Campaign</RouterLink>
            </li>
            <li class="nav-item">
  <router-link to="/sponsor/influencers" class="nav-link">View Influencers</router-link>
</li>

<li class="nav-item">
      <router-link to="/sponsor/adrequests" class="nav-link">All Ad Requests</router-link>
    </li>
          </template>

          <!-- Influencer Links -->
          <template v-if="isInfluencer">
            <li class="nav-item">
              <RouterLink to="/influencer/search-campaigns" class="nav-link">Search Campaigns</RouterLink>
            </li>
            <router-link
  to="/influencer/ad-requests"
  class="btn btn-outline-primary mx-2"
>
  My Ad Requests
</router-link>
          </template>
          <li v-if="authStore.isAdminOrSponsor()" class="nav-item">
            <router-link to="/flagged-campaigns" class="nav-link">Flagged Campaigns</router-link>
          </li>

          <!-- Logged-in User Links -->
          <template v-if="isAuthenticated">
            <li class="nav-item">
              <span class="nav-link">Hello {{ userDetails.username }},</span>
            </li>
            <li v-if="isAuthenticated" class="nav-item">
            <RouterLink to="/update-profile" class="nav-link">Profile</RouterLink>
          </li>
         
  <li class="nav-item">
    <RouterLink to="/view-campaigns" class="nav-link">View Campaigns</RouterLink>
  </li>
 <li class="nav-item">
              <button @click="logout" class="btn btn-link nav-link">Logout</button>
            </li>
          </template>
        </ul>

       
      </div>
    </div>
  </nav>

  <!-- Flash Message -->
  <div v-if="message" class="alert alert-primary text-center" role="alert">
    {{ message }}
  </div>

  <!-- Main Content -->
  <RouterView />
</template>
