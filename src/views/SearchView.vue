<template>
  <div class="search-container">
    <h1>Search Profiles</h1>
    
    <div class="search-form">
      <div class="form-row">
        <div class="form-group">
          <label>Location</label>
          <input v-model="searchParams.location" type="text" placeholder="City or area" />
        </div>
        
        <div class="form-group">
          <label>Age Range</label>
          <div class="age-inputs">
            <input v-model.number="searchParams.age_min" type="number" placeholder="Min" min="18" max="100" />
            <span>-</span>
            <input v-model.number="searchParams.age_max" type="number" placeholder="Max" min="18" max="100" />
          </div>
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label>Gender</label>
          <select v-model="searchParams.gender">
            <option value="">Any</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="non-binary">Non-binary</option>
          </select>
        </div>
        
        <div class="form-group">
          <label>Relationship Goal</label>
          <select v-model="searchParams.relationship_goal">
            <option value="">Any</option>
            <option value="dating">Dating</option>
            <option value="relationship">Relationship</option>
            <option value="friendship">Friendship</option>
            <option value="casual">Casual</option>
          </select>
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label>Interests</label>
          <input v-model="interestsInput" type="text" placeholder="music, travel, gaming (comma separated)" />
        </div>
        
        <div class="form-group">
          <label>Occupation</label>
          <input v-model="searchParams.occupation" type="text" placeholder="Job title or field" />
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label>Sort By</label>
          <select v-model="searchParams.sort_by">
            <option value="newest">Newest</option>
            <option value="oldest">Oldest</option>
            <option value="similarity">Most Similar</option>
            <option value="distance">Nearest</option>
            <option value="age_asc">Age: Youngest first</option>
            <option value="age_desc">Age: Oldest first</option>
          </select>
        </div>
        
        <div class="form-group btn-group">
          <button @click="handleSearch" class="btn-primary" :disabled="searching">
            {{ searching ? 'Searching...' : 'Search' }}
          </button>
          <button @click="clearFilters" class="btn-secondary">Clear</button>
        </div>
      </div>
    </div>
    
    <div v-if="loading" class="loading">Loading results...</div>
    
    <div v-else-if="results.length === 0 && searched" class="no-results">
      <h3>No profiles found</h3>
      <p>Try adjusting your search criteria</p>
    </div>
    
    <div v-else class="results-grid">
      <div v-for="profile in results" :key="profile.user_id" class="profile-card">
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
          
          <div class="profile-actions">
            <button @click="toggleBookmark(profile)" class="btn-icon" :class="{ active: profile.is_bookmarked }">
              {{ profile.is_bookmarked ? '★' : '☆' }}
            </button>
            <router-link :to="`/profile/${profile.user_id}`" class="btn-secondary">View Profile</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import searchService from '../services/searchService';

const searchParams = reactive({
  location: '',
  age_min: null,
  age_max: null,
  gender: '',
  relationship_goal: '',
  occupation: '',
  sort_by: 'newest'
});

const interestsInput = ref('');
const results = ref([]);
const loading = ref(false);
const searching = ref(false);
const searched = ref(false);

const handleSearch = async () => {
  loading.value = true;
  searching.value = true;
  searched.value = true;
  
  try {
    const params = { ...searchParams };
    
    if (interestsInput.value) {
      params.interests = interestsInput.value.split(',').map(i => i.trim()).filter(i => i);
    }
    
    Object.keys(params).forEach(key => {
      if (params[key] === '' || params[key] === null) {
        delete params[key];
      }
    });
    
    results.value = await searchService.searchProfiles(params);
  } catch (error) {
    console.error('Search failed:', error);
  } finally {
    loading.value = false;
    searching.value = false;
  }
};

const clearFilters = () => {
  searchParams.location = '';
  searchParams.age_min = null;
  searchParams.age_max = null;
  searchParams.gender = '';
  searchParams.relationship_goal = '';
  searchParams.occupation = '';
  searchParams.sort_by = 'newest';
  interestsInput.value = '';
  results.value = [];
  searched.value = false;
};

const toggleBookmark = async (profile) => {
  try {
    await searchService.toggleBookmark(profile.user_id, profile.is_bookmarked);
    profile.is_bookmarked = !profile.is_bookmarked;
  } catch (error) {
    console.error('Failed to toggle bookmark:', error);
  }
};
</script>

<style scoped>
.search-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  margin-bottom: 20px;
}

.search-form {
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  margin-bottom: 20px;
}

.form-row {
  display: flex;
  gap: 20px;
  margin-bottom: 15px;
}

.form-group {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: 500;
  margin-bottom: 5px;
  color: #333;
}

.form-group input,
.form-group select {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 14px;
}

.age-inputs {
  display: flex;
  align-items: center;
  gap: 10px;
}

.age-inputs input {
  width: 80px;
}

.btn-group {
  flex-direction: row;
  align-items: flex-end;
  gap: 10px;
}

.btn-group button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
}

.btn-primary {
  background: #ff6b6b;
  color: white;
}

.btn-primary:disabled {
  background: #ccc;
}

.btn-secondary {
  background: #f0f0f0;
  color: #333;
}

.results-grid {
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

.profile-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.btn-icon {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #ccc;
}

.btn-icon.active {
  color: #ffc107;
}

.no-results {
  text-align: center;
  padding: 40px;
  color: #666;
}

.loading {
  text-align: center;
  padding: 40px;
  color: #666;
}
</style>
