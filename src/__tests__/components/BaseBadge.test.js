import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import BaseBadge from '@/components/ui/BaseBadge.vue'

describe('BaseBadge', () => {
  it('renders with default variant (primary)', () => {
    const wrapper = mount(BaseBadge, {
      slots: { default: 'Badge Text' }
    })
    expect(wrapper.text()).toContain('Badge Text')
    expect(wrapper.find('.bg-primary-100').exists()).toBe(true)
  })

  it('renders with primary variant', () => {
    const wrapper = mount(BaseBadge, {
      props: { variant: 'primary' },
      slots: { default: 'Primary' }
    })
    expect(wrapper.find('.bg-primary-100').exists()).toBe(true)
    expect(wrapper.text()).toContain('Primary')
  })

  it('renders with success variant', () => {
    const wrapper = mount(BaseBadge, {
      props: { variant: 'success' },
      slots: { default: 'Success' }
    })
    expect(wrapper.find('.bg-green-100').exists()).toBe(true)
    expect(wrapper.text()).toContain('Success')
  })

  it('renders with warning variant', () => {
    const wrapper = mount(BaseBadge, {
      props: { variant: 'warning' },
      slots: { default: 'Warning' }
    })
    expect(wrapper.find('.bg-amber-100').exists()).toBe(true)
    expect(wrapper.text()).toContain('Warning')
  })

  it('renders with danger variant', () => {
    const wrapper = mount(BaseBadge, {
      props: { variant: 'danger' },
      slots: { default: 'Danger' }
    })
    expect(wrapper.find('.bg-red-100').exists()).toBe(true)
    expect(wrapper.text()).toContain('Danger')
  })

  it('renders with gray variant', () => {
    const wrapper = mount(BaseBadge, {
      props: { variant: 'gray' },
      slots: { default: 'Gray' }
    })
    expect(wrapper.find('.bg-gray-100').exists()).toBe(true)
    expect(wrapper.text()).toContain('Gray')
  })

  it('renders with dot prop', () => {
    const wrapper = mount(BaseBadge, {
      props: { variant: 'success', dot: true },
      slots: { default: 'With Dot' }
    })
    expect(wrapper.text()).toContain('With Dot')
  })

  it('renders empty slot correctly', () => {
    const wrapper = mount(BaseBadge)
    expect(wrapper.text()).toBe('')
  })

  it('has correct base classes', () => {
    const wrapper = mount(BaseBadge, {
      slots: { default: 'Test' }
    })
    expect(wrapper.find('.inline-flex').exists()).toBe(true)
    expect(wrapper.find('.items-center').exists()).toBe(true)
    expect(wrapper.find('.justify-center').exists()).toBe(true)
    expect(wrapper.find('.px-2\\.5').exists()).toBe(true)
    expect(wrapper.find('.py-0\\.5').exists()).toBe(true)
    expect(wrapper.find('.text-xs').exists()).toBe(true)
    expect(wrapper.find('.font-medium').exists()).toBe(true)
    expect(wrapper.find('.rounded-full').exists()).toBe(true)
  })
})
