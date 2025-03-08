<script setup lang="ts">
import type { JournalEntry } from '@/types'
import { Icon } from '@iconify/vue'
import { ref, computed } from 'vue'

const mockUser = '1'
const expandedEntries = ref<Record<string, boolean>>({})

// Mock data for journal entries
const journalEntries = ref<JournalEntry[]>([
  {
    id: '1',
    content: 'Started learning Vue.js today. The composition API is really powerful!',
    date: new Date().toISOString(),
    isPrivate: false,
    userId: '1',
    technologies: [
      {
        id: '2',
        name: 'React',
        description: 'A JavaScript library for building user interfaces',
        language: 'Javascript',
      },
    ],
    project: {
      id: 1,
      name: 'Vue Dashboard',
      description:
        'A responsive admin dashboard built with Vue.js and Tailwind CSS with dark mode support and customizable widgets.',
      link: 'https://github.com/username/vue-dashboard',
      technologies: ['Vue.js', 'Tailwind CSS', 'Chart.js', 'Vite'],
      updatedAt: '2025-02-15T14:22:00Z',
    },
  },
  {
    id: '2',
    content:
      'This is a private entry that contains confidential information about my career plans.',
    date: new Date().toISOString(),
    isPrivate: true,
    userId: '1',
    technologies: [],
    project: null,
  },
])

// Format date for display
const formatDate = (date: Date) => {
  return new Intl.DateTimeFormat('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }).format(date)
}

// Format time for display
const formatTime = (date: Date) => {
  return new Intl.DateTimeFormat('en-US', {
    hour: 'numeric',
    minute: 'numeric',
    hour12: true,
  }).format(date)
}

// Group entries by date
const groupedEntries = computed(() => {
  return journalEntries.value.reduce((groups: Record<string, JournalEntry[]>, entry) => {
    const date = entry.date ? new Date(entry.date) : new Date()
    const dateStr = date.toISOString().split('T')[0]

    if (!groups[dateStr]) {
      groups[dateStr] = []
    }
    groups[dateStr].push(entry)
    return groups
  }, {})
})

// Sort dates in descending order
const sortedDates = computed(() => {
  return Object.keys(groupedEntries.value).sort(
    (a, b) => new Date(b).getTime() - new Date(a).getTime(),
  )
})

const toggleExpanded = (entryId: string) => {
  expandedEntries.value[entryId] = !expandedEntries.value[entryId]
}

const isExpanded = (entryId: string) => !!expandedEntries.value[entryId]

const canViewEntry = (entry: JournalEntry) => !entry.isPrivate || entry.userId === mockUser
</script>

<template>
  <div class="bg-background rounded-lg border">
    <div class="p-4 border-b">
      <h2 class="text-xl font-semibold">Journal Timeline</h2>
      <p class="text-sm text-muted-foreground">
        Viewing {{ journalEntries.length }} entries
        <template v-if="mockUser"> (logged in as {{ mockUser }}) </template>
      </p>
    </div>

    <div class="h-[600px] overflow-auto">
      <div class="space-y-8 p-4">
        <div v-for="dateStr in sortedDates" :key="dateStr" class="relative">
          <div class="sticky top-0 z-10 bg-background py-2">
            <div class="flex items-center">
              <Icon icon="lucide:calendar" class="mr-2 h-4 w-4 text-muted-foreground" />
              <h3 class="text-sm font-medium">
                {{ formatDate(new Date(dateStr)) }}
              </h3>
            </div>
            <div class="my-2 h-px bg-border"></div>
          </div>

          <div class="relative ml-2 space-y-4">
            <!-- Timeline line -->
            <div class="absolute left-3 top-0 bottom-0 w-px bg-muted"></div>

            <div
              v-for="entry in groupedEntries[dateStr]"
              :key="entry.id || Math.random()"
              class="relative pl-8"
            >
              <!-- Timeline dot -->
              <div
                class="absolute left-0 top-3 h-6 w-6 rounded-full border bg-background flex items-center justify-center"
              >
                <Icon
                  v-if="entry.isPrivate"
                  icon="lucide:lock"
                  class="h-3 w-3 text-muted-foreground"
                />
              </div>

              <div
                class="overflow-hidden border rounded-lg"
                :class="{ 'opacity-50': entry.isPrivate && !canViewEntry(entry) }"
              >
                <div class="p-0">
                  <div class="p-4">
                    <div class="flex justify-between items-start mb-3">
                      <div class="flex items-center">
                        <div
                          class="h-8 w-8 mr-2 rounded-full bg-muted flex items-center justify-center overflow-hidden"
                        >
                          <Icon 
                            v-if="entry.project" 
                            icon="lucide:folder" 
                            class="h-4 w-4 text-muted-foreground"
                          />
                          <Icon 
                            v-else 
                            icon="lucide:file-text" 
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

                    <template v-if="canViewEntry(entry)">
                      <div
                        class="prose prose-sm max-w-none"
                        :class="{
                          'line-clamp-3': !isExpanded(entry.id) && entry.content.length > 300,
                        }"
                      >
                        {{ entry.content }}
                      </div>

                      <button
                        v-if="entry.content.length > 300"
                        class="mt-2 h-8 text-xs flex items-center px-3 py-2 rounded-md hover:bg-muted"
                        @click="toggleExpanded(entry.id)"
                      >
                        <template v-if="isExpanded(entry.id)">
                          <Icon icon="lucide:chevron-up" class="h-3 w-3 mr-1" />
                          Show less
                        </template>
                        <template v-else>
                          <Icon icon="lucide:chevron-down" class="h-3 w-3 mr-1" />
                          Show more
                        </template>
                      </button>
                    </template>
                    <p v-else class="text-sm text-muted-foreground italic">This entry is private</p>

                    <div
                      v-if="entry.technologies && entry.technologies.length > 0"
                      class="flex flex-wrap gap-1 mt-3"
                    >
                      <Icon icon="lucide:code" class="h-4 w-4 text-muted-foreground mr-1" />
                      <span
                        v-for="tech in entry.technologies"
                        :key="tech.id || Math.random()"
                        class="inline-flex items-center rounded-md bg-muted px-2 py-1 text-xs font-medium"
                      >
                        {{ tech.name }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="sortedDates.length === 0" class="text-center p-8 text-muted-foreground">
          No journal entries available.
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  line-clamp: 3;
  overflow: hidden;
}
</style>
