import { test, expect } from '@playwright/test'

test.describe('Matching (Requires Auth)', () => {
  test('browse page redirects unauthenticated users', async ({ page }) => {
    console.log('[DEBUG] Testing: browse page redirects unauthenticated users')
    await page.goto('/browse', { waitUntil: 'networkidle' })
    await page.waitForURL('**/login**', { timeout: 10000 })
    await expect(page).toHaveURL(/\/login/)
    console.log('[DEBUG] PASS: browse page redirects unauthenticated users')
  })

  test('matches page redirects unauthenticated users', async ({ page }) => {
    console.log('[DEBUG] Testing: matches page redirects unauthenticated users')
    await page.goto('/matches', { waitUntil: 'networkidle' })
    await page.waitForURL('**/login**', { timeout: 10000 })
    await expect(page).toHaveURL(/\/login/)
    console.log('[DEBUG] PASS: matches page redirects unauthenticated users')
  })

  test('favorites page redirects unauthenticated users', async ({ page }) => {
    console.log('[DEBUG] Testing: favorites page redirects unauthenticated users')
    await page.goto('/favorites', { waitUntil: 'networkidle' })
    await page.waitForURL('**/login**', { timeout: 10000 })
    await expect(page).toHaveURL(/\/login/)
    console.log('[DEBUG] PASS: favorites page redirects unauthenticated users')
  })
})
