<script setup lang="ts">
const props = defineProps<{
  search: string
  isLoading: boolean
}>()

const emit = defineEmits(['update:search'])

const search = computed({
  get() {
    return props.search
  },
  set(value) {
    emit('update:search', value)
  },
})
</script>

<template>
  <div class="flex flex-col sm:flex-row justify-between mb-5 gap-5">
    <Input
      placeholder="Filter technologies..."
      v-model="search"
      class="mt-2"
      :disabled="isLoading"
    />
    <TechMutationModal />
  </div>
</template>
