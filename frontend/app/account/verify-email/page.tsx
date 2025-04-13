"use client"

import { useEffect, useState } from "react"
import { useSearchParams } from "next/navigation"
import { CheckCircle2, XCircle, Loader2 } from "lucide-react"
import { motion } from "framer-motion"
import Link from "next/link"

import { Button } from "@/components/ui/button"
import { AuthLayout } from "@/components/brand/account/auth-layout"
import api from "@/lib/axios"

export default function VerifyEmailPage() {
  const searchParams = useSearchParams()
  const token = searchParams.get("token")

  const [status, setStatus] = useState<"loading" | "success" | "error">(
    "loading",
  )
  const [message, setMessage] = useState("")

  useEffect(() => {
    const verifyEmail = async () => {
      if (!token) {
        setStatus("error")
        setMessage("Invalid verification link. No token provided.")
        return
      }

      try {
        const response = await api.post(`/auth/verify-email?token=${token}`)
        setStatus("success")
        setMessage(
          response.data.message || "Your email has been successfully verified!",
        )
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
      } catch (error) {
        setStatus("error")
        setMessage(
          "Email verification failed. The link may be expired or invalid.",
        )
      }
    }

    verifyEmail()
  }, [token])

  return (
    <AuthLayout
      title="Email Verification"
      subtitle="Verifying your email address"
    >
      <div className="flex flex-col items-center justify-center space-y-6 text-center">
        {status === "loading" && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex flex-col items-center space-y-4"
          >
            <Loader2 className="h-16 w-16 text-primary animate-spin" />
            <p className="text-lg">Verifying your email address...</p>
          </motion.div>
        )}

        {status === "success" && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex flex-col items-center space-y-4"
          >
            <CheckCircle2 className="h-16 w-16 text-green-500" />
            <h2 className="text-xl font-semibold">Email Verified!</h2>
            <p className="text-muted-foreground">{message}</p>
          </motion.div>
        )}

        {status === "error" && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex flex-col items-center space-y-4"
          >
            <XCircle className="h-16 w-16 text-red-500" />
            <h2 className="text-xl font-semibold">Verification Failed</h2>
            <p className="text-muted-foreground">{message}</p>
          </motion.div>
        )}

        <div className="pt-4">
          <Link href="/account">
            <Button className="w-full">
              {status === "success" ? "Continue to Login" : "Back to Account"}
            </Button>
          </Link>
        </div>
      </div>
    </AuthLayout>
  )
}
