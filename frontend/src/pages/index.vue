<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { Icon } from '@iconify/vue'
</script>

<template>
  <div class="h-screen w-full flex items-center justify-center">
    <div class="w-full max-w-4xl px-4">
      <h1 class="text-3xl font-bold tracking-tight mb-8 text-center">
        Welcome to Your Career Journal
      </h1>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div
          class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm hover:shadow-md transition-shadow p-6"
        >
          <div class="flex items-center gap-2">
            <h2 class="text-xl font-semibold mb-4">Projects</h2>
            <Icon icon="lucide:folder-git" width="24" height="24" class="mb-3" />
          </div>
          <p class="text-gray-500 dark:text-gray-400 mb-4">
            Track and manage your professional projects and achievements.
          </p>
          <Button variant="default" class="w-full" as-child>
            <a href="/projects">View Projects</a>
          </Button>
        </div>

        <div
          class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm hover:shadow-md transition-shadow p-6"
        >
          <div class="flex items-center gap-2">
            <h2 class="text-xl font-semibold mb-4">Journal Entries</h2>
            <Icon icon="lucide:notebook-pen" width="24" height="24" class="mb-3" />
          </div>
          <p class="text-gray-500 dark:text-gray-400 mb-4">
            Record your daily progress, challenges, and learning experiences.
          </p>
          <Button variant="default" class="w-full" as-child>
            <a href="/journal-entries">View Journal</a>
          </Button>
        </div>

        <div
          class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm hover:shadow-md transition-shadow p-6"
        >
          <div class="flex items-center gap-2">
            <h2 class="text-xl font-semibold mb-4">Technologies</h2>
            <Icon icon="lucide:atom" width="24" height="24" class="mb-3" />
          </div>
          <p class="text-gray-500 dark:text-gray-400 mb-4">
            Manage your technology stack and skills development.
          </p>
          <Button variant="default" class="w-full" as-child>
            <a href="/technologies">View Technologies</a>
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Override parent grid layout from main.css */
:deep(#app) {
  display: block;
  max-width: 100%;
  padding: 0;
  margin: 0;
}
</style>
