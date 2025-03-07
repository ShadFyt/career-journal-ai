<script setup lang="ts">
import { computed } from 'vue'
import { Icon } from '@iconify/vue'

const props = defineProps<{
  searchQuery: string
  techFilter: string
  allTechnologies: string[]
  viewType: 'grid' | 'list'
}>()
const emit = defineEmits(['update:searchQuery', 'update:techFilter', 'update:viewType'])

const searchQuery = computed({
  get() {
    return props.searchQuery
  },
  set(value) {
    emit('update:searchQuery', value)
  },
})

const techFilter = computed({
  get() {
    return props.techFilter
  },
  set(value) {
    emit('update:techFilter', value)
  },
})

const viewType = computed({
  get() {
    return props.viewType
  },
  set(value) {
    emit('update:viewType', value)
  },
})
</script>

<template>
  <div class="flex flex-col md:flex-row justify-between mb-6 gap-4">
    <div class="relative flex-grow max-w-md">
      <Input
        v-model="searchQuery"
        type="text"
        placeholder="Search projects..."
        class="w-full pl-10 pr-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
        <Icon icon="lucide:search" width="20" height="20" class="text-gray-400" />
      </div>
    </div>

    <div class="flex gap-2">
      <Select :value="techFilter" v-model="techFilter">
        <SelectTrigger class="w-[180px]">
          <SelectValue placeholder="All Technologies" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="all">All Technologies</SelectItem>
          <SelectItem v-for="tech in allTechnologies" :key="tech" :value="tech">
            {{ tech }}
          </SelectItem>
        </SelectContent>
      </Select>

      <Button
        @click="viewType = 'grid'"
        variant="outline"
        size="icon"
        :class="{ 'bg-blue-100 border-blue-500': viewType === 'grid' }"
      >
        <Icon icon="lucide:grid" width="20" height="20" />
      </Button>

      <Button
        @click="viewType = 'list'"
        variant="outline"
        size="icon"
        :class="{ 'bg-blue-100 border-blue-500': viewType === 'list' }"
      >
        <Icon icon="lucide:list" width="20" height="20" />
      </Button>
    </div>
  </div>
</template>
