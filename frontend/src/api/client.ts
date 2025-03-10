import axios from 'axios'
import type { AxiosError, AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios'
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8008'

const axiosInstance: AxiosInstance = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
})

// Helper function to get token from Pinia store
const getAccessToken = (): string | null => {
  const authStore = useAuthStore()
  const { accessToken } = storeToRefs(authStore)
  return accessToken.value
}

// Request interceptor for adding auth token
axiosInstance.interceptors.request.use(
  (config) => {
    const token = getAccessToken()
    
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor for handling common errors
axiosInstance.interceptors.response.use(
  (response: AxiosResponse) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean }
    
    // Handle 401 Unauthorized errors (token expired)
    if (error.response?.status === 401 && !originalRequest._retry) {
      // Could add refresh token logic here
      console.error('Unauthorized: Token expired')
      return Promise.reject(error)
    }
    
    // Handle other errors
    return Promise.reject(error)
  }
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