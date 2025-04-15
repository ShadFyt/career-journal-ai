export type Project = {
  id: string
  name: string
  description: string
  link?: string | null
  technologies: string[]
  lastEntryDate?: string
  isPrivate: boolean
}
