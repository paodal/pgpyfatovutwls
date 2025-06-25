<template>
  <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
    <div class="px-4 py-6 sm:px-0">
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">
          {{ $t('subscription.title') }}
        </h1>
        <p class="mt-1 text-sm text-gray-500">
          {{ $t('subscription.subtitle') }}
        </p>
      </div>

      <!-- Current Subscription -->
      <div class="mb-8">
        <div class="card">
          <h3 class="text-lg font-medium text-gray-900 mb-4">
            {{ $t('subscription.current_plan') }}
          </h3>
          
          <div v-if="subscriptionStore.currentSubscription?.plan" class="flex items-center justify-between">
            <div>
              <h4 class="text-xl font-semibold text-gray-900">
                {{ subscriptionStore.currentSubscription.plan.name }}
              </h4>
              <p class="text-sm text-gray-500">
                €{{ subscriptionStore.currentSubscription.plan.price }}/{{ $t('subscription.month') }}
              </p>
              <div class="mt-2">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                      :class="subscriptionStore.currentSubscription.status === 'active' 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-gray-100 text-gray-800'">
                  {{ $t(`subscription.status.${subscriptionStore.currentSubscription.status}`) }}
                </span>
              </div>
            </div>
            
            <div v-if="subscriptionStore.currentSubscription.status === 'active' && 
                      subscriptionStore.currentSubscription.subscription?.id" 
                 class="flex space-x-3">
              <button
                @click="cancelSubscription"
                :disabled="cancelling"
                class="btn btn-danger disabled:opacity-50"
              >
                <span v-if="cancelling">{{ $t('common.loading') }}...</span>
                <span v-else>{{ $t('subscription.cancel') }}</span>
              </button>
            </div>
          </div>
          
          <div v-else class="text-center py-8">
            <p class="text-gray-500">{{ $t('subscription.no_active_plan') }}</p>
          </div>
        </div>
      </div>

      <!-- Available Plans -->
      <div class="mb-8">
        <h3 class="text-lg font-medium text-gray-900 mb-4">
          {{ $t('subscription.available_plans') }}
        </h3>
        
        <div v-if="subscriptionStore.loading" class="text-center py-8">
          <p class="text-gray-500">{{ $t('common.loading') }}...</p>
        </div>
        
        <div v-else class="grid grid-cols-1 gap-6 lg:grid-cols-2">
          <div
            v-for="plan in subscriptionStore.plans"
            :key="plan.id"
            class="card border-2"
            :class="plan.plan_type === 'premium' ? 'border-primary-200 bg-primary-50' : 'border-gray-200'"
          >
            <div class="flex items-center justify-between mb-4">
              <h4 class="text-xl font-semibold text-gray-900">{{ plan.name }}</h4>
              <div v-if="plan.plan_type === 'premium'" class="bg-primary-600 text-white px-2 py-1 rounded text-sm">
                {{ $t('subscription.popular') }}
              </div>
            </div>
            
            <div class="mb-4">
              <span class="text-3xl font-bold text-gray-900">€{{ plan.price }}</span>
              <span class="text-gray-500">/{{ $t('subscription.month') }}</span>
            </div>
            
            <ul class="space-y-2 mb-6">
              <li class="flex items-center">
                <svg class="h-5 w-5 text-green-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                <span class="text-sm text-gray-600">
                  {{ $t('subscription.features.projects', { count: plan.max_projects }) }}
                </span>
              </li>
              <li class="flex items-center">
                <svg class="h-5 w-5 text-green-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                <span class="text-sm text-gray-600">
                  {{ $t('subscription.features.storage', { gb: plan.max_storage_gb }) }}
                </span>
              </li>
              <li v-if="plan.has_priority_support" class="flex items-center">
                <svg class="h-5 w-5 text-green-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                <span class="text-sm text-gray-600">
                  {{ $t('subscription.features.priority_support') }}
                </span>
              </li>
              <li v-if="plan.has_advanced_features" class="flex items-center">
                <svg class="h-5 w-5 text-green-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                <span class="text-sm text-gray-600">
                  {{ $t('subscription.features.advanced_features') }}
                </span>
              </li>
            </ul>
            
            <button
              v-if="plan.plan_type !== 'free'"
              @click="upgradeToplan(plan)"
              :disabled="subscribing || isCurrentPlan(plan)"
              class="w-full btn"
              :class="plan.plan_type === 'premium' ? 'btn-primary' : 'btn-secondary'"
            >
              <span v-if="subscribing">{{ $t('common.loading') }}...</span>
              <span v-else-if="isCurrentPlan(plan)">{{ $t('subscription.current_plan') }}</span>
              <span v-else>{{ $t('subscription.upgrade') }}</span>
            </button>
            
            <div v-else class="w-full text-center py-2 text-gray-500">
              {{ $t('subscription.free_plan') }}
            </div>
          </div>
        </div>
      </div>

      <!-- Billing Information -->
      <div v-if="subscriptionStore.currentSubscription?.subscription" class="card">
        <h3 class="text-lg font-medium text-gray-900 mb-4">
          {{ $t('subscription.billing_info') }}
        </h3>
        
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div>
            <dt class="text-sm font-medium text-gray-500">
              {{ $t('subscription.next_billing') }}
            </dt>
            <dd class="mt-1 text-sm text-gray-900">
              {{ formatDate(subscriptionStore.currentSubscription.subscription.billing_period_ends_at) }}
            </dd>
          </div>
          
          <div>
            <dt class="text-sm font-medium text-gray-500">
              {{ $t('subscription.billing_period') }}
            </dt>
            <dd class="mt-1 text-sm text-gray-900">
              {{ formatDate(subscriptionStore.currentSubscription.subscription.billing_period_starts_at) }} - 
              {{ formatDate(subscriptionStore.currentSubscription.subscription.billing_period_ends_at) }}
            </dd>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useSubscriptionStore } from '../stores/subscription'

const subscriptionStore = useSubscriptionStore()
const subscribing = ref(false)
const cancelling = ref(false)

onMounted(() => {
  subscriptionStore.fetchPlans()
  subscriptionStore.fetchCurrentSubscription()
})

const upgradeToplan = async (plan) => {
  subscribing.value = true
  
  const result = await subscriptionStore.createCheckout(plan.id)
  
  if (!result.success) {
    alert(result.error)
  }
  
  subscribing.value = false
}

const cancelSubscription = async () => {
  if (!confirm($t('subscription.cancel_confirm'))) {
    return
  }
  
  cancelling.value = true
  
  const result = await subscriptionStore.cancelSubscription(
    subscriptionStore.currentSubscription.subscription.id
  )
  
  if (!result.success) {
    alert(result.error)
  }
  
  cancelling.value = false
}

const isCurrentPlan = (plan) => {
  return subscriptionStore.currentSubscription?.plan?.id === plan.id &&
         subscriptionStore.currentSubscription?.status === 'active'
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString()
}
</script>