<template>
  <div class="settings-container">
    <div class="settings-header">
      <h1>Settings</h1>
      <p>Manage your account preferences</p>
    </div>

    <div class="settings-content">
      <div class="settings-nav">
        <button
          v-for="section in sections"
          :key="section.id"
          class="nav-item"
          :class="{ active: activeSection === section.id }"
          @click="activeSection = section.id"
        >
          <span class="nav-icon" v-html="section.icon"></span>
          <span class="nav-label">{{ section.label }}</span>
        </button>
      </div>

      <div class="settings-panel">
        <div v-if="activeSection === 'account'" class="section">
          <h2>Account Settings</h2>
          <p class="section-desc">
            Manage your account security and information
          </p>

          <div class="setting-group">
            <div class="setting-item">
              <div class="setting-info">
                <h4>Email</h4>
                <p>{{ userEmail }}</p>
              </div>
              <button class="btn-secondary">Change</button>
            </div>

            <div class="setting-item">
              <div class="setting-info">
                <h4>Password</h4>
                <p>Last changed: Never</p>
              </div>
              <button class="btn-secondary">Update</button>
            </div>
          </div>

          <div class="danger-zone">
            <h3>Danger Zone</h3>
            <div class="setting-item danger">
              <div class="setting-info">
                <h4>Delete Account</h4>
                <p>Permanently delete your account and all data</p>
              </div>
              <button class="btn-danger" @click="confirmDelete">
                Delete Account
              </button>
            </div>
          </div>
        </div>

        <div v-if="activeSection === 'privacy'" class="section">
          <h2>Privacy Settings</h2>
          <p class="section-desc">
            Control who can see your profile and information
          </p>

          <div class="setting-group">
            <div class="setting-item toggle-item">
              <div class="setting-info">
                <h4>Public Profile</h4>
                <p>Allow others to discover your profile in search</p>
              </div>
              <label class="toggle">
                <input
                  v-model="privacySettings.publicProfile"
                  type="checkbox"
                />
                <span class="toggle-slider"></span>
              </label>
            </div>

            <div class="setting-item toggle-item">
              <div class="setting-info">
                <h4>Show Online Status</h4>
                <p>Let others see when you're online</p>
              </div>
              <label class="toggle">
                <input v-model="privacySettings.showOnline" type="checkbox" />
                <span class="toggle-slider"></span>
              </label>
            </div>

            <div class="setting-item">
              <div class="setting-info">
                <h4>Blocked Users</h4>
                <p>{{ blockedUsers.length }} users blocked</p>
              </div>
              <button class="btn-secondary" @click="showBlockedModal = true">
                Manage
              </button>
            </div>
          </div>
        </div>

        <div v-if="activeSection === 'notifications'" class="section">
          <h2>Notification Preferences</h2>
          <p class="section-desc">Choose how you want to be notified</p>

          <div class="setting-group">
            <div class="setting-item toggle-item">
              <div class="setting-info">
                <h4>Push Notifications</h4>
                <p>Receive push notifications on your device</p>
              </div>
              <label class="toggle">
                <input v-model="notificationSettings.push" type="checkbox" />
                <span class="toggle-slider"></span>
              </label>
            </div>

            <div class="setting-item toggle-item">
              <div class="setting-info">
                <h4>Email Notifications</h4>
                <p>Receive notifications via email</p>
              </div>
              <label class="toggle">
                <input v-model="notificationSettings.email" type="checkbox" />
                <span class="toggle-slider"></span>
              </label>
            </div>

            <div class="setting-item toggle-item">
              <div class="setting-info">
                <h4>New Matches</h4>
                <p>Get notified when you have new matches</p>
              </div>
              <label class="toggle">
                <input
                  v-model="notificationSettings.newMatches"
                  type="checkbox"
                />
                <span class="toggle-slider"></span>
              </label>
            </div>

            <div class="setting-item toggle-item">
              <div class="setting-info">
                <h4>New Messages</h4>
                <p>Get notified when you receive messages</p>
              </div>
              <label class="toggle">
                <input
                  v-model="notificationSettings.newMessages"
                  type="checkbox"
                />
                <span class="toggle-slider"></span>
              </label>
            </div>

            <div class="setting-item toggle-item">
              <div class="setting-info">
                <h4>Likes</h4>
                <p>Get notified when someone likes your profile</p>
              </div>
              <label class="toggle">
                <input v-model="notificationSettings.likes" type="checkbox" />
                <span class="toggle-slider"></span>
              </label>
            </div>
          </div>
        </div>

        <div v-if="activeSection === 'appearance'" class="section">
          <h2>Appearance</h2>
          <p class="section-desc">Customize how the app looks</p>

          <div class="setting-group">
            <div class="setting-item">
              <div class="setting-info">
                <h4>Theme</h4>
                <p>Choose your preferred color scheme</p>
              </div>
            </div>
            <div class="theme-options">
              <button
                v-for="theme in themes"
                :key="theme.value"
                class="theme-option"
                :class="{ active: currentTheme === theme.value }"
                @click="setTheme(theme.value)"
              >
                <span
                  class="theme-icon"
                  :style="{ background: theme.preview }"
                ></span>
                <span class="theme-label">{{ theme.label }}</span>
              </button>
            </div>
          </div>
        </div>

        <div v-if="activeSection === 'about'" class="section">
          <h2>About</h2>
          <p class="section-desc">App information and legal</p>

          <div class="setting-group">
            <div class="setting-item">
              <div class="setting-info">
                <h4>Version</h4>
                <p>1.0.0</p>
              </div>
            </div>

            <router-link to="/about" class="setting-item link-item">
              <div class="setting-info">
                <h4>About DriftDater</h4>
                <p>Learn more about our app</p>
              </div>
              <span class="arrow">→</span>
            </router-link>

            <a href="#" class="setting-item link-item">
              <div class="setting-info">
                <h4>Terms of Service</h4>
                <p>Read our terms</p>
              </div>
              <span class="arrow">→</span>
            </a>

            <a href="#" class="setting-item link-item">
              <div class="setting-info">
                <h4>Privacy Policy</h4>
                <p>How we handle your data</p>
              </div>
              <span class="arrow">→</span>
            </a>

            <a href="#" class="setting-item link-item">
              <div class="setting-info">
                <h4>Help & Support</h4>
                <p>Get help with any issues</p>
              </div>
              <span class="arrow">→</span>
            </a>
          </div>
        </div>
      </div>
    </div>

    <div
      v-if="showBlockedModal"
      class="modal-overlay"
      @click.self="showBlockedModal = false"
    >
      <div class="modal">
        <h3>Blocked Users</h3>
        <div v-if="blockedUsers.length === 0" class="empty-state">
          <p>No blocked users</p>
        </div>
        <div v-else class="blocked-list">
          <div v-for="user in blockedUsers" :key="user.id" class="blocked-item">
            <div class="blocked-info">
              <span class="blocked-name">{{ user.name }}</span>
            </div>
            <button class="btn-secondary small" @click="unblockUser(user.id)">
              Unblock
            </button>
          </div>
        </div>
        <button class="btn-secondary" @click="showBlockedModal = false">
          Close
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import authService from "../services/authService";

const activeSection = ref("account");
const userEmail = ref("");
const showBlockedModal = ref(false);
const currentTheme = ref(localStorage.getItem("theme") || "light");

let mediaQuery = null;
let mediaQueryListener = null;

const sections = [
  {
    id: "account",
    label: "Account",
    icon: '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
  },
  {
    id: "privacy",
    label: "Privacy",
    icon: '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>',
  },
  {
    id: "notifications",
    label: "Notifications",
    icon: '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/></svg>',
  },
  {
    id: "appearance",
    label: "Appearance",
    icon: '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>',
  },
  {
    id: "about",
    label: "About",
    icon: '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>',
  },
];

const themes = [
  {
    value: "light",
    label: "Light",
    preview:
      "linear-gradient(135deg, var(--color-surface), var(--color-gray-100))",
  },
  {
    value: "dark",
    label: "Dark",
    preview: "linear-gradient(135deg, var(--color-bg), var(--color-surface))",
  },
  {
    value: "system",
    label: "System",
    preview:
      "linear-gradient(135deg, var(--color-card) 50%, var(--color-bg) 50%)",
  },
];

const privacySettings = ref({
  publicProfile: true,
  showOnline: true,
});

const notificationSettings = ref({
  push: true,
  email: false,
  newMatches: true,
  newMessages: true,
  likes: true,
});

const blockedUsers = ref([]);

const setTheme = (theme) => {
  if (mediaQuery && mediaQueryListener) {
    mediaQuery.removeEventListener("change", mediaQueryListener);
    mediaQuery = null;
    mediaQueryListener = null;
  }

  currentTheme.value = theme;

  if (theme === "system") {
    const prefersDark = window.matchMedia(
      "(prefers-color-scheme: dark)",
    ).matches;
    const systemTheme = prefersDark ? "dark" : "light";
    document.documentElement.setAttribute("data-theme", systemTheme);
    localStorage.setItem("theme", "system");
  } else {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
  }
};

const confirmDelete = () => {
  if (
    confirm(
      "Are you sure you want to delete your account? This action cannot be undone.",
    )
  ) {
    alert("Account deletion would be processed here.");
  }
};

const unblockUser = (userId) => {
  blockedUsers.value = blockedUsers.value.filter((u) => u.id !== userId);
};

onMounted(() => {
  const savedTheme = localStorage.getItem("theme");
  if (savedTheme) {
    currentTheme.value = savedTheme;
    if (savedTheme === "system") {
      const prefersDark = window.matchMedia(
        "(prefers-color-scheme: dark)",
      ).matches;
      const systemTheme = prefersDark ? "dark" : "light";
      document.documentElement.setAttribute("data-theme", systemTheme);
    } else {
      document.documentElement.setAttribute("data-theme", savedTheme);
    }
  } else {
    const prefersDark = window.matchMedia(
      "(prefers-color-scheme: dark)",
    ).matches;
    const theme = prefersDark ? "dark" : "light";
    document.documentElement.setAttribute("data-theme", theme);
  }
});
</script>

<style scoped>
.settings-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}

.settings-header {
  text-align: center;
  margin-bottom: 2rem;
}

.settings-header h1 {
  font-size: 2rem;
  font-weight: 700;
  background: linear-gradient(
    135deg,
    var(--color-primary),
    var(--color-accent)
  );
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
}

.settings-header p {
  color: var(--color-text-secondary);
}

[data-theme="dark"] .settings-header p {
  color: var(--color-text-secondary);
}

.settings-content {
  display: grid;
  grid-template-columns: 240px 1fr;
  gap: 2rem;
}

@media (max-width: 768px) {
  .settings-content {
    grid-template-columns: 1fr;
  }

  .settings-nav {
    flex-direction: row;
    overflow-x: auto;
    gap: 0.5rem;
    padding-bottom: 0.5rem;
  }

  .nav-item {
    flex-direction: column;
    min-width: 80px;
    padding: 0.75rem;
    text-align: center;
  }
}

.settings-nav {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border: none;
  background: transparent;
  border-radius: 0.75rem;
  cursor: pointer;
  transition: all 0.2s;
  color: var(--color-text-secondary);
  text-align: left;
}

[data-theme="dark"] .nav-item {
  color: var(--color-text-secondary);
}

.nav-item:hover {
  background: var(--surface);
  color: var(--color-primary);
}

.nav-item.active {
  background: var(--surface);
  color: var(--color-primary);
  font-weight: 600;
}

.nav-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

.settings-panel {
  background: var(--bg);
  backdrop-filter: blur(10px);
  border: 1px solid var(--surface);
  border-radius: 1rem;
  padding: 1.5rem;
}

[data-theme="dark"] .settings-panel {
  background: var(--color-surface);
  border-color: var(--surface);
}

.section h2 {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: 0.25rem;
}

[data-theme="dark"] .section h2 {
  color: var(--color-text);
}

.section-desc {
  color: var(--color-text-secondary);
  margin-bottom: 1.5rem;
}

[data-theme="dark"] .section-desc {
  color: var(--color-text-secondary);
}

.setting-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.setting-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  background: var(--bg);
  border: 1px solid var(--surface);
  border-radius: 0.75rem;
}

[data-theme="dark"] .setting-item {
  background: var(--color-card);
  border-color: var(--bg);
}

.setting-item.link-item {
  cursor: pointer;
  color: inherit;
}

.setting-info h4 {
  font-weight: 600;
  color: var(--color-text);
  margin: 0 0 0.25rem 0;
}

[data-theme="dark"] .setting-info h4 {
  color: var(--color-text);
}

.setting-info p {
  font-size: 0.875rem;
  color: var(--color-text-secondary);
  margin: 0;
}

[data-theme="dark"] .setting-info p {
  color: var(--color-text-secondary);
}

.arrow {
  color: var(--color-text-secondary);
  font-size: 1.25rem;
}

.toggle-item {
  align-items: center;
}

.toggle {
  position: relative;
  display: inline-block;
  width: 48px;
  height: 26px;
  flex-shrink: 0;
}

.toggle input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: var(--color-text-secondary);
  border-radius: 26px;
  transition: 0.3s;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 20px;
  width: 20px;
  left: 3px;
  bottom: 3px;
  background-color: var(--color-text);
  border-radius: 50%;
  transition: 0.3s;
}

.toggle input:checked + .toggle-slider {
  background: linear-gradient(
    135deg,
    var(--color-primary-light),
    var(--color-primary)
  );
}

.toggle input:checked + .toggle-slider:before {
  transform: translateX(22px);
}

.btn-secondary {
  padding: 0.5rem 1rem;
  background: var(--color-surface);
  color: var(--color-text);
  border: none;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

[data-theme="dark"] .btn-secondary {
  background: var(--color-card);
  color: var(--color-text);
}

.btn-secondary:hover {
  background: var(--color-surface);
}

[data-theme="dark"] .btn-secondary:hover {
  background: var(--color-card);
}

.btn-secondary.small {
  padding: 0.375rem 0.75rem;
  font-size: 0.875rem;
}

.btn-danger {
  padding: 0.5rem 1rem;
  background: var(--surface);
  color: var(--color-danger);
  border: none;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

[data-theme="dark"] .btn-danger {
  background: var(--surface);
  color: var(--color-danger);
}

.btn-danger:hover {
  background: var(--surface);
}

.danger-zone {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--surface);
}

[data-theme="dark"] .danger-zone {
  border-top-color: var(--bg);
}

.danger-zone h3 {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color-danger);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 1rem;
}

[data-theme="dark"] .danger-zone h3 {
  color: var(--color-danger);
}

.danger-zone .setting-item {
  border-color: var(--surface);
}

.theme-options {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.theme-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  background: var(--bg);
  border: 2px solid transparent;
  border-radius: 0.75rem;
  cursor: pointer;
  transition: all 0.2s;
}

[data-theme="dark"] .theme-option {
  background: var(--color-card);
}

.theme-option:hover {
  border-color: var(--surface);
}

.theme-option.active {
  border-color: var(--color-primary);
  background: var(--surface);
}

.theme-icon {
  width: 48px;
  height: 48px;
  border-radius: 0.5rem;
  border: 1px solid var(--surface);
}

.theme-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--color-text);
}

[data-theme="dark"] .theme-label {
  color: var(--color-text);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--surface);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  padding: 1rem;
}

.modal {
  background: var(--bg);
  border-radius: 1rem;
  padding: 1.5rem;
  max-width: 400px;
  width: 100%;
  max-height: 80vh;
  overflow-y: auto;
}

[data-theme="dark"] .modal {
  background: var(--color-card);
}

.modal h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: 1rem;
}

[data-theme="dark"] .modal h3 {
  color: var(--color-text);
}

.empty-state {
  text-align: center;
  padding: 2rem;
  color: var(--color-text-secondary);
}

.blocked-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.blocked-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem;
  background: var(--color-text);
  border-radius: 0.5rem;
}

[data-theme="dark"] .blocked-item {
  background: var(--color-card);
}

.blocked-name {
  font-weight: 500;
  color: var(--color-text);
}

[data-theme="dark"] .blocked-name {
  color: var(--color-text);
}
</style>
