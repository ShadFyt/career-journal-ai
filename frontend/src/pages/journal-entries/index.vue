<script setup lang="ts">
import type { JournalEntry } from '@/types'
import { Icon } from '@iconify/vue'
import { Header as MainHeader } from '@/components/journal'
import { useJournalEntryService } from '@/services'

const mockUser = '1'
const expandedEntries = ref<Record<string, boolean>>({})

const { journalEntries } = useJournalEntryService()

// Group entries by date
const groupedEntries = computed(() => {
  const entries = journalEntries.value ?? []
  if (entries.length === 0) {
    return {}
  }
  return entries.reduce((groups: Record<string, JournalEntry[]>, entry) => {
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
const sortedDates = computed(() =>
  Object.keys(groupedEntries.value ?? {}).sort(
    (a, b) => new Date(b).getTime() - new Date(a).getTime(),
  ),
)

const toggleExpanded = (id: string) => {
  if (!id) return
  expandedEntries.value[id] = !expandedEntries.value[id]
}

const isExpanded = (id: string) => {
  if (!id) return false
  return expandedEntries.value[id]
}

const canViewEntry = (entry: JournalEntry) => !entry.isPrivate || entry.userId === mockUser
</script>

<template>
  <div v-if="journalEntries && groupedEntries" class="bg-background h-full flex flex-col">
    <Card class="border h-full flex flex-col">
      <MainHeader :journal-entries="journalEntries" :mock-user="mockUser" />

      <ScrollArea class="flex-1">
        <div class="space-y-8 p-4">
          <div v-for="dateStr in sortedDates" :key="dateStr">
            <TimelineHeader :date-str="dateStr" />

            <div class="relative ml-2 space-y-4">
              <!-- Timeline line -->
              <div class="absolute left-3 top-0 bottom-0 w-px bg-muted"></div>

              <div v-for="entry in groupedEntries[dateStr]" :key="entry.id" class="relative pl-8">
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

                <Card
                  class="overflow-hidden"
                  :class="{ 'opacity-50': entry.isPrivate && !canViewEntry(entry) }"
                >
                  <CardContent class="p-0">
                    <div class="p-4">
                      <JournalHeader :entry="entry" />

                      <template v-if="canViewEntry(entry)">
                        <div class="prose prose-sm max-w-none">
                          <div
                            v-if="!isExpanded(entry.id) && entry.content.length > 200"
                            class="line-clamp-3"
                          >
                            {{ entry.content }}
                          </div>
                          <div v-else>
                            {{ entry.content }}
                          </div>
                        </div>

                        <Button
                          v-if="entry.content.length > 200"
                          variant="ghost"
                          size="sm"
                          class="mt-2 h-8 text-xs"
                          @click="toggleExpanded(entry.id)"
                        >
                          <Icon
                            :icon="
                              isExpanded(entry.id) ? 'lucide:chevron-up' : 'lucide:chevron-down'
                            "
                            class="h-3 w-3 mr-1"
                          />
                          {{ isExpanded(entry.id) ? 'Show less' : 'Show more' }}
                        </Button>
                      </template>
                      <p v-else class="text-sm text-muted-foreground italic">
                        This entry is private
                      </p>

                      <div
                        v-if="entry.technologies && entry.technologies.length > 0"
                        class="flex flex-wrap gap-1 mt-3"
                      >
                        <Icon icon="lucide:code" class="h-4 w-4 text-muted-foreground mr-1" />
                        <span
                          v-for="tech in entry.technologies.slice(0, 3)"
                          :key="tech.id"
                          class="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full"
                        >
                          {{ tech.name }}
                        </span>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
          </div>

          <div v-if="sortedDates.length === 0" class="text-center p-8 text-muted-foreground">
            No journal entries available.
          </div>
        </div>
      </ScrollArea>
    </Card>
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
