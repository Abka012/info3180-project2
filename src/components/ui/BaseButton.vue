<template>
  <button
    :class="[
      'btn',
      variantClasses,
      sizeClasses,
      { 'opacity-50 cursor-not-allowed': disabled || loading },
    ]"
    :disabled="disabled || loading"
    @click="$emit('click', $event)"
  >
    <svg
      v-if="loading"
      class="animate-spin -ml-1 mr-2 h-4 w-4"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle
        class="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        stroke-width="4"
      />
      <path
        class="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      />
    </svg>
    <slot />
  </button>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  variant: {
    type: String,
    default: "primary",
    validator: (v) =>
      ["primary", "secondary", "outline", "ghost", "danger"].includes(v),
  },
  size: {
    type: String,
    default: "md",
    validator: (v) => ["sm", "md", "lg"].includes(v),
  },
  disabled: Boolean,
  loading: Boolean,
});

defineEmits(["click"]);

const variantClasses = computed(
  () =>
    ({
      primary:
        "bg-[var(--primary)] text-[var(--bg)] hover:bg-[color-mix(in srgb,var(--primary),var(--text-primary) 15%)] focus:ring-[var(--primary)]",
      secondary:
        "bg-[var(--surface)] text-[var(--text-secondary)] hover:bg-[color-mix(in srgb,var(--surface),var(--text-primary) 5%)] focus:ring-[var(--border)]",
      outline:
        "border-2 border-[var(--primary)] text-[var(--text-primary)] hover:bg-[color-mix(in srgb,var(--primary),transparent 80%)] focus:ring-[var(--primary)]",
      ghost:
        "text-[var(--text-secondary)] hover:bg-[color-mix(in srgb,var(--surface),var(--text-primary) 5%)] focus:ring-[var(--border)]",
      danger:
        "bg-[var(--danger)] text-[var(--bg)] hover:bg-[color-mix(in srgb,var(--danger),var(--text-primary) 15%)] focus:ring-[var(--danger)]",
    })[props.variant],
);

const sizeClasses = computed(
  () =>
    ({
      sm: "px-3 py-1.5 text-sm rounded-[var(--radius-sm)]",
      md: "px-4 py-2 rounded-[var(--radius-md)]",
      lg: "px-6 py-3 text-lg rounded-[var(--radius-md)]",
    })[props.size],
);
</script>
