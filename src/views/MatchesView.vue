<template>
  <div class="matches-container">
    <h1>Your Matches</h1>

    <div v-if="loading" class="loading">Loading matches...</div>

    <div v-else-if="matches.length === 0" class="no-matches">
      <h3>No matches yet</h3>
      <p>Start browsing to find your perfect match!</p>
      <router-link to="/browse" class="btn-primary"
        >Browse Profiles</router-link
      >
    </div>

    <div v-else class="matches-grid">
      <div v-for="match in matches" :key="match.match_id" class="match-card">
        <div class="match-image">
          <img
            v-if="match.profile.profile_picture"
            :src="`http://localhost:5000/uploads/${match.profile.profile_picture}`"
            alt="Profile"
          />
          <div v-else class="avatar-placeholder">
            {{ match.profile.name?.charAt(0) }}
          </div>
        </div>

        <div class="match-info">
          <h3>{{ match.profile.name }}, {{ match.profile.age }}</h3>
          <p class="matched-at">Matched {{ formatDate(match.matched_at) }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import matchService from "../services/matchService";

const matches = ref([]);
const loading = ref(true);

const loadMatches = async () => {
  loading.value = true;
  try {
    matches.value = await matchService.getMatches();
  } catch (error) {
    console.error("Failed to load matches:", error);
  } finally {
    loading.value = false;
  }
};

const formatDate = (dateString) => {
  if (!dateString) return "";
  const date = new Date(dateString);
  const now = new Date();
  const diff = now - date;

  if (diff < 60000) return "just now";
  if (diff < 3600000) return `${Math.floor(diff / 60000)} minutes ago`;
  if (diff < 86400000) return `${Math.floor(diff / 3600000)} hours ago`;
  if (diff < 604800000) return `${Math.floor(diff / 86400000)} days ago`;
  return date.toLocaleDateString();
};

onMounted(loadMatches);
</script>

<style scoped>
.matches-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 1.5rem;
}

h1 {
  font-size: 1.75rem;
  font-weight: 700;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 1.5rem;
}

.loading {
  text-align: center;
  padding: 3.75rem;
  color: var(--text-secondary);
}

.no-matches {
  text-align: center;
  padding: 3.75rem;
  background: var(--surface);
  border-radius: 1rem;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border);
}

.no-matches h3 {
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.no-matches p {
  color: var(--text-secondary);
  margin-bottom: 1.25rem;
}

.btn-primary {
  display: inline-block;
  padding: 0.875rem 1.875rem;
  background: var(--primary);
  color: var(--bg);
  border-radius: 0.5rem;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.matches-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1.25rem;
}

.match-card {
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: var(--shadow-md);
  transition: all 0.3s;
  cursor: pointer;
}

.match-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.match-image {
  width: 100%;
  height: 200px;
  background: var(--surface);
  display: flex;
  align-items: center;
  justify-content: center;
}

.match-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  font-size: 60px;
  color: var(--primary);
  font-weight: bold;
}

.match-info {
  padding: 15px;
}

.match-info h3 {
  margin: 0 0 5px 0;
  color: var(--text-primary);
}

.matched-at {
  font-size: 12px;
  color: var(--text-secondary);
  margin: 0;
}
</style>
