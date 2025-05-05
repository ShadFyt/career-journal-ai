import { useToast } from '@/components/ui/toast'
import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'
import { createTechnology, getTechnologiesFromApi } from '@/api'

export const technologyQueryKeys = {
  all: ['technologies'] as const,
  detail: (id: string) => [technologyQueryKeys.all, id] as const,
  list: () => [...technologyQueryKeys.all, 'list'] as const,
}

export const useTechnologyFetchService = () => {
  const { toast } = useToast()

  const getTechnologies = async () => {
    try {
      return await getTechnologiesFromApi()
    } catch (error: unknown) {
      console.error('getTechnologies', error)
      toast({
        title: 'Something went wrong while fetching technologies',
        description: 'Please try again later.',
      })
    }
  }

  const { data: technologies, isLoading } = useQuery({
    queryKey: technologyQueryKeys.list(),
    queryFn: getTechnologies,
  })

  return { technologies, isLoading }
}

export const useTechnologyMutationService = () => {
  const { toast } = useToast()
  const queryClient = useQueryClient()

  const createMutation = useMutation({
    mutationFn: createTechnology,
    onSuccess() {
      queryClient.invalidateQueries({ queryKey: technologyQueryKeys.all })
    },
    onError(error) {
      console.error('createTechnology', error)
      toast({
        title: 'Something went wrong while creating the technology',
        description: 'Please try again later.',
        variant: 'destructive',
      })
    },
  })

  return { create: createMutation }
}
