<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from '@/components/ui/toast'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
import { z } from 'zod'
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import { useAuthStore } from '@/stores/auth'
import { Icon } from '@iconify/vue'

const router = useRouter()
const { toast } = useToast()
const authStore = useAuthStore()

// Define form validation schema
const formSchema = toTypedSchema(
  z.object({
    email: z.string().email('Please enter a valid email address'),
    password: z.string().min(6, 'Password must be at least 6 characters'),
  }),
)

// Set up form with validation
const { handleSubmit } = useForm({
  validationSchema: formSchema,
  initialValues: {
    email: '',
    password: '',
  },
})

const isLoading = ref(false)
const loginError = ref('')

// Form submission handler
const onSubmit = handleSubmit(async (values) => {
  try {
    isLoading.value = true
    loginError.value = ''
    console.log('values', values)

    // await authStore.login(values.email, values.password)
    toast({
      title: 'Login successful',
      description: 'Welcome back!',
    })
    router.push('/')
  } catch (error: any) {
    loginError.value = error?.message || 'Failed to login. Please try again.'
    toast({
      title: 'Login failed',
      description: loginError.value,
      variant: 'destructive',
    })
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <div class="flex min-h-screen w-full items-center justify-center bg-gray-50 px-4 py-12">
    <Card class="w-full max-w-md shadow-xl">
      <CardHeader class="space-y-1">
        <CardTitle class="text-2xl font-bold text-center">Sign in</CardTitle>
        <CardDescription class="text-center">
          Enter your credentials to access your account
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form :validation-schema="formSchema" @submit="onSubmit">
          <div class="space-y-4">
            <FormField v-slot="{ componentField }" name="email">
              <FormItem>
                <FormLabel>Email</FormLabel>
                <FormControl>
                  <div class="relative">
                    <Icon
                      icon="lucide:mail"
                      class="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground h-5 w-5"
                    />
                    <Input
                      v-bind="componentField"
                      type="email"
                      placeholder="name@example.com"
                      class="pl-10"
                      autocomplete="email"
                    />
                  </div>
                </FormControl>
                <FormMessage />
              </FormItem>
            </FormField>

            <FormField v-slot="{ componentField }" name="password">
              <FormItem>
                <FormLabel>Password</FormLabel>
                <FormControl>
                  <div class="relative">
                    <Icon
                      icon="lucide:lock"
                      class="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground h-5 w-5"
                    />
                    <Input
                      v-bind="componentField"
                      type="password"
                      placeholder="••••••••"
                      class="pl-10"
                      autocomplete="current-password"
                    />
                  </div>
                </FormControl>
                <FormMessage />
              </FormItem>
            </FormField>

            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <input
                  type="checkbox"
                  id="remember"
                  class="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary"
                />
                <label for="remember" class="text-sm text-gray-600">Remember me</label>
              </div>
              <a href="#" class="text-sm font-medium text-primary hover:text-primary/80"
                >Forgot password?</a
              >
            </div>

            <Button type="submit" class="w-full" :disabled="isLoading">
              <Icon v-if="isLoading" icon="lucide:loader-2" class="mr-2 h-4 w-4 animate-spin" />
              {{ isLoading ? 'Signing in...' : 'Sign in' }}
            </Button>
          </div>
        </form>

        <div class="mt-6">
          <div class="relative">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-gray-300"></div>
            </div>
            <div class="relative flex justify-center text-sm">
              <span class="bg-white px-2 text-gray-500">Or continue with</span>
            </div>
          </div>

          <div class="mt-6 grid grid-cols-2 gap-3">
            <Button variant="outline" class="w-full" disabled>
              <Icon icon="lucide:github" class="mr-2 h-4 w-4" />
              GitHub
            </Button>
            <Button variant="outline" class="w-full" disabled>
              <Icon icon="lucide:google" class="mr-2 h-4 w-4" />
              Google
            </Button>
          </div>
        </div>
      </CardContent>
      <CardFooter>
        <p class="text-center text-sm text-gray-600 mt-2 w-full">
          Don't have an account?
          <router-link to="/register" class="font-medium text-primary hover:text-primary/80">
            Create one
          </router-link>
        </p>
      </CardFooter>
    </Card>
  </div>
</template>
