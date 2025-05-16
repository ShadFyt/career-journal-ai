<script setup lang="ts">
import { Icon } from '@iconify/vue'
import { computed, type HTMLAttributes } from 'vue'
import { cn } from '@/lib/utils'

interface LoaderProps {
  /**
   * Spinner size (small, medium, large)
   */
  size?: 's' | 'm' | 'l' | 'xl'
  /**
   * Color variant of the spinner
   */
  variant?: 'primary' | 'secondary' | 'muted'
  /**
   * Extra Tailwind classes
   */
  class?: HTMLAttributes['class']
  /**
   * Full screen loader
   */
  fullScreen?: boolean
  /**
   * Message to display below the spinner
   */
  message?: string
}

const props = withDefaults(defineProps<LoaderProps>(), {
  size: 's',
  variant: 'primary',
  fullScreen: false,
  message: 'Loading...',
})

const sizeClasses = {
  s: 'h-4 w-4',
  m: 'h-6 w-6',
  l: 'h-8 w-8',
  xl: 'h-12 w-12',
} as const

const variantClasses = {
  primary: 'text-primary',
  secondary: 'text-secondary',
  muted: 'text-muted-foreground',
} as const

const iconClass = computed(() =>
  cn('animate-spin', sizeClasses[props.size], variantClasses[props.variant], props.class),
)
</script>

<template>
  <div
    v-if="props.fullScreen"
    class="flex h-screen w-full items-center justify-center"
    role="status"
    aria-live="polite"
  >
    <div class="flex flex-col items-center gap-4">
      <Icon icon="lucide:loader-2" :class="iconClass" />
      <p class="text-lg font-medium">{{ props.message }}</p>
    </div>
  </div>
  <Icon v-else icon="lucide:loader-2" :class="iconClass" aria-label="Loading" />
</template>
