export interface ErrorDetail {
    message: string
    code: number,
    description?: string,
    stack?: string,
    params?: Record<string, any> | null
}