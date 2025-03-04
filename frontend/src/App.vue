<script setup lang="ts">
const { activeError } = storeToRefs(useErrorStore())
const { setActiveError } = useErrorStore()

onErrorCaptured((error) => {
  console.error(`[App] Uncaught error: ${error}`)
  setActiveError(error)
})
</script>

<template>
  <AppErrorPage v-if="activeError !== null" />
  <RouterView v-else v-slot="{ Component, route }">
    <Suspense v-if="Component">
      <Component :is="Component" :key="route.name" />
    </Suspense>
  </RouterView>
</template>
