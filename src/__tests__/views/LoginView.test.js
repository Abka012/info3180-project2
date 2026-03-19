import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createMemoryHistory } from 'vue-router'
import LoginView from '@/views/LoginView.vue'

const mockLoginFn = vi.fn()
const mockLogoutFn = vi.fn()
const mockCheckAuthFn = vi.fn()
const mockRegisterFn = vi.fn()
const mockVerifyEmailFn = vi.fn()
const mockRefreshUserFn = vi.fn()
const mockClearErrorFn = vi.fn()

const mockAuthService = vi.hoisted(() => ({
  login: vi.fn(),
  logout: vi.fn(),
  register: vi.fn(),
  getStoredUser: vi.fn(() => null),
  getCurrentUser: vi.fn(),
  verifyEmail: vi.fn(),
  resendVerification: vi.fn(),
  forgotPassword: vi.fn(),
  resetPassword: vi.fn(),
  isAuthenticated: vi.fn(() => false),
  getToken: vi.fn(() => null),
  storeAuthData: vi.fn(),
  clearAuthData: vi.fn(),
  passwordValidation: {
    validate: vi.fn(() => ({ isValid: true, errors: [] })),
    calculateStrength: vi.fn(() => 'strong')
  }
}))

const mockValidateEmail = vi.hoisted(() => vi.fn((email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(email)
}))

vi.mock('@/services/authService', () => ({
  authService: mockAuthService,
  validateEmail: mockValidateEmail,
  default: mockAuthService
}))

vi.mock('@/composables/useAuth', () => {
  const { ref } = require('vue')
  return {
    useAuth: () => ({
      user: ref(null),
      isAuthenticated: ref(false),
      isLoading: ref(false),
      authError: ref(null),
      login: mockLoginFn,
      logout: mockLogoutFn,
      checkAuth: mockCheckAuthFn,
      register: mockRegisterFn,
      verifyEmail: mockVerifyEmailFn,
      refreshUser: mockRefreshUserFn,
      clearError: mockClearErrorFn
    }),
    default: () => ({
      user: ref(null),
      isAuthenticated: ref(false),
      isLoading: ref(false),
      authError: ref(null),
      login: mockLoginFn,
      logout: mockLogoutFn,
      checkAuth: mockCheckAuthFn,
      register: mockRegisterFn,
      verifyEmail: mockVerifyEmailFn,
      refreshUser: mockRefreshUserFn,
      clearError: mockClearErrorFn
    })
  }
})

const router = createRouter({
  history: createMemoryHistory(),
  routes: [
    { path: '/', name: 'home', component: { template: '<div>Home</div>' } },
    { path: '/register', name: 'register', component: { template: '<div>Register</div>' } },
    { path: '/login', name: 'login', component: LoginView }
  ]
})

describe('LoginView', () => {
  beforeEach(async () => {
    router.push('/login')
    await router.isReady()
    vi.clearAllMocks()
  })

  it('renders login form with all required elements', () => {
    const wrapper = mount(LoginView, {
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

    expect(wrapper.find('h1').text()).toBe('Welcome Back')
    expect(wrapper.find('#email').exists()).toBe(true)
    expect(wrapper.find('#password').exists()).toBe(true)
    expect(wrapper.find('button[type="submit"]').text()).toBe('Sign In')
    expect(wrapper.find('a[href="/register"]').exists()).toBe(true)
  })

  it('shows validation error for invalid email', async () => {
    const wrapper = mount(LoginView, {
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

    const emailInput = wrapper.find('#email')
    await emailInput.setValue('invalid-email')
    await wrapper.find('form').trigger('submit.prevent')

    expect(wrapper.find('.text-red-500').exists()).toBe(true)
  })

  it('shows validation error for empty password', async () => {
    const wrapper = mount(LoginView, {
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

    const emailInput = wrapper.find('#email')
    await emailInput.setValue('test@example.com')
    await wrapper.find('form').trigger('submit.prevent')

    expect(wrapper.find('.text-red-500').exists()).toBe(true)
  })

  it('toggles password visibility when eye icon is clicked', async () => {
    const wrapper = mount(LoginView, {
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

    const passwordInput = wrapper.find('#password')
    expect(passwordInput.attributes('type')).toBe('password')

    const toggleButton = wrapper.find('button[type="button"]')
    await toggleButton.trigger('click')

    expect(passwordInput.attributes('type')).toBe('text')
  })

  it('shows loading state during form submission', async () => {
    mockLoginFn.mockImplementation(() => new Promise(() => {}))

    const wrapper = mount(LoginView, {
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

    const emailInput = wrapper.find('#email')
    const passwordInput = wrapper.find('#password')
    await emailInput.setValue('test@example.com')
    await passwordInput.setValue('password123')
    await wrapper.find('form').trigger('submit.prevent')

    await wrapper.vm.$nextTick()
    expect(wrapper.find('button[type="submit"]').text()).toBe('Signing in...')
  })

  it('displays error message on failed login', async () => {
    mockLoginFn.mockRejectedValue(new Error('Invalid credentials'))

    const wrapper = mount(LoginView, {
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

    const emailInput = wrapper.find('#email')
    const passwordInput = wrapper.find('#password')
    await emailInput.setValue('test@example.com')
    await passwordInput.setValue('wrongpassword')
    await wrapper.find('form').trigger('submit.prevent')

    await wrapper.vm.$nextTick()
    expect(wrapper.find('.bg-red-50').exists()).toBe(true)
  })

  it('opens forgot password modal when link is clicked', async () => {
    const wrapper = mount(LoginView, {
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

    const forgotLink = wrapper.findAll('button').find(btn => btn.text().includes('Forgot password?'))
    expect(forgotLink).toBeDefined()
    await forgotLink.trigger('click')

    expect(wrapper.find('[class*="fixed inset-0"]').exists()).toBe(true)
  })

  it('navigates to register page when sign up link is clicked', async () => {
    const pushSpy = vi.spyOn(router, 'push')
    const wrapper = mount(LoginView, {
      global: {
        plugins: [router],
        stubs: {
          'router-link': {
            template: '<a :href="to" @click.prevent="navigate"><slot /></a>',
            props: ['to'],
            methods: { navigate() { router.push(this.to) } }
          }
        }
      }
    })

    const registerLink = wrapper.find('a[href="/register"]')
    await registerLink.trigger('click')

    expect(pushSpy).toHaveBeenCalledWith('/register')
  })

  it('shows success message when redirected from registration', async () => {
    const route = createRouter({
      history: createMemoryHistory(),
      routes: [
        { path: '/login', name: 'login', component: LoginView }
      ]
    })
    route.push('/login?registered=true')
    await route.isReady()

    const wrapper = mount(LoginView, {
      global: {
        plugins: [route],
        stubs: {
          'router-link': {
            template: '<a :href="to" @click.prevent><slot /></a>',
            props: ['to']
          }
        }
      }
    })
    
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 0))

    expect(wrapper.find('.bg-green-50').exists()).toBe(true)
  })

  it('has remember me checkbox', () => {
    const wrapper = mount(LoginView, {
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

    expect(wrapper.find('input[type="checkbox"]').exists()).toBe(true)
    expect(wrapper.text()).toContain('Remember me')
  })

  it('displays app branding', () => {
    const wrapper = mount(LoginView, {
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

    expect(wrapper.text()).toContain('DriftDater')
  })
})
