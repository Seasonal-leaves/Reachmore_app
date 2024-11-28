import { createRouter, createWebHistory } from 'vue-router';
import Registration from '../views/Registration.vue';
import Login from '../views/Login.vue'; // Adjust the path based on your folder structure

const routes = [
  { path: '/login', component: Login }, // Add this route
  {
    path: '/register',
    name: 'Register',
    component: Registration,
  },
  {
    path: '/update-profile',
    name: 'UpdateProfile',
    component: () => import('@/views/UpdateProfile.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: "/admin/pending-approvals",
    name: "PendingApprovals",
    component: () => import('@/views/PendingApprovals.vue'),
    meta: { requiresAuth: true, role: "admin" },
  },
  {
    path: "/sponsor/create-campaign",
    name: "CreateCampaign",
    component: () => import("@/views/CreateCampaign.vue"),
    meta: { requiresAuth: true, role: "sponsor" },
  }
  
  // Add other routes here
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

