export interface ErrorDetail {
    message: string
    code: number
    params?: Record<string, any> | null
}