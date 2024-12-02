<template>
    <div class="container mt-5">
      <h1 class="text-center mb-4">Admin Dashboard</h1>
  
      <!-- Statistics Section -->
      <div class="row mb-4">
        <!-- Total Users -->
        <div class="col-md-4">
          <div class="card text-white bg-primary mb-3">
            <div class="card-body">
              <h5 class="card-title">Total Sponsors</h5>
              <p class="card-text display-4">{{ statistics.total_users.sponsors }}</p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card text-white bg-success mb-3">
            <div class="card-body">
              <h5 class="card-title">Total Influencers</h5>
              <p class="card-text display-4">{{ statistics.total_users.influencers }}</p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card text-white bg-dark mb-3">
            <div class="card-body">
              <h5 class="card-title">Total Campaigns</h5>
              <p class="card-text display-4">{{ statistics.total_campaigns }}</p>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Campaign Visibility -->
      <div class="row mb-4">
        <div class="col-md-6">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">Campaign Visibility</h5>
              <canvas id="campaignVisibilityChart"></canvas>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">Ad Request Status</h5>
              <canvas id="adRequestStatusChart"></canvas>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Flagged Entities -->
      <div class="row">
        <div class="col-md-6">
          <div class="card text-white bg-warning mb-3">
            <div class="card-body">
              <h5 class="card-title">Flagged Users</h5>
              <p class="card-text display-4">{{ statistics.flagged_entities.users }}</p>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card text-white bg-danger mb-3">
            <div class="card-body">
              <h5 class="card-title">Flagged Campaigns</h5>
              <p class="card-text display-4">{{ statistics.flagged_entities.campaigns }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from "vue";
  import { useAuthStore } from "@/stores/auth_store";
  import Chart from "chart.js/auto";
  
  const authStore = useAuthStore();
  const statistics = ref({
    total_users: { sponsors: 0, influencers: 0 },
    total_campaigns: 0,
    campaign_visibility: { public: 0, private: 0 },
    ad_requests_status: {},
    flagged_entities: { users: 0, campaigns: 0 },
  });
  
  const fetchStatistics = async () => {
    try {
      const response = await fetch(
        `${authStore.getBackendServerURL()}/admin/statistics`,
        {
          headers: {
            "Content-Type": "application/json",
            "Authentication-Token": authStore.getAuthToken(),
          },
        }
      );
  
      const data = await response.json();
      if (response.ok) {
        statistics.value = data.data;
        renderCharts();
      } else {
        console.error("Error fetching statistics:", data.message);
      }
    } catch (error) {
      console.error("Error fetching statistics:", error);
    }
  };
  
  const renderCharts = () => {
    // Campaign Visibility Pie Chart
    const ctx1 = document.getElementById("campaignVisibilityChart").getContext("2d");
    new Chart(ctx1, {
      type: "pie",
      data: {
        labels: ["Public Campaigns", "Private Campaigns"],
        datasets: [
          {
            data: [
              statistics.value.campaign_visibility.public,
              statistics.value.campaign_visibility.private,
            ],
            backgroundColor: ["#007bff", "#6c757d"],
          },
        ],
      },
    });
  
    // Ad Request Status Bar Chart
    const ctx2 = document.getElementById("adRequestStatusChart").getContext("2d");
    new Chart(ctx2, {
      type: "bar",
      data: {
        labels: Object.keys(statistics.value.ad_requests_status),
        datasets: [
          {
            label: "Ad Requests",
            data: Object.values(statistics.value.ad_requests_status),
            backgroundColor: "#28a745",
          },
        ],
      },
    });
  };
  
  onMounted(() => {
    fetchStatistics();
  });
  </script>
  
  <style>
  .card {
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  
  .card-title {
    font-size: 1.25rem;
  }
  
  .card-text {
    font-size: 2rem;
    font-weight: bold;
  }
  
  .canvas-container {
    position: relative;
    margin: auto;
    height: 300px;
    width: 100%;
  }
  </style>
  