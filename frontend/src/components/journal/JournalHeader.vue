<script setup lang="ts">
import type { JournalEntry } from '@/types'

defineProps<{
  entry: JournalEntry
}>()

const formatTime = (date: Date) =>
  new Intl.DateTimeFormat('en-US', {
    hour: 'numeric',
    minute: 'numeric',
    hour12: true,
  }).format(date)
</script>

<template>
  <div class="flex justify-between items-start mb-3">
    <div class="flex items-center">
      <div
        class="h-8 w-8 mr-2 rounded-full bg-muted flex items-center justify-center overflow-hidden"
      >
        <Icon
          :icon="entry.project ? 'lucide:folder' : 'lucide:file-text'"
          class="h-4 w-4 text-muted-foreground"
        />
      </div>
      <div>
        <p class="text-sm font-medium">
          {{ entry.project?.name || 'Personal Note' }}
        </p>
        <p class="text-xs text-muted-foreground">
          {{ entry.date && formatTime(new Date(entry.date)) }}
        </p>
      </div>
    </div>

    <div
      v-if="entry.isPrivate"
      class="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors"
    >
      <Icon icon="lucide:lock" class="h-3 w-3 mr-1" />
      Private
    </div>
  </div>
</template>
