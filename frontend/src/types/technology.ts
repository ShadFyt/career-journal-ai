import { z } from 'zod'
import { techSchemaCreate } from '@/schemas/technology.schema.ts'

export type TechnologyRead = {
  id: string
  name: string
  description: string | null
  language: string | null
  journalEntries: number
}

export type TechnologyCreateDto = z.infer<typeof techSchemaCreate>
