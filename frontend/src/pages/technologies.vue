<script setup lang="ts">
import { useTechnologyService } from '@/services'
import { Icon } from '@iconify/vue'

const router = useRouter()

const navigateToHome = () => {
  router.push('/')
}

const { technologies, isLoading } = useTechnologyService()

const searchQuery = ref('')

const filterTechnologies = computed(
  () =>
    technologies.value?.filter(
      (tech) =>
        (tech.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
          tech?.description?.toLowerCase().includes(searchQuery.value.toLowerCase())) ??
        '',
    ) ?? [],
)
</script>

<template>
  <Card class="w-full h-full">
    <CardHeader class="pb-2">
      <div class="flex items-center mb-4">
        <Button
          variant="ghost"
          size="sm"
          @click="navigateToHome"
          class="mr-2 -ml-2 h-8"
          aria-label="Back to Home"
        >
          <Icon icon="lucide:arrow-left" width="18" height="18" />
          <span class="ml-1 text-sm text-muted-foreground">Back</span>
        </Button>
      </div>
      <CardTitle>Technologies</CardTitle>
      <CardDescription> Browse and search through your technology stack </CardDescription>
      <TechnologyActionBar :search="searchQuery" :isLoading />
    </CardHeader>
    <TechnologyLoading v-if="isLoading" />
    <CardContent v-else>
      <ScrollArea class="h-full">
        <div class="space-y-4">
          <template v-if="filterTechnologies.length > 0">
            <div v-for="tech in filterTechnologies" :key="tech.id" class="p-4 border rounded-lg">
              <div class="flex justify-between items-start">
                <div>
                  <h3 class="font-semibold text-lg">{{ tech.name || 'Unnamed Technology' }}</h3>
                  <Badge v-if="tech.language" class="mt-1" variant="secondary">
                    {{ tech.language }}
                  </Badge>
                </div>
                <Badge variant="outline"> {{ tech?.journalEntries ?? 0 }} entries </Badge>
              </div>
              <p v-if="tech.description" class="mt-2 text-sm text-gray-500">
                {{ tech.description }}
              </p>
            </div>
          </template>
          <div v-else class="text-center p-4 text-gray-500">
            No technologies found matching your filter.
          </div>
        </div>
      </ScrollArea>
    </CardContent>
    <router-view />
  </Card>
</template>
