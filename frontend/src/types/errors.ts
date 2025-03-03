export interface ErrorDetail {
    message: string
    code: string
    params?: Record<string, any> | null
}