<script setup lang="ts">
import { onErrorCaptured } from 'vue'
import { storeToRefs } from 'pinia'
import { useErrorStore } from '@/stores/error'
import { MainLayout } from '@/components/layout'
import AppErrorPage from '@/components/app-error/AppErrorPage.vue'

const { activeError } = storeToRefs(useErrorStore())
const { setActiveError } = useErrorStore()

onErrorCaptured((error) => {
  console.error(`[App] Uncaught error: ${error}`)
  setActiveError(error)
})
</script>

<template>
  <MainLayout>
    <AppErrorPage v-if="activeError !== null" />
    <template v-else>
      <RouterView v-slot="{ Component, route }">
        <Suspense v-if="Component">
          <Component :is="Component" :key="route.name" />
        </Suspense>
      </RouterView>
    </template>
  </MainLayout>
</template>
