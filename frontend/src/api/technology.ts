import { apiClient } from './client'
import type { TechnologyCreateDto, TechnologyRead, TechnologyUpdateDto } from '@/types'

const BASE_URL = '/technologies'

export const getTechnologiesFromApi = async () =>
  await apiClient.get<TechnologyRead[]>(BASE_URL, { withCredentials: true })

export const createTechnology = async (technology: TechnologyCreateDto) =>
  await apiClient.post<TechnologyRead>(BASE_URL, technology, {
    withCredentials: true,
  })

export const updateTechnology = async (tech: TechnologyUpdateDto) =>
  await apiClient.patch<TechnologyRead>(`${BASE_URL}/${tech.id}`, tech, {
    withCredentials: true,
  })

export const deleteTechnology = async (techId: string) =>
  await apiClient.delete(`${BASE_URL}/${techId}`, {
    withCredentials: true,
  })
