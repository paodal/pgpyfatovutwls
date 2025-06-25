<template>
  <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
    <div class="px-4 py-6 sm:px-0">
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">
          {{ $t('dashboard.welcome') }}, {{ authStore.user?.full_name }}!
        </h1>
        <p class="mt-1 text-sm text-gray-500">
          {{ $t('dashboard.subtitle') }}
        </p>
      </div>

      <!-- Subscription Status -->
      <div class="mb-8">
        <div class="card">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-lg font-medium text-gray-900">
                {{ $t('dashboard.subscription_status') }}
              </h3>
              <p class="mt-1 text-sm text-gray-500">
                <span v-if="subscriptionStore.currentSubscription?.plan">
                  {{ $t('dashboard.current_plan') }}: 
                  <span class="font-medium">{{ subscriptionStore.currentSubscription.plan.name }}</span>
                </span>
                <span v-else>{{ $t('dashboard.no_subscription') }}</span>
              </p>
            </div>
            <div>
              <router-link to="/subscription" class="btn btn-primary">
                {{ $t('dashboard.manage_subscription') }}
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Stats -->
      <div class="grid grid-cols-1 gap-5 sm:grid-cols-3 mb-8">
        <div class="card">
          <dt class="text-sm font-medium text-gray-500 truncate">
            {{ $t('dashboard.stats.projects') }}
          </dt>
          <dd class="mt-1 text-3xl font-semibold text-gray-900">
            0
          </dd>
        </div>
        
        <div class="card">
          <dt class="text-sm font-medium text-gray-500 truncate">
            {{ $t('dashboard.stats.storage_used') }}
          </dt>
          <dd class="mt-1 text-3xl font-semibold text-gray-900">
            0 GB
          </dd>
        </div>
        
        <div class="card">
          <dt class="text-sm font-medium text-gray-500 truncate">
            {{ $t('dashboard.stats.last_activity') }}
          </dt>
          <dd class="mt-1 text-3xl font-semibold text-gray-900">
            {{ $t('dashboard.stats.today') }}
          </dd>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="card">
        <h3 class="text-lg font-medium text-gray-900 mb-4">
          {{ $t('dashboard.quick_actions') }}
        </h3>
        
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <button class="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 text-left">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
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
                <svg class="h-6 w-6 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
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
                <svg class="h-6 w-6 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
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
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useSubscriptionStore } from '../stores/subscription'

const authStore = useAuthStore()
const subscriptionStore = useSubscriptionStore()

onMounted(() => {
  subscriptionStore.fetchCurrentSubscription()
})
</script>