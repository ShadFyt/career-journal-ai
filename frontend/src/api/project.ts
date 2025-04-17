import { apiClient } from './client'
import type { Project, ProjectCreateDto } from '@/types'

export const getProjectsFromApi = async () => {
  return await apiClient.get<Project[]>('/projects', { withCredentials: true })
}

export const createProject = async (project: ProjectCreateDto) => {
  return await apiClient.post<Project>('/projects', project, { withCredentials: true })
}
