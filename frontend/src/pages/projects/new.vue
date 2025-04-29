<script setup lang="ts">
import { useRouter } from 'vue-router'
import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'
import { ProjectSchemaCreate } from '@/schemas/project.schema'
import { useProjectService } from '@/services'
import { useToast } from '@/components/ui/toast'
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Checkbox } from '@/components/ui/checkbox'
import { Icon } from '@iconify/vue'

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
  <div class="container mx-auto px-4 py-8">
    <div class="flex items-center mb-6">
      <div class="flex items-center">
        <Button
          variant="ghost"
          size="sm"
          @click="goBack"
          class="mr-2 -ml-2 h-8"
          aria-label="Back to Projects page"
        >
          <Icon icon="lucide:arrow-left" width="18" height="18" />
          <span class="ml-1 text-sm text-muted-foreground">Back</span>
        </Button>
      </div>
      <h2 class="text-2xl font-bold">Create New Project</h2>
    </div>

    <div class="max-w-2xl">
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

          <FormField v-slot="{ componentField }" name="isPrivate" type="checkbox">
            <FormItem class="flex flex-row items-start space-x-3 space-y-0 rounded-md border p-4">
              <FormControl>
                <Checkbox v-bind="componentField" />
              </FormControl>
              <div class="space-y-1 leading-none">
                <FormLabel>Private Project</FormLabel>
                <p class="text-sm text-muted-foreground">
                  Make this project private and visible only to you
                </p>
              </div>
            </FormItem>
          </FormField>

          <Button type="submit" :disabled="isDisabled" class="mt-4">
            <span v-if="isSubmitting" class="mr-2">
              <i class="i-lucide-loader-2 animate-spin"></i>
            </span>
            Create Project
          </Button>
        </div>
      </form>
    </div>
  </div>
</template>
