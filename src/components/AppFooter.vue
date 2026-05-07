<template>
  <footer class="bg-[var(--surface)] border-t border-[var(--border)] mt-auto">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="flex flex-col md:flex-row justify-between items-center gap-4">
        <div class="flex items-center space-x-2">
          <div
            class="w-8 h-8 rounded-full bg-gradient-to-br from-[var(--primary)] to-[var(--accent)] flex items-center justify-center"
          >
            <span class="text-[var(--text-primary)] font-bold text-sm">D</span>
          </div>
          <span class="text-lg font-bold text-[var(--text-secondary)]">
            DriftDater
          </span>
        </div>

        <div
          class="flex items-center space-x-6 text-sm text-[var(--text-secondary)]"
        >
          <router-link to="/about" class="transition-colors">
            About
          </router-link>
          <router-link to="/login" class="transition-colors">
            Login
          </router-link>
          <router-link to="/register" class="transition-colors">
            Register
          </router-link>
        </div>

        <div class="text-sm text-[var(--text-secondary)]">
          &copy; {{ year }} DriftDater. All rights reserved.
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
const year = new Date().getFullYear();
</script>
