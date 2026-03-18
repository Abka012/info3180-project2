<template>
  <div class="min-h-[calc(100vh-4rem)]">
    <!-- Hero Section -->
    <section class="relative overflow-hidden bg-gradient-to-br from-primary-50 via-white to-accent-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      <!-- Background Pattern -->
      <div class="absolute inset-0 opacity-30">
        <div class="absolute inset-0" style="background-image: radial-gradient(circle at 25% 25%, rgba(20, 184, 166, 0.1) 0%, transparent 50%), radial-gradient(circle at 75% 75%, rgba(139, 92, 246, 0.1) 0%, transparent 50%);"></div>
      </div>
      
      <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 lg:py-32">
        <div class="grid lg:grid-cols-2 gap-12 items-center">
          <!-- Left Content -->
          <div class="text-center lg:text-left animate-fade-in">
            <span class="inline-block px-4 py-1.5 rounded-full bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 text-sm font-medium mb-6">
              Find Your Perfect Match
            </span>
            <h1 class="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-900 dark:text-white leading-tight mb-6">
              Connect with 
              <span class="text-transparent bg-clip-text bg-gradient-to-r from-primary-600 to-accent-600">
                Real People
              </span>
            </h1>
            <p class="text-lg sm:text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-xl mx-auto lg:mx-0">
              Discover meaningful connections based on shared interests, values, and chemistry. Your perfect match is just a swipe away.
            </p>
            <div class="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
              <router-link 
                to="/register" 
                class="px-8 py-4 bg-primary-500 hover:bg-primary-600 text-white font-semibold rounded-xl transition-all duration-300 shadow-lg hover:shadow-xl hover:-translate-y-1"
              >
                Get Started Free
              </router-link>
              <router-link 
                to="/about" 
                class="px-8 py-4 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-200 font-semibold rounded-xl transition-all duration-300 border border-gray-200 dark:border-gray-700"
              >
                Learn More
              </router-link>
            </div>
            
            <!-- Stats -->
            <div class="mt-12 flex flex-wrap gap-8 justify-center lg:justify-start">
              <div class="text-center">
                <div class="text-3xl font-bold text-primary-600">10K+</div>
                <div class="text-sm text-gray-500 dark:text-gray-400">Active Users</div>
              </div>
              <div class="text-center">
                <div class="text-3xl font-bold text-primary-600">5K+</div>
                <div class="text-sm text-gray-500 dark:text-gray-400">Matches Made</div>
              </div>
              <div class="text-center">
                <div class="text-3xl font-bold text-primary-600">4.8</div>
                <div class="text-sm text-gray-500 dark:text-gray-400">App Rating</div>
              </div>
            </div>
          </div>
          
          <!-- Right Content - Floating Cards -->
          <div class="relative hidden lg:block">
            <div class="relative w-full aspect-square max-w-md mx-auto">
              <!-- Card 1 -->
              <div class="absolute top-0 right-0 w-48 h-64 bg-white dark:bg-gray-800 rounded-2xl shadow-2xl rotate-6 animate-pulse-soft p-4">
                <div class="w-full h-40 bg-gradient-to-br from-primary-400 to-accent-500 rounded-xl mb-3"></div>
                <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4 mb-2"></div>
                <div class="h-3 bg-gray-200 dark:bg-gray-700 rounded w-1/2"></div>
              </div>
              <!-- Card 2 -->
              <div class="absolute top-8 left-4 w-48 h-64 bg-white dark:bg-gray-800 rounded-2xl shadow-2xl -rotate-3 animate-pulse-soft p-4" style="animation-delay: 0.5s;">
                <div class="w-full h-40 bg-gradient-to-br from-accent-400 to-primary-500 rounded-xl mb-3"></div>
                <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4 mb-2"></div>
                <div class="h-3 bg-gray-200 dark:bg-gray-700 rounded w-1/2"></div>
              </div>
              <!-- Card 3 -->
              <div class="absolute top-16 left-16 w-48 h-64 bg-white dark:bg-gray-800 rounded-2xl shadow-2xl rotate-1 animate-pulse-soft p-4" style="animation-delay: 1s;">
                <div class="w-full h-40 bg-gradient-to-br from-amber-400 to-orange-500 rounded-xl mb-3"></div>
                <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4 mb-2"></div>
                <div class="h-3 bg-gray-200 dark:bg-gray-700 rounded w-1/2"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Wave Divider -->
      <div class="absolute bottom-0 left-0 right-0">
        <svg class="w-full h-16 text-white dark:text-gray-900" viewBox="0 0 1440 100" fill="currentColor">
          <path d="M0,50 C360,100 1080,0 1440,50 L1440,100 L0,100 Z"></path>
        </svg>
      </div>
    </section>

    <!-- Features Section -->
    <section class="py-20 bg-white dark:bg-gray-900">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white mb-4">
            Why Choose DriftDater?
          </h2>
          <p class="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
            We use advanced algorithms to match you with people who truly complement your personality and preferences.
          </p>
        </div>
        
        <div class="grid md:grid-cols-3 gap-8">
          <!-- Feature 1 -->
          <div class="text-center p-8 rounded-2xl bg-gray-50 dark:bg-gray-800 hover:shadow-lg transition-shadow duration-300">
            <div class="w-16 h-16 mx-auto mb-6 bg-gradient-to-br from-primary-400 to-primary-600 rounded-2xl flex items-center justify-center">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-3">Smart Matching</h3>
            <p class="text-gray-600 dark:text-gray-400">
              Our algorithm considers interests, location, and preferences to find your perfect match.
            </p>
          </div>
          
          <!-- Feature 2 -->
          <div class="text-center p-8 rounded-2xl bg-gray-50 dark:bg-gray-800 hover:shadow-lg transition-shadow duration-300">
            <div class="w-16 h-16 mx-auto mb-6 bg-gradient-to-br from-accent-400 to-accent-600 rounded-2xl flex items-center justify-center">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-3">Privacy First</h3>
            <p class="text-gray-600 dark:text-gray-400">
              Your data is secure with us. We never share your information with third parties.
            </p>
          </div>
          
          <!-- Feature 3 -->
          <div class="text-center p-8 rounded-2xl bg-gray-50 dark:bg-gray-800 hover:shadow-lg transition-shadow duration-300">
            <div class="w-16 h-16 mx-auto mb-6 bg-gradient-to-br from-amber-400 to-orange-500 rounded-2xl flex items-center justify-center">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-3">Real Connections</h3>
            <p class="text-gray-600 dark:text-gray-400">
              Chat with your matches in real-time and build genuine relationships.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-20 bg-gradient-to-r from-primary-600 to-accent-600">
      <div class="max-w-4xl mx-auto px-4 text-center">
        <h2 class="text-3xl sm:text-4xl font-bold text-white mb-6">
          Ready to Find Your Match?
        </h2>
        <p class="text-xl text-white/90 mb-8">
          Join thousands of happy users who found their perfect partner on DriftDater.
        </p>
        <router-link 
          to="/register" 
          class="inline-block px-10 py-4 bg-white text-primary-600 font-semibold rounded-xl hover:bg-gray-100 transition-colors duration-300 shadow-lg"
        >
          Start Dating Today
        </router-link>
      </div>
    </section>
  </div>
</template>

<script setup>
</script>
