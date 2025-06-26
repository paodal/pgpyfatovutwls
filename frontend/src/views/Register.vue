<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Simple Header -->
    <header class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-4">
          <div class="flex items-center">
            <router-link to="/" class="text-xl font-bold text-primary-600">pgpyfatovutwls</router-link>
          </div>
          
          <div class="flex items-center space-x-4">
            <LanguageSelector />
            <router-link to="/login" class="btn btn-secondary">
              {{ $t('auth.login') }}
            </router-link>
          </div>
        </div>
      </div>
    </header>

    <div class="flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          {{ $t('auth.register_title') }}
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          {{ $t('auth.have_account') }}
          <router-link to="/login" class="font-medium text-primary-600 hover:text-primary-500">
            {{ $t('auth.login_link') }}
          </router-link>
        </p>
      </div>
      
      <form class="mt-8 space-y-6" @submit.prevent="handleRegister">
        <div v-if="error" class="rounded-md bg-red-50 p-4">
          <div class="text-sm text-red-700">{{ error }}</div>
        </div>
        
        <div class="space-y-4">
          <div>
            <label for="full_name" class="sr-only">{{ $t('auth.full_name') }}</label>
            <input
              id="full_name"
              v-model="form.full_name"
              name="full_name"
              type="text"
              required
              class="input"
              :placeholder="$t('auth.full_name')"
            />
          </div>
          
          <div>
            <label for="email" class="sr-only">{{ $t('auth.email') }}</label>
            <input
              id="email"
              v-model="form.email"
              name="email"
              type="email"
              required
              class="input"
              :placeholder="$t('auth.email')"
            />
          </div>
          
          <div>
            <label for="password" class="sr-only">{{ $t('auth.password') }}</label>
            <input
              id="password"
              v-model="form.password"
              name="password"
              type="password"
              required
              minlength="6"
              class="input"
              :placeholder="$t('auth.password')"
            />
          </div>
          
          <div>
            <label for="language" class="block text-sm font-medium text-gray-700">
              {{ $t('auth.language') }}
            </label>
            <select
              id="language"
              v-model="form.language"
              name="language"
              class="input mt-1"
            >
              <option value="it">🇮🇹 Italiano</option>
              <option value="en">🇺🇸 English</option>
              <option value="es">🇪🇸 Español</option>
            </select>
          </div>
        </div>

        <div>
          <button
            type="submit"
            :disabled="loading"
            class="group relative w-full btn btn-primary disabled:opacity-50"
          >
            <span v-if="loading">{{ $t('common.loading') }}...</span>
            <span v-else>{{ $t('auth.register') }}</span>
          </button>
        </div>
      </form>
    </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useI18n } from 'vue-i18n'
import LanguageSelector from '../components/LanguageSelector.vue'

const authStore = useAuthStore()
const { locale } = useI18n()

const form = reactive({
  full_name: '',
  email: '',
  password: '',
  language: locale.value
})

const loading = ref(false)
const error = ref('')

const handleRegister = async () => {
  loading.value = true
  error.value = ''
  
  const result = await authStore.register(form)
  
  if (!result.success) {
    error.value = result.error
  }
  
  loading.value = false
}
</script>