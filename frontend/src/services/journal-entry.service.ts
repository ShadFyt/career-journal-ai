import { getJournalEntriesFromApi } from '@/api'
import { useToast } from '@/components/ui/toast'
import { useQuery } from '@tanstack/vue-query'

export const journalEntryQueryKeys = {
  all: ['journal-entries'] as const,
  detail: (id: string) => [...journalEntryQueryKeys.all, id] as const,
  list: () => [...journalEntryQueryKeys.all, 'list'] as const,
}

export const useJournalEntryService = () => {
  const { toast } = useToast()
  const getJournalEntries = async () => {
    try {
      return await getJournalEntriesFromApi()
    } catch (error: unknown) {
      console.error('getJournalEntries', error)
      toast({
        title: 'Something went wrong while fetching journal entries',
        description: 'Please try again later.',
      })
    }
  }

  const {
    data: journalEntries,
    isLoading,
    isFetched,
  } = useQuery({
    queryKey: journalEntryQueryKeys.list(),
    queryFn: getJournalEntries,
  })

  return { journalEntries, isLoading, isFetched }
}
