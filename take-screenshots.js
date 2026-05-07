import { chromium } from "playwright";
import { mkdirSync, existsSync } from "fs";
import { dirname, join, resolve } from "path";
import { fileURLToPath } from "url";

// ===== 1. PATH SETUP (MUST COME FIRST) =====
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Find project root by looking for package.json (most reliable method)
let projectRoot = __dirname;
while (projectRoot !== dirname(projectRoot)) {
  if (existsSync(resolve(projectRoot, "package.json"))) {
    break;
  }
  projectRoot = dirname(projectRoot);
}

// Allow env var override, fallback to detected root
projectRoot = process.env.PROJECT_ROOT || projectRoot;

// Define imagesDir AFTER projectRoot is set
const imagesDir = join(__dirname, "docs", "images");
mkdirSync(imagesDir, { recursive: true });

// Debug logging
console.log(`🔍 __dirname: ${__dirname}`);
console.log(`🔍 projectRoot: ${projectRoot}`);
console.log(`🔍 imagesDir: ${imagesDir}`);
console.log(`🔍 CWD: ${process.cwd()}\n`);

// ===== 2. CLI ARGS =====
const args = process.argv.slice(2);
const force = args.includes("--force");
const routeArgs = args.filter((arg) => !arg.startsWith("--"));

// ===== 3. ROUTES TO CAPTURE =====
const defaultRoutes = [
  { path: "/", slug: "home", waitFor: "h1" },
  { path: "/register", slug: "register", waitFor: "form" },
  { path: "/login", slug: "login", waitFor: "form" },
  { path: "/about", slug: "about", waitFor: ".features" },
  { path: "/browse", slug: "browse", waitFor: ".browse-container", auth: true },
  { path: "/search", slug: "search", waitFor: ".search-form", auth: true },
  { path: "/matches", slug: "matches", waitFor: "h1", auth: true },
  {
    path: "/messages",
    slug: "conversations",
    waitFor: "body",
    auth: true,
  },
  { path: "/favorites", slug: "favorites", waitFor: "h1", auth: true },
  { path: "/profile/edit", slug: "profile-edit", waitFor: "form", auth: true },
  { path: "/notifications", slug: "notifications", waitFor: "h1", auth: true },
  { path: "/messages/2", slug: "chat", waitFor: ".chat-container", auth: true },
  { path: "/nonexistent", slug: "404", waitFor: "body" },
];

const routesToCapture =
  routeArgs.length > 0
    ? defaultRoutes.filter((r) =>
        routeArgs.some((arg) => r.path.startsWith(arg)),
      )
    : defaultRoutes;

// ===== 4. SCREENSHOT FUNCTION =====
const takeScreenshot = async (page, url, slug, waitFor, theme) => {
  const filename = `${theme}-${slug}.png`;
  const filepath = resolve(imagesDir, filename);

  console.log(`💾 Target: ${filepath}`);

  if (existsSync(filepath) && !force) {
    console.log(`⏭️  Skipping: docs/images/${filename}`);
    return true;
  }

  const fullUrl = `http://127.0.0.1:5173${url}`;
  console.log(`📸 Capturing ${theme} mode: ${slug}...`);

  for (let attempt = 1; attempt <= 3; attempt++) {
    try {
      // Set theme BEFORE any page JS runs
      await page.addInitScript((t) => {
        try {
          localStorage.setItem("theme", t);
          document.documentElement.setAttribute("data-theme", t);
        } catch (e) {
          /* ignore */
        }
      }, theme);

      // Navigate + reload to guarantee theme applies
      await page.goto(fullUrl, { waitUntil: "commit", timeout: 20000 });
      await page.reload({ waitUntil: "networkidle", timeout: 20000 });

      await page.waitForSelector(waitFor, { timeout: 10000 });

      // Wait for CSS variable to reflect theme
      await page.waitForFunction(
        (t) => {
          const bg = getComputedStyle(document.documentElement)
            .getPropertyValue("--bg")
            .trim();
          const isDark =
            bg.startsWith("#0") || bg.startsWith("#1") || bg === "#0f172a";
          return t === "dark" ? isDark : !isDark;
        },
        theme,
        { timeout: 8000 },
      );

      await page.waitForTimeout(1000);
      await page.screenshot({ path: filepath, fullPage: true });

      const relativePath = filepath.replace(projectRoot, ".");
      console.log(`✅ Saved: ${relativePath}`);
      return true;
    } catch (error) {
      if (attempt < 3) {
        console.warn(
          `⚠️  Attempt ${attempt} failed for ${slug} (${theme}). Retrying...`,
        );
        await page.waitForTimeout(2000);
      } else {
        // Debug theme state on failure
        try {
          const debug = await page.evaluate(() => ({
            attr: document.documentElement.getAttribute("data-theme"),
            storage: localStorage.getItem("theme"),
            bg: getComputedStyle(document.documentElement)
              .getPropertyValue("--bg")
              ?.trim(),
            url: window.location.href,
          }));
          console.error(`❌ Theme debug ${slug} (${theme}):`, debug);
        } catch (e) {
          // Ignore errors for optional debug logging
        }

        console.error(`❌ Failed: ${slug} (${theme}) - ${error.message}`);
        return false;
      }
    }
  }
};

// ===== 5. MAIN EXECUTION =====
(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  await page.setViewportSize({ width: 1280, height: 800 });

  console.log("🎯 Starting dual-theme capture...\n");
  const results = { success: [], failed: [] };

  // Capture unauthenticated routes
  for (const route of routesToCapture.filter((r) => !r.auth)) {
    for (const theme of ["light", "dark"]) {
      const success = await takeScreenshot(
        page,
        route.path,
        route.slug,
        route.waitFor,
        theme,
      );
      const key = `${theme}-${route.slug}`;
      (success ? results.success : results.failed).push(key);
    }
  }

  // Login for authenticated routes
  if (routesToCapture.some((r) => r.auth)) {
    console.log("\n🔐 Logging in for authenticated screenshots...");
    try {
      await page.goto("http://127.0.0.1:5173/login", {
        waitUntil: "networkidle",
      });
      await page.fill("#email", "user1@test.com");
      await page.fill("#password", "password123");

      const [request] = await Promise.all([
        page.waitForRequest(
          (req) =>
            req.url().includes("/api/auth/login") && req.method() === "POST",
        ),
        page.click('button[type="submit"]'),
      ]);

      const response = await request.response();
      if (!response?.ok())
        throw new Error(`Login failed: ${response?.status()}`);

      await page.waitForURL("http://127.0.0.1:5173/**", { timeout: 15000 });
      await page.waitForTimeout(2000);
      console.log("✅ Login successful!\n");

      for (const route of routesToCapture.filter((r) => r.auth)) {
        for (const theme of ["light", "dark"]) {
          const success = await takeScreenshot(
            page,
            route.path,
            route.slug,
            route.waitFor,
            theme,
          );
          const key = `${theme}-${route.slug}`;
          (success ? results.success : results.failed).push(key);
        }
      }
    } catch (error) {
      console.error("❌ Login failed:", error.message);
      results.failed.push("login");
    }
  }

  await browser.close();

  // Summary
  console.log("\n" + "=".repeat(60));
  console.log("📊 SCREENSHOT SUMMARY");
  console.log("=".repeat(60));
  console.log(`✅ Success: ${results.success.length}`);
  console.log(`❌ Failed: ${results.failed.length}`);
  if (results.failed.length > 0) {
    console.log("\nFailed:", results.failed.join(", "));
    process.exit(1);
  } else {
    console.log("\n✅ All screenshots captured!");
    process.exit(0);
  }
})();
