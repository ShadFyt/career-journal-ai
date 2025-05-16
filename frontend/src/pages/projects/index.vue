<script setup lang="ts">
import { computed, ref } from 'vue'
import { useProjectService } from '@/services'
import { useLocalStorage } from '@vueuse/core'
import { VIEW_TYPE } from '@/constants'

const { projects, isLoading } = useProjectService()

const viewType = useLocalStorage<'grid' | 'list'>(VIEW_TYPE, 'grid')

const searchQuery = ref('')
const techFilter = ref('all')

const allTechnologies = computed(() => {
  const techSet = new Set<string>()
  if (!projects.value) return []
  projects.value?.forEach((project) => {
    project?.technologies?.forEach((tech) => techSet.add(tech))
  })
  return [...techSet].sort()
})

const filteredProjects = computed(() => {
  if (!projects.value) return []
  return projects.value?.filter((project) => {
    const matchesSearch =
      searchQuery.value === '' ||
      project.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      project.description.toLowerCase().includes(searchQuery.value.toLowerCase())

    const matchesTech =
      techFilter.value === 'all' || project.technologies.includes(techFilter.value)

    return matchesSearch && matchesTech
  })
})
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-6">My Projects</h1>

    <!-- Filter and Search Section -->
    <FilterSection
      v-model:searchQuery="searchQuery"
      v-model:techFilter="techFilter"
      v-model:viewType="viewType"
      :allTechnologies="allTechnologies"
    />

    <!-- Loading State -->
    <div v-if="isLoading" class="py-4">
      <ProjectsLoading :viewType="viewType" />
    </div>

    <!-- Content when loaded -->
    <div v-else>
      <!-- Grid View -->
      <ProjectGridView v-if="viewType === 'grid'" :filteredProjects="filteredProjects" />
      <!-- List View -->
      <ProjectListView v-else :filteredProjects="filteredProjects" />
      <!-- Empty State -->
      <EmptyState v-if="filteredProjects.length === 0" :filteredProjects="filteredProjects" />
    </div>
    <FabRoutingButton to="/projects/new" message="Add new project" iconName="lucide:folder-plus" />
  </div>
</template>
