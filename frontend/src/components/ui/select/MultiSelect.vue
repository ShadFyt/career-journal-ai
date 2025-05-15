<script setup lang="ts">
import { cn } from '@/lib/utils'
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
} from '@/components/ui/dropdown-menu'
import { ChevronDown, XCircle } from 'lucide-vue-next'

export interface MultiSelectOption {
  label: string
  value: string
  disabled?: boolean
}

defineOptions({ name: 'MultiSelect' })

const props = withDefaults(
  defineProps<{
    options: MultiSelectOption[]
    modelValue: string[]
    placeholder?: string
    disabled?: boolean
    class?: string // For trigger custom classes
    clearable?: boolean
  }>(),
  {
    options: () => [],
    modelValue: () => [],
    placeholder: 'Select options...',
    disabled: false,
    clearable: false,
  },
)

const emits = defineEmits<{
  (e: 'update:modelValue', value: string[]): void
}>()

// Use a computed property for two-way binding with props.modelValue
const selectedValues = computed({
  get: () => props.modelValue,
  set: (newValue) => emits('update:modelValue', newValue),
})

function isSelected(value: string): boolean {
  return selectedValues.value.includes(value)
}

function toggleOption(value: string): void {
  const newValues = [...selectedValues.value]
  const index = newValues.indexOf(value)
  if (index > -1) {
    newValues.splice(index, 1)
  } else {
    newValues.push(value)
  }
  selectedValues.value = newValues
}

function clearAll(): void {
  console.info('[MultiSelect] clearAll called.')
  if (props.clearable) {
    selectedValues.value = []
  }
}

const triggerLabel = computed<string>(() => {
  if (selectedValues.value.length === 0) return props.placeholder
  return props.options
    .filter((opt) => selectedValues.value.includes(opt.value))
    .map((opt) => opt.label)
    .join(', ')
})

const showClearButton = computed<boolean>(() => props.clearable && selectedValues.value.length > 0)
</script>

<template>
  <DropdownMenu>
    <DropdownMenuTrigger
      :disabled="props.disabled"
      :class="
        cn(
          'flex h-9 w-full items-center justify-between whitespace-nowrap rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-ring disabled:cursor-not-allowed disabled:opacity-50 [&>span]:truncate text-start',
          props.class,
        )
      "
    >
      <span class="truncate">{{ triggerLabel }}</span>
      <ChevronDown class="ml-2 h-4 w-4 shrink-0 opacity-50" />
    </DropdownMenuTrigger>
    <DropdownMenuContent align="start" class="w-[var(--reka-popper-anchor-width)] p-1">
      <DropdownMenuItem
        v-if="showClearButton"
        @select="
          (event) => {
            event.originalEvent?.preventDefault()
            clearAll()
          }
        "
        class="flex cursor-pointer items-center justify-between text-sm text-destructive hover:bg-destructive/10 focus:bg-destructive/10 focus:text-destructive data-[disabled]:pointer-events-none data-[disabled]:opacity-50"
        :disabled="!selectedValues.length"
      >
        <span>Clear all</span>
        <XCircle class="h-4 w-4 opacity-70" />
      </DropdownMenuItem>
      <DropdownMenuSeparator v-if="showClearButton && props.options.length > 0" />
      <div
        v-for="option in props.options"
        :key="option.value + '-debug'"
        class="relative flex select-none items-center rounded-sm py-1.5 pl-3 pr-2 text-sm outline-none transition-colors focus-within:bg-accent focus-within:text-accent-foreground data-[disabled]:pointer-events-none"
        :class="{
          'hover:bg-accent hover:text-accent-foreground': !option.disabled,
          'opacity-50': option.disabled,
        }"
      >
        <label
          class="flex w-full items-center"
          :class="option.disabled ? 'cursor-not-allowed' : 'cursor-pointer'"
        >
          <Checkbox
            :model-value="isSelected(option.value)"
            @update:model-value="toggleOption(option.value)"
          />
          <span class="flex-grow ml-2">{{ option.label }}</span>
        </label>
      </div>
      <div
        v-if="!props.options.length"
        class="px-2 py-1.5 text-sm text-muted-foreground text-center"
      >
        No options available.
      </div>
    </DropdownMenuContent>
  </DropdownMenu>
</template>
