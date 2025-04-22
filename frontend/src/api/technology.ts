import { apiClient } from './client'
import type { ProjectCreateDto, TechnologyRead } from '@/types'

export const getTechnologiesFromApi = async () => {
  return await apiClient.get<TechnologyRead[]>('/technologies', { withCredentials: true })
}

export const createTechnology = async (technology: ProjectCreateDto) => {
  return await apiClient.post<TechnologyRead>('/technologies', technology, {
    withCredentials: true,
  })
}
