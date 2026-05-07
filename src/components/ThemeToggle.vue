<script setup>
import { ref, onMounted } from "vue";

const isDark = ref(false);

onMounted(() => {
  const saved = localStorage.getItem("theme");
  const systemDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  isDark.value = saved === "dark" || (!saved && systemDark);
  document.documentElement.setAttribute(
    "data-theme",
    isDark.value ? "dark" : "light",
  );
});

const toggle = () => {
  isDark.value = !isDark.value;
  document.documentElement.setAttribute(
    "data-theme",
    isDark.value ? "dark" : "light",
  );
  localStorage.setItem("theme", isDark.value ? "dark" : "light");
};
</script>

<template>
  <button
    @click="toggle"
    class="theme-toggle"
    :aria-label="'Switch to ' + (isDark ? 'light' : 'dark') + ' mode'"
  >
    {{ isDark ? "☀️" : "🌙" }}
  </button>
</template>

<style scoped>
.theme-toggle {
  background: none;
  border: 1px solid var(--color-border);
  border-radius: 0.5rem;
  padding: 0.5rem;
  cursor: pointer;
  font-size: 1.25rem;
  line-height: 1;
  transition: all 0.2s;
}
.theme-toggle:hover {
  background-color: var(--primary);
  color: var(--bg);
}
</style>
