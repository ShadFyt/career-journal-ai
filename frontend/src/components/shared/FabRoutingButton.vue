<script setup lang="ts">
import { useRouter, type RouteLocationRaw } from 'vue-router'
import { Icon } from '@iconify/vue'

const props = defineProps<{ to: RouteLocationRaw; message: string; iconName?: string }>()
const router = useRouter()

const showTooltip = ref(false)

const goToNewEntry = () => {
  router.push(props.to)
}
</script>

<template>
  <div class="fixed bottom-6 right-6 z-50 flex flex-col items-end">
    <transition name="fade">
      <div
        v-if="showTooltip"
        class="mb-2 px-3 py-2 rounded-lg bg-gray-900 text-white text-sm shadow-lg whitespace-nowrap"
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
      class="rounded-full text-white shadow-lg hover:bg-primary/90 w-14 h-14 transition"
      :aria-label="props.message"
    >
      <Icon :icon="props.iconName || 'lucide:plus'" class="text-2xl" />
    </Button>
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
