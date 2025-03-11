export interface AuthResponse {
    accessToken: string
    refreshToken: string | null
    email: string
    userId: string
}