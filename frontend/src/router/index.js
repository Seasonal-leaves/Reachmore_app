import { createRouter, createWebHistory } from 'vue-router';
import Registration from '../views/Registration.vue';
import Login from '../views/Login.vue'; // Adjust the path based on your folder structure
import { useAuthStore } from "@/stores/auth_store";
import ViewInfluencers from "@/views/ViewInfluencers.vue";

const routes = [
  {
    path: "/",
    redirect: "/view-campaigns", // Always redirect to ViewCampaigns
  },  
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
    path: "/view-campaigns",
    name: "ViewCampaigns",
    component: () => import('@/views/ViewCampaigns.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/sponsor/edit-campaign/:campaignId',
    name: 'EditCampaign',
    component: () => import('@/views/EditCampaign.vue'),
    meta: { requiresAuth: true, role: "sponsor" },
  },
  {
    path: "/sponsor/influencers",
    name: "ViewInfluencers",
    component: ViewInfluencers,
    meta: { requiresAuth: true },
  },
  {
    path: "/influencer/ad-requests",
    name: "AdRequests",
    component: () => import("@/views/InfluencerAdRequests.vue"),
  },
  {
    path: '/sponsor/adrequests',
    component: () => import('@/views/AllAdRequests.vue'),
    meta: { requiresAuth: true, sponsorOnly: true },
  },
  {
    path: '/sponsor/adrequests/:campaignId',
    component: () => import('@/views/CampaignAdRequests.vue'),
    meta: { requiresAuth: true, sponsorOnly: true },
  },
  {
    path: "/admin/user-management",
    name: "AdminUserManagement",
    component: () => import("@/views/AdminUserManagement.vue"),
    meta: { requiresAuth: true, role: "admin" },
  },
  {
    path: "/flagged-campaigns",
    component: () => import("@/views/FlaggedCampaigns.vue"),
    beforeEnter: (to, from, next) => {
      const authStore = useAuthStore();
      if (authStore.isAdminOrSponsor()) {
        next();
      } else {
        next("/unauthorized"); // Redirect unauthorized users
      }
    },
  },
  {
    path: "/admin/flagged-users",
    name: "FlaggedUsers",
    component: () => import("@/views/FlaggedUsers.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/admin/dashboard",
    name: "AdminDashboard",
    component: () => import("@/views/AdminDashboard.vue"),
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

