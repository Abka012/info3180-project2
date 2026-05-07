<template>
  <div class="browse-container">
    <div class="filters-bar">
      <div class="filter-group">
        <label>Age Range:</label>
        <input
          v-model="filters.ageMin"
          type="number"
          placeholder="Min"
          min="18"
          max="100"
          class="filter-input"
        />
        <span class="filter-separator">-</span>
        <input
          v-model="filters.ageMax"
          type="number"
          placeholder="Max"
          min="18"
          max="100"
          class="filter-input"
        />
      </div>
      <button class="filter-btn" @click="applyFilters">Apply Filters</button>
    </div>

    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
      <p>Finding your perfect match...</p>
    </div>

    <div v-else-if="!currentProfile" class="no-profiles">
      <div class="no-profiles-icon">✨</div>
      <h3>No more profiles to show</h3>
      <p>Check back later for new matches!</p>
    </div>

    <div v-else class="profile-card">
      <div class="profile-image">
        <img
          v-if="currentProfile.profile_picture"
          :src="`http://localhost:5000/uploads/${currentProfile.profile_picture}`"
          alt="Profile"
        />
        <div v-else class="avatar-placeholder">
          {{ currentProfile.name?.charAt(0) }}
        </div>
        <div v-if="currentProfile.match_score" class="match-badge">
          {{ currentProfile.match_score }}% Match
        </div>
      </div>

      <div class="profile-info">
        <h2>{{ currentProfile.name }}, {{ currentProfile.age }}</h2>

        <p class="bio">{{ currentProfile.bio }}</p>

        <div class="interests">
          <span
            v-for="interest in currentProfile.interests"
            :key="interest"
            class="interest-tag"
          >
            {{ interest }}
          </span>
        </div>

        <div class="profile-details">
          <div>
            <span class="detail-label">Goal:</span>
            {{ formatGoal(currentProfile.relationship_goal) }}
          </div>
          <div>
            <span class="detail-label">Occupation:</span>
            {{ currentProfile.occupation }}
          </div>
        </div>
      </div>

      <div class="action-buttons">
        <button class="btn-action btn-pass" @click="handlePass">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="btn-icon-svg"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fill-rule="evenodd"
              d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
              clip-rule="evenodd"
            />
          </svg>
          Pass
        </button>
        <button class="btn-action btn-dislike" @click="handleDislike">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="btn-icon-svg"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fill-rule="evenodd"
              d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z"
              clip-rule="evenodd"
            />
          </svg>
          Dislike
        </button>
        <button class="btn-action btn-like" @click="handleLike">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="btn-icon-svg"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fill-rule="evenodd"
              d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z"
              clip-rule="evenodd"
            />
          </svg>
          Like
        </button>
      </div>
    </div>

    <div
      v-if="showMatchPopup"
      class="match-popup"
      @click.self="closeMatchPopup"
    >
      <div class="popup-content">
        <div class="match-animation">
          <div class="heart heart-1">❤️</div>
          <div class="heart heart-2">💕</div>
          <div class="heart heart-3">💗</div>
        </div>
        <h2>It's a Match!</h2>
        <p>You and {{ matchedProfile?.name }} liked each other!</p>
        <button class="btn-primary" @click="closeMatchPopup">
          Keep Browsing
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import matchService from "../services/matchService";

const profiles = ref([]);
const currentIndex = ref(0);
const loading = ref(true);
const showMatchPopup = ref(false);
const matchedProfile = ref(null);

const filters = ref({
  ageMin: 18,
  ageMax: 50,
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
    console.error("Failed to load profiles:", error);
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
    console.error("Failed to like user:", error);
    nextProfile();
  }
};

const handleDislike = async () => {
  if (!currentProfile.value) return;

  try {
    await matchService.dislikeUser(currentProfile.value.user_id);
  } catch (error) {
    console.error("Failed to dislike user:", error);
  }

  nextProfile();
};

const handlePass = async () => {
  if (!currentProfile.value) return;

  try {
    await matchService.passUser(currentProfile.value.user_id);
  } catch (error) {
    console.error("Failed to pass user:", error);
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
    friendship: "Friendship",
    casual_dating: "Casual Dating",
    serious_relationship: "Serious Relationship",
    marriage: "Marriage",
  };
  return map[goal] || goal;
};

onMounted(loadProfiles);
</script>

<style scoped>
.browse-container {
  max-width: 420px;
  margin: 0 auto;
  padding: 1rem;
  min-height: calc(100vh - 8rem);
}

.filters-bar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: var(--bg);
  backdrop-filter: blur(10px);
  border: 1px solid var(--border);
  border-radius: 1rem;
  box-shadow: var(--shadow-md);
}

[data-theme="dark"] .filters-bar {
  background: var(--surface);
  border-color: var(--border);
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-group label {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-primary);
}

[data-theme="dark"] .filter-group label {
  color: var(--text-secondary);
}

.filter-input {
  width: 60px;
  padding: 0.5rem;
  border: 1px solid var(--border);
  border-radius: 0.5rem;
  font-size: 0.8rem;
  background: var(--bg);
  color: var(--text-primary);
  transition: all 0.2s;
}

[data-theme="dark"] .filter-input {
  background: var(--surface);
  border-color: var(--border);
  color: var(--text-primary);
}

.filter-input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px var(--surface);
}

.filter-separator {
  color: var(--text-secondary);
  font-weight: 600;
}

.filter-btn {
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, var(--primary-light), var(--primary));
  color: var(--bg);
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-btn:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow-lg);
}

.profile-card {
  background: var(--bg);
  backdrop-filter: blur(10px);
  border: 1px solid var(--border);
  border-radius: 1.5rem;
  overflow: hidden;
  box-shadow: var(--shadow-lg);
}

[data-theme="dark"] .profile-card {
  background: var(--surface);
  border-color: var(--border);
}

.profile-image {
  position: relative;
  height: 380px;
  overflow: hidden;
}

.profile-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 6rem;
  font-weight: bold;
  color: var(--bg);
}

.match-badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  padding: 0.35rem 0.85rem;
  background: var(--primary);
  color: var(--bg);
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 700;
  box-shadow: var(--shadow-md);
}

.profile-info {
  padding: 1.25rem;
}

.profile-info h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}

[data-theme="dark"] .profile-info h2 {
  color: var(--text-primary);
}

.bio {
  color: var(--text-secondary);
  font-size: 0.9rem;
  line-height: 1.5;
  margin-bottom: 1rem;
}

[data-theme="dark"] .bio {
  color: var(--text-secondary);
}

.interests {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin-bottom: 1rem;
}

.interest-tag {
  padding: 0.25rem 0.7rem;
  background: var(--surface);
  color: var(--text-primary);
  border-radius: 9999px;
  font-size: 0.7rem;
  font-weight: 600;
  border: 1px solid var(--border);
}

[data-theme="dark"] .interest-tag {
  background: var(--surface);
  color: var(--text-primary);
}

.profile-details {
  display: flex;
  gap: 1rem;
  font-size: 0.8rem;
  color: var(--text-secondary);
}

[data-theme="dark"] .profile-details {
  color: var(--text-secondary);
}

.detail-label {
  font-weight: 600;
  color: var(--text-primary);
}

[data-theme="dark"] .detail-label {
  color: var(--text-primary);
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 0.75rem;
  padding: 1rem;
  border-top: 1px solid var(--border);
}

[data-theme="dark"] .action-buttons {
  border-color: var(--border);
}

.btn-action {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.35rem;
  padding: 0.7rem 1.25rem;
  border: none;
  border-radius: 9999px;
  font-weight: 600;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-icon-svg {
  width: 18px;
  height: 18px;
}

.btn-pass {
  background: var(--surface);
  color: var(--danger);
  border: 1px solid var(--border);
}

.btn-pass:hover {
  background: var(--surface);
  transform: scale(1.05);
}

.btn-dislike {
  background: var(--surface);
  color: var(--warning);
  border: 1px solid var(--border);
}

.btn-dislike:hover {
  background: var(--surface);
  transform: scale(1.05);
}

.btn-like {
  background: linear-gradient(135deg, var(--primary-light), var(--primary));
  color: var(--bg);
  box-shadow: var(--shadow-md);
}

.btn-like:hover {
  transform: scale(1.05);
  box-shadow: var(--shadow-lg);
}

.no-profiles {
  text-align: center;
  padding: 3rem;
}

.no-profiles-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.no-profiles h3 {
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

[data-theme="dark"] .no-profiles h3 {
  color: var(--text-primary);
}

.no-profiles p {
  color: var(--text-secondary);
}

[data-theme="dark"] .no-profiles p {
  color: var(--text-secondary);
}

.loading {
  text-align: center;
  padding: 3rem;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid var(--surface);
  border-top-color: var(--primary);
  border-radius: 50%;
  margin: 0 auto 1rem;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading p {
  color: var(--text-secondary);
  font-weight: 500;
}

.match-popup {
  position: fixed;
  inset: 0;
  background: var(--overlay);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  animation: fadeIn 0.3s ease;
}

.popup-content {
  background: var(--bg);
  padding: 2.5rem;
  border-radius: 1.5rem;
  text-align: center;
  max-width: 360px;
  animation: scaleIn 0.4s ease;
  box-shadow: var(--shadow-2xl);
}

[data-theme="dark"] .popup-content {
  background: var(--surface);
}

.match-animation {
  position: relative;
  height: 60px;
  margin-bottom: 1rem;
}

.heart {
  position: absolute;
  font-size: 2.5rem;
  animation: heartbeat 1.2s ease-in-out infinite;
}

.heart-1 {
  left: 50%;
  transform: translateX(-50%);
}
.heart-2 {
  left: 30%;
  animation-delay: 0.2s;
}
.heart-3 {
  right: 30%;
  animation-delay: 0.4s;
}

@keyframes heartbeat {
  0%,
  100% {
    transform: translateX(-50%) scale(1);
  }
  50% {
    transform: translateX(-50%) scale(1.2);
  }
}

.popup-content h2 {
  background: linear-gradient(135deg, var(--primary), var(--accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
  font-size: 1.75rem;
  font-weight: 700;
}

.popup-content p {
  color: var(--text-secondary);
  font-size: 0.95rem;
}

[data-theme="dark"] .popup-content p {
  color: var(--text-secondary);
}

.btn-primary {
  margin-top: 1.5rem;
  padding: 0.875rem 2rem;
  background: linear-gradient(135deg, var(--primary-light), var(--primary));
  color: var(--bg);
  border: none;
  border-radius: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}
</style>
tyle> >
