import { z } from 'zod'
import { techSchemaCreate, techSchemaUpdate } from '@/schemas/technology.schema.ts'

export type TechnologyRead = {
  id: string
  name: string
  description: string | null
  language: string | null
  usageCount: number
}

export type TechnologyCreateDto = z.infer<typeof techSchemaCreate>
export type TechnologyUpdateDto = z.infer<typeof techSchemaUpdate>
