"use client"

import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"

import { Button } from "@/components/ui/button"
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { useState } from "react"
import { useMutation } from "@tanstack/react-query"
import api from "@/lib/axios"
import { SignupBody, SignupData, signupSchema } from "./types"
import { AxiosError } from "axios"
import { Eye, EyeOff } from "lucide-react"

export default function SignupForm({
  onToggleForm,
}: Readonly<{ onToggleForm: () => void }>) {
  const [showPassword, setShowPassword] = useState(false)
  const form = useForm<SignupData>({
    resolver: zodResolver(signupSchema),
    defaultValues: {
      full_name: "",
      email: "",
      phone: "",
      address: "",
      password: "",
      confirmPassword: "",
      terms: false,
    },
  })

  const [verificationSent, setVerificationSent] = useState(false)

  const signupMutation = useMutation({
    mutationKey: ["signup"],
    mutationFn: async (data: SignupBody) => {
      return api.post("/auth/register", data)
    },
    onSuccess: () => {
      setVerificationSent(true)
      form.reset()
    },
    onError: (error: AxiosError) => {
      // eslint-disable-next-line @typescript-eslint/ban-ts-comment
      // @ts-ignore
      form.setError("", { message: error.response?.data?.detail })
    },
  })

  function onSubmit(data: SignupData) {
    const body = {
      username: data.email,
      email: data.email,
      password: data.password,
      full_name: data.full_name,
      phone: data.phone,
      address: data.address,
    }
    signupMutation.mutate(body)
  }

  if (verificationSent) {
    return (
      <div className="space-y-6 text-center">
        <div className="rounded-lg bg-green-50 p-6 border border-green-200">
          <h3 className="text-xl font-semibold text-green-800 mb-2">
            Verification Email Sent
          </h3>
          <p className="text-green-700">
            We&apos;ve sent a verification link to{" "}
            <strong>{form.getValues("email")}</strong>. Please check your inbox
            and click the link to activate your account.
          </p>
        </div>
        <p className="text-sm text-muted-foreground">
          Didn&apos;t receive the email? Check your spam folder
        </p>
        <Button onClick={onToggleForm} className="mt-4">
          Return to Login
        </Button>
      </div>
    )
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="full_name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Full Name</FormLabel>
              <FormControl>
                <Input placeholder="John Doe" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input type="email" placeholder="name@example.com" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <div className="grid grid-cols-2 gap-4">
          <FormField
            control={form.control}
            name="phone"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Phone Number</FormLabel>
                <FormControl>
                  <Input placeholder="+1234567890" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="address"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Address</FormLabel>
                <FormControl>
                  <Input placeholder="Your address" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>
        <div className="grid grid-cols-2 gap-4">
          <FormField
            control={form.control}
            name="password"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Password</FormLabel>
                <FormControl>
                  <div className="relative">
                    <Input
                      type={showPassword ? "text" : "password"}
                      {...field}
                      placeholder="Enter your password"
                    />
                    <button
                      className="absolute inset-y-0 right-0 flex items-center pr-3"
                      type="button"
                      onClick={() => setShowPassword((prev) => !prev)}
                    >
                      {showPassword ? (
                        <EyeOff className="h-4 w-4 text-muted-foreground cursor-pointer transition duration-300" />
                      ) : (
                        <Eye className="h-4 w-4 text-muted-foreground cursor-pointer transition duration-300" />
                      )}
                    </button>
                  </div>
                </FormControl>
                <FormDescription>
                  Must be at least 8 characters long
                </FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="confirmPassword"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Confirm Password</FormLabel>
                <FormControl>
                  <Input
                    type="password"
                    {...field}
                    placeholder="Confirm your password"
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>

        <FormField
          control={form.control}
          name="terms"
          render={({ field }) => (
            <FormItem className="flex flex-row items-start space-x-3 space-y-0 rounded-md border p-4">
              <FormControl>
                <input
                  type="checkbox"
                  checked={field.value}
                  onChange={field.onChange}
                  className="h-4 w-4 rounded border-gray-300"
                />
              </FormControl>
              <div className="space-y-1 leading-none">
                <FormLabel>Accept terms and conditions</FormLabel>
                <FormDescription>
                  You agree to our Terms of Service and Privacy Policy.
                </FormDescription>
              </div>
              <FormMessage />
            </FormItem>
          )}
        />

        <Button
          type="submit"
          className="w-full"
          disabled={signupMutation.isPending}
        >
          {signupMutation.isPending ? "Signing up..." : "Sign up"}
        </Button>
      </form>
    </Form>
  )
}
