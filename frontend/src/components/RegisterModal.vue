<template>
  <div v-if="isOpen" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg p-8 max-w-md w-full mx-4">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold">{{ $t('auth.signUp') }}</h2>
        <button @click="close" class="text-gray-500 hover:text-gray-700">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>

      <form @submit.prevent="handleRegister" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            {{ $t('auth.fullName') }}
          </label>
          <input
            v-model="form.full_name"
            type="text"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :placeholder="$t('auth.fullNamePlaceholder')"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            {{ $t('auth.email') }}
          </label>
          <input
            v-model="form.email"
            type="email"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :placeholder="$t('auth.emailPlaceholder')"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            {{ $t('auth.password') }}
          </label>
          <input
            v-model="form.password"
            type="password"
            required
            minlength="6"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :placeholder="$t('auth.passwordPlaceholder')"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            {{ $t('auth.confirmPassword') }}
          </label>
          <input
            v-model="form.confirmPassword"
            type="password"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :placeholder="$t('auth.confirmPasswordPlaceholder')"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            {{ $t('auth.language') }}
          </label>
          <select
            v-model="form.language"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="it">Italiano</option>
            <option value="en">English</option>
          </select>
        </div>

        <div v-if="error" class="text-red-600 text-sm">
          {{ error }}
        </div>

        <button
          type="submit"
          :disabled="loading || !isPasswordValid"
          class="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="loading">{{ $t('auth.signingUp') }}</span>
          <span v-else>{{ $t('auth.signUp') }}</span>
        </button>
      </form>

      <div class="mt-6 text-center">
        <p class="text-sm text-gray-600">
          {{ $t('auth.hasAccount') }}
          <button @click="switchToLogin" class="text-blue-600 hover:underline">
            {{ $t('auth.login') }}
          </button>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useAuthStore } from '../stores/auth'

const emit = defineEmits(['close', 'switch-to-login'])

defineProps({
  isOpen: {
    type: Boolean,
    default: false
  }
})

const authStore = useAuthStore()
const loading = ref(false)
const error = ref('')

const form = reactive({
  full_name: '',
  email: '',
  password: '',
  confirmPassword: '',
  language: 'it'
})

const isPasswordValid = computed(() => {
  return form.password.length >= 6 && form.password === form.confirmPassword
})

const handleRegister = async () => {
  if (form.password !== form.confirmPassword) {
    error.value = 'Passwords do not match'
    return
  }

  loading.value = true
  error.value = ''

  try {
    const result = await authStore.register({
      email: form.email,
      full_name: form.full_name,
      password: form.password,
      language: form.language
    })
    
    if (result.success) {
      close()
    } else {
      error.value = result.error
    }
  } catch (err) {
    error.value = 'Registration failed'
  } finally {
    loading.value = false
  }
}

const close = () => {
  form.full_name = ''
  form.email = ''
  form.password = ''
  form.confirmPassword = ''
  form.language = 'it'
  error.value = ''
  emit('close')
}

const switchToLogin = () => {
  emit('switch-to-login')
}
</script>