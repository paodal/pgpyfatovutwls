<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-6">
          <div class="flex items-center">
            <h1 class="text-2xl font-bold text-gray-900">{{ $t('dashboard.title') }}</h1>
          </div>
          <div class="flex items-center space-x-4">
            <LanguageSelector />
            <div class="relative">
              <button @click="showUserMenu = !showUserMenu" class="flex items-center space-x-2 text-gray-700 hover:text-gray-900">
                <span>{{ user?.full_name || user?.email }}</span>
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                </svg>
              </button>
              
              <div v-if="showUserMenu" class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-50">
                <button @click="logout" class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                  {{ $t('auth.logout') }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Profile Card -->
        <div class="lg:col-span-1">
          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
                {{ $t('dashboard.profile.title') }}
              </h3>
              
              <div class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700">{{ $t('auth.fullName') }}</label>
                  <p class="mt-1 text-sm text-gray-900">{{ user?.full_name }}</p>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700">{{ $t('auth.email') }}</label>
                  <p class="mt-1 text-sm text-gray-900">{{ user?.email }}</p>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700">{{ $t('auth.language') }}</label>
                  <p class="mt-1 text-sm text-gray-900">{{ user?.language === 'it' ? 'Italiano' : 'English' }}</p>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700">Status</label>
                  <span class="mt-1 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium" 
                        :class="user?.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'">
                    {{ user?.is_active ? $t('dashboard.profile.active') : $t('dashboard.profile.inactive') }}
                  </span>
                </div>
                
                <div v-if="user?.is_superuser">
                  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                    {{ $t('dashboard.profile.superuser') }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Subscription Card -->
        <div class="lg:col-span-2">
          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
                {{ $t('dashboard.subscription.title') }}
              </h3>
              
              <div v-if="subscriptionLoading" class="text-center py-4">
                <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              </div>
              
              <div v-else-if="currentSubscription" class="space-y-4">
                <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <div class="flex items-center justify-between">
                    <div>
                      <h4 class="text-lg font-medium text-blue-900">
                        {{ currentSubscription.plan?.name || 'Premium Plan' }}
                      </h4>
                      <p class="text-sm text-blue-700">
                        {{ $t('dashboard.subscription.status') }}: {{ currentSubscription.status }}
                      </p>
                    </div>
                    <div class="text-right">
                      <p class="text-2xl font-bold text-blue-900">
                        €{{ currentSubscription.plan?.price || '29' }}
                      </p>
                      <p class="text-sm text-blue-700">/{{ $t('home.pricing.month') }}</p>
                    </div>
                  </div>
                  
                  <div class="mt-4 flex space-x-2">
                    <button @click="cancelSubscription" 
                            :disabled="cancelling"
                            class="px-4 py-2 bg-red-600 text-white text-sm rounded-md hover:bg-red-700 disabled:opacity-50">
                      {{ cancelling ? $t('dashboard.subscription.cancelling') : $t('dashboard.subscription.cancel') }}
                    </button>
                  </div>
                </div>
              </div>
              
              <div v-else class="text-center py-8">
                <div class="mb-4">
                  <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                  </svg>
                </div>
                <h4 class="text-lg font-medium text-gray-900 mb-2">
                  {{ $t('dashboard.subscription.noSubscription') }}
                </h4>
                <p class="text-gray-600 mb-6">
                  {{ $t('dashboard.subscription.upgradeMessage') }}
                </p>
                
                <!-- Subscription Plans -->
                <div v-if="plans.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div v-for="plan in plans" :key="plan.id" 
                       class="border border-gray-200 rounded-lg p-4 hover:border-blue-500 transition-colors">
                    <h5 class="font-medium text-gray-900">{{ plan.name }}</h5>
                    <p class="text-2xl font-bold text-gray-900 mt-2">
                      €{{ plan.price }}<span class="text-sm text-gray-500">/{{ $t('home.pricing.month') }}</span>
                    </p>
                    <p class="text-sm text-gray-600 mt-2">{{ plan.description }}</p>
                    <button @click="subscribe(plan.id)" 
                            :disabled="subscribing"
                            class="mt-4 w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50">
                      {{ subscribing ? $t('dashboard.subscription.subscribing') : $t('dashboard.subscription.subscribe') }}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Quick Actions -->
      <div class="bg-white overflow-hidden shadow rounded-lg mt-6">
        <div class="px-4 py-5 sm:p-6">
          <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
            {{ $t('dashboard.quick_actions') }}
          </h3>
          
          <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <button class="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 text-left">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <svg class="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                </div>
                <div class="ml-3">
                  <p class="text-sm font-medium text-gray-900">
                    {{ $t('dashboard.actions.new_project') }}
                  </p>
                  <p class="text-sm text-gray-500">
                    {{ $t('dashboard.actions.new_project_desc') }}
                  </p>
                </div>
              </div>
            </button>
            
            <button class="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 text-left">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <svg class="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <div class="ml-3">
                  <p class="text-sm font-medium text-gray-900">
                    {{ $t('dashboard.actions.view_docs') }}
                  </p>
                  <p class="text-sm text-gray-500">
                    {{ $t('dashboard.actions.view_docs_desc') }}
                  </p>
                </div>
              </div>
            </button>
            
            <button class="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 text-left">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <svg class="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192L5.636 18.364M12 12h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div class="ml-3">
                  <p class="text-sm font-medium text-gray-900">
                    {{ $t('dashboard.actions.get_support') }}
                  </p>
                  <p class="text-sm text-gray-500">
                    {{ $t('dashboard.actions.get_support_desc') }}
                  </p>
                </div>
              </div>
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useSubscriptionStore } from '../stores/subscription'
import LanguageSelector from '../components/LanguageSelector.vue'

const authStore = useAuthStore()
const subscriptionStore = useSubscriptionStore()

const showUserMenu = ref(false)
const subscriptionLoading = ref(false)
const subscribing = ref(false)
const cancelling = ref(false)

const user = computed(() => authStore.user)
const currentSubscription = computed(() => subscriptionStore.currentSubscription)
const plans = computed(() => subscriptionStore.plans)

onMounted(async () => {
  await authStore.checkAuthStatus()
  
  subscriptionLoading.value = true
  await Promise.all([
    subscriptionStore.fetchCurrentSubscription(),
    subscriptionStore.fetchPlans()
  ])
  subscriptionLoading.value = false
})

const logout = () => {
  authStore.logout()
  showUserMenu.value = false
}

const subscribe = async (planId) => {
  subscribing.value = true
  try {
    await subscriptionStore.createCheckout(planId)
  } catch (error) {
    console.error('Subscription failed:', error)
  } finally {
    subscribing.value = false
  }
}

const cancelSubscription = async () => {
  if (!currentSubscription.value?.id) return
  
  cancelling.value = true
  try {
    const result = await subscriptionStore.cancelSubscription(currentSubscription.value.id)
    if (result.success) {
      // Subscription cancelled successfully
    }
  } catch (error) {
    console.error('Cancellation failed:', error)
  } finally {
    cancelling.value = false
  }
}

// Close user menu when clicking outside
document.addEventListener('click', (e) => {
  if (!e.target.closest('.relative')) {
    showUserMenu.value = false
  }
})
</script>