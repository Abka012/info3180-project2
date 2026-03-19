import { test, expect } from '@playwright/test'

test.describe('Messaging (Requires Auth)', () => {
  test('messages page redirects unauthenticated users', async ({ page }) => {
    console.log('[DEBUG] Testing: messages page redirects unauthenticated users')
    await page.goto('/messages', { waitUntil: 'networkidle' })
    await page.waitForURL('**/login**', { timeout: 10000 })
    await expect(page).toHaveURL(/\/login/)
    console.log('[DEBUG] PASS: messages page redirects unauthenticated users')
  })

  test('specific chat page redirects unauthenticated users', async ({ page }) => {
    console.log('[DEBUG] Testing: specific chat page redirects unauthenticated users')
    await page.goto('/messages/1', { waitUntil: 'networkidle' })
    await page.waitForURL('**/login**', { timeout: 10000 })
    await expect(page).toHaveURL(/\/login/)
    console.log('[DEBUG] PASS: specific chat page redirects unauthenticated users')
  })
})
