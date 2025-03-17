import { getUserSession, login } from '@/api/auth'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth-store', () => {
  const router = useRouter()

  const isLoading = ref(true)
  const isAuthenticated = ref(false)

  const setIsAuthenticated = (value: boolean) => {
    isAuthenticated.value = value
  }

  const handleLogin = async ({
    email,
    password,
    rememberMe = false,
  }: {
    email: string
    password: string
    rememberMe: boolean
  }) => {
    try {
      const { email: userEmail, userId } = await login(email, password, rememberMe)
      setIsAuthenticated(true)
    } catch (error) {
      throw error
    }
  }

  const checkSession = async () => {
    try {
      await getUserSession()
      if (router.currentRoute.value.path === '/login') {
        await router.push({ path: '/' })
      }
      setIsAuthenticated(true)

      return true
    } catch (error) {
      console.error('Session check failed:', error)
      await router.push({ path: '/login' })
      setIsAuthenticated(false)

      return false
    } finally {
      isLoading.value = false
    }
  }

  return {
    isAuthenticated,
    setIsAuthenticated,
    handleLogin,
    checkSession,
    isLoading,
  }
})
