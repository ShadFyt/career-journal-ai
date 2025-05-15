<script setup lang="ts">
import {
  FormField,
  FormItem,
  FormControl,
  FormLabel,
  FormDescription,
  FormMessage,
} from '@/components/ui/form'
import { Checkbox } from '@/components/ui/checkbox'
defineProps<{ name: string; title: string; description: string }>()
</script>

<template>
  <FormField v-slot="{ value, handleChange }" type="checkbox" :name="name">
    <FormItem class="flex flex-row items-start gap-x-3 space-y-0 rounded-md border p-4 shadow">
      <FormControl>
        <Checkbox :model-value="value" @update:model-value="handleChange" />
      </FormControl>
      <div class="space-y-1 leading-none">
        <FormLabel>{{ title }}</FormLabel>
        <FormDescription> {{ description }} </FormDescription>
        <FormMessage />
      </div>
    </FormItem>
  </FormField>
</template>
