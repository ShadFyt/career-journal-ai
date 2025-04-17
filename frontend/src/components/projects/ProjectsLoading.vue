<script setup lang="ts">
import { Skeleton } from '@/components/ui/skeleton'

defineProps<{
  viewType?: 'grid' | 'list'
}>()
</script>

<template>
  <div class="w-full">
    <!-- Grid View Loading State -->
    <div v-if="viewType === 'grid'" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="i in 6"
        :key="`skeleton-${i}`"
        class="bg-card rounded-lg shadow overflow-hidden flex flex-col"
      >
        <div class="p-4 space-y-3">
          <Skeleton class="h-6 w-3/4" />
          <Skeleton class="h-4 w-full" />
          <Skeleton class="h-4 w-5/6" />
          <div class="flex flex-wrap gap-2 mt-4">
            <Skeleton v-for="j in 3" :key="`tag-${j}`" class="h-6 w-16 rounded-full" />
          </div>
        </div>
      </div>
    </div>

    <!-- List View Loading State -->
    <div v-else class="space-y-4">
      <div
        v-for="i in 6"
        :key="`skeleton-${i}`"
        class="bg-card rounded-lg shadow overflow-hidden p-4"
      >
        <div class="flex flex-col md:flex-row gap-4">
          <div class="flex-1 space-y-3">
            <Skeleton class="h-6 w-1/3" />
            <Skeleton class="h-4 w-full" />
            <div class="flex flex-wrap gap-2 mt-4">
              <Skeleton v-for="j in 3" :key="`tag-${j}`" class="h-6 w-16 rounded-full" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
