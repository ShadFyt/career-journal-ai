<script setup lang="ts">
import { ref } from 'vue'
import { Icon } from '@iconify/vue'
import { RouterLink } from 'vue-router'
import { navItems } from './nav-options'

const isOpen = ref(true)
const toggleSidebar = () => {
  isOpen.value = !isOpen.value
}
</script>

<template>
  <div
    class="h-screen border-r bg-background flex flex-col transition-all duration-300"
    :class="isOpen ? 'w-64' : 'w-16'"
  >
    <div class="p-4 flex items-center justify-between">
      <h2 class="text-xl font-bold" v-if="isOpen">Career Journal</h2>
      <button
        @click="toggleSidebar"
        class="p-2 rounded-md hover:bg-accent hover:text-accent-foreground"
      >
        <Icon :icon="isOpen ? 'lucide:chevron-left' : 'lucide:chevron-right'" class="h-5 w-5" />
      </button>
    </div>
    <nav class="flex-1 px-2 py-2 overflow-y-auto">
      <ul class="space-y-2">
        <li v-for="item in navItems" :key="item.title">
          <RouterLink
            :to="item.href"
            class="flex items-center rounded-md px-3 py-2 text-sm font-medium hover:bg-accent hover:text-accent-foreground"
            :class="{ 'bg-accent text-accent-foreground': $route.path === item.href }"
          >
            <Icon :icon="item.icon" class="h-5 w-5" />
            <span v-if="isOpen" class="ml-2">{{ item.title }}</span>
          </RouterLink>
        </li>
      </ul>
    </nav>
    <div class="p-4 border-t" v-if="isOpen">
      <div class="flex items-center">
        <div
          class="h-8 w-8 rounded-full bg-muted flex items-center justify-center overflow-hidden mr-2"
        >
          <Icon icon="lucide:user" class="h-4 w-4 text-muted-foreground" />
        </div>
        <div>
          <p class="text-sm font-medium">User Profile</p>
          <p class="text-xs text-muted-foreground">View profile</p>
        </div>
      </div>
    </div>
  </div>
</template>
