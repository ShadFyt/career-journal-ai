import type { journalEntryCreate, journalEntryUpdate } from '@/schemas/journal-entry.schema'
import type { Project } from './projects'
import type { TechnologyRead } from './technology'
import type { z } from 'zod'

export type JournalEntry = {
  id: string
  content: string
  date: string
  isPrivate: boolean
  technologies: TechnologyRead[]
  project: Project | null
  userId: string
}

export type JournalEntryCreateDto = z.infer<typeof journalEntryCreate>
export type JournalEntryUpdateDto = z.infer<typeof journalEntryUpdate>
