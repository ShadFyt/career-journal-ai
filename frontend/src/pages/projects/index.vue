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
const viewType = ref('grid')

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
    <div class="flex flex-col md:flex-row justify-between mb-6 gap-4">
      <div class="relative flex-grow max-w-md">
        <Input
          v-model="searchQuery"
          type="text"
          placeholder="Search projects..."
          class="w-full pl-10 pr-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
          <Icon icon="lucide:search" class="w-5 h-5 text-gray-400" />
        </div>
      </div>

      <div class="flex gap-2">
        <Select v-model="techFilter">
          <SelectTrigger class="w-[180px]">
            <SelectValue placeholder="All Technologies" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Technologies</SelectItem>
            <SelectItem v-for="tech in allTechnologies" :key="tech" :value="tech">
              {{ tech }}
            </SelectItem>
          </SelectContent>
        </Select>

        <Button
          @click="viewType = 'grid'"
          variant="outline"
          size="icon"
          :class="{ 'bg-blue-100 border-blue-500': viewType === 'grid' }"
        >
          <svg
            class="w-5 h-5"
            fill="currentColor"
            viewBox="0 0 20 20"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM11 5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V5zM11 13a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"
            ></path>
          </svg>
        </Button>

        <Button
          @click="viewType = 'list'"
          variant="outline"
          size="icon"
          :class="{ 'bg-blue-100 border-blue-500': viewType === 'list' }"
        >
          <svg
            class="w-5 h-5"
            fill="currentColor"
            viewBox="0 0 20 20"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              fill-rule="evenodd"
              d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z"
              clip-rule="evenodd"
            ></path>
          </svg>
        </Button>
      </div>
    </div>

    <!-- Grid View -->
    <div v-if="viewType === 'grid'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <Card
        v-for="project in filteredProjects"
        :key="project.id"
        class="hover:shadow-lg transition-shadow duration-300"
      >
        <CardHeader class="pb-2">
          <div class="flex justify-between items-start">
            <CardTitle class="text-xl font-semibold text-blue-700">{{ project.name }}</CardTitle>
            <a :href="project.repoUrl" target="_blank" class="text-gray-500 hover:text-gray-700">
              <svg
                class="w-6 h-6"
                fill="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  fill-rule="evenodd"
                  d="M12 2C6.477 2 2 6.477 2 12c0 4.42 2.865 8.166 6.839 9.489.5.092.682-.217.682-.482 0-.237-.008-.866-.013-1.7-2.782.605-3.369-1.343-3.369-1.343-.454-1.157-1.11-1.465-1.11-1.465-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.699 1.028 1.592 1.028 2.683 0 3.841-2.337 4.687-4.565 4.935.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12c0-5.523-4.477-10-10-10z"
                  clip-rule="evenodd"
                ></path>
              </svg>
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

            <span class="text-sm text-gray-500">
              Updated: {{ formatDate(project.updatedAt) }}
            </span>
          </div>
        </CardContent>
      </Card>
    </div>

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
                <svg
                  class="w-5 h-5"
                  fill="currentColor"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    fill-rule="evenodd"
                    d="M12 2C6.477 2 2 6.477 2 12c0 4.42 2.865 8.166 6.839 9.489.5.092.682-.217.682-.482 0-.237-.008-.866-.013-1.7-2.782.605-3.369-1.343-3.369-1.343-.454-1.157-1.11-1.465-1.11-1.465-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.699 1.028 1.592 1.028 2.683 0 3.841-2.337 4.687-4.565 4.935.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12c0-5.523-4.477-10-10-10z"
                    clip-rule="evenodd"
                  ></path>
                </svg>
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
