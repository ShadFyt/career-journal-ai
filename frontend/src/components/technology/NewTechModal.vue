<script lang="ts" setup>
import { Icon } from '@iconify/vue'

const router = useRouter()
const isOpen = computed(() => router.currentRoute.value.name === '/technologies/new')
const openModal = () => {
  router.push('/technologies/new')
}
const closeModal = (isOpen: boolean) => {
  if (!isOpen) {
    router.push('/technologies')
  }
}
</script>
<template>
  <Dialog :open="isOpen" @update:open="closeModal">
    <DialogTrigger as-child>
      <Button variant="outline" size="icon" class="bg-blue-100 mt-2" :onclick="openModal">
        <Icon icon="lucide:file-plus-2" width="20" height="20" />
      </Button>
    </DialogTrigger>
    <DialogContent class="sm:max-w-[425px]">
      <DialogHeader>
        <DialogTitle>Add new technology</DialogTitle>
      </DialogHeader>
      <div class="grid gap-4 py-4">
        <div class="grid grid-cols-4 items-center gap-4">
          <Label for="name" class="text-right"> Name </Label>
          <Input id="name" value="Pedro Duarte" class="col-span-3" />
        </div>
        <div class="grid grid-cols-4 items-center gap-4">
          <Label for="description" class="text-right"> Description </Label>
          <Input id="description" class="col-span-3" />
        </div>
      </div>
      <DialogFooter>
        <Button type="submit"> Add </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
