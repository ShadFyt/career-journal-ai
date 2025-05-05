import { z } from 'zod'

export const techSchemaCreate = z.object({
  name: z.string().min(3, 'Name must be at least 3 characters'),
  description: z.string().optional(),
  userId: z.string().uuid().min(1, 'User ID must be set'),
})
