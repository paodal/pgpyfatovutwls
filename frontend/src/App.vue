<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <router-link to="/" class="text-xl font-bold text-primary-600">
              pgpyfatovutwls
            </router-link>
          </div>
          
          <div class="flex items-center space-x-4">
            <LanguageSelector />
            
            <div v-if="authStore.isAuthenticated" class="flex items-center space-x-4">
              <router-link to="/dashboard" class="text-gray-700 hover:text-primary-600">
                {{ $t('nav.dashboard') }}
              </router-link>
              <router-link to="/subscription" class="text-gray-700 hover:text-primary-600">
                {{ $t('nav.subscription') }}
              </router-link>
              <button @click="logout" class="btn btn-secondary">
                {{ $t('auth.logout') }}
              </button>
            </div>
            
            <div v-else class="flex items-center space-x-2">
              <router-link to="/login" class="btn btn-secondary">
                {{ $t('auth.login') }}
              </router-link>
              <router-link to="/register" class="btn btn-primary">
                {{ $t('auth.register') }}
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </nav>
    
    <main>
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from './stores/auth'
import LanguageSelector from './components/LanguageSelector.vue'

const authStore = useAuthStore()

onMounted(() => {
  authStore.checkAuthStatus()
})

const logout = () => {
  authStore.logout()
}
</script>