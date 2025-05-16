<script setup lang="ts">
/**
 * A floating action button with tooltip and routing capabilities.
 *
 * @example
 * <FabRoutingButton
 *   to="/new-entry"
 *   message="Create new entry"
 *   iconName="plus"
 *   position="bottom-right"
 *   size="m"
 * />
 */
import { useRouter, type RouteLocationRaw } from 'vue-router'
import { Icon } from '@iconify/vue'
import { cn } from '@/lib/utils'

const props = withDefaults(
  defineProps<{
    to: RouteLocationRaw
    message: string
    iconName?: string
    size?: 's' | 'm' | 'l' | 'xl'
    position?: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right'
  }>(),
  {
    position: 'bottom-right',
    size: 'm',
  },
)
const router = useRouter()

const showTooltip = ref(false)

const sizeClasses = {
  s: 'w-12 h-12',
  m: 'w-14 h-14',
  l: 'w-16 h-16',
  xl: 'w-20 h-20',
} as const

const fabClass = computed(() =>
  cn('rounded-full text-white shadow-lg hover:bg-primary/90 transition', sizeClasses[props.size]),
)
const positionClasses = computed(
  () =>
    ({
      'top-left': 'top-6 left-6',
      'top-right': 'top-6 right-6',
      'bottom-left': 'bottom-6 left-6',
      'bottom-right': 'bottom-6 right-6',
    })[props.position] || 'bottom-right',
)

const goToNewEntry = () => {
  router.push(props.to)
}
</script>

<template>
  <div
    :class="[
      'fixed z-50 flex flex-col',
      positionClasses.includes('top-') ? 'items-start' : 'items-end',
      positionClasses,
    ]"
  >
    <div class="relative">
      <transition name="fade">
        <div
          v-if="showTooltip"
          :class="[
            'absolute px-3 py-2 rounded-lg bg-gray-900 text-white text-sm shadow-lg whitespace-nowrap',
            positionClasses.includes('right-') ? 'right-full mr-2' : 'left-full ml-2',
            positionClasses.includes('bottom-') ? 'bottom-0' : 'top-0',
          ]"
          style="pointer-events: none"
        >
          {{ props.message }}
        </div>
      </transition>
      <Button
        @mouseenter="showTooltip = true"
        @mouseleave="showTooltip = false"
        @focus="showTooltip = true"
        @blur="showTooltip = false"
        @click="goToNewEntry"
        :class="fabClass"
        :aria-label="props.message"
        data-testid="fab-button"
      >
        <Icon :icon="props.iconName || 'lucide:plus'" class="text-2xl" />
      </Button>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
