import { useToast } from '@/components/ui/toast'
import { createProject, getProjectsFromApi } from '@/api'
import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'

export const queryKeys = {
  projects: {
    all: ['projects'] as const,
    detail: (id: string) => [...queryKeys.projects.all, id] as const,
    list: () => [...queryKeys.projects.all, 'list'] as const,
  },
}

export const useProjectService = () => {
  const { toast } = useToast()
  const queryClient = useQueryClient()

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

  const mutation = useMutation({
    mutationFn: createProject,
    onSuccess: () => {
      // Invalidate and refetch
      queryClient.invalidateQueries({ queryKey: queryKeys.projects.all })
    },
    onError(error) {
      console.error('createNewProject', error)
      toast({
        title: 'Something went wrong while creating the project',
        description: 'Please try again later.',
        variant: 'destructive',
      })
    },
  })

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
    projects,
    isLoading,
    isFetched,
    mutation,
  }
}
