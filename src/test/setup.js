import { beforeAll, afterEach, vi } from 'vitest'
import { setupCentralMocks, resetAllMocks } from './mocks/index.js'

beforeAll(() => {
  setupCentralMocks(vi)
})

const localStorageMock = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
  key: vi.fn(),
  length: 0
}

const sessionStorageMock = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
  key: vi.fn(),
  length: 0
}

Object.defineProperty(global, 'localStorage', { value: localStorageMock })
Object.defineProperty(global, 'sessionStorage', { value: sessionStorageMock })

global.fetch = vi.fn()

afterEach(() => {
  resetAllMocks()
  vi.clearAllMocks()
})
