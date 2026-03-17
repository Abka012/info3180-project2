<template>
  <div class="auth-container">
    <div class="auth-card">
      <h2>Join DriftDater</h2>
      <p class="subtitle">Find your perfect match</p>
      
      <div v-if="showSuccess" class="success-message">
        <div class="success-icon">✓</div>
        <h3>Registration Successful!</h3>
        <p>{{ successMessage }}</p>
        <router-link to="/login" class="btn-primary">Go to Login</router-link>
      </div>
      
      <form v-else @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="email">Email</label>
          <input 
            id="email"
            v-model="email" 
            type="email" 
            placeholder="Enter your email"
            required
          />
          <span class="error" v-if="errors.email">{{ errors.email[0] }}</span>
        </div>
        
        <div class="form-group">
          <label for="password">Password</label>
          <input 
            id="password"
            v-model="password" 
            type="password" 
            placeholder="Create a password"
            required
          />
          <span class="error" v-if="errors.password">{{ errors.password[0] }}</span>
        </div>
        
        <div class="form-group">
          <label for="confirmPassword">Confirm Password</label>
          <input 
            id="confirmPassword"
            v-model="confirmPassword" 
            type="password" 
            placeholder="Confirm your password"
            required
          />
          <span class="error" v-if="passwordMismatch">{{ passwordMismatch }}</span>
        </div>
        
        <div class="error" v-if="errors.general">{{ errors.general[0] }}</div>
        
        <button type="submit" :disabled="loading">
          {{ loading ? 'Creating Account...' : 'Register' }}
        </button>
      </form>
      
      <p class="switch-link">
        Already have an account? <router-link to="/login">Login</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import authService from '../services/authService';

const router = useRouter();

const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const loading = ref(false);
const errors = ref({});
const showSuccess = ref(false);
const successMessage = ref('');

const passwordMismatch = computed(() => {
  if (confirmPassword.value && password.value !== confirmPassword.value) {
    return 'Passwords do not match';
  }
  return '';
});

const handleRegister = async () => {
  errors.value = {};
  
  if (password.value !== confirmPassword.value) {
    return;
  }
  
  loading.value = true;
  
  try {
    await authService.register(email.value, password.value);
    successMessage.value = `Registration successful! 
    
Please check your Mailtrap inbox (or spam folder) for the verification email sent to: ${email.value}

Click the verification link in the email to activate your account.`;
    showSuccess.value = true;
  } catch (error) {
    if (error.response?.data?.errors) {
      errors.value = error.response.data.errors;
    } else {
      errors.value = { general: ['Registration failed. Please try again.'] };
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
  font-size: 12px;
  margin-top: 4px;
  display: block;
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

.success-message {
  text-align: center;
  padding: 20px;
}

.success-icon {
  width: 60px;
  height: 60px;
  background: #e8f5e9;
  color: #4caf50;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 30px;
  margin: 0 auto 20px;
}

.success-message h3 {
  color: #4caf50;
  margin-bottom: 15px;
}

.success-message p {
  color: #666;
  white-space: pre-line;
  margin-bottom: 20px;
}

.btn-primary {
  display: inline-block;
  padding: 12px 30px;
  background: #e91e63;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  font-weight: 600;
}
</style>
