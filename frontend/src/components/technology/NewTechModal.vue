<script lang="ts" setup>
import { Icon } from '@iconify/vue'
import { useTechnologyMutationService } from '@/services'
import { toTypedSchema } from '@vee-validate/zod'
import { techSchemaCreate } from '@/schemas/technology.schema.ts'
import { useForm } from 'vee-validate'
import { FormField, FormItem } from '@/components/ui/form'

const { createMutation } = useTechnologyMutationService()
const { profile } = useAuthStore()

const router = useRouter()
const isOpen = computed(() => router.currentRoute.value.name === '/technologies/new')

const validationSchema = toTypedSchema(techSchemaCreate)

const { handleSubmit, isSubmitting, meta } = useForm({
  validationSchema,
  initialValues: {
    name: '',
    description: '',
    userId: profile.userId,
  },
})

const isDisabled = computed(() => isSubmitting.value || !meta.value.valid)

const openModal = () => {
  router.push('/technologies/new')
}
const closeModal = (isOpen: boolean | globalThis.ComputedRef<boolean>) => {
  if (!isOpen) {
    router.push('/technologies')
  }
}

const onSubmit = handleSubmit(async (values) => {
  await createMutation.mutateAsync(values, {
    onSettled: () => closeModal(!isOpen),
  })
})
</script>
<template>
  <Dialog :open="isOpen" @update:open="closeModal">
    <DialogTrigger as-child>
      <Button variant="outline" size="icon" class="bg-blue-100 mt-2" :onclick="openModal">
        <Icon icon="lucide:file-plus-2" width="20" height="20" />
      </Button>
    </DialogTrigger>
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
        <FormField v-slot="{ componentField }" name="description">
          <Label for="description" class="text-right"> Description </Label>
          <Textarea id="description" v-bind="componentField" class="col-span-3" />
        </FormField>
        <DialogFooter class="mt-3">
          <Button :disabled="isDisabled" type="submit">
            <span v-if="isSubmitting" class="mr-2">
              <i class="i-lucide-loader-2 animate-spin"></i>
            </span>
            Add
          </Button>
        </DialogFooter>
      </form>
    </DialogContent>
  </Dialog>
</template>
