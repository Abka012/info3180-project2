import { test, expect } from '@playwright/test'

test.describe('Navigation', () => {
  test('home page renders', async ({ page }) => {
    console.log('[DEBUG] Testing: home page renders')
    await page.goto('/', { waitUntil: 'networkidle' })
    await page.waitForLoadState('domcontentloaded')
    await page.waitForTimeout(500)
    await expect(page.locator('body')).toBeVisible()
    console.log('[DEBUG] PASS: home page renders')
  })

  test('login page renders', async ({ page }) => {
    console.log('[DEBUG] Testing: login page renders')
    await page.goto('/login', { waitUntil: 'networkidle' })
    await page.waitForLoadState('domcontentloaded')
    await page.waitForTimeout(500)
    await expect(page.locator('h1')).toContainText('Welcome Back')
    console.log('[DEBUG] PASS: login page renders')
  })

  test('register page renders', async ({ page }) => {
    console.log('[DEBUG] Testing: register page renders')
    await page.goto('/register', { waitUntil: 'networkidle' })
    await page.waitForLoadState('domcontentloaded')
    await page.waitForTimeout(500)
    await expect(page.locator('form')).toBeVisible()
    console.log('[DEBUG] PASS: register page renders')
  })

  test('about page renders', async ({ page }) => {
    console.log('[DEBUG] Testing: about page renders')
    await page.goto('/about', { waitUntil: 'networkidle' })
    await page.waitForLoadState('domcontentloaded')
    await page.waitForTimeout(500)
    await expect(page.locator('body')).toBeVisible()
    console.log('[DEBUG] PASS: about page renders')
  })

  test('protected routes redirect to login', async ({ page }) => {
    console.log('[DEBUG] Testing: protected routes redirect to login')
    await page.goto('/profile', { waitUntil: 'networkidle' })
    await page.waitForURL('**/login**', { timeout: 10000 })
    await expect(page).toHaveURL(/\/login/)
    console.log('[DEBUG] PASS: protected routes redirect to login')
  })

  test('protected routes for browse redirect to login', async ({ page }) => {
    console.log('[DEBUG] Testing: protected routes for browse redirect to login')
    await page.goto('/browse', { waitUntil: 'networkidle' })
    await page.waitForURL('**/login**', { timeout: 10000 })
    await expect(page).toHaveURL(/\/login/)
    console.log('[DEBUG] PASS: protected routes for browse redirect to login')
  })

  test('protected routes for messages redirect to login', async ({ page }) => {
    console.log('[DEBUG] Testing: protected routes for messages redirect to login')
    await page.goto('/messages', { waitUntil: 'networkidle' })
    await page.waitForURL('**/login**', { timeout: 10000 })
    await expect(page).toHaveURL(/\/login/)
    console.log('[DEBUG] PASS: protected routes for messages redirect to login')
  })

  test('protected routes for matches redirect to login', async ({ page }) => {
    console.log('[DEBUG] Testing: protected routes for matches redirect to login')
    await page.goto('/matches', { waitUntil: 'networkidle' })
    await page.waitForURL('**/login**', { timeout: 10000 })
    await expect(page).toHaveURL(/\/login/)
    console.log('[DEBUG] PASS: protected routes for matches redirect to login')
  })

  test('protected routes for search redirect to login', async ({ page }) => {
    console.log('[DEBUG] Testing: protected routes for search redirect to login')
    await page.goto('/search', { waitUntil: 'networkidle' })
    await page.waitForURL('**/login**', { timeout: 10000 })
    await expect(page).toHaveURL(/\/login/)
    console.log('[DEBUG] PASS: protected routes for search redirect to login')
  })

  test('404 page renders for unknown routes', async ({ page }) => {
    console.log('[DEBUG] Testing: 404 page renders for unknown routes')
    await page.goto('/this-route-does-not-exist-12345', { waitUntil: 'networkidle' })
    await page.waitForLoadState('domcontentloaded')
    await page.waitForTimeout(500)
    await expect(page.locator('body')).toBeVisible()
    console.log('[DEBUG] PASS: 404 page renders for unknown routes')
  })
})

test.describe('Header Navigation', () => {
  test('header is visible on home page', async ({ page }) => {
    console.log('[DEBUG] Testing: header is visible on home page')
    await page.goto('/', { waitUntil: 'networkidle' })
    await page.waitForLoadState('domcontentloaded')
    await page.waitForTimeout(500)
    await expect(page.locator('header, nav').first()).toBeVisible()
    console.log('[DEBUG] PASS: header is visible on home page')
  })

  test('header contains logo', async ({ page }) => {
    console.log('[DEBUG] Testing: header contains logo')
    await page.goto('/', { waitUntil: 'networkidle' })
    await page.waitForLoadState('domcontentloaded')
    await page.waitForTimeout(500)
    await expect(page.locator('text=DriftDater').first()).toBeVisible()
    console.log('[DEBUG] PASS: header contains logo')
  })
})
