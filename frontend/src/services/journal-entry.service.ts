import { createJournalEntry, getJournalEntriesFromApi } from '@/api'
import { useToast } from '@/components/ui/toast'
import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'

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

export const useJournalEntryMutationService = () => {
  const { toast } = useToast()
  const queryClient = useQueryClient()

  const createMutation = useMutation({
    mutationFn: createJournalEntry,
    onSuccess() {
      toast({
        title: 'Journal entry created',
        description: 'Your journal entry has been created successfully.',
        variant: 'default',
      })
    },
    onError(error) {
      console.error('createJournalEntry', error)
      toast({
        title: 'Something went wrong while creating the journal entry',
        description: 'Please try again later.',
        variant: 'destructive',
      })
    },
    onSettled() {
      queryClient.invalidateQueries({ queryKey: journalEntryQueryKeys.all })
    },
  })

  return { createMutation }
}
