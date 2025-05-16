<script setup lang="ts">
import Toaster from '@/components/ui/toast/Toaster.vue'
import { VueQueryDevtools } from '@tanstack/vue-query-devtools'

import { onErrorCaptured, onMounted, ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useErrorStore } from '@/stores/error'
import { useAuthStore } from '@/stores/auth'
import { MainLayout } from '@/components/layout'
import AppErrorPage from '@/components/app-error/AppErrorPage.vue'
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
  if (isLoading.value) {
    start()
  } else {
    showLoader.value = false
  }
  await checkSession()
})
</script>

<template>
  <Toaster />
  <MainLayout>
    <!-- Show loading spinner while checking auth -->
    <Loader full-screen size="xl" v-if="isLoading && showLoader" />
    <AppErrorPage v-else-if="activeError !== null" />
    <template v-else>
      <RouterView v-slot="{ Component, route }">
        <Suspense v-if="Component">
          <Component :is="Component" :key="route.name" />
        </Suspense>
      </RouterView>
    </template>
  </MainLayout>
  <VueQueryDevtools />
</template>
