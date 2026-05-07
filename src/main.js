/**
 * Main application entry point
 *
 * This file initializes the Vue application, sets up routing,
 * handles dark mode preferences, and manages service worker registration.
 */

import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import socketService from "./services/socketService";
import "./assets/base.css";

const app = createApp(App);

app.use(router);

/**
 * Register service worker for production builds
 *
 * Enables offline capabilities and caching for the application
 * when running in production mode.
 */
if ("serviceWorker" in navigator && import.meta.env.PROD) {
  window.addEventListener("load", () => {
    navigator.serviceWorker
      .register("/sw.js")
      .then((registration) => {
        console.log("SW registered:", registration);
      })
      .catch((error) => {
        console.log("SW registration failed:", error);
      });
  });
}

/**
 * Initialize socket connection if user is logged in
 *
 * Checks for user data in localStorage and establishes
 * WebSocket connection if user is authenticated.
 */
const user = JSON.parse(localStorage.getItem("user"));
if (user) {
  socketService.connect();
}

/**
 * Mount the Vue application to the DOM
 */
app.mount("#app");
