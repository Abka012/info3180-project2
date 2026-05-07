<template>
  <div class="favorites-container">
    <div class="favorites-header">
      <h1>Favorites</h1>
      <p>Profiles you've bookmarked</p>
    </div>

    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
      <p>Loading favorites...</p>
    </div>

    <div v-else-if="favorites.length === 0" class="no-favorites">
      <div class="no-favorites-icon">💜</div>
      <h3>No favorites yet</h3>
      <p>Bookmark profiles to save them here for later</p>
      <router-link to="/search" class="btn-primary"
        >Search Profiles</router-link
      >
    </div>

    <div v-else>
      <div class="filters-bar">
        <label>Sort:</label>
        <select v-model="sortBy" class="sort-select" @change="sortFavorites">
          <option value="recent">Most Recent</option>
          <option value="similarity">Similarity</option>
          <option value="age">Age</option>
        </select>
      </div>

      <div class="favorites-grid">
        <div
          v-for="profile in sortedFavorites"
          :key="profile.user_id"
          class="profile-card"
        >
          <div class="profile-image">
            <img
              v-if="profile.profile_picture"
              :src="`${API_BASE_URL}/uploads/${profile.profile_picture}`"
              alt="Profile"
            />
            <div v-else class="avatar-placeholder">
              {{ profile.name?.charAt(0) }}
            </div>
            <div v-if="profile.match_score" class="match-badge">
              {{ profile.match_score }}%
            </div>
          </div>

          <div class="profile-info">
            <h3>{{ profile.name }}, {{ profile.age }}</h3>

            <p class="bio">
              {{ profile.bio?.substring(0, 80)
              }}{{ profile.bio?.length > 80 ? "..." : "" }}
            </p>

            <div class="interests">
              <span
                v-for="interest in profile.interests?.slice(0, 3)"
                :key="interest"
                class="interest-tag"
              >
                {{ interest }}
              </span>
            </div>

            <div class="profile-meta">
              <span class="bookmarked-at">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="meta-icon"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z"
                    clip-rule="evenodd"
                  />
                </svg>
                Saved {{ formatDate(profile.bookmarked_at) }}
              </span>
            </div>

            <div class="profile-actions">
              <button class="btn-remove" @click="removeBookmark(profile)">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="remove-icon"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fill-rule="evenodd"
                    d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z"
                    clip-rule="evenodd"
                  />
                </svg>
                Remove
              </button>
              <router-link :to="`/profile/${profile.user_id}`" class="btn-view"
                >View Profile</router-link
              >
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import searchService from "../services/searchService";
import { API_BASE_URL } from "../services/api";

const favorites = ref([]);
const loading = ref(true);
const sortBy = ref("recent");

const sortedFavorites = computed(() => {
  const sorted = [...favorites.value];

  if (sortBy.value === "similarity") {
    sorted.sort((a, b) => b.match_score - a.match_score);
  } else if (sortBy.value === "age") {
    sorted.sort((a, b) => a.age - b.age);
  } else {
    sorted.sort(
      (a, b) => new Date(b.bookmarked_at) - new Date(a.bookmarked_at),
    );
  }

  return sorted;
});

const loadFavorites = async () => {
  loading.value = true;
  try {
    favorites.value = await searchService.getBookmarks();
  } catch (error) {
    console.error("Failed to load favorites:", error);
  } finally {
    loading.value = false;
  }
};

const removeBookmark = async (profile) => {
  try {
    await searchService.removeBookmark(profile.user_id);
    favorites.value = favorites.value.filter(
      (f) => f.user_id !== profile.user_id,
    );
  } catch (error) {
    console.error("Failed to remove bookmark:", error);
  }
};

const sortFavorites = () => {};

const formatDate = (dateString) => {
  if (!dateString) return "";
  const date = new Date(dateString);
  const now = new Date();
  const diff = now - date;

  if (diff < 60000) return "just now";
  if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`;
  if (diff < 604800000) return `${Math.floor(diff / 86400000)}d ago`;
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
  padding: 1.5rem;
}

.favorites-header {
  text-align: center;
  margin-bottom: 2rem;
}

.favorites-header h1 {
  font-size: 2rem;
  font-weight: 700;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
}

.favorites-header p {
  color: var(--text-secondary);
}

.filters-bar {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  padding: 0.75rem 1rem;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 0.75rem;
}

[data-theme="dark"] .filters-bar {
  background: var(--surface);
  border-color: var(--border);
}

.filters-bar label {
  font-weight: 600;
  font-size: 0.85rem;
  color: var(--text-primary);
}

.sort-select {
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--border);
  border-radius: 0.5rem;
  font-size: 0.85rem;
  background: var(--bg);
  color: var(--text-primary);
  cursor: pointer;
}

[data-theme="dark"] .sort-select {
  background: var(--input-bg);
  border-color: var(--border);
  color: var(--text-primary);
}

.favorites-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1.5rem;
}

.profile-card {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 1rem;
  overflow: hidden;
  transition: all 0.3s;
  box-shadow: var(--shadow-md);
}

[data-theme="dark"] .profile-card {
  background: var(--surface);
  border-color: var(--border);
}

.profile-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.profile-image {
  position: relative;
  height: 180px;
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
  background: linear-gradient(135deg, var(--accent), var(--accent));
  color: var(--text-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  font-weight: bold;
}

.match-badge {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  padding: 0.25rem 0.6rem;
  background: var(--success);
  color: var(--bg);
  border-radius: 9999px;
  font-size: 0.7rem;
  font-weight: 700;
}

.profile-info {
  padding: 1rem;
}

.profile-info h3 {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 0.25rem;
}

.bio {
  font-size: 0.8rem;
  color: var(--text-secondary);
  margin: 0 0 0.75rem;
  line-height: 1.4;
}

.interests {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
  margin-bottom: 0.75rem;
}

.interest-tag {
  padding: 0.2rem 0.5rem;
  background: var(--surface);
  color: var(--text-secondary);
  border-radius: 9999px;
  font-size: 0.65rem;
  font-weight: 600;
  border: 1px solid var(--border);
}

.profile-meta {
  margin-bottom: 0.75rem;
}

.bookmarked-at {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.7rem;
  color: var(--text-secondary);
}

.meta-icon {
  width: 12px;
  height: 12px;
}

.profile-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 0.75rem;
  border-top: 1px solid var(--border);
}

.btn-remove {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.45rem 0.75rem;
  background: var(--surface);
  color: var(--danger);
  border: 1px solid var(--border);
  border-radius: 0.5rem;
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-remove:hover {
  background: var(--border);
}

.remove-icon {
  width: 14px;
  height: 14px;
}

.btn-view {
  padding: 0.5rem 1rem;
  background: var(--accent);
  color: var(--text-primary);
  border-radius: 0.5rem;
  font-size: 0.8rem;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-view:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.no-favorites {
  text-align: center;
  padding: 4rem 2rem;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 1rem;
}

[data-theme="dark"] .no-favorites {
  background: var(--surface);
}

.no-favorites-icon {
  font-size: 3.5rem;
  margin-bottom: 1rem;
}

.no-favorites h3 {
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.no-favorites p {
  color: var(--text-secondary);
  margin-bottom: 1.5rem;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: var(--primary);
  color: var(--bg);
  border-radius: 0.6rem;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.loading {
  text-align: center;
  padding: 4rem;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--border);
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
</style>
