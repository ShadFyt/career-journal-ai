<script lang="ts" setup>
import { useTechnologyFetchService, useTechnologyMutationService } from '@/services'
import { toTypedSchema } from '@vee-validate/zod'
import { techSchemaCreate } from '@/schemas/technology.schema.ts'
import { useForm } from 'vee-validate'
import { FormField, FormItem } from '@/components/ui/form'
import { useTextareaAutosize } from '@vueuse/core'
import type { Textarea } from '@/components/ui/textarea'

const { technologies } = useTechnologyFetchService()
const { createMutation, updateMutation } = useTechnologyMutationService()
const { textarea, input } = useTextareaAutosize()

const { profile } = useAuthStore()
const router = useRouter()

const route = useRoute('/technologies/edit.[id]')

const textareaComponentRef = ref<InstanceType<typeof Textarea> | null>(null)

const isEdit = computed(() => router.currentRoute.value.name.includes('edit'))

const tech = computed(() => {
  const techId = route.params?.id
  if (!techId || !isEdit) return null
  return technologies.value?.find((tech) => tech.id === techId) ?? null
})

const isOpen = computed(
  () =>
    router.currentRoute.value.name === '/technologies/new' ||
    router.currentRoute.value.name.includes('edit'),
)

const validationSchema = toTypedSchema(techSchemaCreate)

const { handleSubmit, isSubmitting, meta } = useForm({
  validationSchema,
  initialValues: {
    name: tech.value?.name ?? '',
    description: tech.value?.description ?? '',
    language: tech.value?.language ?? '',
    userId: profile.userId,
  },
})

const isDisabled = computed(() => isSubmitting.value || !meta.value.valid)

const closeModal = (isOpen: boolean | globalThis.ComputedRef<boolean>) => {
  if (!isOpen) {
    router.push('/technologies')
  }
}

const onSubmit = handleSubmit(async (values) => {
  const onSettled = () => closeModal(!isOpen)
  if (isEdit && tech.value?.id) {
    updateMutation.mutate(
      { ...values, id: tech.value.id },
      {
        onSettled,
      },
    )
    return
  }
  await createMutation.mutateAsync(values, {
    onSettled,
  })
})

watch(
  textareaComponentRef,
  (instance) => {
    if (instance && instance.textareaElement) {
      textarea.value = instance.textareaElement // Assign the exposed HTMLTextAreaElement
    }
  },
  { immediate: true },
) // immediate: true to run on mount
</script>
<template>
  <Dialog :open="isOpen" @update:open="closeModal">
    <DialogContent class="sm:max-w-[425px]">
      <form :validation-schema="validationSchema" @submit="onSubmit" class="gap-4 py-4">
        <DialogHeader class="mb-3">
          <DialogTitle>Add new technology</DialogTitle>
        </DialogHeader>
        <FormField v-slot="{ componentField }" name="name">
          <FormItem class="mb-2">
            <Label for="name" class="text-right"> Name </Label>
            <Input id="name" v-bind="componentField" class="col-span-3" />
          </FormItem>
        </FormField>
        <FormField v-slot="{ componentField }" name="language">
          <FormItem class="mb-2">
            <Label for="language" class="text-right"> Language </Label>
            <Input id="language" v-bind="componentField" class="col-span-3" />
          </FormItem>
        </FormField>
        <FormField v-slot="{ componentField }" name="description">
          <Label for="description" class="text-right"> Description </Label>
          <Textarea
            id="description"
            ref="textareaComponentRef"
            v-bind="componentField"
            :v-model="input"
            class="col-span-3"
          />
        </FormField>
        <DialogFooter class="mt-3">
          <Button :disabled="isDisabled" type="submit">
            <span v-if="isSubmitting" class="mr-2">
              <i class="i-lucide-loader-2 animate-spin"></i>
            </span>
            {{ isEdit ? 'Update' : 'Add' }}
          </Button>
        </DialogFooter>
      </form>
    </DialogContent>
  </Dialog>
</template>
