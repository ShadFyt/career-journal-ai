export const useErrorStore = defineStore('error-store', () => {
    const isErrorActive = ref(false)

    const setActiveError = () => {
        isErrorActive.value = true
    }

    return {
        setActiveError,
        isErrorActive
    }
})