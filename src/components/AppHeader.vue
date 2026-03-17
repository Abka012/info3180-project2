<template>
  <header>
    <nav class="navbar">
      <div class="nav-container">
        <router-link to="/" class="logo">DriftDater</router-link>
        
        <div class="nav-links">
          <router-link to="/">Home</router-link>
          <router-link to="/about">About</router-link>
          
          <template v-if="isAuthenticated">
            <router-link to="/profile">My Profile</router-link>
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
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import authService from '../services/authService';

const router = useRouter();
const isAuthenticated = ref(false);

const checkAuth = () => {
  isAuthenticated.value = authService.isAuthenticated();
};

const handleLogout = async () => {
  try {
    await authService.logout();
    router.push('/');
  } catch (error) {
    console.error('Logout failed');
  }
};

onMounted(checkAuth);
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
