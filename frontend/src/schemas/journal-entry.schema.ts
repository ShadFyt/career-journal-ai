import { z } from 'zod'

export const journalEntryCreate = z.object({
  content: z.string().optional(),
  projectId: z.string().uuid().optional(),
  isPrivate: z.boolean(),
  technologyIds: z.array(z.string().uuid()).optional(),
})

export const journalEntryUpdate = journalEntryCreate
  .extend({
    id: z.string().uuid().min(1, 'ID must be set'),
  })
  .optional()
