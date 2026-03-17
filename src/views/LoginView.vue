<template>
  <div class="auth-container">
    <div class="auth-card">
      <h2>Welcome Back</h2>
      <p class="subtitle">Login to your DriftDater account</p>
      
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="email">Email</label>
          <input 
            id="email"
            v-model="email" 
            type="email" 
            placeholder="Enter your email"
            required
          />
        </div>
        
        <div class="form-group">
          <label for="password">Password</label>
          <input 
            id="password"
            v-model="password" 
            type="password" 
            placeholder="Enter your password"
            required
          />
        </div>
        
        <div class="error" v-if="error">{{ error }}</div>
        
        <button type="submit" :disabled="loading">
          {{ loading ? 'Logging in...' : 'Login' }}
        </button>
      </form>
      
      <p class="switch-link">
        Don't have an account? <router-link to="/register">Register</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import authService from '../services/authService';

const router = useRouter();
const route = useRoute();

const email = ref('');
const password = ref('');
const loading = ref(false);
const error = ref('');

const handleLogin = async () => {
  error.value = '';
  loading.value = true;
  
  try {
    await authService.login(email.value, password.value);
    const redirect = route.query.redirect || '/profile';
    router.push(redirect);
  } catch (err) {
    const errorMsg = err.message || err.response?.data?.errors?.general?.[0];
    if (errorMsg && errorMsg.includes('verify')) {
      error.value = 'Your email is not verified. Please check your Mailtrap inbox for the verification email.';
    } else if (err.response?.data?.errors?.general) {
      error.value = err.response.data.errors.general[0];
    } else {
      error.value = 'Login failed. Please check your credentials.';
    }
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  padding: 20px;
}

.auth-card {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

h2 {
  text-align: center;
  color: #e91e63;
  margin-bottom: 8px;
}

.subtitle {
  text-align: center;
  color: #666;
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 6px;
  font-weight: 500;
  color: #333;
}

input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  box-sizing: border-box;
}

input:focus {
  outline: none;
  border-color: #e91e63;
}

button {
  width: 100%;
  padding: 14px;
  background: #e91e63;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s;
}

button:hover:not(:disabled) {
  background: #c2185b;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error {
  color: #e53935;
  font-size: 14px;
  margin-bottom: 16px;
  text-align: center;
  padding: 10px;
  background: #ffebee;
  border-radius: 6px;
}

.switch-link {
  text-align: center;
  margin-top: 20px;
  color: #666;
}

.switch-link a {
  color: #e91e63;
  text-decoration: none;
}
</style>
