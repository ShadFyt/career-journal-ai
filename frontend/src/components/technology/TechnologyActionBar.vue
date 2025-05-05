<script setup lang="ts">
defineProps({
  search: String,
  isLoading: Boolean,
})
</script>

<template>
  <div class="flex flex-col sm:flex-row justify-between mb-5 gap-5">
    <Input
      placeholder="Filter technologies..."
      :v-model="search"
      class="mt-2"
      :disabled="isLoading"
    />
    <TechMutationModal />
  </div>
</template>
