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
  type SidebarProps,
} from '@/components/ui/sidebar'

const { state } = useSidebar()

const expanded = computed(() => state.value !== 'collapsed')
const props = withDefaults(defineProps<SidebarProps>(), {
  collapsible: 'icon',
})
</script>

<template>
  <ShadcnSidebar class="border-r" v-bind="props">
    <SidebarHeader class="p-4 flex flex-row items-center justify-between">
      <h2 class="text-xl font-bold" v-if="expanded">Career Journal</h2>
      <SidebarTrigger />
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

    <SidebarFooter class="p-4 border-t">
      <UserMenu />
    </SidebarFooter>
    <SidebarRail />
  </ShadcnSidebar>
</template>
