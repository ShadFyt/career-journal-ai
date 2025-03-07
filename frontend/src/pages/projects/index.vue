<script setup lang="ts">
import { ref, computed } from 'vue'
import { Icon } from '@iconify/vue'

const projects = ref([
  {
    id: 1,
    name: 'Vue Dashboard',
    description:
      'A responsive admin dashboard built with Vue.js and Tailwind CSS with dark mode support and customizable widgets.',
    repoUrl: 'https://github.com/username/vue-dashboard',
    technologies: ['Vue.js', 'Tailwind CSS', 'Chart.js', 'Vite'],
    updatedAt: '2025-02-15T14:22:00Z',
  },
  {
    id: 2,
    name: 'E-Commerce API',
    description:
      'RESTful API for e-commerce applications with user authentication, product management, and order processing.',
    repoUrl: 'https://github.com/username/ecommerce-api',
    technologies: ['Node.js', 'Express', 'MongoDB', 'JWT', 'Docker'],
    updatedAt: '2025-01-20T09:45:00Z',
  },
  {
    id: 3,
    name: 'Portfolio Website',
    description:
      'Personal portfolio website showcasing projects and skills with a modern, minimalist design.',
    repoUrl: 'https://github.com/username/portfolio',
    technologies: ['Vue.js', 'GSAP', 'Tailwind CSS', 'Firebase'],
    updatedAt: '2025-02-28T16:30:00Z',
  },
  {
    id: 4,
    name: 'Weather App',
    description:
      'A weather forecast application providing real-time weather data with location detection and 5-day forecasts.',
    repoUrl: 'https://github.com/username/weather-app',
    technologies: ['Vue.js', 'OpenWeather API', 'Geolocation API'],
    updatedAt: '2025-01-05T11:15:00Z',
  },
  {
    id: 5,
    name: 'Task Manager',
    description:
      'Collaborative task management application with real-time updates, task assignments, and progress tracking.',
    repoUrl: 'https://github.com/username/task-manager',
    technologies: ['Vue.js', 'Pinia', 'Firebase', 'Tailwind CSS'],
    updatedAt: '2025-02-10T13:40:00Z',
  },
])

const searchQuery = ref('')
const techFilter = ref('all')
const viewType = ref<'grid' | 'list'>('grid')

const allTechnologies = computed(() => {
  const techSet = new Set<string>()
  projects.value.forEach((project) => {
    project.technologies.forEach((tech) => techSet.add(tech))
  })
  return [...techSet].sort()
})

const filteredProjects = computed(() => {
  return projects.value.filter((project) => {
    const matchesSearch =
      searchQuery.value === '' ||
      project.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      project.description.toLowerCase().includes(searchQuery.value.toLowerCase())

    const matchesTech =
      techFilter.value === 'all' || project.technologies.includes(techFilter.value)

    return matchesSearch && matchesTech
  })
})

const formatDate = (dateString: string) => {
  const options = { year: 'numeric', month: 'short', day: 'numeric' }
  return new Date(dateString).toLocaleDateString(undefined, options)
}
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

    <!-- Grid View -->
    <ProjectGridView v-if="viewType === 'grid'" :filteredProjects="filteredProjects" />

    <!-- List View -->
    <Card v-else>
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
                :href="project.repoUrl"
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

    <!-- Empty State -->
    <EmptyState :filteredProjects="filteredProjects" />
  </div>
</template>
