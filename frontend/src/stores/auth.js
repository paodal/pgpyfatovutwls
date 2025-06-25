import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'
import router from '../router'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token'))

  const isAuthenticated = computed(() => !!token.value)

  const setAuthData = (authData) => {
    user.value = authData.user
    token.value = authData.access_token
    localStorage.setItem('token', authData.access_token)
    
    // Set axios default header
    axios.defaults.headers.common['Authorization'] = `Bearer ${authData.access_token}`
  }

  const clearAuthData = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
    delete axios.defaults.headers.common['Authorization']
  }

  const login = async (credentials) => {
    try {
      const formData = new FormData()
      formData.append('username', credentials.email)
      formData.append('password', credentials.password)
      
      const response = await axios.post('/v1/auth/token', formData)
      
      setAuthData(response.data)
      router.push('/dashboard')
      
      return { success: true }
    } catch (error) {
      const message = error.response?.data?.detail || 'Login failed'
      return { success: false, error: message }
    }
  }

  const register = async (userData) => {
    try {
      const response = await axios.post('/v1/auth/register', userData)
      
      // Auto-login after registration
      const loginResult = await login({
        email: userData.email,
        password: userData.password
      })
      
      return loginResult
    } catch (error) {
      const message = error.response?.data?.detail || 'Registration failed'
      return { success: false, error: message }
    }
  }

  const logout = () => {
    clearAuthData()
    router.push('/')
  }

  const checkAuthStatus = async () => {
    if (!token.value) return

    try {
      // Set axios header
      axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
      
      const response = await axios.get('/v1/auth/me')
      user.value = response.data
    } catch (error) {
      // Token is invalid, clear auth data
      clearAuthData()
    }
  }

  const updateProfile = async (profileData) => {
    try {
      const response = await axios.put('/v1/auth/me', profileData)
      user.value = response.data
      return { success: true }
    } catch (error) {
      const message = error.response?.data?.detail || 'Profile update failed'
      return { success: false, error: message }
    }
  }

  return {
    user,
    token,
    isAuthenticated,
    login,
    register,
    logout,
    checkAuthStatus,
    updateProfile
  }
})