import { login } from '@/api/auth'
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth-store', () => {
  const isAuthenticated = ref(false)
  const accessToken = ref<string | null>(null)

  const setIsAuthenticated = (value: boolean) => {
    isAuthenticated.value = value
  }

  const handleLogin = async ({ email, password }: { email: string; password: string }) => {
    try {
      const { accessToken: token } = await login(email, password)
      accessToken.value = token
      setIsAuthenticated(true)
    } catch (error) {
      throw error
    }
  }

  return {
    isAuthenticated,
    setIsAuthenticated,
    accessToken,
    handleLogin,
  }
})
