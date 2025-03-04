<script setup lang="ts">
import { ref } from 'vue'
import { 
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger 
} from '@/components/ui/collapsible'
const router = useRouter()
const { activeError } = storeToRefs(useErrorStore())
const isOpen = ref(false)

router.afterEach(() => {
  useErrorStore().setActiveError()
})
</script>

<template>
  <section class="h-screen w-full flex flex-col items-center justify-center bg-background px-4">
    <div class="max-w-md text-center space-y-6">
      <h1 class="text-9xl font-bold text-primary">{{ activeError?.code ?? 500 }}</h1>
      <h2 class="text-2xl font-semibold tracking-tight">
        {{ activeError?.message ?? 'Unknown Error has occurred' }}
      </h2>
      <p class="text-muted-foreground">
        {{ activeError?.description ?? 'Something went wrong' }}
      </p>

      <Collapsible v-if="activeError?.stack" v-model:open="isOpen" class="w-full">
        <CollapsibleTrigger class="flex items-center justify-center w-full px-4 py-2 rounded-md bg-muted hover:bg-muted/80 transition-colors text-sm">
          <span>{{ isOpen ? 'Hide' : 'Show' }} Error Details</span>
          <span class="ml-2">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
              :class="isOpen ? 'rotate-180' : ''"
              class="transition-transform"
            >
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </span>
        </CollapsibleTrigger>
        <CollapsibleContent class="mt-2">
          <div class="p-4 bg-muted/50 rounded-md text-left overflow-auto max-h-60 text-xs font-mono whitespace-pre-wrap">
            {{ activeError.stack }}
          </div>
        </CollapsibleContent>
      </Collapsible>

      <Button asChild>
        <router-link to="/" class="w-full"> Return Home </router-link>
      </Button>
    </div>
  </section>
</template>
