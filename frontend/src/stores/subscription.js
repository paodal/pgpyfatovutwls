import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useSubscriptionStore = defineStore('subscription', () => {
  const plans = ref([])
  const currentSubscription = ref(null)
  const loading = ref(false)

  const fetchPlans = async () => {
    try {
      loading.value = true
      const response = await axios.get('/api/v1/subscriptions/plans')
      plans.value = response.data
    } catch (error) {
      console.error('Failed to fetch subscription plans:', error)
    } finally {
      loading.value = false
    }
  }

  const fetchCurrentSubscription = async () => {
    try {
      loading.value = true
      const response = await axios.get('/api/v1/subscriptions/current')
      currentSubscription.value = response.data
    } catch (error) {
      console.error('Failed to fetch current subscription:', error)
    } finally {
      loading.value = false
    }
  }

  const createCheckout = async (planId) => {
    try {
      const response = await axios.post(`/api/v1/subscriptions/checkout/${planId}`)
      
      // Redirect to Lemon Squeezy checkout
      window.location.href = response.data.checkout_url
      
      return { success: true }
    } catch (error) {
      const message = error.response?.data?.detail || 'Checkout creation failed'
      return { success: false, error: message }
    }
  }

  const cancelSubscription = async (subscriptionId) => {
    try {
      await axios.post(`/api/v1/subscriptions/cancel/${subscriptionId}`)
      
      // Refresh current subscription
      await fetchCurrentSubscription()
      
      return { success: true }
    } catch (error) {
      const message = error.response?.data?.detail || 'Subscription cancellation failed'
      return { success: false, error: message }
    }
  }

  const isPremium = () => {
    return currentSubscription.value?.plan?.plan_type === 'premium' && 
           currentSubscription.value?.status === 'active'
  }

  return {
    plans,
    currentSubscription,
    loading,
    fetchPlans,
    fetchCurrentSubscription,
    createCheckout,
    cancelSubscription,
    isPremium
  }
})