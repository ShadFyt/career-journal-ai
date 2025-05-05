import { apiClient } from './client'
import type { TechnologyCreateDto, TechnologyRead, TechnologyUpdateDto } from '@/types'

const BASE_URL = '/technologies'

export const getTechnologiesFromApi = async () => {
  return await apiClient.get<TechnologyRead[]>(BASE_URL, { withCredentials: true })
}

export const createTechnology = async (technology: TechnologyCreateDto) => {
  return await apiClient.post<TechnologyRead>(BASE_URL, technology, {
    withCredentials: true,
  })
}

export const updateTechnology = async (tech: TechnologyUpdateDto) => {
  return await apiClient.patch<TechnologyRead>(`${BASE_URL}/${tech.id}`, tech, {
    withCredentials: true,
  })
}
