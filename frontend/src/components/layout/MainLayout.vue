<script setup lang="ts">
import Sidebar from './Sidebar.vue'
import { SidebarProvider } from '@/components/ui/sidebar'
</script>

<template>
  <SidebarProvider>
    <div class="flex h-screen w-full overflow-hidden bg-background">
      <Sidebar />
      
      <main class="flex-1 overflow-auto w-full">
        <div class="container mx-auto p-4 lg:p-6">
          <slot></slot>
        </div>
      </main>
    </div>
  </SidebarProvider>
</template>
