import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import BaseAvatar from '@/components/ui/BaseAvatar.vue'

describe('BaseAvatar', () => {
  it('renders initials when no src provided', () => {
    const wrapper = mount(BaseAvatar, {
      props: { name: 'John Doe' }
    })
    expect(wrapper.text()).toContain('JD')
  })

  it('renders question mark when no name provided', () => {
    const wrapper = mount(BaseAvatar)
    expect(wrapper.text()).toContain('?')
  })

  it('renders image when src is provided', () => {
    const wrapper = mount(BaseAvatar, {
      props: { src: 'https://example.com/avatar.jpg', name: 'Jane' }
    })
    expect(wrapper.find('img').exists()).toBe(true)
    expect(wrapper.find('img').attributes('src')).toBe('https://example.com/avatar.jpg')
  })

  it('shows initials when src is empty', () => {
    const wrapper = mount(BaseAvatar, {
      props: { src: '', name: 'Jane Doe' }
    })
    expect(wrapper.text()).toContain('JD')
  })

  it('applies correct size class for xs', () => {
    const wrapper = mount(BaseAvatar, {
      props: { name: 'Test', size: 'xs' }
    })
    expect(wrapper.find('.w-6').exists()).toBe(true)
  })

  it('applies correct size class for sm', () => {
    const wrapper = mount(BaseAvatar, {
      props: { name: 'Test', size: 'sm' }
    })
    expect(wrapper.find('.w-8').exists()).toBe(true)
  })

  it('applies correct size class for md', () => {
    const wrapper = mount(BaseAvatar, {
      props: { name: 'Test', size: 'md' }
    })
    expect(wrapper.find('.w-10').exists()).toBe(true)
  })

  it('applies correct size class for lg', () => {
    const wrapper = mount(BaseAvatar, {
      props: { name: 'Test', size: 'lg' }
    })
    expect(wrapper.find('.w-12').exists()).toBe(true)
  })

  it('applies correct size class for xl', () => {
    const wrapper = mount(BaseAvatar, {
      props: { name: 'Test', size: 'xl' }
    })
    expect(wrapper.find('.w-16').exists()).toBe(true)
  })

  it('shows online indicator when showOnline and online are true', () => {
    const wrapper = mount(BaseAvatar, {
      props: { name: 'Test', showOnline: true, online: true }
    })
    expect(wrapper.find('.bg-green-500').exists()).toBe(true)
  })

  it('hides online indicator when showOnline is false', () => {
    const wrapper = mount(BaseAvatar, {
      props: { name: 'Test', showOnline: false, online: true }
    })
    expect(wrapper.find('.bg-green-500').exists()).toBe(false)
  })

  it('handles single name correctly', () => {
    const wrapper = mount(BaseAvatar, {
      props: { name: 'John' }
    })
    expect(wrapper.text()).toContain('J')
  })

  it('handles name with multiple spaces', () => {
    const wrapper = mount(BaseAvatar, {
      props: { name: 'John    Doe' }
    })
    expect(wrapper.text()).toContain('JD')
  })
})
