export const useAuthStore = defineStore('auth-store', () => {
    const isAuthenticated = ref(false)
    const accessToken = ref<string | null>(null)

    const setIsAuthenticated = (value: boolean) => {
        isAuthenticated.value = value
    }

    return {
        isAuthenticated,
        setIsAuthenticated,
        accessToken,
    }
})