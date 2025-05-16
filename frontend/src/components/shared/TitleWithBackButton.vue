<script setup lang="ts">
import { Icon } from '@iconify/vue'

defineProps<{ title: string }>()
const router = useRouter()
const goBack = () => {
  router.back()
}
</script>

<template>
  <header class="flex items-center mb-6">
    <div class="flex items-center">
      <Button
        variant="ghost"
        size="sm"
        @click="goBack"
        class="mr-2 -ml-2 h-8"
        aria-label="Back to previous page"
      >
        <Icon icon="lucide:arrow-left" width="18" height="18" />
        <span class="ml-1 text-sm text-muted-foreground">Back</span>
      </Button>
    </div>
    <h2 class="text-2xl font-bold">{{ title }}</h2>
  </header>
</template>
