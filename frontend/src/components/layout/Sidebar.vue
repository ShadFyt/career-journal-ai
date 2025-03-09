<script setup lang="ts">
import { Icon } from '@iconify/vue'
import { RouterLink } from 'vue-router'
import { navItems } from './nav-options'
import {
  Sidebar as ShadcnSidebar,
  SidebarContent,
  SidebarHeader,
  SidebarFooter,
  SidebarMenu,
  SidebarMenuButton,
  SidebarTrigger,
  useSidebar,
} from '@/components/ui/sidebar'

const { state, toggleSidebar } = useSidebar()

const expanded = computed(() => state.value !== 'collapsed')
</script>

<template>
  <ShadcnSidebar collapsible="icon" class="border-r">
    <SidebarHeader class="p-4 flex flex-row items-center justify-between">
      <h2 class="text-xl font-bold" v-if="expanded">Career Journal</h2>
      <SidebarTrigger @click="toggleSidebar" />
    </SidebarHeader>

    <SidebarContent class="px-2 py-2">
      <SidebarMenu>
        <li v-for="item in navItems" :key="item.title">
          <SidebarMenuButton as-child :tooltip="item.title">
            <RouterLink :to="item.href" class="flex w-full items-center" active-class="bg-muted">
              <Icon :icon="item.icon" class="h-5 w-5" />
              <span v-if="expanded" class="ml-2">{{ item.title }}</span>
            </RouterLink>
          </SidebarMenuButton>
        </li>
      </SidebarMenu>
    </SidebarContent>

    <SidebarFooter v-if="expanded" class="p-4 border-t">
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
    </SidebarFooter>
  </ShadcnSidebar>
</template>
