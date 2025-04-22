import { useToast } from '@/components/ui/toast'
import { useQuery, useQueryClient } from '@tanstack/vue-query'
import { getTechnologiesFromApi } from '@/api'

export const technologyQueryKeys = {
  all: ['technologies'] as const,
  detail: (id: string) => [technologyQueryKeys.all, id] as const,
  list: () => [...technologyQueryKeys.all, 'list'] as const,
}

export const useTechnologyService = () => {
  const { toast } = useToast()
  const queryClient = useQueryClient()

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
