import { apiClient } from './client'
import type { Project } from '@/types'

export const getProjectsFromApi = async () => {
  return await apiClient.get<Project[]>('/projects', { withCredentials: true })
}
