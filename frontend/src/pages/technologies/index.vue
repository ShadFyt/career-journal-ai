<script setup lang="ts">
const router = useRouter()
import { Icon } from '@iconify/vue'

const navigateToHome = () => {
  router.push('/')
}

const mockTechnologies = ref([
  {
    id: '1',
    name: 'Vue.js',
    description: 'A progressive JavaScript framework for building user interfaces',
    language: 'Javascript',
    journalEntries: [],
  },
  {
    id: '2',
    name: 'React',
    description: 'A JavaScript library for building user interfaces',
    language: 'Javascript',
    journalEntries: [],
  },
  {
    id: '3',
    name: 'Python',
    description: 'A high-level programming language for general-purpose programming',
    language: 'Python',
    journalEntries: [],
  },
  {
    id: '4',
    name: 'Node.js',
    description: 'A runtime environment for building server-side applications',
    language: 'Javascript',
    journalEntries: [],
  },
  {
    id: '5',
    name: 'Django',
    description: 'A high-level Python web framework',
    language: 'Python',
    journalEntries: [],
  },
  {
    id: '6',
    name: 'Flask',
    description: 'A micro web framework for Python',
    language: 'Python',
    journalEntries: [],
  },
  {
    id: '7',
    name: 'Express.js',
    description: 'A Node.js framework for building APIs',
    language: 'Javascript',
    journalEntries: [],
  },
])

const searchQuery = ref('')

const filterTechnologies = computed(() =>
  mockTechnologies.value.filter(
    (tech) =>
      tech.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      tech.description.toLowerCase().includes(searchQuery.value.toLowerCase()),
  ),
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
      <Input placeholder="Filter technologies..." v-model="searchQuery" class="mt-2" />
    </CardHeader>
    <CardContent>
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
                <Badge variant="outline"> {{ (tech?.journalEntries || []).length }} entries </Badge>
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
  </Card>
</template>
