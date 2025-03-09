<script setup lang="ts">
import { ref } from 'vue'
import { Icon } from '@iconify/vue'
import Sidebar from './Sidebar.vue'

const isMobileMenuOpen = ref(false)

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}
</script>

<template>
  <div class="flex h-screen w-full overflow-hidden bg-background">
    <!-- Mobile sidebar overlay -->
    <div 
      v-if="isMobileMenuOpen" 
      class="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
      @click="toggleMobileMenu"
    ></div>
    
    <!-- Sidebar - hidden on mobile by default, shown when toggled -->
    <div 
      class="fixed inset-y-0 left-0 z-50 transform transition-transform duration-300 lg:relative lg:translate-x-0"
      :class="isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'"
    >
      <Sidebar />
    </div>
    
    <!-- Main content -->
    <main class="flex-1 overflow-auto w-full">
      <!-- Mobile header with menu button -->
      <div class="sticky top-0 z-30 flex items-center border-b bg-background p-4 lg:hidden">
        <button 
          @click="toggleMobileMenu" 
          class="mr-2 rounded-md p-2 hover:bg-accent hover:text-accent-foreground"
        >
          <Icon icon="lucide:menu" class="h-6 w-6" />
        </button>
        <h1 class="text-lg font-bold">Career Journal</h1>
      </div>
      
      <!-- Page content -->
      <div class="container mx-auto p-4 lg:p-6">
        <slot></slot>
      </div>
    </main>
  </div>
</template>
