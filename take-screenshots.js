import { chromium } from "playwright";
import { mkdirSync, existsSync } from "fs";
import { dirname, join, resolve } from "path";
import { fileURLToPath } from "url";

// ======================================================
// 1. PATH SETUP
// ======================================================

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Detect project root
let projectRoot = __dirname;

while (projectRoot !== dirname(projectRoot)) {
  if (existsSync(resolve(projectRoot, "package.json"))) {
    break;
  }

  projectRoot = dirname(projectRoot);
}

projectRoot = process.env.PROJECT_ROOT || projectRoot;

const imagesDir = join(projectRoot, "docs", "images");

mkdirSync(imagesDir, { recursive: true });

console.log(`🔍 __dirname: ${__dirname}`);
console.log(`🔍 projectRoot: ${projectRoot}`);
console.log(`🔍 imagesDir: ${imagesDir}`);
console.log(`🔍 CWD: ${process.cwd()}\n`);

// ======================================================
// 2. CLI ARGS
// ======================================================

const args = process.argv.slice(2);

const force = args.includes("--force");

const routeArgs = args.filter((arg) => !arg.startsWith("--"));

// ======================================================
// 3. ROUTES
// ======================================================

const defaultRoutes = [
  { path: "/", slug: "home", waitFor: "h1" },
  { path: "/register", slug: "register", waitFor: "form" },
  { path: "/login", slug: "login", waitFor: "form" },
  { path: "/about", slug: "about", waitFor: ".features" },

  // Authenticated
  {
    path: "/browse",
    slug: "browse",
    waitFor: ".browse-container",
    auth: true,
  },
  {
    path: "/search",
    slug: "search",
    waitFor: ".search-form",
    auth: true,
  },
  {
    path: "/matches",
    slug: "matches",
    waitFor: "h1",
    auth: true,
  },
  {
    path: "/messages",
    slug: "conversations",
    waitFor: "body",
    auth: true,
  },
  {
    path: "/favorites",
    slug: "favorites",
    waitFor: "h1",
    auth: true,
  },
  {
    path: "/profile/edit",
    slug: "profile-edit",
    waitFor: "form",
    auth: true,
  },
  {
    path: "/notifications",
    slug: "notifications",
    waitFor: "h1",
    auth: true,
  },
  {
    path: "/messages/2",
    slug: "chat",
    waitFor: ".chat-container",
    auth: true,
  },

  // 404
  {
    path: "/nonexistent",
    slug: "404",
    waitFor: "body",
  },
];

const routesToCapture =
  routeArgs.length > 0
    ? defaultRoutes.filter((r) =>
        routeArgs.some((arg) => r.path.startsWith(arg)),
      )
    : defaultRoutes;

// ======================================================
// 4. HELPERS
// ======================================================

async function applyTheme(page, theme) {
  await page.addInitScript((t) => {
    try {
      localStorage.setItem("theme", t);
      document.documentElement.setAttribute("data-theme", t);
    } catch (err) {
      console.error(err);
    }
  }, theme);
}

async function takeScreenshot(page, route, theme) {
  const filename = `${theme}-${route.slug}.png`;

  const filepath = resolve(imagesDir, filename);

  console.log(`💾 Target: ${filepath}`);

  if (existsSync(filepath) && !force) {
    console.log(`⏭️  Skipping existing screenshot`);
    return true;
  }

  try {
    await applyTheme(page, theme);

    const fullUrl = `http://localhost:5173${route.path}`;

    console.log(`📸 Capturing ${theme} mode: ${route.slug}...`);

    await page.goto(fullUrl, {
      waitUntil: "networkidle",
      timeout: 30000,
    });

    console.log(`🌐 Current URL: ${page.url()}`);

    await page.waitForSelector(route.waitFor, {
      timeout: 15000,
    });

    await page.waitForTimeout(1000);

    await page.screenshot({
      path: filepath,
      fullPage: true,
    });

    const relativePath = filepath.replace(projectRoot, ".");

    console.log(`✅ Saved: ${relativePath}`);

    return true;
  } catch (error) {
    console.error(
      `❌ Failed screenshot (${theme}-${route.slug}):`,
      error.message,
    );

    return false;
  }
}

// ======================================================
// 5. LOGIN FUNCTION
// ======================================================

async function login(page) {
  console.log("\n🔐 Starting login flow...");

  // Browser console debugging
  page.on("console", (msg) => {
    console.log("BROWSER LOG:", msg.text());
  });

  page.on("pageerror", (err) => {
    console.log("PAGE ERROR:", err.message);
  });

  await page.goto("http://localhost:5173/login", {
    waitUntil: "networkidle",
    timeout: 30000,
  });

  console.log("✅ Login page loaded");

  // Debug inputs
  const emailInputs = await page.locator('input[type="email"]').count();

  const passwordInputs = await page
    .locator('input[type="password"]')
    .count();

  console.log(`Email inputs found: ${emailInputs}`);
  console.log(`Password inputs found: ${passwordInputs}`);

  // Fill form
  await page.fill('input[type="email"]', "user1@test.com");

  await page.fill('input[type="password"]', "password123");

  console.log("✅ Filled login form");

  // Debug actual values
  const emailValue = await page
    .locator('input[type="email"]')
    .inputValue();

  const passwordValue = await page
    .locator('input[type="password"]')
    .inputValue();

  console.log(`Email value: ${emailValue}`);
  console.log(`Password length: ${passwordValue.length}`);

  // Verify submit button
  const submitButton = page.locator('button[type="submit"]').first();

  const isDisabled = await submitButton.isDisabled();

  console.log(`Submit button disabled: ${isDisabled}`);

  if (isDisabled) {
    throw new Error("Submit button is disabled");
  }

  // Listen for requests
  page.on("request", (req) => {
    console.log(`➡️ REQUEST: ${req.method()} ${req.url()}`);
  });

  page.on("response", async (res) => {
    console.log(`⬅️ RESPONSE: ${res.status()} ${res.url()}`);
  });

  // Use form submission instead of button click
  const form = page.locator("form").first();

  console.log("Submitting login form...");

  const [response] = await Promise.all([
    page.waitForResponse(
      (res) =>
        res.url().includes("/api/auth/login") &&
        res.request().method() === "POST",
      {
        timeout: 30000,
      },
    ),

    form.evaluate((formElement) => {
      formElement.requestSubmit();
    }),
  ]);

  console.log(`Login response status: ${response.status()}`);

  if (!response.ok()) {
    const body = await response.text();

    console.error("Login response body:", body);

    throw new Error(`Login failed with status ${response.status()}`);
  }

  // Wait for redirect/navigation
  await page.waitForTimeout(3000);

  console.log(`✅ Login successful`);
  console.log(`🌐 Current URL after login: ${page.url()}`);
}

// ======================================================
// 6. MAIN
// ======================================================

(async () => {
  const browser = await chromium.launch({
    headless: true,
  });

  const context = await browser.newContext();

  const page = await context.newPage();

  await page.setViewportSize({
    width: 1280,
    height: 800,
  });

  console.log("🎯 Starting screenshot capture...\n");

  const results = {
    success: [],
    failed: [],
  };

  // --------------------------------------------------
  // PUBLIC ROUTES
  // --------------------------------------------------

  for (const route of routesToCapture.filter((r) => !r.auth)) {
    for (const theme of ["light", "dark"]) {
      const success = await takeScreenshot(page, route, theme);

      const key = `${theme}-${route.slug}`;

      (success ? results.success : results.failed).push(key);
    }
  }

  // --------------------------------------------------
  // LOGIN
  // --------------------------------------------------

  try {
    if (routesToCapture.some((r) => r.auth)) {
      await login(page);

      // Authenticated screenshots
      for (const route of routesToCapture.filter((r) => r.auth)) {
        for (const theme of ["light", "dark"]) {
          const success = await takeScreenshot(page, route, theme);

          const key = `${theme}-${route.slug}`;

          (success ? results.success : results.failed).push(key);
        }
      }
    }
  } catch (error) {
    console.error(`❌ Login failed: ${error.message}`);

    results.failed.push("login");
  }

  await browser.close();

  // ==================================================
  // SUMMARY
  // ==================================================

  console.log("\n" + "=".repeat(60));
  console.log("📊 SCREENSHOT SUMMARY");
  console.log("=".repeat(60));

  console.log(`✅ Success: ${results.success.length}`);
  console.log(`❌ Failed: ${results.failed.length}`);

  if (results.failed.length > 0) {
    console.log(`\nFailed: ${results.failed.join(", ")}`);

    process.exit(1);
  }

  console.log("\n✅ All screenshots captured!");

  process.exit(0);
})();