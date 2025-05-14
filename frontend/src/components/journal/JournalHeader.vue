<script setup lang="ts">
import type { JournalEntry } from '@/types'
import { formatTime } from '@/utils'
import { Icon } from '@iconify/vue'

defineProps<{
  entry: JournalEntry
}>()
</script>

<template>
  <header class="flex justify-between items-start mb-3">
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
        <p class="text-lg font-bold">
          {{ entry.project?.name || 'Personal Note' }}
        </p>
        <p class="text-sm text-muted-foreground font-semibold">
          {{ entry.date && formatTime(new Date(entry.date)) }}
        </p>
      </div>
    </div>
    <div class="flex flex-row gap-1">
      <div
        v-if="entry.isPrivate"
        class="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors"
      >
        <Icon icon="lucide:lock" class="h-5 w-5 mr-1" />
        Private
      </div>
      <Tooltip>
        <TooltipTrigger asChild>
          <a
            v-if="entry.project?.link"
            :href="entry.project.link"
            target="_blank"
            class="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors hover:bg-accent hover:text-accent-foreground"
            aria-label="GitHub link"
          >
            <Icon icon="lucide:github" class="h-5 w-5 mr-1" />
            GitHub
          </a>
        </TooltipTrigger>
        <TooltipContent>
          <p>{{ entry.project?.link }}</p>
        </TooltipContent>
      </Tooltip>
    </div>
  </header>
</template>
