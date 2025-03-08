<script setup lang="ts">
import type { Project } from '@/types/projects'
import { formatDate } from '@/utils'

defineProps<{
  filteredProjects: Project[]
}>()
</script>

<template>
  <Card>
    <div
      v-for="project in filteredProjects"
      :key="project.id"
      class="p-4 hover:bg-gray-50 transition-colors duration-150 border-b last:border-b-0"
    >
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div class="flex-grow">
          <div class="flex items-start justify-between">
            <h3 class="text-lg font-medium text-blue-700">{{ project.name }}</h3>
            <a
              v-if="project.link"
              :href="project.link"
              target="_blank"
              class="text-gray-500 hover:text-gray-700 ml-2"
            >
              <Icon icon="mdi:github" width="24" height="24" />
            </a>
          </div>
          <p class="text-gray-600 mt-1 mb-2">{{ project.description }}</p>
          <div class="flex flex-wrap gap-2">
            <span
              v-for="tech in project.technologies.slice(0, 5)"
              :key="tech"
              class="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full"
            >
              {{ tech }}
            </span>
            <span
              v-if="project.technologies.length > 5"
              class="px-2 py-1 text-xs font-medium bg-gray-100 text-gray-800 rounded-full"
            >
              +{{ project.technologies.length - 5 }}
            </span>
          </div>
        </div>
        <div class="text-sm text-gray-500 whitespace-nowrap">
          Updated: {{ formatDate(project.updatedAt) }}
        </div>
      </div>
    </div>
  </Card>
</template>
