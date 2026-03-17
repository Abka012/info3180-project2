<template>
  <div class="profile-container">
    <div v-if="loading" class="loading">Loading...</div>
    
    <div v-else-if="!hasProfile" class="no-profile">
      <h2>Create Your Profile</h2>
      <p>You haven't created a profile yet. Let's get started!</p>
      <router-link to="/profile/edit" class="btn-primary">Create Profile</router-link>
    </div>
    
    <div v-else class="profile-card">
      <div class="profile-header">
        <div class="avatar">
          <img v-if="profile.profile_picture" :src="`http://localhost:5000/uploads/${profile.profile_picture}`" alt="Profile Picture" />
          <div v-else class="avatar-placeholder">{{ profile.name?.charAt(0) }}</div>
        </div>
        <div class="profile-info">
          <h2>{{ profile.name }}</h2>
          <p class="age-location">{{ profile.age }} years old {{ profile.location ? `• ${profile.location}` : '' }}</p>
          <span class="visibility-badge" :class="{ private: !profile.visibility }">
            {{ profile.visibility ? 'Public' : 'Private' }}
          </span>
        </div>
        <router-link to="/profile/edit" class="btn-edit">Edit Profile</router-link>
      </div>
      
      <div class="profile-section">
        <h3>About Me</h3>
        <p>{{ profile.bio || 'No bio added yet.' }}</p>
      </div>
      
      <div class="profile-section">
        <h3>Interests</h3>
        <div class="interests">
          <span v-for="interest in profile.interests" :key="interest" class="interest-tag">
            {{ interest }}
          </span>
        </div>
      </div>
      
      <div class="profile-details">
        <div class="detail-item">
          <strong>Gender:</strong> {{ profile.gender || 'Not specified' }}
        </div>
        <div class="detail-item">
          <strong>Interested In:</strong> {{ formatGenderPreference(profile.gender_preference) }}
        </div>
        <div class="detail-item">
          <strong>Location Preference:</strong> {{ formatGeoPreference(profile.geo_preferences) }}
        </div>
        <div class="detail-item">
          <strong>Relationship Goal:</strong> {{ formatRelationshipGoal(profile.relationship_goal) }}
        </div>
        <div class="detail-item">
          <strong>Occupation:</strong> {{ profile.occupation || 'Not specified' }}
        </div>
      </div>
      
      <div class="profile-actions">
        <label class="upload-btn">
          <input type="file" @change="handlePictureUpload" accept="image/*" />
          Upload New Photo
        </label>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import profileService from '../services/profileService';
import authService from '../services/authService';

const router = useRouter();
const loading = ref(true);
const hasProfile = ref(false);
const profile = ref({});

const formatGenderPreference = (pref) => {
  const map = {
    'all': 'Everyone',
    'male': 'Men',
    'female': 'Women',
    'non_binary': 'Non-Binary'
  };
  return map[pref] || pref;
};

const formatGeoPreference = (pref) => {
  const map = {
    'anywhere': 'Anywhere',
    'same_city': 'Same City',
    'same_country': 'Same Country',
    'nearby': 'Nearby (25km)'
  };
  return map[pref] || pref;
};

const formatRelationshipGoal = (goal) => {
  const map = {
    'friendship': 'Friendship',
    'casual_dating': 'Casual Dating',
    'serious_relationship': 'Serious Relationship',
    'marriage': 'Marriage'
  };
  return map[goal] || 'Not specified';
};

const loadProfile = async () => {
  try {
    const user = authService.getStoredUser();
    if (!user) {
      router.push('/login');
      return;
    }
    
    const data = await profileService.getProfile();
    profile.value = data;
    hasProfile.value = true;
  } catch (error) {
    if (error.response?.status === 404) {
      hasProfile.value = false;
    }
  } finally {
    loading.value = false;
  }
};

const handlePictureUpload = async (event) => {
  const file = event.target.files[0];
  if (!file) return;
  
  try {
    await profileService.uploadPicture(file);
    await loadProfile();
    alert('Profile picture updated!');
  } catch (error) {
    alert('Failed to upload picture');
  }
};

onMounted(loadProfile);
</script>

<style scoped>
.profile-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 20px;
}

.loading {
  text-align: center;
  padding: 60px;
  color: #666;
}

.no-profile {
  text-align: center;
  padding: 60px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.no-profile h2 {
  color: #e91e63;
  margin-bottom: 10px;
}

.btn-primary {
  display: inline-block;
  margin-top: 20px;
  padding: 14px 30px;
  background: #e91e63;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  font-weight: 600;
}

.profile-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 30px;
  background: linear-gradient(135deg, #e91e63 0%, #f48fb1 100%);
  color: white;
}

.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  overflow: hidden;
  border: 4px solid white;
  flex-shrink: 0;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  color: #e91e63;
  font-size: 40px;
  font-weight: bold;
}

.profile-info {
  flex: 1;
}

.profile-info h2 {
  margin: 0 0 5px 0;
}

.age-location {
  margin: 0;
  opacity: 0.9;
}

.visibility-badge {
  display: inline-block;
  padding: 4px 12px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  font-size: 12px;
  margin-top: 8px;
}

.visibility-badge.private {
  background: rgba(0, 0, 0, 0.2);
}

.btn-edit {
  padding: 10px 20px;
  background: white;
  color: #e91e63;
  text-decoration: none;
  border-radius: 6px;
  font-weight: 600;
  transition: background 0.3s;
}

.btn-edit:hover {
  background: #f5f5f5;
}

.profile-section {
  padding: 25px 30px;
  border-bottom: 1px solid #eee;
}

.profile-section h3 {
  margin: 0 0 12px 0;
  color: #333;
  font-size: 16px;
}

.profile-section p {
  margin: 0;
  color: #666;
  line-height: 1.6;
}

.interests {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.interest-tag {
  padding: 6px 14px;
  background: #fce4ec;
  color: #e91e63;
  border-radius: 20px;
  font-size: 14px;
}

.profile-details {
  padding: 25px 30px;
}

.detail-item {
  margin-bottom: 12px;
  color: #555;
}

.detail-item strong {
  color: #333;
}

.profile-actions {
  padding: 20px 30px;
  border-top: 1px solid #eee;
}

.upload-btn {
  display: inline-block;
  padding: 10px 20px;
  background: #f5f5f5;
  color: #333;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
}

.upload-btn input {
  display: none;
}

.upload-btn:hover {
  background: #eee;
}
</style>
