<script setup lang="ts">
import type { Project } from '@/types/projects'

defineProps<{
  filteredProjects: Project[]
}>()

const formatDate = (dateString: string) => {
  const options: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  }
  return new Date(dateString).toLocaleDateString(undefined, options)
}
</script>

<template>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    <Card
      v-for="project in filteredProjects"
      :key="project.id"
      class="hover:shadow-lg transition-shadow duration-300"
    >
      <CardHeader class="pb-2">
        <div class="flex justify-between items-start">
          <CardTitle class="text-xl font-semibold text-blue-700">{{ project.name }}</CardTitle>
          <a :href="project.repoUrl" target="_blank" class="text-gray-500 hover:text-gray-700">
            <Icon icon="mdi:github" width="24" height="24" />
          </a>
        </div>
      </CardHeader>

      <CardContent>
        <p class="text-gray-600 mb-4 line-clamp-3">{{ project.description }}</p>

        <div class="flex justify-between items-center">
          <div class="flex flex-wrap gap-2">
            <span
              v-for="tech in project.technologies.slice(0, 3)"
              :key="tech"
              class="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full"
            >
              {{ tech }}
            </span>
            <span
              v-if="project.technologies.length > 3"
              class="px-2 py-1 text-xs font-medium bg-gray-100 text-gray-800 rounded-full"
            >
              +{{ project.technologies.length - 3 }}
            </span>
          </div>

          <span class="text-sm text-gray-500"> Updated: {{ formatDate(project.updatedAt) }} </span>
        </div>
      </CardContent>
    </Card>
  </div>
</template>
