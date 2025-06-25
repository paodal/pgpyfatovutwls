<template>
  <div class="bg-white">
    <!-- Hero Section -->
    <div class="relative isolate px-6 pt-14 lg:px-8">
      <div class="mx-auto max-w-2xl py-32 sm:py-48 lg:py-56">
        <div class="text-center">
          <h1 class="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
            {{ $t('home.hero.title') }}
          </h1>
          <p class="mt-6 text-lg leading-8 text-gray-600">
            {{ $t('home.hero.subtitle') }}
          </p>
          <div class="mt-10 flex items-center justify-center gap-x-6">
            <button @click="showRegisterModal = true" class="btn btn-primary text-lg px-8 py-3">
              {{ $t('home.hero.cta') }}
            </button>
            <button @click="showLoginModal = true" class="text-sm font-semibold leading-6 text-gray-900 hover:underline">
              {{ $t('auth.login') }} <span aria-hidden="true">→</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Features Section -->
    <div id="features" class="py-24 bg-gray-50">
      <div class="mx-auto max-w-7xl px-6 lg:px-8">
        <div class="mx-auto max-w-2xl text-center">
          <h2 class="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
            {{ $t('home.features.title') }}
          </h2>
          <p class="mt-6 text-lg leading-8 text-gray-600">
            {{ $t('home.features.subtitle') }}
          </p>
        </div>
        
        <div class="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-none">
          <dl class="grid max-w-xl grid-cols-1 gap-x-8 gap-y-16 lg:max-w-none lg:grid-cols-3">
            <div class="flex flex-col">
              <dt class="text-base font-semibold leading-7 text-gray-900">
                <div class="mb-6 flex h-10 w-10 items-center justify-center rounded-lg bg-primary-600">
                  <svg class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z" />
                  </svg>
                </div>
                {{ $t('home.features.feature1.title') }}
              </dt>
              <dd class="mt-1 flex flex-auto flex-col text-base leading-7 text-gray-600">
                <p class="flex-auto">{{ $t('home.features.feature1.description') }}</p>
              </dd>
            </div>
            
            <div class="flex flex-col">
              <dt class="text-base font-semibold leading-7 text-gray-900">
                <div class="mb-6 flex h-10 w-10 items-center justify-center rounded-lg bg-primary-600">
                  <svg class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z" />
                  </svg>
                </div>
                {{ $t('home.features.feature2.title') }}
              </dt>
              <dd class="mt-1 flex flex-auto flex-col text-base leading-7 text-gray-600">
                <p class="flex-auto">{{ $t('home.features.feature2.description') }}</p>
              </dd>
            </div>
            
            <div class="flex flex-col">
              <dt class="text-base font-semibold leading-7 text-gray-900">
                <div class="mb-6 flex h-10 w-10 items-center justify-center rounded-lg bg-primary-600">
                  <svg class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 18L9 11.25l4.306 4.307a11.95 11.95 0 015.814-5.519l2.74-1.22m0 0l-5.94-2.28m5.94 2.28l-2.28 5.941" />
                  </svg>
                </div>
                {{ $t('home.features.feature3.title') }}
              </dt>
              <dd class="mt-1 flex flex-auto flex-col text-base leading-7 text-gray-600">
                <p class="flex-auto">{{ $t('home.features.feature3.description') }}</p>
              </dd>
            </div>
          </dl>
        </div>
      </div>
    </div>

    <!-- Pricing Section -->
    <div class="py-24 bg-white">
      <div class="mx-auto max-w-7xl px-6 lg:px-8">
        <div class="mx-auto max-w-2xl text-center">
          <h2 class="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
            {{ $t('home.pricing.title') }}
          </h2>
          <p class="mt-6 text-lg leading-8 text-gray-600">
            {{ $t('home.pricing.subtitle') }}
          </p>
        </div>
        
        <div class="mx-auto mt-16 grid max-w-lg grid-cols-1 items-center gap-y-6 sm:mt-20 sm:gap-y-0 lg:max-w-4xl lg:grid-cols-2">
          <!-- Free Plan -->
          <div class="rounded-3xl rounded-t-3xl bg-white/60 p-8 ring-1 ring-gray-900/10 sm:p-10">
            <h3 class="text-base font-semibold leading-7 text-primary-600">{{ $t('home.pricing.free.name') }}</h3>
            <p class="mt-4 flex items-baseline gap-x-2">
              <span class="text-5xl font-bold tracking-tight text-gray-900">€0</span>
              <span class="text-base text-gray-500">/{{ $t('home.pricing.month') }}</span>
            </p>
            <p class="mt-6 text-base leading-7 text-gray-600">{{ $t('home.pricing.free.description') }}</p>
            <ul role="list" class="mt-8 space-y-3 text-sm leading-6 text-gray-600">
              <li class="flex gap-x-3">
                <svg class="h-6 w-5 flex-none text-primary-600" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd" />
                </svg>
                {{ $t('home.pricing.free.feature1') }}
              </li>
              <li class="flex gap-x-3">
                <svg class="h-6 w-5 flex-none text-primary-600" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd" />
                </svg>
                {{ $t('home.pricing.free.feature2') }}
              </li>
            </ul>
            <button @click="showRegisterModal = true" class="mt-8 block w-full btn btn-secondary text-center">
              {{ $t('home.pricing.free.cta') }}
            </button>
          </div>
          
          <!-- Premium Plan -->
          <div class="rounded-3xl bg-primary-600 p-8 ring-1 ring-gray-900/10 sm:p-10">
            <h3 class="text-base font-semibold leading-7 text-white">{{ $t('home.pricing.premium.name') }}</h3>
            <p class="mt-4 flex items-baseline gap-x-2">
              <span class="text-5xl font-bold tracking-tight text-white">€29</span>
              <span class="text-base text-white/70">/{{ $t('home.pricing.month') }}</span>
            </p>
            <p class="mt-6 text-base leading-7 text-white/70">{{ $t('home.pricing.premium.description') }}</p>
            <ul role="list" class="mt-8 space-y-3 text-sm leading-6 text-white/70">
              <li class="flex gap-x-3">
                <svg class="h-6 w-5 flex-none text-white" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd" />
                </svg>
                {{ $t('home.pricing.premium.feature1') }}
              </li>
              <li class="flex gap-x-3">
                <svg class="h-6 w-5 flex-none text-white" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd" />
                </svg>
                {{ $t('home.pricing.premium.feature2') }}
              </li>
              <li class="flex gap-x-3">
                <svg class="h-6 w-5 flex-none text-white" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd" />
                </svg>
                {{ $t('home.pricing.premium.feature3') }}
              </li>
            </ul>
            <button @click="showRegisterModal = true" class="mt-8 block w-full bg-white text-primary-600 hover:bg-gray-50 btn text-center">
              {{ $t('home.pricing.premium.cta') }}
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Login Modal -->
    <LoginModal 
      :is-open="showLoginModal" 
      @close="showLoginModal = false" 
      @switch-to-register="switchToRegister"
    />
    
    <!-- Register Modal -->
    <RegisterModal 
      :is-open="showRegisterModal" 
      @close="showRegisterModal = false" 
      @switch-to-login="switchToLogin"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import LoginModal from '../components/LoginModal.vue'
import RegisterModal from '../components/RegisterModal.vue'

const showLoginModal = ref(false)
const showRegisterModal = ref(false)

const switchToRegister = () => {
  showLoginModal.value = false
  showRegisterModal.value = true
}

const switchToLogin = () => {
  showRegisterModal.value = false
  showLoginModal.value = true
}
</script>