import { apiClient } from './client'
import type { AuthResponse } from '@/types/auth'

export const login = async (email: string, password: string, rememberMe: boolean) => {
  try {
    return await apiClient.post<AuthResponse>(
      '/auth/login',
      { email, password, rememberMe },
      {
        withCredentials: true,
      },
    )
  } catch (error) {
    console.error('Login failed:', error)
    throw error
  }
}

export const getUserSession = async () => {
  try {
    return await apiClient.get<AuthResponse>('/auth/session', {
      withCredentials: true,
    })
  } catch (error) {
    console.error('Failed to get user session:', error)
    throw error
  }
}

export const logoutCurrentUser = async () => {
  try {
    await apiClient.post('/auth/logout', {}, {
      withCredentials: true,
    })
  } catch (error) {
    console.error('Logout failed:', error)
    throw error
  }
}
