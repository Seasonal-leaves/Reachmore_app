<template>
    <div class="container mt-5">
      <h2 class="text-center">Register</h2>
      <form @submit.prevent="register" class="w-50 mx-auto">
        <!-- Common Fields -->
        <div class="mb-3">
          <label for="username" class="form-label">Username</label>
          <input
            type="text"
            v-model="username"
            class="form-control"
            id="username"
            placeholder="Enter a username"
            required
          />
        </div>
        <div class="mb-3">
          <label for="email" class="form-label">Email</label>
          <input
            type="email"
            v-model="email"
            class="form-control"
            id="email"
            placeholder="Enter your email"
            @blur="checkEmailExists"
            :class="{ 'is-invalid': emailError }"
            required
          />
          <div v-if="emailError" class="invalid-feedback">{{ emailError }}</div>
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input
            type="password"
            v-model="password"
            class="form-control"
            id="password"
            placeholder="Enter your password"
            minlength="8"
            required
          />
        </div>
        <div class="mb-3">
        <label for="confirmPassword" class="form-label">Confirm Password</label>
        <input
          type="password"
          v-model="confirmPassword"
          class="form-control"
          id="confirmPassword"
          placeholder="Confirm your password"
          :class="{ 'is-invalid': confirmPasswordError }"
          required
        />
        <div v-if="confirmPasswordError" class="invalid-feedback">{{ confirmPasswordError }}</div>
      </div>
        <div class="mb-3">
          <label for="role" class="form-label">Role</label>
          <select
            v-model="role"
            class="form-select"
            id="role"
            required
          >
            <option value="" disabled>Select a role</option>
            <option value="influencer">Influencer</option>
            <option value="sponsor">Sponsor</option>
          </select>
        </div>
  
        <!-- Role-Specific Fields -->
        <div v-if="role === 'influencer'">
          <div class="mb-3">
            <label for="category" class="form-label">Category</label>
            <input
              type="text"
              v-model="category"
              class="form-control"
              id="category"
              placeholder="Enter category"
              required
            />
          </div>
          <div class="mb-3">
            <label for="niche" class="form-label">Niche</label>
            <input
              type="text"
              v-model="niche"
              class="form-control"
              id="niche"
              placeholder="Enter niche"
              required
            />
          </div>
          <div class="mb-3">
            <label for="reach" class="form-label">Reach</label>
            <input
              type="number"
              v-model="reach"
              class="form-control"
              id="reach"
              placeholder="Enter your reach"
              min="1"
              required
            />
          </div>
        </div>
  
        <div v-if="role === 'sponsor'">
          <div class="mb-3">
            <label for="company_name" class="form-label">Company Name</label>
            <input
              type="text"
              v-model="company_name"
              class="form-control"
              id="company_name"
              placeholder="Enter company name"
              required
            />
          </div>
          <div class="mb-3">
            <label for="industry" class="form-label">Industry</label>
            <input
              type="text"
              v-model="industry"
              class="form-control"
              id="industry"
              placeholder="Enter industry"
              required
            />
          </div>
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
        </div>
  
        <!-- Submit Button -->
        <div class="text-center">
          <button
            type="submit"
            class="btn btn-primary w-100"
            :disabled="isSubmitting || emailError !== ''|| confirmPasswordError !== ''"
          >
            Register
          </button>
        </div>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue';
  import { useRouter } from 'vue-router';
  import { useMessageStore } from '@/stores/messageStore';
  import { useAuthStore } from '@/stores/auth_store';
  import { watchEffect } from 'vue';

// Add debug logs to observe state changes
// watchEffect(() => {
//   console.log('Email Error:', emailError.value);
//   console.log('Is Submitting:', isSubmitting.value);
// });
  
  const messageStore = useMessageStore();
  const authStore = useAuthStore();
  const router = useRouter();
  
  // Reactive variables
  const username = ref('');
  const email = ref('');
  const password = ref('');
  const confirmPassword = ref('');
  const role = ref('');
  const category = ref('');
  const niche = ref('');
  const reach = ref(null);
  const company_name = ref('');
  const industry = ref('');
  const budget = ref(null);
  
  // State
  const emailError = ref('');
  const isSubmitting = ref(false);
  
  // Methods
  async function checkEmailExists() {
    if (!email.value) {
      emailError.value = 'Email is required';
      return;
    }
  
    try {
      const response = await fetch(`${authStore.getBackendServerURL()}/check-email?email=${email.value}`);
      if (response.ok) {
        emailError.value = ''; // Clear error if email is available
      } else {
        const errorData = await response.json(); // Parse error response
        emailError.value = errorData.message || 'Email already exists.';
      }
    } catch (error) {
      emailError.value = 'Unable to validate email.';
      console.error('Error during email validation:', error);
    }
  }
  
  const confirmPasswordError = computed(() => {
  if (confirmPassword.value && confirmPassword.value !== password.value) {
    return 'Passwords do not match';
  }
  return '';
});

  async function register() {
    if (!role.value) {
      messageStore.setFlashMessage('Please select a role.', 'error');
      return;
    }
  
    isSubmitting.value = true;
  
    const payload = {
      username: username.value,
      email: email.value,
      password: password.value,
      role: role.value,
      ...(role.value === 'influencer' && {
        category: category.value,
        niche: niche.value,
        reach: reach.value,
      }),
      ...(role.value === 'sponsor' && {
        company_name: company_name.value,
        industry: industry.value,
        budget: budget.value,
      }),
    };
  
    try {
      const response = await fetch(`${authStore.getBackendServerURL()}/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
  
      const data = await response.json();
      if (response.ok) {
        messageStore.setFlashMessage('Registration successful!', 'success');
        router.push('/login'); // Redirect to login after success
      } else {
        messageStore.setFlashMessage(data.message || 'Registration failed.', 'error');
      }
    } catch (error) {
      messageStore.setFlashMessage('Registration failed. Try again.', 'error');
      console.error('Error during registration:', error);
    } finally {
      isSubmitting.value = false;
    }
  }
  </script>
  