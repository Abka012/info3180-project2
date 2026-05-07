<template>
  <span :class="[badgeClasses, variantClasses]">
    <slot />
  </span>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  variant: {
    type: String,
    default: "primary",
    validator: (v) =>
      ["primary", "success", "warning", "danger", "gray"].includes(v),
  },
  dot: Boolean,
});

const variantClasses = computed(
  () =>
    ({
      primary: "bg-[var(--primary)]/30 text-[var(--text-primary)]",
      success: "bg-[var(--success)]/30 text-[var(--success)]",
      warning: "bg-[var(--warning)]/30 text-[var(--warning)]",
      danger: "bg-[var(--danger)]/30 text-[var(--danger)]",
      gray: "bg-[var(--surface)] text-[var(--text-secondary)]",
    })[props.variant],
);

const badgeClasses =
  "inline-flex items-center justify-center px-2.5 py-0.5 text-xs font-medium rounded-[var(--radius-full)]";
</script>
