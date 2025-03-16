<script setup lang="ts">
import { onErrorCaptured, onMounted, ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useErrorStore } from '@/stores/error'
import { useAuthStore } from '@/stores/auth'
import { MainLayout } from '@/components/layout'
import AppErrorPage from '@/components/app-error/AppErrorPage.vue'
import { Icon } from '@iconify/vue'
import { useTimeoutFn } from '@vueuse/core'

const { activeError } = storeToRefs(useErrorStore())
const { setActiveError } = useErrorStore()
const { checkSession } = useAuthStore()
const showLoader = ref(false)
const { start } = useTimeoutFn(() => (showLoader.value = true), 100, { immediate: false })

const { isLoading } = storeToRefs(useAuthStore())

onErrorCaptured((error) => {
  console.error(`[App] Uncaught error: ${error}`)
  setActiveError(error)
})

onMounted(async () => {
  if (isLoading.value === true) {
    start()
  } else {
    showLoader.value = false
  }
  await checkSession()
})
</script>

<template>
  <MainLayout>
    <!-- Show loading spinner while checking auth -->
    <div v-if="isLoading && showLoader" class="flex h-screen w-full items-center justify-center">
      <div class="flex flex-col items-center gap-4">
        <Icon icon="lucide:loader-2" class="h-12 w-12 animate-spin text-primary" />
        <p class="text-lg font-medium">Loading...</p>
      </div>
    </div>
    <AppErrorPage v-else-if="activeError !== null" />
    <template v-else>
      <RouterView v-slot="{ Component, route }">
        <Suspense v-if="Component">
          <Component :is="Component" :key="route.name" />
        </Suspense>
      </RouterView>
    </template>
  </MainLayout>
</template>
