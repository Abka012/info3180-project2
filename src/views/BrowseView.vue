<template>
  <div class="browse-container">
    <div class="filters-bar">
      <div class="filter-group">
        <label>Age Range:</label>
        <input type="number" v-model="filters.ageMin" placeholder="Min" min="18" max="100" />
        <span>-</span>
        <input type="number" v-model="filters.ageMax" placeholder="Max" min="18" max="100" />
      </div>
      <div class="filter-group">
        <label>Distance (km):</label>
        <input type="number" v-model="filters.distance" placeholder="Max" min="1" />
      </div>
      <button @click="applyFilters" class="filter-btn">Apply Filters</button>
    </div>

    <div v-if="loading" class="loading">Loading potential matches...</div>
    
    <div v-else-if="!currentProfile" class="no-profiles">
      <h3>No more profiles to show</h3>
      <p>Check back later for new matches!</p>
    </div>
    
    <div v-else class="profile-card">
      <div class="profile-image">
        <img v-if="currentProfile.profile_picture" :src="`http://localhost:5000/uploads/${currentProfile.profile_picture}`" alt="Profile" />
        <div v-else class="avatar-placeholder">{{ currentProfile.name?.charAt(0) }}</div>
      </div>
      
      <div class="profile-info">
        <h2>{{ currentProfile.name }}, {{ currentProfile.age }}</h2>
        <p class="location">{{ currentProfile.location }}</p>
        
        <div v-if="currentProfile.match_score" class="match-score">
          <span class="score-badge">{{ currentProfile.match_score }}% Match</span>
        </div>
        
        <p class="bio">{{ currentProfile.bio }}</p>
        
        <div class="interests">
          <span v-for="interest in currentProfile.interests" :key="interest" class="interest-tag">
            {{ interest }}
          </span>
        </div>
        
        <div class="profile-details">
          <div><strong>Goal:</strong> {{ formatGoal(currentProfile.relationship_goal) }}</div>
          <div><strong>Occupation:</strong> {{ currentProfile.occupation }}</div>
        </div>
      </div>
      
      <div class="action-buttons">
        <button class="btn-pass" @click="handlePass">
          <span class="icon">✕</span>
          Pass
        </button>
        <button class="btn-dislike" @click="handleDislike">
          <span class="icon">♥</span>
          Dislike
        </button>
        <button class="btn-like" @click="handleLike">
          <span class="icon">❤️</span>
          Like
        </button>
      </div>
    </div>
    
    <div v-if="showMatchPopup" class="match-popup">
      <div class="popup-content">
        <div class="hearts">💕</div>
        <h2>It's a Match!</h2>
        <p>You and {{ matchedProfile?.name }} liked each other!</p>
        <button @click="closeMatchPopup" class="btn-primary">Keep Browsing</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import matchService from '../services/matchService';

const profiles = ref([]);
const currentIndex = ref(0);
const loading = ref(true);
const showMatchPopup = ref(false);
const matchedProfile = ref(null);

const filters = ref({
  ageMin: 18,
  ageMax: 50,
  distance: 50
});

const currentProfile = ref(null);

const loadProfiles = async () => {
  loading.value = true;
  try {
    const data = await matchService.getPotentialMatches(filters.value);
    profiles.value = data;
    currentIndex.value = 0;
    currentProfile.value = profiles.value[0] || null;
  } catch (error) {
    console.error('Failed to load profiles:', error);
  } finally {
    loading.value = false;
  }
};

const applyFilters = () => {
  loadProfiles();
};

const handleLike = async () => {
  if (!currentProfile.value) return;
  
  try {
    const result = await matchService.likeUser(currentProfile.value.user_id);
    
    if (result.match) {
      matchedProfile.value = result.matched_profile;
      showMatchPopup.value = true;
    }
    
    nextProfile();
  } catch (error) {
    console.error('Failed to like user:', error);
    nextProfile();
  }
};

const handleDislike = async () => {
  if (!currentProfile.value) return;
  
  try {
    await matchService.dislikeUser(currentProfile.value.user_id);
  } catch (error) {
    console.error('Failed to dislike user:', error);
  }
  
  nextProfile();
};

const handlePass = async () => {
  if (!currentProfile.value) return;
  
  try {
    await matchService.passUser(currentProfile.value.user_id);
  } catch (error) {
    console.error('Failed to pass user:', error);
  }
  
  nextProfile();
};

const nextProfile = () => {
  currentIndex.value++;
  currentProfile.value = profiles.value[currentIndex.value] || null;
};

const closeMatchPopup = () => {
  showMatchPopup.value = false;
  matchedProfile.value = null;
};

const formatGoal = (goal) => {
  const map = {
    'friendship': 'Friendship',
    'casual_dating': 'Casual Dating',
    'serious_relationship': 'Serious Relationship',
    'marriage': 'Marriage'
  };
  return map[goal] || goal;
};

onMounted(loadProfiles);
</script>

<style scoped>
.browse-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.filters-bar {
  display: flex;
  gap: 15px;
  align-items: flex-end;
  padding: 15px;
  background: white;
  border-radius: 12px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-group label {
  font-size: 14px;
  color: #666;
}

.filter-group input {
  width: 60px;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 6px;
}

.filter-btn {
  padding: 8px 16px;
  background: #e91e63;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.loading {
  text-align: center;
  padding: 60px;
  color: #666;
}

.no-profiles {
  text-align: center;
  padding: 60px;
  background: white;
  border-radius: 12px;
}

.profile-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.profile-image {
  width: 100%;
  height: 350px;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
}

.profile-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  font-size: 80px;
  color: #e91e63;
  font-weight: bold;
}

.profile-info {
  padding: 20px;
}

.profile-info h2 {
  margin: 0 0 5px 0;
  color: #333;
}

.location {
  color: #666;
  margin: 0 0 10px 0;
}

.match-score {
  margin-bottom: 10px;
}

.score-badge {
  display: inline-block;
  padding: 4px 12px;
  background: #4caf50;
  color: white;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
}

.bio {
  color: #555;
  margin: 15px 0;
  line-height: 1.5;
}

.interests {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 15px 0;
}

.interest-tag {
  padding: 6px 14px;
  background: #fce4ec;
  color: #e91e63;
  border-radius: 20px;
  font-size: 14px;
}

.profile-details {
  margin-top: 15px;
  font-size: 14px;
  color: #666;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  padding: 20px;
  border-top: 1px solid #eee;
}

.action-buttons button {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  padding: 15px 25px;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  font-weight: 600;
  transition: transform 0.2s;
}

.action-buttons button:hover {
  transform: scale(1.1);
}

.btn-pass {
  background: #f5f5f5;
  color: #999;
}

.btn-dislike {
  background: #fff3e0;
  color: #ff9800;
}

.btn-like {
  background: #fce4ec;
  color: #e91e63;
}

.icon {
  font-size: 24px;
}

.match-popup {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.popup-content {
  background: white;
  padding: 40px;
  border-radius: 20px;
  text-align: center;
  max-width: 400px;
}

.hearts {
  font-size: 60px;
  margin-bottom: 20px;
}

.popup-content h2 {
  color: #e91e63;
  margin-bottom: 10px;
}

.btn-primary {
  margin-top: 20px;
  padding: 14px 30px;
  background: #e91e63;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
}
</style>
