<script setup lang="ts">
import { formatDate } from '@/utils/date.utils'
import { Icon } from '@iconify/vue'

defineProps<{
  dateStr: string
}>()
</script>

<template>
  <header class="sticky top-0 z-10 bg-background py-2">
    <div class="flex items-center">
      <Icon icon="lucide:calendar" class="mr-2 h-4 w-4 text-muted-foreground" />
      <h3 class="text-sm font-medium">
        {{ formatDate(dateStr, 'full') }}
      </h3>
    </div>
    <div class="my-2 h-px bg-border"></div>
  </header>
</template>
