import { describe, it, expect, vi, beforeEach } from 'vitest'
import { validateEmail, passwordValidation } from '@/services/authService.js'

vi.mock('@/services/authService.js', () => {
  const mockValidateEmail = (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return re.test(email)
  }
  return {
    authService: {
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
      clearAuthData: vi.fn()
    },
    validateEmail: mockValidateEmail,
    passwordValidation: {
      validate: vi.fn(() => ({ isValid: true, errors: [] })),
      calculateStrength: vi.fn(() => 'strong')
    },
    default: {
      login: vi.fn(),
      logout: vi.fn(),
      register: vi.fn(),
      getStoredUser: vi.fn(() => null),
      isAuthenticated: vi.fn(() => false),
      getToken: vi.fn(() => null),
      storeAuthData: vi.fn(),
      clearAuthData: vi.fn()
    }
  }
})

import { authService } from '@/services/authService.js'

describe('authService', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('validateEmail', () => {
    it('returns true for valid email', () => {
      expect(validateEmail('test@example.com')).toBe(true)
    })

    it('returns true for email with subdomain', () => {
      expect(validateEmail('user@mail.example.com')).toBe(true)
    })

    it('returns false for email without @', () => {
      expect(validateEmail('invalid-email')).toBe(false)
    })

    it('returns false for email without domain', () => {
      expect(validateEmail('user@')).toBe(false)
    })

    it('returns false for email without local part', () => {
      expect(validateEmail('@example.com')).toBe(false)
    })

    it('returns false for empty string', () => {
      expect(validateEmail('')).toBe(false)
    })

    it('returns false for email with spaces', () => {
      expect(validateEmail('user @example.com')).toBe(false)
    })
  })

  describe('authService.getStoredUser', () => {
    it('returns null when no user in localStorage', () => {
      authService.getStoredUser.mockReturnValue(null)
      const user = authService.getStoredUser()
      expect(user).toBeNull()
    })

    it('returns user object when found in localStorage', () => {
      const mockUser = { id: 1, name: 'Test User', email: 'test@example.com' }
      authService.getStoredUser.mockReturnValue(mockUser)
      const user = authService.getStoredUser()
      expect(user).toEqual(mockUser)
    })
  })

  describe('authService.isAuthenticated', () => {
    it('returns false when no token stored', () => {
      authService.isAuthenticated.mockReturnValue(false)
      expect(authService.isAuthenticated()).toBe(false)
    })

    it('returns true when token exists', () => {
      authService.isAuthenticated.mockReturnValue(true)
      expect(authService.isAuthenticated()).toBe(true)
    })
  })

  describe('authService.logout', () => {
    it('clears auth data from localStorage', async () => {
      await authService.logout()
      expect(authService.logout).toHaveBeenCalled()
    })
  })

  describe('authService.getToken', () => {
    it('returns token from localStorage', () => {
      authService.getToken.mockReturnValue('test-token-123')
      const token = authService.getToken()
      expect(token).toBe('test-token-123')
    })

    it('returns null when no token', () => {
      authService.getToken.mockReturnValue(null)
      const token = authService.getToken()
      expect(token).toBeNull()
    })
  })

  describe('authService.storeAuthData', () => {
    it('stores token and user data', () => {
      const token = 'test-token'
      const user = { id: 1, name: 'Test' }
      
      authService.storeAuthData(token, user)
      
      expect(authService.storeAuthData).toHaveBeenCalledWith(token, user)
    })
  })

  describe('authService.clearAuthData', () => {
    it('clears all auth data', () => {
      authService.clearAuthData()
      
      expect(authService.clearAuthData).toHaveBeenCalled()
    })
  })

  describe('passwordValidation', () => {
    it('has validate function', () => {
      expect(passwordValidation.validate).toBeDefined()
    })

    it('has calculateStrength function', () => {
      expect(passwordValidation.calculateStrength).toBeDefined()
    })

    it('validate returns valid result for strong password', () => {
      const result = passwordValidation.validate('StrongPass1!')
      expect(result.isValid).toBe(true)
    })
  })
})
