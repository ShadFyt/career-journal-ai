<script setup lang="ts">
import type { HTMLAttributes } from 'vue'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { useSidebar } from './utils'
import { Icon } from '@iconify/vue'

const props = defineProps<{
  class?: HTMLAttributes['class']
}>()

const { toggleSidebar, state } = useSidebar()
</script>

<template>
  <Button
    data-sidebar="trigger"
    variant="ghost"
    size="icon"
    :class="cn('h-7 w-7', props.class)"
    @click="toggleSidebar"
  >
    <Icon
      :icon="state === 'collapsed' ? 'lucide:chevron-right' : 'lucide:chevron-left'"
      class="h-5 w-5"
    />
    <span class="sr-only">Toggle Sidebar</span>
  </Button>
</template>
