import { useToast } from '@/components/ui/toast'
import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'
import { createTechnology, getTechnologiesFromApi, updateTechnology } from '@/api'

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
      toast({
        title: 'Technology created',
        description: 'Your technology has been created successfully.',
        variant: 'default',
      })
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

  const updateMutation = useMutation({
    mutationFn: updateTechnology,
    onSuccess(values) {
      toast({
        title: `Technology ${values.name} updated`,
        description: 'Your technology has been updated successfully.',
        variant: 'default',
      })
      queryClient.invalidateQueries({ queryKey: technologyQueryKeys.all })
    },
    onError(error) {
      console.error('updateTechnology', error)
      toast({
        title: 'Something went wrong while updating the technology',
        description: 'Please try again later.',
        variant: 'destructive',
      })
    },
  })

  return { createMutation, updateMutation }
}
