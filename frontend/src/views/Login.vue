<template>
  <div class="container mt-5">
    <h2 class="text-center">Login</h2>
    <form @submit.prevent="login" class="w-50 mx-auto">
      <div class="mb-3">
        <label for="email" class="form-label">Email</label>
        <input
          type="email"
          v-model="email"
          class="form-control"
          id="email"
          placeholder="Enter your email"
          required
        />
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input
          type="password"
          v-model="password"
          class="form-control"
          id="password"
          placeholder="Enter your password"
          required
        />
      </div>
      <div class="mb-3">
        <label for="role" class="form-label">Role</label>
        <select v-model="role" class="form-select">
          <option value="sponsor">Sponsor</option>
          <option value="influencer">Influencer</option>
          <option value="admin">Admin</option>
        </select>
      </div>
      <div class="text-center">
        <button type="submit" class="btn btn-primary w-100">Login</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth_store';
import { useMessageStore } from '@/stores/messageStore';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const messageStore = useMessageStore();
const router = useRouter();

const email = ref('');
const password = ref('');
const role = ref('sponsor'); // Default role

async function login() {
    try {
        await authStore.login(email.value, password.value, role.value);
        messageStore.setFlashMessage('Login successful!', 'success');
        router.push('/'); // Redirect to home/dashboard
    } catch (error) {
        messageStore.setFlashMessage(error.message || 'Login failed.', 'error');
    }
}
</script>

  