<template>
  <header class="fixed top-0 left-0 right-0 z-50 bg-white/80 dark:bg-gray-900/80 backdrop-blur-md border-b border-gray-200 dark:border-gray-700 transition-colors duration-300">
    <nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo -->
        <router-link to="/" class="flex items-center space-x-2">
          <div class="w-8 h-8 rounded-full bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center">
            <span class="text-white font-bold text-sm">D</span>
          </div>
          <span class="text-xl font-bold bg-gradient-to-r from-primary-600 to-accent-600 bg-clip-text text-transparent">
            DriftDater
          </span>
        </router-link>

        <!-- Desktop Navigation -->
        <div class="hidden md:flex items-center space-x-1">
          <template v-if="isAuthenticated">
            <router-link 
              v-for="item in authNavItems" 
              :key="item.path"
              :to="item.path"
              class="relative px-3 py-2 rounded-lg text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
              :class="{ '!bg-primary-50 dark:!bg-primary-900/20 !text-primary-600 dark:!text-primary-400': $route.path === item.path }"
            >
              {{ item.name }}
              <span v-if="item.badge" class="absolute -top-1 -right-1 bg-primary-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                {{ item.badge }}
              </span>
            </router-link>
          </template>
          <template v-else>
            <router-link to="/about" class="px-3 py-2 rounded-lg text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800">
              About
            </router-link>
          </template>
        </div>

        <!-- Right Side Actions -->
        <div class="flex items-center space-x-2">
          <!-- Dark Mode Toggle -->
          <button
            @click="toggleDarkMode"
            class="p-2 rounded-lg text-gray-500 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-800 transition-colors"
          >
            <svg v-if="isDark" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
            <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
            </svg>
          </button>

          <!-- Auth Buttons -->
          <template v-if="!isAuthenticated">
            <router-link to="/login" class="hidden sm:block px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors">
              Login
            </router-link>
            <router-link to="/register" class="px-4 py-2 text-sm font-medium text-white bg-primary-500 hover:bg-primary-600 rounded-lg transition-colors">
              Sign Up
            </router-link>
          </template>
          <button
            v-else
            @click="handleLogout"
            class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors"
          >
            Logout
          </button>

          <!-- Mobile Menu Button -->
          <button
            @click="mobileMenuOpen = !mobileMenuOpen"
            class="md:hidden p-2 rounded-lg text-gray-500 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-800"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path v-if="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
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
        <div v-if="mobileMenuOpen" class="md:hidden py-4 border-t border-gray-200 dark:border-gray-700">
          <div class="flex flex-col space-y-1">
            <template v-if="isAuthenticated">
              <router-link 
                v-for="item in authNavItems" 
                :key="item.path"
                :to="item.path"
                class="px-3 py-2 rounded-lg text-base font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800"
                @click="mobileMenuOpen = false"
              >
                {{ item.name }}
                <span v-if="item.badge" class="ml-2 bg-primary-500 text-white text-xs rounded-full px-2 py-0.5">
                  {{ item.badge }}
                </span>
              </router-link>
            </template>
            <template v-else>
              <router-link to="/about" class="px-3 py-2 rounded-lg text-base font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800" @click="mobileMenuOpen = false">
                About
              </router-link>
            </template>
          </div>
        </div>
      </transition>
    </nav>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import authService from '../services/authService';
import notificationService from '../services/notificationService';
import messageService from '../services/messageService';
import socketService from '../services/socketService';

const router = useRouter();
const route = useRoute();

const isAuthenticated = ref(false);
const unreadCount = ref(0);
const messageUnread = ref(0);
const mobileMenuOpen = ref(false);
const isDark = ref(false);

const totalUnread = computed(() => unreadCount.value + messageUnread.value);

const authNavItems = computed(() => {
  const items = [
    { name: 'Browse', path: '/browse' },
    { name: 'Search', path: '/search' },
    { name: 'Matches', path: '/matches' },
    { name: 'Favorites', path: '/favorites' },
    { name: 'Notifications', path: '/notifications', badge: unreadCount.value || null },
    { name: 'Messages', path: '/conversations', badge: messageUnread.value || null },
  ];
  return items;
});

const toggleDarkMode = () => {
  isDark.value = !isDark.value;
  if (isDark.value) {
    document.documentElement.classList.add('dark');
    localStorage.setItem('theme', 'dark');
  } else {
    document.documentElement.classList.remove('dark');
    localStorage.setItem('theme', 'light');
  }
};

const checkAuth = () => {
  isAuthenticated.value = authService.isAuthenticated();
  isDark.value = document.documentElement.classList.contains('dark');
};

const loadUnreadCount = async () => {
  if (!isAuthenticated.value) return;
  try {
    const [notifData, msgData] = await Promise.all([
      notificationService.getUnreadCount().catch(() => ({ unread_count: 0 })),
      messageService.getUnreadCount().catch(() => ({ unread_count: 0 }))
    ]);
    unreadCount.value = notifData.unread_count || 0;
    messageUnread.value = msgData.unread_count || 0;
  } catch (error) {
    console.error('Failed to load unread count:', error);
  }
};

const handleLogout = async () => {
  socketService.disconnect();
  await authService.logout();
  router.push('/');
};

const handleNewNotification = () => {
  loadUnreadCount();
};

const handleNewMessage = () => {
  loadUnreadCount();
};

onMounted(() => {
  checkAuth();
  loadUnreadCount();
  
  if (isAuthenticated.value) {
    socketService.connect();
    socketService.on('notification', handleNewNotification);
    socketService.on('new_match', handleNewNotification);
    socketService.on('new_like', handleNewNotification);
    socketService.on('new_message', handleNewMessage);
  }
});

onUnmounted(() => {
  socketService.off('notification', handleNewNotification);
  socketService.off('new_match', handleNewNotification);
  socketService.off('new_like', handleNewNotification);
  socketService.off('new_message', handleNewMessage);
});
</script>
