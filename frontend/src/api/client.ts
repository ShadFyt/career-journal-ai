import type { AxiosError, AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const CSRF_TOKEN_COOKIE_NAME = 'csrf_access_token'
const CSRF_TOKEN_HEADER_NAME = 'X-CSRF-Token'

const axiosInstance: AxiosInstance = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
})

/**
 * Get CSRF token from cookies
 * Extracts csrf_access_token from cookies
 */
const getCsrfToken = (): string | null => {
  const cookies = document.cookie.split(';')
  for (const cookie of cookies) {
    const [name, value] = cookie.trim().split('=')
    if (name === CSRF_TOKEN_COOKIE_NAME) {
      return value
    }
  }
  return null
}

// Request interceptor for adding CSRF token
axiosInstance.interceptors.request.use(
  (config) => {
    const csrfToken = getCsrfToken()
    if (csrfToken) {
      config.headers[CSRF_TOKEN_HEADER_NAME] = csrfToken
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

// Response interceptor for handling common errors
axiosInstance.interceptors.response.use(
  (response: AxiosResponse) => response,
  async (error: AxiosError) => {
    const authStore = useAuthStore()
    const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean }

    // Handle 401 Unauthorized errors (token expired)
    if (error.response?.status === 401 && originalRequest.url !== '/auth/refresh-token') {
      if (originalRequest._retry) {
        await authStore.handleLogout()
        return Promise.reject(error)
      }
      originalRequest._retry = true
      await authStore.handleRefreshToken()
      return axiosInstance(originalRequest)
    }

    // Handle other errors
    await authStore.handleLogout()
    return Promise.reject(error)
  },
)

// Helper methods for common HTTP operations
export const apiClient = {
  get: <T>(url: string, config?: AxiosRequestConfig) =>
    axiosInstance.get<T>(url, config).then((response) => response.data),

  post: <T>(url: string, data?: any, config?: AxiosRequestConfig) =>
    axiosInstance.post<T>(url, data, config).then((response) => response.data),

  put: <T>(url: string, data?: any, config?: AxiosRequestConfig) =>
    axiosInstance.put<T>(url, data, config).then((response) => response.data),

  delete: <T>(url: string, config?: AxiosRequestConfig) =>
    axiosInstance.delete<T>(url, config).then((response) => response.data),

  patch: <T>(url: string, data?: any, config?: AxiosRequestConfig) =>
    axiosInstance.patch<T>(url, data, config).then((response) => response.data),
}

export default axiosInstance
