import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createMemoryHistory } from 'vue-router'
import AppFooter from '@/components/AppFooter.vue'

const router = createRouter({
  history: createMemoryHistory(),
  routes: [
    { path: '/', component: { template: '<div>Home</div>' } },
    { path: '/about', component: { template: '<div>About</div>' } },
    { path: '/login', component: { template: '<div>Login</div>' } },
    { path: '/register', component: { template: '<div>Register</div>' } }
  ]
})

describe('AppFooter', () => {
  it('renders footer element', () => {
    const wrapper = mount(AppFooter, {
      global: { plugins: [router] }
    })
    expect(wrapper.find('footer').exists()).toBe(true)
  })

  it('displays DriftDater branding', () => {
    const wrapper = mount(AppFooter, {
      global: { plugins: [router] }
    })
    expect(wrapper.text()).toContain('DriftDater')
  })

  it('displays current year in copyright', () => {
    const currentYear = new Date().getFullYear()
    const wrapper = mount(AppFooter, {
      global: { plugins: [router] }
    })
    expect(wrapper.text()).toContain(`© ${currentYear}`)
  })

  it('displays copyright text', () => {
    const wrapper = mount(AppFooter, {
      global: { plugins: [router] }
    })
    expect(wrapper.text()).toContain('All rights reserved')
  })

  it('has link to About page', () => {
    const wrapper = mount(AppFooter, {
      global: { plugins: [router] }
    })
    expect(wrapper.find('a[href="/about"]').exists()).toBe(true)
    expect(wrapper.text()).toContain('About')
  })

  it('has link to Login page', () => {
    const wrapper = mount(AppFooter, {
      global: { plugins: [router] }
    })
    expect(wrapper.find('a[href="/login"]').exists()).toBe(true)
    expect(wrapper.text()).toContain('Login')
  })

  it('has link to Register page', () => {
    const wrapper = mount(AppFooter, {
      global: { plugins: [router] }
    })
    expect(wrapper.find('a[href="/register"]').exists()).toBe(true)
    expect(wrapper.text()).toContain('Register')
  })

  it('has logo icon', () => {
    const wrapper = mount(AppFooter, {
      global: { plugins: [router] }
    })
    expect(wrapper.find('.rounded-full').exists()).toBe(true)
    expect(wrapper.find('.bg-gradient-to-br').exists()).toBe(true)
  })

  it('has correct background styling', () => {
    const wrapper = mount(AppFooter, {
      global: { plugins: [router] }
    })
    expect(wrapper.find('.bg-gray-50').exists()).toBe(true)
    expect(wrapper.find('.dark\\:bg-gray-800').exists()).toBe(true)
  })
})
