<script setup lang="ts">
import { boolean, string } from 'zod'

defineProps({
  search: string,
  isLoading: boolean,
})
</script>

<template>
  <Input
    placeholder="Filter technologies..."
    v-model="searchQuery"
    class="mt-2"
    :disabled="isLoading"
  />
</template>
