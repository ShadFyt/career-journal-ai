import { getUserSession, login, logoutCurrentUser, refreshToken } from '@/api/auth'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth-store', () => {
  const router = useRouter()

  const isLoading = ref(true)
  const isAuthenticated = ref(false)
  const profile = ref<{ email: string; userId: string }>({
    email: '',
    userId: '',
  })
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
      profile.value = { email: userEmail, userId }
    } catch (error) {
      throw error
    }
  }

  const handleLogout = async () => {
    try {
      await logoutCurrentUser()
      setIsAuthenticated(false)
      profile.value = { email: '', userId: '' }
      await router.push({ path: '/login' })
    } catch (error) {
      console.error('Logout failed:', error)
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
      const { email, userId } = await getUserSession()
      profile.value = { email, userId }
      return true
    } catch (error) {
      console.error('Session check failed:', error)
      await router.push({ path: '/login' })
      setIsAuthenticated(false)
      profile.value = { email: '', userId: '' }

      return false
    } finally {
      isLoading.value = false
    }
  }

  const handleRefreshToken = async () => {
    try {
      const { email, userId } = await refreshToken()
      profile.value = { email, userId }
    } catch (error) {
      console.error('Refresh token failed:', error)
      await handleLogout()
    }
  }

  return {
    isAuthenticated,
    setIsAuthenticated,
    handleLogin,
    handleLogout,
    handleRefreshToken,
    checkSession,
    isLoading,
    profile,
  }
})
