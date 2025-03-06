<script setup lang="ts">
import type { Project } from '@/types/projects'

defineProps<{
  filteredProjects: Project[]
}>()
</script>

<template>
  <Card v-if="filteredProjects.length === 0" class="text-center py-12">
    <CardContent class="relative flex-grow">
      <svg
        class="w-16 h-16 mx-auto text-gray-400"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M12 13h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
        ></path>
      </svg>
      <h3 class="mt-4 text-lg font-medium text-gray-900">No projects found</h3>
      <p class="mt-1 text-gray-500">
        Try adjusting your search or filter to find what you're looking for.
      </p>
    </CardContent>
  </Card>
</template>
