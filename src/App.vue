<script setup>
/**
 * Main application component
 *
 * This is the root component that sets up the application layout,
 * including the header and main content area with route transitions.
 */
import { RouterView } from "vue-router";
import AppHeader from "@/components/AppHeader.vue";
</script>

<template>
  <!--
    Main application layout container

    Features:
    - Full height screen container
    - Light/dark mode support with smooth transitions
    - Fixed header with content area below
    - Route transitions for smooth page navigation
  -->
  <div
    class="min-h-screen transition-colors duration-300"
    style="background-color: var(--color-bg); color: var(--color-text)"
  >
    <AppHeader />
    <main class="pt-16">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<style>
/*
  Global styles for the application

  scroll-padding-top: Compensates for fixed header when scrolling
  to anchored elements
*/
html {
  scroll-padding-top: 4rem;
}
</style>
