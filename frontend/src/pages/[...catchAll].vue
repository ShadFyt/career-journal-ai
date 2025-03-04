<script setup lang="ts">
const route = useRoute()
const currentPath = route.path.slice(1)
useErrorStore().setActiveError({
  message: `${currentPath} not found`,
  code: 404,
  description: 'The page you are looking for does not exist or has been moved.',
})
</script>

<template>
  <div></div>
</template>
