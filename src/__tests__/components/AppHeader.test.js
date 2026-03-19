import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createMemoryHistory } from 'vue-router'
import { ref } from 'vue'
import AppHeader from '@/components/AppHeader.vue'

vi.mock('../composables/useAuth', () => ({
  useAuth: () => ({
    isAuthenticated: ref(false),
    user: ref(null),
    logout: vi.fn()
  }),
  default: () => ({
    isAuthenticated: ref(false),
    user: ref(null),
    logout: vi.fn()
  })
}))

vi.mock('../services/authService', () => ({
  authService: {
    logout: vi.fn()
  },
  default: {
    logout: vi.fn()
  }
}))

const router = createRouter({
  history: createMemoryHistory(),
  routes: [
    { path: '/', name: 'home', component: { template: '<div>Home</div>' } },
    { path: '/login', name: 'login', component: { template: '<div>Login</div>' } },
    { path: '/register', name: 'register', component: { template: '<div>Register</div>' } },
    { path: '/profile', name: 'profile', component: { template: '<div>Profile</div>' } },
    { path: '/messages', name: 'messages', component: { template: '<div>Messages</div>' } },
    { path: '/matches', name: 'matches', component: { template: '<div>Matches</div>' } },
    { path: '/notifications', name: 'notifications', component: { template: '<div>Notifications</div>' } }
  ]
})

describe('AppHeader', () => {
  beforeEach(async () => {
    router.push('/')
    await router.isReady()
    vi.clearAllMocks()
  })

  it('displays logo and app name', () => {
    const wrapper = mount(AppHeader, {
      global: {
        plugins: [router]
      }
    })

    expect(wrapper.text()).toContain('DriftDater')
  })

  it('shows login and register links for guests', () => {
    const wrapper = mount(AppHeader, {
      global: {
        plugins: [router],
        stubs: {
          'router-link': {
            template: '<a :href="to" @click.prevent><slot /></a>',
            props: ['to']
          }
        }
      }
    })

    expect(wrapper.text()).toContain('Login')
    expect(wrapper.text()).toContain('Sign Up')
  })

  it('shows navigation links for guests', () => {
    const wrapper = mount(AppHeader, {
      global: {
        plugins: [router],
        stubs: {
          'router-link': {
            template: '<a :href="to" @click.prevent><slot /></a>',
            props: ['to']
          }
        }
      }
    })

    expect(wrapper.find('a[href="/login"]').exists()).toBe(true)
    expect(wrapper.find('a[href="/register"]').exists()).toBe(true)
  })
})
