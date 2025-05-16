import { apiClient } from './client'
import type { JournalEntry, JournalEntryCreateDto, JournalEntryUpdateDto } from '@/types'

const BASE_URL = '/journal-entries'

export const getJournalEntriesFromApi = async () =>
  await apiClient.get<JournalEntry[]>(BASE_URL, { withCredentials: true })

export const createJournalEntry = async (dto: JournalEntryCreateDto) =>
  await apiClient.post<JournalEntry>(BASE_URL, dto, {
    withCredentials: true,
  })

export const updateJournalEntry = async (id: string, dto: JournalEntryUpdateDto) =>
  await apiClient.patch<JournalEntry>(`${BASE_URL}/${id}`, dto, {
    withCredentials: true,
  })

export const deleteJournalEntry = async (id: string) =>
  await apiClient.delete(`${BASE_URL}/${id}`, {
    withCredentials: true,
  })
