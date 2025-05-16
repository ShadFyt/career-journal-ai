<script setup lang="ts">
import { InvalidUiElementError } from '@/errors'
import { useTechnologyFetchService, useTechnologyMutationService } from '@/services'
import { Icon } from '@iconify/vue'

const router = useRouter()

const navigateToHome = () => {
  router.push('/')
}

const navigateToEdit = (e: MouseEvent) => {
  const currentTarget = e.currentTarget
  if (currentTarget instanceof HTMLElement) {
    router.push('/technologies/edit/' + currentTarget.id)
    return
  }
  const error = new InvalidUiElementError('navigate to edit', currentTarget)
  console.error(error.message, { eventTarget: currentTarget })
  throw error
}

const { technologies, isLoading } = useTechnologyFetchService()
const { deleteMutation } = useTechnologyMutationService()

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

const isNotEmpty = computed(() => filterTechnologies.value.length > 0)

const handleDelete = (e: MouseEvent) => {
  const currentTarget = e.currentTarget
  if (currentTarget instanceof HTMLElement) {
    deleteMutation.mutate(currentTarget.id)
    return
  }
  const error = new InvalidUiElementError('delete technology', currentTarget)
  console.error(error.message, { eventTarget: currentTarget })
  throw error
}
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
      <TechnologyActionBar v-model:search="searchQuery" :isLoading />
    </CardHeader>
    <TechnologyLoading v-if="isLoading" />
    <CardContent v-else>
      <ScrollArea class="h-full">
        <section class="space-y-4">
          <template v-if="isNotEmpty">
            <article
              v-for="tech in filterTechnologies"
              :key="tech.id"
              class="p-4 border rounded-lg"
            >
              <div class="flex flex-row">
                <header class="flex-1">
                  <div class="flex justify-between items-start">
                    <hgroup>
                      <h3 class="text-lg font-bold">
                        {{ tech.name || 'Unnamed Technology' }}
                      </h3>
                      <p v-if="tech.language" class="mt-1">
                        {{ tech.language }}
                      </p>
                    </hgroup>
                    <p class="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full">
                      {{ tech?.usageCount ?? 0 }} {{ tech?.usageCount === 1 ? 'entry' : 'entries' }}
                    </p>
                  </div>
                  <p v-if="tech.description" class="mt-2 text-sm text-gray-500">
                    {{ tech.description }}
                  </p>
                </header>
                <aside class="border-l border-gray-200 ml-3 flex flex-col justify-center gap-3">
                  <Button
                    :id="tech.id"
                    variant="outline"
                    size="sm"
                    class="ml-2 h-8"
                    :aria-label="`edit ${tech.name}`"
                    @click="navigateToEdit"
                  >
                    <span class="text-sm text-muted-foreground">Edit</span>
                    <Icon icon="lucide:edit" width="18" height="18" />
                  </Button>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Button
                        :id="tech.id"
                        variant="destructive"
                        size="sm"
                        class="ml-2 h-8"
                        :aria-label="`delete ${tech.name}`"
                        :disabled="tech.usageCount > 0"
                        @click="handleDelete"
                      >
                        <span class="text-sm text-muted-foreground">Delete</span>
                        <Icon icon="lucide:delete" width="18" height="18" />
                      </Button>
                    </TooltipTrigger>
                    <TooltipContent>
                      <p>
                        {{
                          tech.usageCount > 0
                            ? 'Unable to delete technologies that are used in journal entries'
                            : 'delete technology'
                        }}
                      </p>
                    </TooltipContent>
                  </Tooltip>
                </aside>
              </div>
            </article>
          </template>
          <div v-else class="text-center p-4 text-gray-500">
            No technologies found matching your filter.
          </div>
        </section>
      </ScrollArea>
    </CardContent>
    <router-view />
  </Card>
</template>
