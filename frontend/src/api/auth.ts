import { apiClient } from "./client"
import type { AuthResponse } from "@/types/auth"

export const login = async (email: string, password: string) => {
    try{
        return await apiClient.post<AuthResponse>('/auth/login', { email, password })
    }catch(error){
        console.error('Login failed:', error)
        throw error
    }
}

