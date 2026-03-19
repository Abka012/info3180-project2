import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import BaseInput from '@/components/ui/BaseInput.vue'

describe('BaseInput', () => {
  it('renders input element', () => {
    const wrapper = mount(BaseInput)
    expect(wrapper.find('input').exists()).toBe(true)
  })

  it('renders with label when provided', () => {
    const wrapper = mount(BaseInput, {
      props: { label: 'Email' }
    })
    expect(wrapper.find('label').text()).toContain('Email')
  })

  it('renders placeholder when provided', () => {
    const wrapper = mount(BaseInput, {
      props: { placeholder: 'Enter email' }
    })
    expect(wrapper.find('input').attributes('placeholder')).toBe('Enter email')
  })

  it('shows required asterisk when required is true', () => {
    const wrapper = mount(BaseInput, {
      props: { label: 'Email', required: true }
    })
    expect(wrapper.find('.text-red-500').text()).toBe('*')
  })

  it('shows error message when error is provided', () => {
    const wrapper = mount(BaseInput, {
      props: { error: 'Invalid email' }
    })
    expect(wrapper.find('.text-red-500').text()).toBe('Invalid email')
  })

  it('shows hint when provided and no error', () => {
    const wrapper = mount(BaseInput, {
      props: { hint: 'Enter your email address' }
    })
    expect(wrapper.find('.text-gray-500').text()).toBe('Enter your email address')
  })

  it('does not show hint when error is present', () => {
    const wrapper = mount(BaseInput, {
      props: { 
        error: 'Invalid email',
        hint: 'Enter your email address'
      }
    })
    expect(wrapper.find('.text-gray-500').exists()).toBe(false)
  })

  it('is disabled when disabled prop is true', () => {
    const wrapper = mount(BaseInput, {
      props: { disabled: true }
    })
    expect(wrapper.find('input').attributes('disabled')).toBeDefined()
  })

  it('emits update:modelValue when input changes', async () => {
    const wrapper = mount(BaseInput)
    await wrapper.find('input').setValue('test@example.com')
    expect(wrapper.emitted('update:modelValue')).toBeTruthy()
    expect(wrapper.emitted('update:modelValue')[0]).toEqual(['test@example.com'])
  })

  it('emits blur event when input loses focus', async () => {
    const wrapper = mount(BaseInput)
    await wrapper.find('input').trigger('blur')
    expect(wrapper.emitted('blur')).toBeTruthy()
  })

  it('applies input-error class when error is present', () => {
    const wrapper = mount(BaseInput, {
      props: { error: 'Error' }
    })
    expect(wrapper.find('.input-error').exists()).toBe(true)
  })

  it('has correct default type', () => {
    const wrapper = mount(BaseInput)
    expect(wrapper.find('input').attributes('type')).toBe('text')
  })

  it('accepts custom id', () => {
    const wrapper = mount(BaseInput, {
      props: { id: 'custom-input' }
    })
    expect(wrapper.find('input').attributes('id')).toBe('custom-input')
  })

  it('shows password toggle when showPasswordToggle is true', () => {
    const wrapper = mount(BaseInput, {
      props: { type: 'password', showPasswordToggle: true }
    })
    expect(wrapper.findAll('button').length).toBeGreaterThan(0)
  })

  it('toggles password visibility when toggle is clicked', async () => {
    const wrapper = mount(BaseInput, {
      props: { type: 'password', showPasswordToggle: true }
    })
    expect(wrapper.find('input').attributes('type')).toBe('password')
    await wrapper.find('button').trigger('click')
    expect(wrapper.find('input').attributes('type')).toBe('text')
  })

  it('shows icon when icon prop is provided', () => {
    const wrapper = mount(BaseInput, {
      props: { icon: 'email' }
    })
    expect(wrapper.find('.pl-10').exists()).toBe(true)
  })
})
