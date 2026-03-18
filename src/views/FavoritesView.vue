<template>
  <div class="favorites-container">
    <h1>Favorites</h1>
    
    <div v-if="loading" class="loading">Loading favorites...</div>
    
    <div v-else-if="favorites.length === 0" class="no-favorites">
      <h3>No favorites yet</h3>
      <p>Bookmark profiles to save them here for later</p>
      <router-link to="/search" class="btn-primary">Search Profiles</router-link>
    </div>
    
    <div v-else class="filters-bar">
      <label>Sort by:</label>
      <select v-model="sortBy" @change="sortFavorites">
        <option value="recent">Most Recent</option>
        <option value="similarity">Similarity</option>
        <option value="age">Age</option>
      </select>
    </div>
    
    <div v-if="!loading && favorites.length > 0" class="favorites-grid">
      <div v-for="profile in sortedFavorites" :key="profile.user_id" class="profile-card">
        <div class="profile-image">
          <img v-if="profile.profile_picture" :src="`http://localhost:5000/uploads/${profile.profile_picture}`" alt="Profile" />
          <div v-else class="avatar-placeholder">{{ profile.name?.charAt(0) }}</div>
        </div>
        
        <div class="profile-info">
          <h3>{{ profile.name }}, {{ profile.age }}</h3>
          <p class="location">{{ profile.location }}</p>
          
          <div v-if="profile.match_score" class="match-score">
            <span class="score-badge">{{ profile.match_score }}% Match</span>
          </div>
          
          <p class="bio">{{ profile.bio?.substring(0, 100) }}{{ profile.bio?.length > 100 ? '...' : '' }}</p>
          
          <div class="interests">
            <span v-for="interest in profile.interests?.slice(0, 3)" :key="interest" class="interest-tag">
              {{ interest }}
            </span>
          </div>
          
          <div class="profile-meta">
            <span class="bookmarked-at">Saved {{ formatDate(profile.bookmarked_at) }}</span>
          </div>
          
          <div class="profile-actions">
            <button @click="removeBookmark(profile)" class="btn-remove">Remove</button>
            <router-link :to="`/profile/${profile.user_id}`" class="btn-secondary">View Profile</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import searchService from '../services/searchService';

const favorites = ref([]);
const loading = ref(true);
const sortBy = ref('recent');

const sortedFavorites = computed(() => {
  const sorted = [...favorites.value];
  
  if (sortBy.value === 'similarity') {
    sorted.sort((a, b) => b.match_score - a.match_score);
  } else if (sortBy.value === 'age') {
    sorted.sort((a, b) => a.age - b.age);
  } else {
    sorted.sort((a, b) => new Date(b.bookmarked_at) - new Date(a.bookmarked_at));
  }
  
  return sorted;
});

const loadFavorites = async () => {
  loading.value = true;
  try {
    favorites.value = await searchService.getBookmarks();
  } catch (error) {
    console.error('Failed to load favorites:', error);
  } finally {
    loading.value = false;
  }
};

const removeBookmark = async (profile) => {
  try {
    await searchService.removeBookmark(profile.user_id);
    favorites.value = favorites.value.filter(f => f.user_id !== profile.user_id);
  } catch (error) {
    console.error('Failed to remove bookmark:', error);
  }
};

const sortFavorites = () => {};

const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  const now = new Date();
  const diff = now - date;
  
  if (diff < 60000) return 'just now';
  if (diff < 3600000) return `${Math.floor(diff / 60000)} minutes ago`;
  if (diff < 86400000) return `${Math.floor(diff / 3600000)} hours ago`;
  if (diff < 604800000) return `${Math.floor(diff / 86400000)} days ago`;
  return date.toLocaleDateString();
};

onMounted(() => {
  loadFavorites();
});
</script>

<style scoped>
.favorites-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  margin-bottom: 20px;
}

.filters-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

.filters-bar label {
  font-weight: 500;
}

.filters-bar select {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.favorites-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.profile-card {
  background: white;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.profile-image {
  height: 200px;
  overflow: hidden;
}

.profile-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 200px;
  background: #ff6b6b;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48px;
  font-weight: bold;
}

.profile-info {
  padding: 15px;
}

.profile-info h3 {
  margin: 0 0 5px;
  font-size: 18px;
}

.location {
  color: #666;
  font-size: 14px;
  margin: 0 0 10px;
}

.match-score {
  margin-bottom: 10px;
}

.score-badge {
  background: #4caf50;
  color: white;
  padding: 3px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: bold;
}

.bio {
  font-size: 14px;
  color: #666;
  margin: 10px 0;
}

.interests {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin-bottom: 10px;
}

.interest-tag {
  background: #f0f0f0;
  padding: 3px 8px;
  border-radius: 12px;
  font-size: 12px;
}

.profile-meta {
  margin-bottom: 10px;
}

.bookmarked-at {
  font-size: 12px;
  color: #888;
}

.profile-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.btn-remove {
  background: #ff4444;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 5px;
  cursor: pointer;
}

.btn-secondary {
  background: #f0f0f0;
  color: #333;
  padding: 8px 12px;
  border-radius: 5px;
  text-decoration: none;
  font-size: 14px;
}

.no-favorites {
  text-align: center;
  padding: 40px;
}

.btn-primary {
  display: inline-block;
  background: #ff6b6b;
  color: white;
  padding: 10px 20px;
  border-radius: 20px;
  text-decoration: none;
  margin-top: 15px;
}

.loading {
  text-align: center;
  padding: 40px;
  color: #666;
}
</style>
