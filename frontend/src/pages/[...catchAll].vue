<script setup lang="ts">
import { Button } from '@/components/ui/button'
</script>

<template>
  <div class="h-screen w-full flex flex-col items-center justify-center bg-background px-4">
    <div class="max-w-md text-center space-y-6">
      <h1 class="text-9xl font-bold text-primary">404</h1>
      <h2 class="text-2xl font-semibold tracking-tight">Page Not Found</h2>
      <p class="text-muted-foreground">
        The page you're looking for doesn't exist or has been moved.
      </p>
      <Button asChild>
        <router-link to="/" class="w-full"> Return Home </router-link>
      </Button>
    </div>
  </div>
</template>
