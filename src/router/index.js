import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import { authService } from '../services/authService'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue'),
      meta: { guest: true }
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: { guest: true }
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/ProfileView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/profile/edit',
      name: 'editProfile',
      component: () => import('../views/EditProfileView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/verify/:token',
      name: 'verify',
      component: () => import('../views/VerifyView.vue')
    }
  ]
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = authService.isAuthenticated();
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } });
  } else if (to.meta.guest && isAuthenticated) {
    next({ name: 'home' });
  } else {
    next();
  }
});

export default router
