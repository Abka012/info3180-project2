<template>
  <div
    class="min-h-[calc(100vh-4rem)] flex items-center justify-center px-4 py-12"
  >
    <div class="w-full max-w-md">
      <!-- Success State -->
      <div
        v-if="showSuccess"
        class="bg-[var(--bg)] rounded-2xl shadow-xl p-8 text-center border border-[var(--border)]"
      >
        <div
          class="w-20 h-20 mx-auto mb-6 rounded-full bg-[var(--surface)] flex items-center justify-center"
        >
          <svg
            class="w-10 h-10 text-[var(--success)]"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M5 13l4 4L19 7"
            />
          </svg>
        </div>
        <h1 class="text-2xl font-bold text-[var(--text-primary)] mb-3">
          Registration Successful!
        </h1>
        <p class="text-[var(--text-secondary)] mb-6">
          {{ successMessage }}
        </p>
        <div class="flex gap-3">
          <router-link
            to="/login"
            class="flex-1 py-3.5 px-6 bg-[var(--primary)] text-[var(--bg)] font-semibold rounded-xl transition-all duration-300"
          >
            Go to Login
          </router-link>
          <button
            :disabled="resendLoading"
            class="flex-1 py-3.5 px-6 bg-[var(--surface)] text-[var(--text-secondary)] font-semibold rounded-xl transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
            @click="handleResendVerification"
          >
            {{ resendLoading ? "Sending..." : "Resend Email" }}
          </button>
        </div>
      </div>

      <!-- Register Form -->
      <div
        v-else
        class="bg-[var(--bg)] rounded-2xl shadow-xl p-8 border border-[var(--border)]"
      >
        <!-- Header -->
        <div class="text-center mb-8">
          <div
            class="w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-to-br from-[var(--primary)] to-[var(--accent)] flex items-center justify-center overflow-hidden"
          >
            <img
              src="/src/assets/logo.svg"
              alt="DriftDater Logo"
              class="w-full h-full object-cover"
            />
          </div>
          <h1 class="text-2xl font-bold text-[var(--text-primary)] mb-2">
            Join DriftDater
          </h1>
          <p class="text-[var(--text-secondary)]">
            Find your perfect match today
          </p>
        </div>

        <!-- Error Alert -->
        <div
          v-if="errors.general"
          class="mb-6 p-4 bg-[var(--surface)] border border-[var(--danger)] rounded-xl"
        >
          <p class="text-sm text-[var(--danger)]">
            {{ errors.general[0] }}
          </p>
        </div>

        <!-- Form -->
        <form class="space-y-5" @submit.prevent="handleRegister">
          <!-- Name -->
          <div>
            <label
              for="name"
              class="block text-sm font-medium text-[var(--text-secondary)] mb-1.5"
            >
              Full Name
            </label>
            <input
              id="name"
              v-model="name"
              type="text"
              placeholder="Your Full Name"
              :disabled="loading"
              required
              class="w-full px-4 py-3 bg-[var(--input-bg)] border border-[var(--border)] rounded-xl text-[var(--text-primary)] placeholder-[var(--placeholder)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)] focus:border-transparent transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              :class="{
                'border-[var(--danger)]': errors.name,
              }"
            />
            <p v-if="errors.name" class="mt-1.5 text-sm text-[var(--danger)]">
              {{ errors.name }}
            </p>
          </div>

          <!-- Email -->
          <div>
            <label
              for="email"
              class="block text-sm font-medium text-[var(--text-secondary)] mb-1.5"
            >
              Email Address
            </label>
            <input
              id="email"
              v-model="email"
              type="email"
              placeholder="you@example.com"
              :disabled="loading"
              required
              class="w-full px-4 py-3 bg-[var(--input-bg)] border border-[var(--border)] rounded-xl text-[var(--text-primary)] placeholder-[var(--placeholder)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)] focus:border-transparent transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              :class="{
                'border-[var(--danger)]': errors.email,
                'border-[var(--success)]': emailValid,
              }"
              @blur="validateEmailField"
            />
            <p v-if="errors.email" class="mt-1.5 text-sm text-[var(--danger)]">
              {{ errors.email }}
            </p>
            <p v-if="emailValid" class="mt-1.5 text-sm text-[var(--success)]">
              Email looks good!
            </p>
          </div>

          <!-- Password -->
          <div>
            <label
              for="password"
              class="block text-sm font-medium text-[var(--text-secondary)] mb-1.5"
            >
              Password
            </label>
            <div class="relative">
              <input
                id="password"
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="Create a strong password"
                :disabled="loading"
                required
                class="w-full px-4 py-3 pr-12 bg-[var(--input-bg)] border border-[var(--border)] rounded-xl text-[var(--text-primary)] placeholder-[var(--placeholder)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)] focus:border-transparent transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                :class="{
                  'border-[var(--danger)]': errors.password && password,
                  'border-[var(--success)]': passwordValid,
                }"
                @input="validatePassword"
              />
              <button
                type="button"
                class="absolute right-3 top-1/2 -translate-y-1/2 text-[var(--text-secondary)] transition-colors"
                tabindex="-1"
                @click="showPassword = !showPassword"
              >
                <svg
                  v-if="!showPassword"
                  class="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                  />
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                  />
                </svg>
                <svg
                  v-else
                  class="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"
                  />
                </svg>
              </button>
            </div>

            <!-- Password Strength Indicator -->
            <div v-if="password" class="mt-2 space-y-2">
              <div class="flex gap-1">
                <div
                  v-for="i in 3"
                  :key="i"
                  class="h-1.5 flex-1 rounded-full transition-all duration-300"
                  :class="getStrengthClass(i)"
                ></div>
              </div>
              <p class="text-xs" :class="strengthTextClass">
                Password strength: {{ passwordStrength }}
              </p>

              <!-- Password Requirements -->
              <div class="mt-2 p-3 bg-[var(--surface)] rounded-lg">
                <p
                  class="text-xs font-medium text-[var(--text-secondary)] mb-2"
                >
                  Password must contain:
                </p>
                <ul class="space-y-1">
                  <li
                    class="flex items-center gap-2 text-xs"
                    :class="
                      passwordRequirements.length
                        ? 'text-[var(--success)]'
                        : 'text-[var(--text-secondary)]'
                    "
                  >
                    <svg
                      v-if="passwordRequirements.length"
                      class="w-3.5 h-3.5"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path
                        fill-rule="evenodd"
                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                        clip-rule="evenodd"
                      />
                    </svg>
                    <svg
                      v-else
                      class="w-3.5 h-3.5"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path
                        fill-rule="evenodd"
                        d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                        clip-rule="evenodd"
                      />
                    </svg>
                    At least 8 characters
                  </li>
                  <li
                    class="flex items-center gap-2 text-xs"
                    :class="
                      passwordRequirements.uppercase
                        ? 'text-[var(--success)]'
                        : 'text-[var(--text-secondary)]'
                    "
                  >
                    <svg
                      v-if="passwordRequirements.uppercase"
                      class="w-3.5 h-3.5"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path
                        fill-rule="evenodd"
                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                        clip-rule="evenodd"
                      />
                    </svg>
                    <svg
                      v-else
                      class="w-3.5 h-3.5"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path
                        fill-rule="evenodd"
                        d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                        clip-rule="evenodd"
                      />
                    </svg>
                    One uppercase letter
                  </li>
                  <li
                    class="flex items-center gap-2 text-xs"
                    :class="
                      passwordRequirements.number
                        ? 'text-[var(--success)]'
                        : 'text-[var(--text-secondary)]'
                    "
                  >
                    <svg
                      v-if="passwordRequirements.number"
                      class="w-3.5 h-3.5"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path
                        fill-rule="evenodd"
                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                        clip-rule="evenodd"
                      />
                    </svg>
                    <svg
                      v-else
                      class="w-3.5 h-3.5"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path
                        fill-rule="evenodd"
                        d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                        clip-rule="evenodd"
                      />
                    </svg>
                    One number
                  </li>
                  <li
                    class="flex items-center gap-2 text-xs"
                    :class="
                      passwordRequirements.special
                        ? 'text-[var(--success)]'
                        : 'text-[var(--text-secondary)]'
                    "
                  >
                    <svg
                      v-if="passwordRequirements.special"
                      class="w-3.5 h-3.5"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path
                        fill-rule="evenodd"
                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                        clip-rule="evenodd"
                      />
                    </svg>
                    <svg
                      v-else
                      class="w-3.5 h-3.5"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path
                        fill-rule="evenodd"
                        d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                        clip-rule="evenodd"
                      />
                    </svg>
                    One special character
                  </li>
                </ul>
              </div>
            </div>

            <p
              v-if="errors.password"
              class="mt-1.5 text-sm text-[var(--danger)]"
            >
              {{ errors.password }}
            </p>
          </div>

          <!-- Confirm Password -->
          <div>
            <label
              for="confirmPassword"
              class="block text-sm font-medium text-[var(--text-secondary)] mb-1.5"
            >
              Confirm Password
            </label>
            <input
              id="confirmPassword"
              v-model="confirmPassword"
              type="password"
              placeholder="Confirm your password"
              :disabled="loading"
              required
              class="w-full px-4 py-3 bg-[var(--input-bg)] border border-[var(--border)] rounded-xl text-[var(--text-primary)] placeholder-[var(--placeholder)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)] focus:border-transparent transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              :class="{
                'border-[var(--danger)]': passwordMismatch,
                'border-[var(--success)]': passwordsMatch && confirmPassword,
              }"
              @input="validatePasswordMatch"
            />
            <p
              v-if="passwordMismatch"
              class="mt-1.5 text-sm text-[var(--danger)]"
            >
              {{ passwordMismatch }}
            </p>
            <p
              v-if="passwordsMatch && confirmPassword"
              class="mt-1.5 text-sm text-[var(--success)]"
            >
              Passwords match!
            </p>
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            :disabled="loading"
            class="w-full py-3.5 px-6 bg-[var(--primary)] text-[var(--bg)] font-semibold rounded-xl transition-all duration-300 shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
          >
            <svg
              v-if="loading"
              class="animate-spin -ml-1 mr-2 h-5 w-5"
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
            {{ loading ? "Creating Account..." : "Create Account" }}
          </button>
        </form>

        <!-- Login Link -->
        <p class="text-center mt-8 text-[var(--text-secondary)]">
          Already have an account?
          <router-link
            to="/login"
            class="font-medium text-[var(--text-primary)]"
          >
            Sign in
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from "vue";
import { useRouter } from "vue-router";
import { useAuth } from "../composables/useAuth";
import authService, {
  passwordValidation,
  validateEmail,
} from "../services/authService";

const router = useRouter();
const { register } = useAuth();

const name = ref(""); // Added for name input
const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const loading = ref(false);
const resendLoading = ref(false);
const showSuccess = ref(false);
const successMessage = ref("");
const showPassword = ref(false);
const errors = ref({});

// Validation state
const emailValid = ref(false);
const passwordValid = ref(false);
const passwordsMatch = ref(false);
const passwordStrength = ref("weak");
const passwordRequirements = ref({
  length: false,
  uppercase: false,
  number: false,
  special: false,
});

const passwordMismatch = computed(() => {
  if (confirmPassword.value && password.value !== confirmPassword.value) {
    return "Passwords do not match";
  }
  return "";
});

const strengthTextClass = computed(() => {
  const classes = {
    weak: "text-[var(--danger)]",
    medium: "text-[var(--warning)]",
    strong: "text-[var(--success)]",
  };
  return classes[passwordStrength.value] || classes.weak;
});

const validateEmailField = () => {
  if (!email.value) {
    emailValid.value = false;
    return;
  }

  if (!validateEmail(email.value)) {
    emailValid.value = false;
    errors.value.email = "Please enter a valid email address";
  } else {
    emailValid.value = true;
    errors.value.email = "";
  }
};

const validatePassword = () => {
  if (!password.value) {
    passwordValid.value = false;
    passwordStrength.value = "weak";
    passwordRequirements.value = {
      length: false,
      uppercase: false,
      number: false,
      special: false,
    };
    return;
  }

  const result = passwordValidation.validate(password.value);
  passwordValid.value = result.isValid;
  passwordStrength.value = result.strength;

  // Update requirements
  passwordRequirements.value = {
    length: password.value.length >= 8,
    uppercase: /[A-Z]/.test(password.value),
    number: /[0-9]/.test(password.value),
    special: /[!@#$%^&*(),.?":{}|<>]/.test(password.value),
  };

  // Re-check match
  validatePasswordMatch();
};

const validatePasswordMatch = () => {
  if (!confirmPassword.value) {
    passwordsMatch.value = false;
    return;
  }

  passwordsMatch.value = password.value === confirmPassword.value;
};

const getStrengthClass = (level) => {
  const strengthLevels = { weak: 1, medium: 2, strong: 3 };
  const currentLevel = strengthLevels[passwordStrength.value] || 1;

  const baseClass = "transition-all duration-300";
  const activeClass =
    level <= currentLevel
      ? passwordStrength.value === "weak"
        ? "bg-[var(--danger)]"
        : passwordStrength.value === "medium"
          ? "bg-[var(--warning)]"
          : "bg-[var(--success)]"
      : "bg-[var(--surface)]";

  return `${baseClass} ${activeClass}`;
};

const handleRegister = async () => {
  errors.value = {};

  // Validate all fields
  validateEmailField();
  validatePassword();
  validatePasswordMatch();

  if (!name.value) {
    // Added validation for name
    errors.value.name = "Full name is required";
  }

  if (!emailValid.value || !passwordValid.value || !name.value) {
    if (!passwordValid.value) {
      // Get the specific password validation error message
      const passwordCheckResult = passwordValidation.validate(password.value);
      if (passwordCheckResult.errors.length > 0) {
        errors.value.password = passwordCheckResult.errors[0];
      } else {
        // Fallback message if no specific error is found but password is invalid
        errors.value.password = "Password is invalid.";
      }
    }
    // Other field errors are already handled by their respective validation functions
    return;
  }

  if (passwordMismatch.value) {
    // Explicitly assign the mismatch error to the confirmPassword field
    errors.value.confirmPassword = passwordMismatch.value;
    return;
  }

  // If all checks pass, proceed with registration
  if (!emailValid.value || !passwordValid.value || !name.value) {
    return;
  }

  loading.value = true;

  try {
    // Pass name to the register function
    await register(name.value, email.value, password.value);
    showSuccess.value = true;
    successMessage.value =
      "Please check your email inbox to verify your account before logging in.";
  } catch (err) {
    if (err.response?.data?.errors) {
      errors.value = err.response.data.errors;
    } else {
      errors.value = {
        general: [err.message || "Registration failed. Please try again."],
      };
    }
  } finally {
    loading.value = false;
  }
};

const handleResendVerification = async () => {
  resendLoading.value = true;

  try {
    await authService.resendVerification(email.value);
    successMessage.value =
      "Verification email resent! Please check your inbox.";
  } catch (err) {
    errors.value = {
      general: [err.message || "Failed to resend verification email"],
    };
  } finally {
    resendLoading.value = false;
  }
};

// Watch for password changes to update match validation
watch(password, () => {
  if (confirmPassword.value) {
    validatePasswordMatch();
  }
});
</script>
