<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-6">
          <div class="flex items-center">
            <h1 class="text-2xl font-bold text-gray-900">{{ $t('admin.plans.title') }}</h1>
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
                <router-link to="/dashboard" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                  {{ $t('navigation.dashboard') }}
                </router-link>
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
      <!-- Create New Plan Button -->
      <div class="mb-6">
        <button @click="showCreateModal = true" class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700">
          {{ $t('admin.plans.createNew') }}
        </button>
      </div>

      <!-- Plans List -->
      <div class="bg-white shadow overflow-hidden sm:rounded-md">
        <div v-if="loading" class="text-center py-8">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>

        <ul v-else class="divide-y divide-gray-200">
          <li v-for="plan in plans" :key="plan.id" class="px-6 py-4">
            <div class="flex items-center justify-between">
              <div class="flex-1">
                <div class="flex items-center justify-between">
                  <div>
                    <h3 class="text-lg font-medium text-gray-900">{{ plan.name }}</h3>
                    <p class="text-sm text-gray-500">{{ plan.plan_type.toUpperCase() }}</p>
                  </div>
                  <div class="text-right">
                    <p class="text-lg font-bold text-gray-900">
                      €{{ plan.price }}<span class="text-sm text-gray-500">/{{ $t('home.pricing.month') }}</span>
                    </p>
                    <p class="text-sm" :class="plan.is_active ? 'text-green-600' : 'text-red-600'">
                      {{ plan.is_active ? $t('admin.plans.active') : $t('admin.plans.inactive') }}
                    </p>
                  </div>
                </div>
                
                <div class="mt-2 grid grid-cols-2 md:grid-cols-4 gap-4 text-sm text-gray-600">
                  <div>
                    <span class="font-medium">{{ $t('admin.plans.projects') }}:</span> {{ plan.max_projects }}
                  </div>
                  <div>
                    <span class="font-medium">{{ $t('admin.plans.storage') }}:</span> {{ plan.max_storage_gb }}GB
                  </div>
                  <div>
                    <span class="font-medium">{{ $t('admin.plans.support') }}:</span> 
                    {{ plan.has_priority_support ? $t('admin.plans.yes') : $t('admin.plans.no') }}
                  </div>
                  <div>
                    <span class="font-medium">{{ $t('admin.plans.advanced') }}:</span> 
                    {{ plan.has_advanced_features ? $t('admin.plans.yes') : $t('admin.plans.no') }}
                  </div>
                </div>

                <div v-if="plan.lemon_squeezy_variant_id" class="mt-2 text-xs text-gray-500">
                  Lemon Squeezy Variant ID: {{ plan.lemon_squeezy_variant_id }}
                </div>
              </div>
              
              <div class="ml-6 flex space-x-2">
                <button @click="editPlan(plan)" class="text-blue-600 hover:text-blue-800">
                  {{ $t('admin.plans.edit') }}
                </button>
                <button @click="togglePlanStatus(plan)" 
                        :class="plan.is_active ? 'text-red-600 hover:text-red-800' : 'text-green-600 hover:text-green-800'">
                  {{ plan.is_active ? $t('admin.plans.deactivate') : $t('admin.plans.activate') }}
                </button>
              </div>
            </div>
          </li>
        </ul>
      </div>

      <!-- Create/Edit Plan Modal -->
      <div v-if="showCreateModal || showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-white rounded-lg p-8 max-w-2xl w-full mx-4 max-h-screen overflow-y-auto">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold">
              {{ showCreateModal ? $t('admin.plans.createNew') : $t('admin.plans.editPlan') }}
            </h2>
            <button @click="closeModal" class="text-gray-500 hover:text-gray-700">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>

          <form @submit.prevent="savePlan" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  {{ $t('admin.plans.name') }}
                </label>
                <input
                  v-model="planForm.name"
                  type="text"
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  {{ $t('admin.plans.type') }}
                </label>
                <select
                  v-model="planForm.plan_type"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="free">Free</option>
                  <option value="premium">Premium</option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  {{ $t('admin.plans.price') }} (€)
                </label>
                <input
                  v-model.number="planForm.price"
                  type="number"
                  step="0.01"
                  min="0"
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  {{ $t('admin.plans.billingDays') }}
                </label>
                <input
                  v-model.number="planForm.billing_period_days"
                  type="number"
                  min="1"
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  {{ $t('admin.plans.maxProjects') }}
                </label>
                <input
                  v-model.number="planForm.max_projects"
                  type="number"
                  min="1"
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  {{ $t('admin.plans.maxStorage') }} (GB)
                </label>
                <input
                  v-model.number="planForm.max_storage_gb"
                  type="number"
                  min="1"
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Lemon Squeezy Product ID
                </label>
                <input
                  v-model="planForm.lemon_squeezy_product_id"
                  type="text"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Optional"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Lemon Squeezy Variant ID
                </label>
                <input
                  v-model="planForm.lemon_squeezy_variant_id"
                  type="text"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Optional"
                />
              </div>
            </div>

            <div class="flex items-center space-x-6">
              <label class="flex items-center">
                <input
                  v-model="planForm.has_priority_support"
                  type="checkbox"
                  class="mr-2"
                />
                {{ $t('admin.plans.prioritySupport') }}
              </label>

              <label class="flex items-center">
                <input
                  v-model="planForm.has_advanced_features"
                  type="checkbox"
                  class="mr-2"
                />
                {{ $t('admin.plans.advancedFeatures') }}
              </label>

              <label class="flex items-center">
                <input
                  v-model="planForm.is_active"
                  type="checkbox"
                  class="mr-2"
                />
                {{ $t('admin.plans.active') }}
              </label>
            </div>

            <div v-if="error" class="text-red-600 text-sm">
              {{ error }}
            </div>

            <div class="flex justify-end space-x-4">
              <button
                type="button"
                @click="closeModal"
                class="px-4 py-2 text-gray-700 border border-gray-300 rounded-md hover:bg-gray-50"
              >
                {{ $t('admin.plans.cancel') }}
              </button>
              <button
                type="submit"
                :disabled="saving"
                class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
              >
                {{ saving ? $t('admin.plans.saving') : $t('admin.plans.save') }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useSubscriptionStore } from '../stores/subscription'
import LanguageSelector from '../components/LanguageSelector.vue'

const router = useRouter()
const authStore = useAuthStore()
const subscriptionStore = useSubscriptionStore()

const showUserMenu = ref(false)
const loading = ref(false)
const saving = ref(false)
const showCreateModal = ref(false)
const showEditModal = ref(false)
const error = ref('')

const user = computed(() => authStore.user)
const plans = computed(() => subscriptionStore.plans)

const planForm = ref({
  id: null,
  name: '',
  plan_type: 'free',
  price: 0,
  billing_period_days: 30,
  max_projects: 1,
  max_storage_gb: 1,
  has_priority_support: false,
  has_advanced_features: false,
  lemon_squeezy_product_id: '',
  lemon_squeezy_variant_id: '',
  is_active: true
})

onMounted(async () => {
  await authStore.checkAuthStatus()
  
  // Redirect if not superuser
  if (!user.value?.is_superuser) {
    router.push('/dashboard')
    return
  }
  
  loading.value = true
  await subscriptionStore.fetchPlans()
  loading.value = false
})

const logout = () => {
  authStore.logout()
  showUserMenu.value = false
}

const editPlan = (plan) => {
  planForm.value = {
    id: plan.id,
    name: plan.name,
    plan_type: plan.plan_type,
    price: plan.price,
    billing_period_days: plan.billing_period_days,
    max_projects: plan.max_projects,
    max_storage_gb: plan.max_storage_gb,
    has_priority_support: plan.has_priority_support,
    has_advanced_features: plan.has_advanced_features,
    lemon_squeezy_product_id: plan.lemon_squeezy_product_id || '',
    lemon_squeezy_variant_id: plan.lemon_squeezy_variant_id || '',
    is_active: plan.is_active
  }
  showEditModal.value = true
}

const closeModal = () => {
  showCreateModal.value = false
  showEditModal.value = false
  error.value = ''
  planForm.value = {
    id: null,
    name: '',
    plan_type: 'free',
    price: 0,
    billing_period_days: 30,
    max_projects: 1,
    max_storage_gb: 1,
    has_priority_support: false,
    has_advanced_features: false,
    lemon_squeezy_product_id: '',
    lemon_squeezy_variant_id: '',
    is_active: true
  }
}

const savePlan = async () => {
  saving.value = true
  error.value = ''

  try {
    // This would call the admin API to create/update plans
    // For now, just close the modal
    console.log('Saving plan:', planForm.value)
    closeModal()
    await subscriptionStore.fetchPlans()
  } catch (err) {
    error.value = 'Failed to save plan'
  } finally {
    saving.value = false
  }
}

const togglePlanStatus = async (plan) => {
  try {
    // This would call the admin API to toggle plan status
    console.log('Toggling plan status:', plan.id)
    await subscriptionStore.fetchPlans()
  } catch (err) {
    console.error('Failed to toggle plan status:', err)
  }
}
</script>