<script setup lang="ts">
const { isErrorActive } = storeToRefs(useErrorStore())
</script>

<template>
  <AppErrorPage v-if="isErrorActive" />
  <RouterView v-else v-slot="{ Component, route }">
    <Suspense v-if="Component">
      <Component :is="Component" :key="route.name" />
    </Suspense>
  </RouterView>
</template>
