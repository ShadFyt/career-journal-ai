import type { ErrorDetail } from "@/types/errors"

export const useErrorStore = defineStore('error-store', () => {
    const activeError = ref<ErrorDetail | null>(null)

    const setActiveError = (error: ErrorDetail | Error | null = null) => {
        if (error instanceof Error) {
            activeError.value = {
                message: error.message,
                code: 500,
            }
            return
        }
        activeError.value = error
    }

    return {
        setActiveError,
        activeError,
    }
})
