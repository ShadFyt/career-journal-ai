<script setup lang="ts">
import type { JournalEntry } from '@/types'

defineProps<{
  journalEntries: JournalEntry[]
  mockUser: string | null
}>()
</script>

<template>
  <CardHeader>
    <CardTitle>Journal Timeline</CardTitle>
    <CardDescription>
      Viewing {{ journalEntries.length }} entries
      <template v-if="mockUser"> (logged in as {{ mockUser }}) </template>
    </CardDescription>
  </CardHeader>
</template>
