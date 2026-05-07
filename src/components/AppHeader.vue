<template>
  <header
    class="fixed top-0 left-0 right-0 z-50 bg-[var(--bg)]/80 bg-[var(--surface)]/80 backdrop-blur-md border-b border-[var(--border)] transition-colors duration-300 py-2 px-4"
  >
    <nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo -->
        <router-link to="/" class="flex items-center space-x-2">
          <div
            class="w-8 h-8 rounded-full bg-gradient-to-br from-[var(--primary)] to-[var(--accent)] flex items-center justify-center"
          >
            <span class="text-[var(--text-primary)] font-bold text-sm"
              ><svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 100 100"
                class="w-5 h-5"
              >
                <path
                  d="M50 88.87C25.32 66.64 9.5 55.15 9.5 36.5 9.5 20.44 22.73 9.5 37.5 9.5c8.18 0 15.86 4.72 19.5 12.56C60.64 14.22 68.32 9.5 76.5 9.5 91.27 9.5 104.5 20.44 104.5 36.5c0 18.65-15.82 30.14-40.5 52.37z"
                  fill="currentColor"
                  transform="translate(-7, -7) scale(0.85)"
                /></svg
            ></span>
          </div>
          <span
            class="text-xl font-bold bg-gradient-to-r from-[var(--primary)] to-[var(--success)] bg-clip-text text-transparent"
          >
            DriftDater
          </span>
        </router-link>

        <!-- Desktop Navigation -->
        <div class="hidden md:flex items-center space-x-1">
          <template v-if="isAuthenticated">
            <router-link
              to="/browse"
              class="px-3 py-2 rounded-lg text-sm font-medium text-[var(--text-secondary)] hover:bg-[var(--surface)] hover:bg-[var(--surface)] transition-colors"
            >
              Browse
            </router-link>

            <router-link
              to="/search"
              class="px-3 py-2 rounded-lg text-sm font-medium text-[var(--text-secondary)] hover:bg-[var(--surface)] hover:bg-[var(--surface)] transition-colors"
            >
              Search
            </router-link>

            <router-link
              to="/matches"
              class="px-3 py-2 rounded-lg text-sm font-medium text-[var(--text-secondary)] hover:bg-[var(--surface)] hover:bg-[var(--surface)] transition-colors"
            >
              Matches
            </router-link>

            <router-link
              to="/messages"
              class="relative px-3 py-2 rounded-lg text-sm font-medium text-[var(--text-secondary)] hover:bg-[var(--surface)] hover:bg-[var(--surface)] transition-colors"
            >
              Messages
              <span
                v-if="messageUnread"
                class="absolute -top-1 -right-1 bg-[var(--danger)] text-[var(--text-primary)] text-xs rounded-full w-5 h-5 flex items-center justify-center"
              >
                {{ messageUnread > 9 ? "9+" : messageUnread }}
              </span>
            </router-link>

            <router-link
              to="/favorites"
              class="px-3 py-2 rounded-lg text-sm font-medium text-[var(--text-secondary)] hover:bg-[var(--surface)] hover:bg-[var(--surface)] transition-colors"
            >
              Favorites
            </router-link>
          </template>
        </div>

        <!-- Right Side Actions -->
        <div class="flex items-center space-x-2">
          <!-- Dark Mode Toggle -->
          <button
            class="p-2 rounded-lg text-[var(--text-secondary)] hover:bg-[var(--surface)] text-[var(--text-secondary)] hover:bg-[var(--surface)] transition-colors"
            title="Toggle theme"
            @click="toggleDarkMode"
          >
            <svg
              v-if="isDark"
              class="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
              />
            </svg>
            <svg
              v-else
              class="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
              />
            </svg>
          </button>

          <!-- User Avatar Dropdown (Desktop) -->
          <div v-if="isAuthenticated" class="relative hidden md:block">
            <button
              class="flex items-center gap-2 p-1 rounded-full hover:bg-[var(--surface)] hover:bg-[var(--surface)] transition-colors"
              @click="dropdownOpen = !dropdownOpen"
            >
              <div
                class="w-8 h-8 rounded-full overflow-hidden border-2 border-[var(--bg)] shadow-sm"
              >
                <img
                  v-if="userProfilePicture"
                  :src="`http://localhost:5000/uploads/${userProfilePicture}`"
                  class="w-full h-full object-cover"
                  @error="($event) => ($event.target.style.display = 'none')"
                />
                <div
                  v-else
                  class="w-full h-full bg-gradient-to-br from-[var(--primary)] to-[var(--accent)] flex items-center justify-center"
                >
                  <span class="text-[var(--text-primary)] font-bold text-xs">{{
                    userInitials
                  }}</span>
                </div>
              </div>
              <svg
                class="w-4 h-4 text-[var(--text-secondary)]"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M19 9l-7 7-7-7"
                />
              </svg>
            </button>

            <!-- Dropdown Menu -->
            <transition
              enter-active-class="transition duration-150 ease-out"
              enter-from-class="opacity-0 scale-95"
              enter-to-class="opacity-100 scale-100"
              leave-active-class="transition duration-100 ease-in"
              leave-from-class="opacity-100 scale-100"
              leave-to-class="opacity-0 scale-95"
            >
              <div
                v-if="dropdownOpen"
                class="absolute right-0 mt-2 w-64 bg-[var(--bg)] rounded-xl shadow-lg border border-[var(--border)] py-2 z-50"
                @click="dropdownOpen = false"
              >
                <div
                  class="px-4 py-3 border-b border-[var(--border)] flex items-center gap-3"
                >
                  <div
                    class="w-10 h-10 rounded-full overflow-hidden border-2 border-[var(--border)] flex-shrink-0"
                  >
                    <img
                      v-if="userProfilePicture"
                      :src="`http://localhost:5000/uploads/${userProfilePicture}`"
                      class="w-full h-full object-cover"
                      @error="
                        ($event) => ($event.target.style.display = 'none')
                      "
                    />
                    <div
                      v-else
                      class="w-full h-full bg-gradient-to-br from-[var(--primary)] to-[var(--accent)] flex items-center justify-center"
                    >
                      <span
                        class="text-[var(--text-primary)] font-bold text-sm"
                        >{{ userInitials }}</span
                      >
                    </div>
                  </div>
                  <div class="flex-1 min-w-0">
                    <p
                      class="text-sm font-medium text-[var(--text-primary)] truncate"
                    >
                      {{ userName }}
                    </p>
                  </div>
                </div>

                <!-- Navigation Items -->
                <router-link to="/browse" class="dropdown-item">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="18"
                    height="18"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <circle cx="12" cy="12" r="10" />
                    <polygon
                      points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"
                    />
                  </svg>
                  Browse
                </router-link>

                <router-link to="/search" class="dropdown-item">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="18"
                    height="18"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <circle cx="11" cy="11" r="8" />
                    <path d="m21 21-4.3-4.3" />
                  </svg>
                  Search
                </router-link>

                <router-link to="/matches" class="dropdown-item">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="18"
                    height="18"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <path
                      d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"
                    />
                  </svg>
                  Matches
                </router-link>

                <router-link to="/messages" class="dropdown-item relative">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="18"
                    height="18"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <path
                      d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"
                    />
                  </svg>
                  Messages
                  <span
                    v-if="messageUnread"
                    class="ml-auto bg-[var(--danger)] text-[var(--text-primary)] text-xs rounded-full px-2 py-0.5"
                  >
                    {{ messageUnread > 9 ? "9+" : messageUnread }}
                  </span>
                </router-link>

                <router-link to="/favorites" class="dropdown-item">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="18"
                    height="18"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <path
                      d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"
                    />
                  </svg>
                  Favorites
                </router-link>

                <div class="border-t border-[var(--border)] my-1"></div>

                <!-- Account Settings -->
                <router-link to="/profile" class="dropdown-item">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="18"
                    height="18"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2" />
                    <circle cx="12" cy="7" r="4" />
                  </svg>
                  My Profile
                </router-link>

                <router-link to="/settings" class="dropdown-item">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="18"
                    height="18"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <circle cx="12" cy="12" r="3" />
                    <path
                      d="M12 1v4m0 14v4m-9-9h4m10 0h4m-2.64-6.36-2.82 2.82m-7.08 7.08L4.46 14.1m11.31 0-2.82-2.82m0 0L8.9 7.5"
                    />
                  </svg>
                  Settings
                </router-link>

                <router-link to="/notifications" class="dropdown-item relative">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="18"
                    height="18"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9" />
                    <path d="M10.3 21a1.94 1.94 0 0 0 3.4 0" />
                  </svg>
                  Notifications
                  <span
                    v-if="unreadCount"
                    class="ml-auto bg-[var(--danger)] text-[var(--text-primary)] text-xs rounded-full px-2 py-0.5"
                  >
                    {{ unreadCount > 9 ? "9+" : unreadCount }}
                  </span>
                </router-link>

                <div class="border-t border-[var(--border)] my-1"></div>

                <button
                  class="dropdown-item text-[var(--danger)] text-[var(--danger)] hover:bg-[var(--surface)] w-full"
                  @click="confirmLogout"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="18"
                    height="18"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
                    <polyline points="16 17 21 12 16 7" />
                    <line x1="21" x2="9" y1="12" y2="12" />
                  </svg>
                  Logout
                </button>
              </div>
            </transition>
          </div>

          <!-- Auth Buttons (Desktop) -->
          <div v-else class="hidden md:flex items-center space-x-2">
            <router-link
              to="/login"
              class="px-4 py-2 text-sm font-medium text-[var(--text-secondary)] hover:bg-[var(--surface)] hover:bg-[var(--surface)] rounded-lg transition-colors"
            >
              Login
            </router-link>
            <router-link
              to="/register"
              class="px-4 py-2 text-sm font-medium text-[var(--text-primary)] bg-[var(--primary)] hover:bg-[var(--primary)] rounded-lg transition-colors"
            >
              Sign Up
            </router-link>
          </div>

          <!-- Mobile Menu Button -->
          <button
            class="md:hidden p-2 rounded-lg text-[var(--text-secondary)] hover:bg-[var(--surface)] text-[var(--text-secondary)] hover:bg-[var(--surface)]"
            @click="mobileMenuOpen = !mobileMenuOpen"
          >
            <svg
              class="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                v-if="!mobileMenuOpen"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 6h16M4 12h16M4 18h16"
              />
              <path
                v-else
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>
      </div>

      <!-- Mobile Menu -->
      <transition
        enter-active-class="transition duration-200 ease-out"
        enter-from-class="opacity-0 -translate-y-2"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition duration-150 ease-in"
        leave-from-class="opacity-100 translate-y-0"
        leave-to-class="opacity-0 -translate-y-2"
      >
        <div
          v-if="mobileMenuOpen"
          class="md:hidden py-4 border-t border-[var(--border)]"
        >
          <div class="flex flex-col space-y-1">
            <template v-if="isAuthenticated">
              <!-- Navigation Items -->
              <router-link
                to="/browse"
                class="flex items-center gap-3 px-3 py-2 rounded-lg text-base font-medium text-[var(--text-secondary)] hover:bg-[var(--surface)] hover:bg-[var(--surface)]"
                @click="mobileMenuOpen = false"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <circle cx="12" cy="12" r="10" />
                  <polygon
                    points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"
                  />
                </svg>
                Browse
              </router-link>

              <router-link
                to="/search"
                class="flex items-center gap-3 px-3 py-2 rounded-lg text-base font-medium text-[var(--text-secondary)] hover:bg-[var(--surface)] hover:bg-[var(--surface)]"
                @click="mobileMenuOpen = false"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <circle cx="11" cy="11" r="8" />
                  <path d="m21 21-4.3-4.3" />
                </svg>
                Search
              </router-link>

              <router-link
                to="/matches"
                class="flex items-center gap-3 px-3 py-2 rounded-lg text-base font-medium text-[var(--text-secondary)] hover:bg-[var(--surface)] hover:bg-[var(--surface)]"
                @click="mobileMenuOpen = false"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"
                  />
                </svg>
                Matches
              </router-link>

              <router-link
                to="/messages"
                class="flex items-center gap-3 px-3 py-2 rounded-lg text-base font-medium text-[var(--text-secondary)] hover:bg-[var(--surface)] hover:bg-[var(--surface)]"
                @click="mobileMenuOpen = false"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"
                  />
                </svg>
                Messages
                <span
                  v-if="messageUnread"
                  class="ml-auto bg-[var(--danger)] text-[var(--text-primary)] text-xs rounded-full px-2 py-0.5"
                >
                  {{ messageUnread }}
                </span>
              </router-link>

              <router-link
                to="/favorites"
                class="flex items-center gap-3 px-3 py-2 rounded-lg text-base font-medium text-[var(--text-secondary)] hover:bg-[var(--surface)] hover:bg-[var(--surface)]"
                @click="mobileMenuOpen = false"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z" />
                </svg>
                Favorites
              </router-link>

              <div class="border-t border-[var(--border)] my-2 pt-2">
                <router-link
                  to="/profile"
                  class="flex items-center gap-3 px-3 py-2 rounded-lg text-base font-medium text-[var(--text-secondary)] hover:bg-[var(--surface)] hover:bg-[var(--surface)]"
                  @click="mobileMenuOpen = false"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="20"
                    height="20"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2" />
                    <circle cx="12" cy="7" r="4" />
                  </svg>
                  My Profile
                </router-link>

                <router-link
                  to="/settings"
                  class="flex items-center gap-3 px-3 py-2 rounded-lg text-base font-medium text-[var(--text-secondary)] hover:bg-[var(--surface)] hover:bg-[var(--surface)]"
                  @click="mobileMenuOpen = false"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="20"
                    height="20"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <circle cx="12" cy="12" r="3" />
                    <path
                      d="M12 1v4m0 14v4m-9-9h4m10 0h4m-2.64-6.36-2.82 2.82m-7.08 7.08L4.46 14.1m11.31 0-2.82-2.82m0 0L8.9 7.5"
                    />
                  </svg>
                  Settings
                </router-link>

                <router-link
                  to="/notifications"
                  class="flex items-center gap-3 px-3 py-2 rounded-lg text-base font-medium text-[var(--text-secondary)] hover:bg-[var(--surface)] hover:bg-[var(--surface)]"
                  @click="mobileMenuOpen = false"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="20"
                    height="20"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9" />
                    <path d="M10.3 21a1.94 1.94 0 0 0 3.4 0" />
                  </svg>
                  Notifications
                  <span
                    v-if="unreadCount"
                    class="ml-auto bg-[var(--danger)] text-[var(--text-primary)] text-xs rounded-full px-2 py-0.5"
                  >
                    {{ unreadCount }}
                  </span>
                </router-link>
              </div>

              <button
                class="flex items-center gap-3 px-3 py-2 rounded-lg text-base font-medium text-[var(--danger)] text-[var(--danger)] hover:bg-[var(--surface)]"
                @click="confirmLogout"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="20"
                  height="20"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
                  <polyline points="16 17 21 12 16 7" />
                  <line x1="21" x2="9" y1="12" y2="12" />
                </svg>
                Logout
              </button>
            </template>
            <template v-else>
              <router-link
                to="/login"
                class="flex items-center gap-3 px-3 py-2 rounded-lg text-base font-medium text-[var(--text-secondary)] hover:bg-[var(--surface)] hover:bg-[var(--surface)]"
                @click="mobileMenuOpen = false"
              >
                Login
              </router-link>
              <router-link
                to="/register"
                class="flex items-center gap-3 px-3 py-2 rounded-lg text-base font-medium text-[var(--text-primary)] bg-[var(--primary)] hover:bg-[var(--primary)]"
                @click="mobileMenuOpen = false"
              >
                Sign Up
              </router-link>
            </template>
          </div>
        </div>
      </transition>
    </nav>
  </header>

  <!-- Logout Confirmation Modal (outside header for proper centering) -->
  <transition
    enter-active-class="transition duration-200 ease-out"
    enter-from-class="opacity-0 scale-95"
    enter-to-class="opacity-100 scale-100"
    leave-active-class="transition duration-150 ease-in"
    leave-from-class="opacity-100 scale-100"
    leave-to-class="opacity-0 scale-95"
  >
    <div
      v-if="showLogoutModal"
      class="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-[var(--overlay)] backdrop-blur-sm"
      @click.self="cancelLogout"
    >
      <div
        class="bg-[var(--bg)] rounded-2xl shadow-2xl p-6 w-full max-w-md"
        @click.stop
      >
        <div class="text-center mb-6">
          <div
            class="w-16 h-16 mx-auto mb-4 rounded-full bg-[var(--surface)] flex items-center justify-center"
          >
            <svg
              class="w-8 h-8 text-[var(--danger)] text-[var(--danger)]"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
              />
            </svg>
          </div>
          <h3 class="text-xl font-bold text-[var(--text-primary)] mb-2">
            Logout
          </h3>
          <p class="text-[var(--text-secondary)]">
            Are you sure you want to logout? You'll need to sign in again to
            access your account.
          </p>
        </div>

        <div class="flex gap-3">
          <button
            class="flex-1 py-3 px-4 bg-[var(--surface)] hover:bg-[var(--surface)] hover:bg-[var(--surface)] text-[var(--text-secondary)] font-medium rounded-full transition-colors"
            @click="cancelLogout"
          >
            Cancel
          </button>
          <button
            class="flex-1 py-3 px-4 bg-[var(--primary)] hover:bg-[var(--primary)] text-[var(--text-primary)] font-medium rounded-full transition-all shadow-lg"
            @click="handleLogout"
          >
            Logout
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import authService from "../services/authService";
import notificationService from "../services/notificationService";
import messageService from "../services/messageService";
import socketService from "../services/socketService";
import { useAuth } from "../composables/useAuth";
import ThemeToggle from '@/components/ThemeToggle.vue'

const router = useRouter();
const { isAuthenticated, logout: authLogout } = useAuth();

const unreadCount = ref(0);
const messageUnread = ref(0);
const mobileMenuOpen = ref(false);
const dropdownOpen = ref(false);
const isDark = ref(false);

// Initialize theme state on component creation
const initTheme = () => {
  const saved = localStorage.getItem("theme");
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  const theme = saved || (prefersDark ? "dark" : "light");
  document.documentElement.setAttribute("data-theme", theme);
  isDark.value = theme === "dark";
};

// Call initTheme immediately
initTheme();

const userName = ref("");
const userEmail = ref("");
const userProfilePicture = ref(null);

const userInitials = computed(() => {
  if (userName.value) {
    return userName.value
      .split(" ")
      .map((n) => n[0])
      .join("")
      .toUpperCase()
      .slice(0, 2);
  }
  return "U";
});

const toggleDarkMode = () => {
  isDark.value = !isDark.value;
  const theme = isDark.value ? "dark" : "light";
  document.documentElement.setAttribute("data-theme", theme);
  localStorage.setItem("theme", theme);
};

const checkAuth = async () => {
  const user = authService.getStoredUser();
  if (user) {
    userName.value = user.name || user.username || "User";
    userEmail.value = user.email || "";
    userProfilePicture.value = user.profile_picture || null;

    if (!user.name || !user.profile_picture) {
      try {
        const freshUser = await authService.getCurrentUser();
        if (freshUser) {
          if (freshUser.name) userName.value = freshUser.name;
          if (freshUser.profile_picture) {
            userProfilePicture.value = freshUser.profile_picture;
          }
        }
      } catch {
        console.warn("Could not fetch fresh user data");
      }
    }
  }
};

const loadUnreadCount = async () => {
  if (!isAuthenticated.value) return;
  try {
    const [notifData, msgData] = await Promise.all([
      notificationService.getUnreadCount().catch(() => ({ unread_count: 0 })),
      messageService.getUnreadCount().catch(() => ({ unread_count: 0 })),
    ]);
    unreadCount.value = notifData.unread_count || 0;
    messageUnread.value = msgData.unread_count || 0;
  } catch (error) {
    console.error("Failed to load unread count:", error);
  }
};

const showLogoutModal = ref(false);

const confirmLogout = () => {
  dropdownOpen.value = false;
  mobileMenuOpen.value = false;
  showLogoutModal.value = true;
};

const handleLogout = async () => {
  showLogoutModal.value = false;
  await authLogout();
  router.push("/");
};

const cancelLogout = () => {
  showLogoutModal.value = false;
};

const handleNewNotification = () => {
  loadUnreadCount();
};

const handleNewMessage = () => {
  loadUnreadCount();
};

const handleClickOutside = (event) => {
  if (dropdownOpen.value && !event.target.closest(".relative")) {
    dropdownOpen.value = false;
  }
};

onMounted(() => {
  checkAuth();
  loadUnreadCount();
  document.addEventListener("click", handleClickOutside);

  if (isAuthenticated.value) {
    socketService.connect();
    socketService.on("notification", handleNewNotification);
    socketService.on("new_match", handleNewNotification);
    socketService.on("new_like", handleNewNotification);
    socketService.on("new_message", handleNewMessage);
  }
});

onUnmounted(() => {
  document.removeEventListener("click", handleClickOutside);
  socketService.off("notification", handleNewNotification);
  socketService.off("new_match", handleNewNotification);
  socketService.off("new_like", handleNewNotification);
  socketService.off("new_message", handleNewMessage);
});
</script>

<style scoped>
.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  width: 100%;
  padding: 0.625rem 1rem;
  text-align: left;
  color: var(--text-secondary);
  font-size: 0.875rem;
  font-weight: 500;
  transition: all 0.15s;
}

.dropdown-item:hover {
  background: var(--surface);
}
</style>
