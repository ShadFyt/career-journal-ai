import { getUserSession, login } from '@/api/auth'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth-store', () => {
  const router = useRouter()

  const isAuthenticated = ref(false)

  const setIsAuthenticated = (value: boolean) => {
    isAuthenticated.value = value
  }

  const handleLogin = async ({ email, password }: { email: string; password: string }) => {
    try {
      const { email: userEmail, userId } = await login(email, password)
      setIsAuthenticated(true)
    } catch (error) {
      throw error
    }
  }

  const checkSession = async () => {
    try {
      await getUserSession()
      setIsAuthenticated(true)
      if (router.currentRoute.value.path === '/login') {
        router.push({ path: '/' })
      }
      return true
    } catch (error) {
      console.error('Session check failed:', error)
      setIsAuthenticated(false)
      router.push({ path: '/login' })
      return false
    }
  }

  return {
    isAuthenticated,
    setIsAuthenticated,
    handleLogin,
    checkSession,
  }
})
