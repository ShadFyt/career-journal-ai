import { useToast } from '@/components/ui/toast'
import { getProjectsFromApi } from '@/api'
import { useQuery } from '@tanstack/vue-query'

export const queryKeys = {
  projects: {
    all: ['projects'] as const,
    detail: (id: string) => [...queryKeys.projects.all, id] as const,
    list: () => [...queryKeys.projects.all, 'list'] as const,
  },
}

export const useProjectService = () => {
  const { toast } = useToast()

  const getProjects = async () => {
    try {
      return await getProjectsFromApi()
    } catch (error: unknown) {
      console.error('getProjects', error)
      toast({
        title: 'Something went wrong while fetching projects',
        description: 'Please try again later.',
      })
    }
  }

  const {
    data: projects,
    isLoading,
    isFetched,
  } = useQuery({
    queryKey: queryKeys.projects.list(),
    queryFn: getProjects,
  })

  return {
    getProjects,
    projects: projects.value ?? [],
    isLoading,
    isFetched,
  }
}
