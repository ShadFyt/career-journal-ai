<script setup lang="ts">
import { useRouter } from 'vue-router'
import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'
import { ProjectSchemaCreate } from '@/schemas/project.schema'
import { useProjectService } from '@/services'
import { useToast } from '@/components/ui/toast'
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
import { Input } from '@/components/ui/input'

const router = useRouter()
const { toast } = useToast()
const { mutation } = useProjectService()
const { profile } = useAuthStore()

const validationSchema = toTypedSchema(ProjectSchemaCreate)

const goBack = () => {
  router.push('/projects')
}

const { handleSubmit, isSubmitting, meta } = useForm({
  validationSchema,
  initialValues: {
    name: '',
    description: '',
    userId: profile.userId,
    link: '',
    isPrivate: false,
  },
})

const isDisabled = computed(() => isSubmitting.value || !meta.value.valid)

// Handle form submission
const onSubmit = handleSubmit(async (values) => {
  try {
    await mutation.mutateAsync(values)

    toast({
      title: 'Project created',
      description: 'Your project has been created successfully.',
    })

    goBack()
  } catch (error) {
    // Error is already handled in the service, no need to show another toast
    console.error('Failed to create project:', error)
  }
})
</script>

<template>
  <main class="container mx-auto px-4 py-8">
    <TitleWithBackButton title="Create New Project" />
    <section class="max-w-2xl">
      <form :validation-schema="validationSchema" @submit="onSubmit">
        <div class="space-y-6">
          <FormField v-slot="{ componentField }" name="name">
            <FormItem>
              <FormLabel>Project Name</FormLabel>
              <FormControl>
                <Input v-bind="componentField" placeholder="Enter project name" />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>

          <FormField v-slot="{ componentField }" n name="description">
            <FormItem>
              <FormLabel>Description</FormLabel>
              <FormControl>
                <textarea
                  v-bind="componentField"
                  class="flex min-h-24 w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
                  placeholder="Describe your project"
                ></textarea>
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>

          <FormField v-slot="{ componentField }" n name="link">
            <FormItem>
              <FormLabel>Project Link (Optional)</FormLabel>
              <FormControl>
                <Input v-bind="componentField" placeholder="https://example.com" />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>

          <PrivateCheckboxForm
            name="isPrivate"
            title="Private Project"
            description="Make this project private and visible only to you"
          />

          <FormSubmitButton :disabled="isDisabled" :is-submitting="isSubmitting">
            Create Project
          </FormSubmitButton>
        </div>
      </form>
    </section>
  </main>
</template>
