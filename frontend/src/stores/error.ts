import type { ErrorDetail } from "@/types/errors"

export const useErrorStore = defineStore('error-store', () => {
    const activeError = ref<ErrorDetail | null>(null)

    const setActiveError = (error: ErrorDetail | null = null) => {
        activeError.value = error
    }

    return {
        setActiveError,
        activeError,
    }
})
