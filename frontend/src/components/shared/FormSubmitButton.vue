<script setup lang="ts">
import { Button } from '@/components/ui/button'

interface Props {
  disabled?: boolean
  isSubmitting?: boolean
}

defineProps<Props>()
</script>

<template>
  <Button type="submit" :disabled="disabled">
    <span v-if="isSubmitting" class="mr-2">
      <i class="i-lucide-loader-2 animate-spin"></i>
    </span>
    <slot />
  </Button>
</template>
