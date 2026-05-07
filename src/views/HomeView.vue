<template>
  <div class="min-h-[calc(100vh-4rem)]">
    <!-- Guest View: Public Landing Page -->
    <template v-if="!isAuthenticated">
      <!-- Hero Section -->
      <section class="relative overflow-hidden bg-[var(--bg)]">
        <div class="absolute inset-0 opacity-50">
          <div
            class="absolute inset-0"
            style="
              background-image:
                radial-gradient(
                  circle at 25% 25%,
                  var(--surface) 0%,
                  transparent 50%
                ),
                radial-gradient(
                  circle at 75% 75%,
                  var(--surface) 0%,
                  transparent 50%
                );
            "
          ></div>
        </div>

        <div
          class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 lg:py-32"
        >
          <div class="grid lg:grid-cols-2 gap-12 items-center">
            <div class="text-center lg:text-left animate-fade-in">
              <span
                class="inline-block px-4 py-1.5 rounded-full bg-[var(--surface)] text-[var(--text-primary)] text-sm font-medium mb-6"
              >
                Find Your Perfect Match
              </span>
              <h1
                class="text-4xl sm:text-5xl lg:text-6xl font-bold text-[var(--text-primary)] leading-tight mb-6"
              >
                Connect with
                <span
                  class="text-transparent bg-clip-text bg-gradient-to-r from-[var(--primary)] to-[var(--success)]"
                >
                  Real People
                </span>
              </h1>
              <p
                class="text-lg sm:text-xl text-[var(--text-secondary)] mb-8 max-w-xl mx-auto lg:mx-0"
              >
                Discover meaningful connections based on shared interests,
                values, and chemistry. Your perfect match is just a swipe away.
              </p>
              <div
                class="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start"
              >
                <router-link
                  to="/register"
                  class="px-8 py-4 bg-[var(--primary)] text-[var(--bg)] font-semibold rounded-xl transition-all duration-300 shadow-lg hover:shadow-xl hover:-translate-y-1"
                >
                  Get Started Free
                </router-link>
                <router-link
                  to="/about"
                  class="px-8 py-4 bg-[var(--bg)] hover:bg-[var(--surface)] text-[var(--text-secondary)] font-semibold rounded-xl transition-all duration-300 border border-[var(--border)]"
                >
                  Learn More
                </router-link>
              </div>

              <div
                class="mt-12 flex flex-wrap gap-8 justify-center lg:justify-start"
              >
                <div class="text-center">
                  <div class="text-3xl font-bold text-[var(--text-primary)]">
                    10K+
                  </div>
                  <div class="text-sm text-[var(--text-secondary)]">
                    Active Users
                  </div>
                </div>
                <div class="text-center">
                  <div class="text-3xl font-bold text-[var(--text-primary)]">
                    5K+
                  </div>
                  <div class="text-sm text-[var(--text-secondary)]">
                    Matches Made
                  </div>
                </div>
                <div class="text-center">
                  <div class="text-3xl font-bold text-[var(--text-primary)]">
                    4.8
                  </div>
                  <div class="text-sm text-[var(--text-secondary)]">
                    App Rating
                  </div>
                </div>
              </div>
            </div>

            <div class="relative hidden lg:block">
              <div class="relative w-full aspect-square max-w-md mx-auto">
                <div
                  class="absolute top-0 right-0 w-48 h-64 bg-[var(--bg)] rounded-2xl shadow-2xl rotate-6 animate-pulse-soft p-4"
                >
                  <div
                    class="w-full h-40 bg-gradient-to-br from-[var(--primary)] to-[var(--accent)] rounded-xl mb-3"
                  ></div>
                  <div class="h-4 bg-[var(--surface)] rounded w-3/4 mb-2"></div>
                  <div class="h-3 bg-[var(--surface)] rounded w-1/2"></div>
                </div>
                <div
                  class="absolute top-8 left-4 w-48 h-64 bg-[var(--bg)] rounded-2xl shadow-2xl -rotate-3 animate-pulse-soft p-4"
                  style="animation-delay: 0.5s"
                >
                  <div
                    class="w-full h-40 bg-gradient-to-br from-[var(--accent)] to-[var(--primary)] rounded-xl mb-3"
                  ></div>
                  <div class="h-4 bg-[var(--surface)] rounded w-3/4 mb-2"></div>
                  <div class="h-3 bg-[var(--surface)] rounded w-1/2"></div>
                </div>
                <div
                  class="absolute top-16 left-16 w-48 h-64 bg-[var(--bg)] rounded-2xl shadow-2xl rotate-1 animate-pulse-soft p-4"
                  style="animation-delay: 1s"
                >
                  <div
                    class="w-full h-40 bg-gradient-to-br from-[var(--warning)] to-[var(--primary)] rounded-xl mb-3"
                  ></div>
                  <div class="h-4 bg-[var(--surface)] rounded w-3/4 mb-2"></div>
                  <div class="h-3 bg-[var(--surface)] rounded w-1/2"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Features Section -->
      <section class="py-20 bg-[var(--surface)]">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="text-center mb-16">
            <h2
              class="text-3xl sm:text-4xl font-bold text-[var(--text-primary)] mb-4"
            >
              Why Choose DriftDater?
            </h2>
            <p
              class="text-lg text-[var(--text-secondary)] max-w-2xl mx-auto leading-snug"
            >
              We use advanced algorithms to match you with people who truly
              complement your personality and preferences.
            </p>
          </div>

          <div class="grid md:grid-cols-3 gap-8">
            <div
              class="text-center p-8 rounded-2xl bg-[var(--bg)] hover:shadow-lg transition-shadow duration-300"
            >
              <div
                class="w-16 h-16 mx-auto mb-6 bg-gradient-to-br from-[var(--primary)] to-[var(--accent)] rounded-2xl flex items-center justify-center"
              >
                <svg
                  class="w-8 h-8 text-[var(--bg)]"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
                  />
                </svg>
              </div>
              <h3 class="text-xl font-semibold text-[var(--text-primary)] mb-3">
                Smart Matching
              </h3>
              <p class="text-[var(--text-secondary)]">
                Our algorithm considers interests, location, and preferences to
                find your perfect match.
              </p>
            </div>

            <div
              class="text-center p-8 rounded-2xl bg-[var(--bg)] hover:shadow-lg transition-shadow duration-300"
            >
              <div
                class="w-16 h-16 mx-auto mb-6 bg-gradient-to-br from-[var(--success)] to-[var(--accent)] rounded-2xl flex items-center justify-center"
              >
                <svg
                  class="w-8 h-8 text-[var(--bg)]"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
                  />
                </svg>
              </div>
              <h3 class="text-xl font-semibold text-[var(--text-primary)] mb-3">
                Privacy First
              </h3>
              <p class="text-[var(--text-secondary)]">
                Your data is secure with us. We never share your information
                with third parties.
              </p>
            </div>

            <div
              class="text-center p-8 rounded-2xl bg-[var(--bg)] hover:shadow-lg transition-shadow duration-300"
            >
              <div
                class="w-16 h-16 mx-auto mb-6 bg-gradient-to-br from-[var(--warning)] to-[var(--primary)] rounded-2xl flex items-center justify-center"
              >
                <svg
                  class="w-8 h-8 text-[var(--bg)]"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
                  />
                </svg>
              </div>
              <h3 class="text-xl font-semibold text-[var(--text-primary)] mb-3">
                Real Connections
              </h3>
              <p class="text-[var(--text-secondary)]">
                Chat with your matches in real-time and build genuine
                relationships.
              </p>
            </div>
          </div>
        </div>
      </section>

      <!-- CTA Section -->
      <section
        class="py-20 bg-gradient-to-r from-[var(--primary)] to-[var(--accent)]"
      >
        <div class="max-w-4xl mx-auto px-4 text-center">
          <h2 class="text-3xl sm:text-4xl font-bold text-[var(--bg)] mb-6">
            Ready to Find Your Match?
          </h2>
          <p class="text-xl text-[var(--bg)] mb-8">
            Join thousands of happy users who found their perfect partner on
            DriftDater.
          </p>
          <router-link
            to="/register"
            class="inline-block px-10 py-4 bg-[var(--bg)] text-[var(--text-primary)] font-semibold rounded-xl hover:bg-[var(--surface)] transition-colors duration-300 shadow-lg"
          >
            Start Dating Today
          </router-link>
        </div>
      </section>
    </template>

    <!-- Authenticated: No Profile Created -->
    <template v-else-if="!hasProfile">
      <section
        class="min-h-[calc(100vh-8rem)] flex items-center justify-center px-4 py-12 bg-[var(--surface)]"
      >
        <div class="max-w-lg w-full text-center">
          <div
            class="w-24 h-24 mx-auto mb-8 bg-gradient-to-br from-[var(--primary)] to-[var(--accent)] rounded-full flex items-center justify-center"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="w-12 h-12 text-[var(--bg)]"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"
              />
            </svg>
          </div>

          <h1
            class="text-3xl sm:text-4xl font-bold text-[var(--text-primary)] mb-4"
          >
            Welcome to DriftDater!
          </h1>

          <p class="text-lg text-[var(--text-secondary)] mb-8">
            Create your profile to start connecting with people who share your
            interests.
          </p>

          <router-link
            to="/profile/edit"
            class="inline-flex items-center gap-2 px-8 py-4 bg-[var(--primary)] text-[var(--bg)] font-semibold rounded-xl transition-all duration-300 shadow-lg hover:shadow-xl hover:-translate-y-1"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 6v6m0 0v6m0-6h6m-6 0H6"
              />
            </svg>
            Create Your Profile
          </router-link>

          <div class="mt-12 flex flex-col sm:flex-row gap-6 justify-center">
            <div class="flex items-center gap-3">
              <div
                class="w-10 h-10 bg-[var(--surface)] rounded-full flex items-center justify-center"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="w-5 h-5 text-[var(--success)]"
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
              <span class="text-[var(--text-secondary)]">Free forever</span>
            </div>
            <div class="flex items-center gap-3">
              <div
                class="w-10 h-10 bg-[var(--surface)] rounded-full flex items-center justify-center"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="w-5 h-5 text-[var(--success)]"
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
              <span class="text-[var(--text-secondary)]"
                >Takes only 2 minutes</span
              >
            </div>
            <div class="flex items-center gap-3">
              <div
                class="w-10 h-10 bg-[var(--surface)] rounded-full flex items-center justify-center"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="w-5 h-5 text-[var(--success)]"
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
              <span class="text-[var(--text-secondary)]"
                >Find meaningful connections</span
              >
            </div>
          </div>
        </div>
      </section>
    </template>

    <!-- Authenticated: Has Profile - Redesigned Dashboard -->
    <template v-else>
      <section class="min-h-[calc(100vh-4rem)] bg-[var(--surface)] py-8">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <!-- Welcome Banner -->
          <div
            class="relative overflow-hidden rounded-3xl bg-gradient-to-r from-[var(--primary)] to-[var(--accent)] p-8 mb-8 shadow-xl"
          >
            <div
              class="absolute top-0 right-0 w-64 h-64 bg-[var(--bg)]/10 rounded-full -translate-y-1/2 translate-x-1/2"
            ></div>
            <div
              class="absolute bottom-0 left-0 w-32 h-32 bg-[var(--bg)]/10 rounded-full translate-y-1/2 -translate-x-1/2"
            ></div>

            <div class="relative z-10">
              <div class="flex items-center gap-4 mb-4">
                <div
                  class="w-16 h-16 rounded-full overflow-hidden border-2 border-[var(--bg)] shadow-lg"
                >
                  <img
                    v-if="profilePicture"
                    :src="`${API_BASE_URL}/uploads/${profilePicture}`"

                    class="w-full h-full object-cover"
                    @error="($event) => ($event.target.style.display = 'none')"
                  />
                  <div
                    v-else
                    class="w-full h-full bg-[var(--bg)] flex items-center justify-center text-[var(--text-primary)] text-2xl font-bold"
                  >
                    {{ userName.charAt(0).toUpperCase() }}
                  </div>
                </div>
                <div>
                  <h1 class="text-3xl font-bold text-[var(--bg)] mb-1">
                    Welcome back, {{ userName }}!
                  </h1>
                  <p class="text-[var(--bg)]">
                    Ready to find your perfect match today?
                  </p>
                </div>
              </div>

              <div class="flex flex-wrap gap-3 mt-6">
                <router-link
                  to="/browse"
                  class="inline-flex items-center gap-2 px-5 py-2.5 bg-[var(--bg)] text-[var(--text-primary)] font-semibold rounded-xl hover:shadow-xl transition-all"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="w-5 h-5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <circle cx="12" cy="12" r="10" />
                    <polygon
                      points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"
                    />
                  </svg>
                  Browse Profiles
                </router-link>
                <router-link
                  to="/search"
                  class="inline-flex items-center gap-2 px-5 py-2.5 bg-[var(--bg)] text-[var(--text-primary)] font-semibold rounded-xl hover:shadow-xl transition-all"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="w-5 h-5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <circle cx="11" cy="11" r="8" />
                    <path d="m21 21-4.3-4.3" />
                  </svg>
                  Advanced Search
                </router-link>
              </div>
            </div>
          </div>

          <!-- Stats Cards -->
          <div class="grid grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <!-- New Matches -->
            <div
              class="group bg-[var(--bg)] rounded-2xl p-6 shadow-sm hover:shadow-xl transition-all duration-300 border border-[var(--border)]"
            >
              <router-link to="/matches" class="block">
                <div class="flex items-center justify-between mb-4">
                  <div
                    class="w-14 h-14 rounded-2xl bg-gradient-to-br from-[var(--primary)] to-[var(--accent)] flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="w-7 h-7 text-[var(--bg)]"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
                      />
                    </svg>
                  </div>
                  <span
                    class="text-xs font-medium text-[var(--success)] bg-[var(--surface)] px-2 py-1 rounded-full"
                  >
                    This Week
                  </span>
                </div>
                <div class="text-4xl font-bold text-[var(--text-primary)] mb-1">
                  {{ stats.newMatches }}
                </div>
                <div class="text-sm text-[var(--text-secondary)]">
                  New Matches
                </div>
              </router-link>
            </div>

            <!-- Pending Likes -->
            <div
              class="group bg-[var(--bg)] rounded-2xl p-6 shadow-sm hover:shadow-xl transition-all duration-300 border border-[var(--border)]"
            >
              <router-link to="/browse" class="block">
                <div class="flex items-center justify-between mb-4">
                  <div
                    class="w-14 h-14 rounded-2xl bg-gradient-to-br from-[var(--warning)] to-[var(--primary)] flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="w-7 h-7 text-[var(--bg)]"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"
                      />
                    </svg>
                  </div>
                  <span
                    class="text-xs font-medium text-[var(--warning)] bg-[var(--surface)] px-2 py-1 rounded-full"
                  >
                    Waiting
                  </span>
                </div>
                <div class="text-4xl font-bold text-[var(--text-primary)] mb-1">
                  {{ stats.pendingLikes }}
                </div>
                <div class="text-sm text-[var(--text-secondary)]">
                  Pending Likes
                </div>
              </router-link>
            </div>

            <!-- Unread Messages -->
            <div
              class="group bg-[var(--bg)] rounded-2xl p-6 shadow-sm hover:shadow-xl transition-all duration-300 border border-[var(--border)]"
            >
              <router-link to="/messages" class="block">
                <div class="flex items-center justify-between mb-4">
                  <div
                    class="w-14 h-14 rounded-2xl bg-gradient-to-br from-[var(--accent)] to-[var(--primary)] flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="w-7 h-7 text-[var(--bg)]"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
                      />
                    </svg>
                  </div>
                  <span
                    v-if="stats.unreadMessages > 0"
                    class="text-xs font-medium text-[var(--danger)] bg-[var(--surface)] px-2 py-1 rounded-full"
                  >
                    {{ stats.unreadMessages }} New
                  </span>
                </div>
                <div class="text-4xl font-bold text-[var(--text-primary)] mb-1">
                  {{ stats.unreadMessages }}
                </div>
                <div class="text-sm text-[var(--text-secondary)]">
                  Unread Messages
                </div>
              </router-link>
            </div>

            <!-- Total Matches -->
            <div
              class="group bg-[var(--bg)] rounded-2xl p-6 shadow-sm hover:shadow-xl transition-all duration-300 border border-[var(--border)]"
            >
              <router-link to="/matches" class="block">
                <div class="flex items-center justify-between mb-4">
                  <div
                    class="w-14 h-14 rounded-2xl bg-gradient-to-br from-[var(--success)] to-[var(--accent)] flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="w-7 h-7 text-[var(--bg)]"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                      />
                    </svg>
                  </div>
                  <span
                    class="text-xs font-medium text-[var(--success)] bg-[var(--surface)] px-2 py-1 rounded-full"
                  >
                    All Time
                  </span>
                </div>
                <div class="text-4xl font-bold text-[var(--text-primary)] mb-1">
                  {{ stats.totalMatches }}
                </div>
                <div class="text-sm text-[var(--text-secondary)]">
                  Total Matches
                </div>
              </router-link>
            </div>
          </div>

          <!-- Quick Actions & Recent Matches Grid -->
          <div class="grid lg:grid-cols-3 gap-6">
            <!-- Quick Actions -->
            <div class="lg:col-span-1">
              <div
                class="bg-[var(--bg)] rounded-2xl p-6 shadow-sm border border-[var(--border)] h-full"
              >
                <h2
                  class="text-lg font-semibold text-[var(--text-primary)] mb-4"
                >
                  Quick Actions
                </h2>
                <div class="space-y-3">
                  <router-link
                    to="/browse"
                    class="flex items-center gap-3 p-3 rounded-xl bg-[var(--surface)] hover:shadow-md transition-all group"
                  >
                    <div
                      class="w-10 h-10 rounded-lg bg-[var(--primary)] flex items-center justify-center group-hover:scale-110 transition-transform"
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="w-5 h-5 text-[var(--bg)]"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <circle cx="12" cy="12" r="10" />
                        <polygon
                          points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"
                        />
                      </svg>
                    </div>
                    <div>
                      <div class="font-medium text-[var(--text-primary)]">
                        Browse Profiles
                      </div>
                      <div class="text-xs text-[var(--text-secondary)]">
                        Discover new people
                      </div>
                    </div>
                  </router-link>

                  <router-link
                    to="/search"
                    class="flex items-center gap-3 p-3 rounded-xl bg-[var(--surface)] hover:shadow-md transition-all group"
                  >
                    <div
                      class="w-10 h-10 rounded-lg bg-[var(--accent)] flex items-center justify-center group-hover:scale-110 transition-transform"
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="w-5 h-5 text-[var(--bg)]"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <circle cx="11" cy="11" r="8" />
                        <path d="m21 21-4.3-4.3" />
                      </svg>
                    </div>
                    <div>
                      <div class="font-medium text-[var(--text-primary)]">
                        Advanced Search
                      </div>
                      <div class="text-xs text-[var(--text-secondary)]">
                        Find specific matches
                      </div>
                    </div>
                  </router-link>

                  <router-link
                    to="/favorites"
                    class="flex items-center gap-3 p-3 rounded-xl bg-[var(--surface)] hover:shadow-md transition-all group"
                  >
                    <div
                      class="w-10 h-10 rounded-lg bg-[var(--primary)] flex items-center justify-center group-hover:scale-110 transition-transform"
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="w-5 h-5 text-[var(--bg)]"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"
                        />
                      </svg>
                    </div>
                    <div>
                      <div class="font-medium text-[var(--text-primary)]">
                        Favorites
                      </div>
                      <div class="text-xs text-[var(--text-secondary)]">
                        Saved profiles
                      </div>
                    </div>
                  </router-link>

                  <router-link
                    to="/profile/edit"
                    class="flex items-center gap-3 p-3 rounded-xl bg-[var(--surface)] hover:shadow-md transition-all group"
                  >
                    <div
                      class="w-10 h-10 rounded-lg bg-[var(--primary)] flex items-center justify-center group-hover:scale-110 transition-transform"
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="w-5 h-5 text-[var(--bg)]"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2" />
                        <circle cx="12" cy="7" r="4" />
                      </svg>
                    </div>
                    <div>
                      <div class="font-medium text-[var(--text-primary)]">
                        Edit Profile
                      </div>
                      <div class="text-xs text-[var(--text-secondary)]">
                        Update your info
                      </div>
                    </div>
                  </router-link>
                </div>
              </div>
            </div>

            <!-- Recent Matches -->
            <div class="lg:col-span-2">
              <div
                class="bg-[var(--bg)] rounded-2xl p-6 shadow-sm border border-[var(--border)] h-full"
              >
                <div class="flex items-center justify-between mb-6">
                  <div>
                    <h2
                      class="text-lg font-semibold text-[var(--text-primary)]"
                    >
                      Recent Matches
                    </h2>
                    <p class="text-sm text-[var(--text-secondary)]">
                      People you've recently matched with
                    </p>
                  </div>
                  <router-link
                    to="/matches"
                    class="text-[var(--text-primary)] font-medium text-sm flex items-center gap-1"
                  >
                    View All
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="w-4 h-4"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M9 5l7 7-7 7"
                      />
                    </svg>
                  </router-link>
                </div>

                <div
                  v-if="recentMatches.length > 0"
                  class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4"
                >
                  <div
                    v-for="match in recentMatches"
                    :key="match.user_id"
                    class="group text-center"
                  >
                    <router-link
                      :to="`/profile/${match.user_id}`"
                      class="block"
                    >
                      <div
                        class="relative w-20 h-20 md:w-24 md:h-24 mx-auto mb-3 rounded-full overflow-hidden bg-gradient-to-br from-[var(--primary)] to-[var(--accent)] ring-2 ring-[var(--border)] group-hover:ring-[var(--primary)] transition-all"
                      >
                        <img
                          v-if="match.profile_picture"
                          :src="`${API_BASE_URL}/uploads/${match.profile_picture}`"

                          :alt="match.user_name"
                          class="w-full h-full object-cover"
                        />
                        <div
                          v-else
                          class="w-full h-full flex items-center justify-center text-[var(--bg)] text-2xl font-bold"
                        >
                          {{ match.user_name?.charAt(0) }}
                        </div>
                      </div>
                      <p
                        class="font-medium text-[var(--text-primary)] text-sm truncate transition-colors"
                      >
                        {{ match.user_name }}
                      </p>
                    </router-link>
                  </div>
                </div>

                <div v-else class="text-center py-12">
                  <div
                    class="w-20 h-20 mx-auto mb-4 bg-[var(--surface)] rounded-full flex items-center justify-center"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="w-10 h-10 text-[var(--primary)]"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
                      />
                    </svg>
                  </div>
                  <h3
                    class="text-lg font-semibold text-[var(--text-primary)] mb-2"
                  >
                    No matches yet
                  </h3>
                  <p class="text-[var(--text-secondary)] mb-6 max-w-sm mx-auto">
                    Start browsing profiles to find your perfect match. Your
                    matches will appear here.
                  </p>
                  <router-link
                    to="/browse"
                    class="inline-flex items-center gap-2 px-6 py-3 bg-[var(--primary)] text-[var(--bg)] font-semibold rounded-xl transition-all shadow-lg hover:shadow-xl"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="w-5 h-5"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <circle cx="12" cy="12" r="10" />
                      <polygon
                        points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"
                      />
                    </svg>
                    Start Browsing
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import authService from "../services/authService";
import profileService from "../services/profileService";
import matchService from "../services/matchService";
import { useAuth } from "../composables/useAuth";
import { API_BASE_URL } from "../services/api";
import ThemeToggle from '@/components/ThemeToggle.vue'

const { isAuthenticated, user: currentUser } = useAuth();
const hasProfile = ref(false);
const userName = computed(
  () => currentUser.value?.name || currentUser.value?.username || "User",
);
const profilePicture = ref(null);
const loading = ref(true);

const stats = ref({
  newMatches: 0,
  pendingLikes: 0,
  unreadMessages: 0,
  totalMatches: 0,
});

const recentMatches = ref([]);

const loadData = async () => {
  loading.value = true;

  if (!isAuthenticated.value) {
    loading.value = false;
    return;
  }

  const user = authService.getStoredUser();
  userName.value = user?.name || user?.username || "User";
  profilePicture.value = user?.profile_picture || null;

  try {
    const profileData = await profileService.getProfile();
    hasProfile.value = true;

    if (profileData.profile_picture) {
      profilePicture.value = profileData.profile_picture;
    }

    const matchesData = await matchService.getMatches().catch(() => []);
    recentMatches.value = matchesData.slice(0, 4);
    stats.value.totalMatches = matchesData.length;
    stats.value.newMatches = matchesData.filter((m) => {
      const matchDate = new Date(m.matched_at || Date.now());
      const daysSince = (Date.now() - matchDate) / (1000 * 60 * 60 * 24);
      return daysSince <= 7;
    }).length;
  } catch {
    hasProfile.value = false;
  }

  loading.value = false;
};

onMounted(() => {
  loadData();
});

// Watch for auth changes to update the view reactively
watch(isAuthenticated, () => {
  loadData();
});
</script>
