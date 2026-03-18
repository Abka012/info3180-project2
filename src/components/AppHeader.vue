<template>
  <header>
    <nav class="navbar">
      <div class="nav-container">
        <router-link to="/" class="logo">DriftDater</router-link>
        
        <div class="nav-links">
          <router-link to="/">Home</router-link>
          <router-link to="/about">About</router-link>
          
          <template v-if="isAuthenticated">
            <router-link to="/browse">Browse</router-link>
            <router-link to="/search">Search</router-link>
            <router-link to="/matches">Matches</router-link>
            <router-link to="/favorites">Favorites</router-link>
            <router-link to="/profile">My Profile</router-link>
            <router-link to="/notifications" class="notification-link">
              Notifications
              <span v-if="totalUnread > 0" class="badge">{{ totalUnread }}</span>
            </router-link>
            <router-link to="/conversations" class="message-link">
              Messages
              <span v-if="messageUnread > 0" class="badge">{{ messageUnread }}</span>
            </router-link>
            <a href="#" @click.prevent="handleLogout">Logout</a>
          </template>
          
          <template v-else>
            <router-link to="/login">Login</router-link>
            <router-link to="/register" class="btn-register">Register</router-link>
          </template>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import authService from '../services/authService';
import notificationService from '../services/notificationService';
import messageService from '../services/messageService';
import socketService from '../services/socketService';

const router = useRouter();
const isAuthenticated = ref(false);
const unreadCount = ref(0);
const messageUnread = ref(0);

const totalUnread = computed(() => unreadCount.value + messageUnread.value);

import { computed } from 'vue';

const checkAuth = () => {
  isAuthenticated.value = authService.isAuthenticated();
};

const loadUnreadCount = async () => {
  if (!isAuthenticated.value) return;
  try {
    const [notifData, msgData] = await Promise.all([
      notificationService.getUnreadCount(),
      messageService.getUnreadCount()
    ]);
    unreadCount.value = notifData.unread_count;
    messageUnread.value = msgData.unread_count;
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

<style scoped>
.navbar {
  background: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 15px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 24px;
  font-weight: bold;
  color: #e91e63;
  text-decoration: none;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 25px;
}

.nav-links a {
  color: #333;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s;
}

.nav-links a:hover {
  color: #e91e63;
}

.notification-link {
  position: relative;
}

.badge {
  position: absolute;
  top: -8px;
  right: -12px;
  background: #e91e63;
  color: white;
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 10px;
  font-weight: bold;
}

.btn-register {
  padding: 8px 20px;
  background: #e91e63;
  color: white !important;
  border-radius: 20px;
}

.btn-register:hover {
  background: #c2185b;
}
</style>
