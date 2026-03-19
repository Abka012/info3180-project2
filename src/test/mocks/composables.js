import { ref, computed } from 'vue'
import { vi } from 'vitest'

export const createMockUseAuth = (overrides = {}) => {
  const user = ref(overrides.user ?? null)
  const currentUser = ref(overrides.user ?? null)
  const isLoading = ref(overrides.isLoading ?? false)
  const authError = ref(overrides.authError ?? null)
  const isAuthenticated = computed(() => !!user.value)

  return {
    user,
    currentUser,
    isLoading,
    authError,
    isAuthenticated,
    login: vi.fn().mockResolvedValue({ 
      user: overrides.user ?? null, 
      token: 'mock-token' 
    }),
    logout: vi.fn().mockResolvedValue(undefined),
    register: vi.fn().mockResolvedValue({ user_id: 1 }),
    verifyEmail: vi.fn().mockResolvedValue({ message: 'Verified' }),
    refreshUser: vi.fn().mockResolvedValue(user.value),
    clearError: vi.fn(() => { authError.value = null }),
    checkAuth: vi.fn()
  }
}

export const mockUseAuth = createMockUseAuth()

export const createMockUseNotifications = (overrides = {}) => {
  const notifications = ref(overrides.notifications ?? [])
  const unreadCount = ref(overrides.unreadCount ?? 0)
  const loading = ref(overrides.loading ?? false)

  return {
    notifications,
    unreadCount,
    loading,
    fetchNotifications: vi.fn(),
    markAsRead: vi.fn(),
    markAllAsRead: vi.fn()
  }
}

export const createMockUseMatches = (overrides = {}) => {
  const matches = ref(overrides.matches ?? [])
  const potentialMatches = ref(overrides.potentialMatches ?? [])
  const loading = ref(overrides.loading ?? false)

  return {
    matches,
    potentialMatches,
    loading,
    fetchMatches: vi.fn(),
    fetchPotentialMatches: vi.fn(),
    likeUser: vi.fn(),
    passUser: vi.fn()
  }
}

export const createMockUseMessages = (overrides = {}) => {
  const conversations = ref(overrides.conversations ?? [])
  const currentConversation = ref(overrides.currentConversation ?? null)
  const messages = ref(overrides.messages ?? [])
  const loading = ref(overrides.loading ?? false)

  return {
    conversations,
    currentConversation,
    messages,
    loading,
    fetchConversations: vi.fn(),
    fetchMessages: vi.fn(),
    sendMessage: vi.fn()
  }
}
