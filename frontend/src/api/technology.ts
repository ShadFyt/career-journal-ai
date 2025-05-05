import { apiClient } from './client'
import type { TechnologyCreateDto, TechnologyRead } from '@/types'

export const getTechnologiesFromApi = async () => {
  return await apiClient.get<TechnologyRead[]>('/technologies', { withCredentials: true })
}

export const createTechnology = async (technology: TechnologyCreateDto) => {
  return await apiClient.post<TechnologyRead>('/technologies', technology, {
    withCredentials: true,
  })
}
