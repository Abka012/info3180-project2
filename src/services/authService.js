import api from './api';

export const authService = {
  async register(email, password) {
    const response = await api.post('/api/auth/register', {
      email,
      password,
      confirm_password: password
    });
    return response.data;
  },

  async login(email, password) {
    const response = await api.post('/api/auth/login', {
      email,
      password
    });
    
    if (response.data.errors?.general) {
      const errorMsg = response.data.errors.general[0];
      if (errorMsg.includes('verify')) {
        throw new Error('Please verify your email first. Check your Mailtrap inbox for the verification link.');
      }
      throw new Error(errorMsg);
    }
    
    if (response.data.token) {
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  },

  async logout() {
    try {
      await api.post('/api/auth/logout');
    } catch (e) {}
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },

  async getCurrentUser() {
    const response = await api.get('/api/auth/me');
    return response.data;
  },

  async verifyEmail(token) {
    const response = await api.get(`/api/auth/verify/${token}`);
    return response.data;
  },

  getStoredUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  },

  isAuthenticated() {
    return !!localStorage.getItem('token');
  }
};

export default authService;
