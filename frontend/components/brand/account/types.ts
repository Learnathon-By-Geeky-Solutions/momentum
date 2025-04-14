import { z } from "zod"

export const signupSchema = z
  .object({
    full_name: z.string().min(2, {
      message: "Full name must be at least 2 characters.",
    }),
    email: z.string().email("Invalid email address"),
    phone: z.string().min(1, "Phone number is required"),
    address: z.string().min(1, "Address is required"),
    password: z.string().min(8, "Password must be at least 8 characters"),
    confirmPassword: z.string().min(1, "Confirm password is required"),
    terms: z.boolean().refine((val) => val === true, {
      message: "You must agree to the terms and conditions",
    }),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: "Passwords do not match",
    path: ["confirmPassword"],
  })

export type SignupData = z.infer<typeof signupSchema>
export type SignupBody = Omit<SignupData, "confirmPassword" | "terms"> & {
  username: string
}
