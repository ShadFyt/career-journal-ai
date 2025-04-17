import type { z } from 'zod'
import type { ProjectSchemaCreate } from '@/schemas/project.schema.ts'

export type Project = {
  id: string
  name: string
  description: string
  link?: string | null
  technologies: string[]
  lastEntryDate?: string
  isPrivate: boolean
}

export type ProjectCreateDto = z.infer<typeof ProjectSchemaCreate>
