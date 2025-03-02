<script setup lang="ts"></script>

<template>
  <RouterView v-slot="{ Component, route }">
    <Suspense v-if="Component">
      <Component :is="Component" :key="route.name" />
    </Suspense>
  </RouterView>
</template>
