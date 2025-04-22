<script setup lang="ts"></script>

<template>
  <div class="space-y-4 mb-4">
    <div
      v-for="i in 4"
      :key="`skeleton-${i}`"
      class="bg-card rounded-lg shadow overflow-hidden p-4 mx-6"
    >
      <div class="flex flex-col md:flex-row gap-4">
        <div class="flex-1 space-y-4 mr-1">
          <div class="flex flex-row justify-between">
            <Skeleton class="h-6 w-1/4" />
            <Skeleton class="h-6 w-1/6" />
          </div>
          <Skeleton class="h-5 w-full" />
        </div>
      </div>
    </div>
  </div>
</template>
