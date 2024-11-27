import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Login.vue'; // Adjust the path based on your folder structure

const routes = [
  { path: '/login', component: Login }, // Add this route
  // Add other routes here
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

