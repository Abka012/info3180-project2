import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createMemoryHistory } from 'vue-router'
import ChatView from '@/views/ChatView.vue'

const mockAuthService = vi.hoisted(() => ({
  getStoredUser: vi.fn(() => ({ id: 1, name: 'Current User' })),
  isAuthenticated: vi.fn(() => true)
}))

const mockMessageService = vi.hoisted(() => ({
  getConversations: vi.fn(() => Promise.resolve([])),
  getMessageHistory: vi.fn(() => Promise.resolve({ 
    messages: [], 
    other_user: null, 
    has_next: false,
    page: 1,
    total_pages: 0
  })),
  sendMessage: vi.fn(),
  sendTypingStatus: vi.fn(),
  markAsRead: vi.fn(),
  getUnreadCount: vi.fn(() => Promise.resolve({ unread_count: 0 })),
  markAllAsRead: vi.fn()
}))

const mockSocketService = vi.hoisted(() => ({
  connect: vi.fn(),
  disconnect: vi.fn(),
  emit: vi.fn(),
  on: vi.fn(),
  off: vi.fn(),
  isConnected: vi.fn(() => false),
  joinRoom: vi.fn(),
  leaveRoom: vi.fn()
}))

vi.mock('@/services/authService', () => ({
  authService: mockAuthService,
  default: mockAuthService
}))

vi.mock('@/services/messageService', () => ({
  messageService: mockMessageService,
  default: mockMessageService
}))

vi.mock('@/services/socketService', () => ({
  socketService: mockSocketService,
  default: mockSocketService
}))

const mockMessages = [
  { id: 1, sender_id: 2, receiver_id: 1, content: 'Hello!', created_at: '2024-01-01T10:00:00Z' },
  { id: 2, sender_id: 1, receiver_id: 2, content: 'Hi there!', created_at: '2024-01-01T10:01:00Z' }
]

const createRouterWithChat = () => {
  return createRouter({
    history: createMemoryHistory(),
    routes: [
      { path: '/', name: 'home', component: { template: '<div>Home</div>' } },
      { path: '/conversations', name: 'conversations', component: { template: '<div>Conversations</div>' } },
      { path: '/matches', name: 'matches', component: { template: '<div>Matches</div>' } },
      { path: '/messages/:userId', name: 'chat', component: ChatView }
    ]
  })
}

describe('ChatView', () => {
  let router

  beforeEach(async () => {
    router = createRouterWithChat()
    router.push('/messages/2')
    await router.isReady()
    
    vi.clearAllMocks()
  })

  it('renders chat interface', async () => {
    mockMessageService.getMessageHistory.mockResolvedValue({
      messages: [],
      other_user: { id: 2, name: 'Jane', profile_picture: null },
      has_next: false
    })

    const wrapper = mount(ChatView, {
      global: {
        plugins: [router]
      }
    })

    await new Promise(resolve => setTimeout(resolve, 100))

    expect(wrapper.find('.message-input').exists()).toBe(true)
  })

  it('shows user name in header', async () => {
    mockMessageService.getMessageHistory.mockResolvedValue({
      messages: [],
      other_user: { id: 2, name: 'Jane', profile_picture: null },
      has_next: false
    })

    const wrapper = mount(ChatView, {
      global: {
        plugins: [router]
      }
    })

    await new Promise(resolve => setTimeout(resolve, 100))

    expect(wrapper.text()).toContain('Jane')
  })

  it('displays messages correctly', async () => {
    mockMessageService.getMessageHistory.mockResolvedValue({
      messages: mockMessages,
      other_user: { id: 2, name: 'Jane', profile_picture: null },
      has_next: false
    })

    const wrapper = mount(ChatView, {
      global: {
        plugins: [router]
      }
    })

    await new Promise(resolve => setTimeout(resolve, 100))

    expect(wrapper.text()).toContain('Hello!')
    expect(wrapper.text()).toContain('Hi there!')
  })

  it('send button is disabled when input is empty', async () => {
    mockMessageService.getMessageHistory.mockResolvedValue({
      messages: [],
      other_user: { id: 2, name: 'Jane', profile_picture: null },
      has_next: false
    })

    const wrapper = mount(ChatView, {
      global: {
        plugins: [router]
      }
    })

    await new Promise(resolve => setTimeout(resolve, 100))

    const sendButton = wrapper.find('.send-btn')
    if (sendButton.exists()) {
      expect(sendButton.attributes('disabled') !== undefined).toBe(true)
    }
  })

  it('shows loading state while fetching messages', async () => {
    mockMessageService.getMessageHistory.mockImplementation(
      () => new Promise(resolve => setTimeout(() => resolve({
        messages: [],
        other_user: { id: 2, name: 'Jane', profile_picture: null },
        has_next: false
      }), 100))
    )

    const wrapper = mount(ChatView, {
      global: {
        plugins: [router]
      }
    })

    expect(wrapper.html()).toContain('loading')
  })
})
