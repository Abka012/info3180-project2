import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createMemoryHistory } from 'vue-router'
import { ref } from 'vue'
import HomeView from '@/views/HomeView.vue'

vi.mock('../services/authService', () => ({
  authService: {
    getStoredUser: vi.fn(() => null),
    logout: vi.fn(),
    isAuthenticated: vi.fn(() => false)
  },
  default: {
    getStoredUser: vi.fn(() => null),
    logout: vi.fn(),
    isAuthenticated: vi.fn(() => false)
  }
}))

vi.mock('../services/profileService', () => ({
  profileService: {
    getProfile: vi.fn(() => Promise.reject(new Error('No profile')))
  },
  default: {
    getProfile: vi.fn(() => Promise.reject(new Error('No profile')))
  }
}))

vi.mock('../services/matchService', () => ({
  matchService: {
    getMatches: vi.fn(() => Promise.resolve([]))
  },
  default: {
    getMatches: vi.fn(() => Promise.resolve([]))
  }
}))

vi.mock('../composables/useAuth', () => ({
  useAuth: () => ({
    isAuthenticated: ref(false),
    user: ref(null),
    login: vi.fn(),
    logout: vi.fn(),
    checkAuth: vi.fn()
  }),
  default: () => ({
    isAuthenticated: ref(false),
    user: ref(null),
    login: vi.fn(),
    logout: vi.fn(),
    checkAuth: vi.fn()
  })
}))

const router = createRouter({
  history: createMemoryHistory(),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/register', name: 'register', component: { template: '<div>Register</div>' } },
    { path: '/browse', name: 'browse', component: { template: '<div>Browse</div>' } },
    { path: '/profile/edit', name: 'editProfile', component: { template: '<div>Edit Profile</div>' } }
  ]
})

describe('HomeView', () => {
  beforeEach(async () => {
    router.push('/')
    await router.isReady()
    vi.clearAllMocks()
  })

  describe('Guest View (Not Authenticated)', () => {
    it('shows hero section with CTA buttons', () => {
      const wrapper = mount(HomeView, {
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

      expect(wrapper.text()).toContain('Connect with')
      expect(wrapper.find('a[href="/register"]').exists()).toBe(true)
      expect(wrapper.text()).toContain('Get Started Free')
    })

    it('shows features section', () => {
      const wrapper = mount(HomeView, {
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

      expect(wrapper.text()).toContain('Why Choose DriftDater?')
      expect(wrapper.text()).toContain('Smart Matching')
      expect(wrapper.text()).toContain('Privacy First')
      expect(wrapper.text()).toContain('Real Connections')
    })

    it('shows statistics section', () => {
      const wrapper = mount(HomeView, {
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

      expect(wrapper.text()).toContain('10K+')
      expect(wrapper.text()).toContain('Active Users')
    })

    it('shows call to action section', () => {
      const wrapper = mount(HomeView, {
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

      expect(wrapper.text()).toContain('Ready to Find Your Match?')
    })
  })
})
