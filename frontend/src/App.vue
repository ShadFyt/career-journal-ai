<script setup lang="ts">
const { activeError } = storeToRefs(useErrorStore())
</script>

<template>
  <AppErrorPage v-if="activeError !== null" />
  <RouterView v-else v-slot="{ Component, route }">
    <Suspense v-if="Component">
      <Component :is="Component" :key="route.name" />
    </Suspense>
  </RouterView>
</template>
