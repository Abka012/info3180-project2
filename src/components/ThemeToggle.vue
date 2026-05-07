<script setup>
import { ref, onMounted } from "vue";

const isDark = ref(false);

const syncTheme = () => {
  isDark.value = document.documentElement.classList.contains("dark");
};

onMounted(() => {
  syncTheme();
});

const toggleTheme = () => {
  const html = document.documentElement;

  if (html.classList.contains("dark")) {
    html.classList.remove("dark");
    localStorage.setItem("theme", "light");
  } else {
    html.classList.add("dark");
    localStorage.setItem("theme", "dark");
  }

  syncTheme(); // 🔥 force sync after toggle
};
</script>

<template>
  <button
    @click="toggleTheme"
    class="px-4 py-2 rounded-xl border transition bg-gray-200 dark:bg-gray-700 dark:text-white"
  >
    {{ isDark ? "🌙 Dark" : "☀️ Light" }}
  </button>
</template>