<script setup lang="ts">
defineProps<{
  dateStr: string
}>()

const formatDate = (date: Date) =>
  new Intl.DateTimeFormat('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }).format(date)
</script>

<template>
  <header class="sticky top-0 z-10 bg-background py-2">
    <div class="flex items-center">
      <Icon icon="lucide:calendar" class="mr-2 h-4 w-4 text-muted-foreground" />
      <h3 class="text-sm font-medium">
        {{ formatDate(new Date(dateStr)) }}
      </h3>
    </div>
    <div class="my-2 h-px bg-border"></div>
  </header>
</template>
