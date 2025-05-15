<script setup lang="ts">
import { toTypedSchema } from '@vee-validate/zod'
import { journalEntryCreate } from '@/schemas/journal-entry.schema'
import { useForm } from 'vee-validate'
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
import { useProjectService, useTechnologyFetchService } from '@/services'
import { MultiSelect, type MultiSelectOption } from '@/components/ui/select'

const { projects, isLoading } = useProjectService()
const { technologies } = useTechnologyFetchService()
const validationSchema = toTypedSchema(journalEntryCreate)

const techOptions = computed<MultiSelectOption[]>(
  () => technologies.value?.map((tech) => ({ label: tech.name, value: tech.id })) ?? [],
)
const { handleSubmit, isSubmitting, meta } = useForm({
  validationSchema,
  initialValues: {
    content: '',
    projectId: undefined,
    isPrivate: false,
    technologyIds: [],
  },
})

const isDisabled = computed(() => isSubmitting.value || !meta.value.valid)

const onSubmit = handleSubmit(async (values) => {
  console.log(values)
})
</script>

<template>
  <main class="container mx-auto px-4 py-8">
    <TitleWithBackButton title="Add New Journal Entry" />
    <section class="max-w-2xl">
      <form :validation-schema="validationSchema" @submit="onSubmit" class="space-y-6">
        <FormField v-slot="{ componentField }" name="projectId">
          <FormItem>
            <FormLabel>Project</FormLabel>
            <Select :disabled="isLoading" v-bind="componentField">
              <SelectTrigger>
                <div class="flex items-center gap-2">
                  <Loader v-if="isLoading" size="m" />
                  <SelectValue
                    :placeholder="isLoading ? 'Fetching projects...' : 'Select a project'"
                  />
                </div>
              </SelectTrigger>
              <SelectContent>
                <SelectItem v-for="project in projects" :key="project.id" :value="project.id">
                  {{ project.name }}
                </SelectItem>
              </SelectContent>
            </Select>
          </FormItem>
        </FormField>
        <FormField v-slot="{ componentField }" name="content">
          <FormItem>
            <FormLabel>Content</FormLabel>
            <FormControl>
              <Textarea
                v-bind="componentField"
                class="flex min-h-24 w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
                placeholder="Describe your journal entry"
              />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>
        <FormField v-slot="{ value, handleChange }" name="technologyIds">
          <FormItem>
            <FormLabel>Technologies</FormLabel>
            <FormControl>
              <MultiSelect
                :modelValue="value"
                @update:modelValue="handleChange"
                :options="techOptions"
                placeholder="Select technologies"
                clearable
              />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>
        <PrivateCheckboxForm
          name="isPrivate"
          title="Private Entry"
          description="Make this entry private and visible only to you"
        />
        <FormSubmitButton :disabled="isDisabled" :is-submitting="isSubmitting">
          Add Entry
        </FormSubmitButton>
      </form>
    </section>
  </main>
</template>
