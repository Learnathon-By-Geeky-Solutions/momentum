"use client"

import { useEffect, useState } from "react"
import { useSearchParams } from "next/navigation"
import { motion } from "framer-motion"
import { CheckCircle2, XCircle, Loader2, Eye, EyeOff } from "lucide-react"
import Link from "next/link"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { AuthLayout } from "@/components/brand/account/auth-layout"
import api from "@/lib/axios"

export default function ResetPasswordPage() {
  const searchParams = useSearchParams()
  const token = searchParams.get("token")

  const [newPassword, setNewPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")
  const [showPassword, setShowPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [status, setStatus] = useState<"idle" | "success" | "error">("idle")
  const [message, setMessage] = useState("")

  useEffect(() => {
    if (!token) {
      setStatus("error")
      setMessage("Invalid reset link. No token provided.")
    }
  }, [token])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    if (newPassword !== confirmPassword) {
      setStatus("error")
      setMessage("Passwords do not match")
      setIsLoading(false)
      return
    }

    try {
      const response = await api.post("/auth/reset-password", {
        token,
        new_password: newPassword,
      })
      setStatus("success")
      setMessage(
        response.data.message || "Your password has been successfully reset!",
      )
    } catch (err) {
      setStatus("error")
      setMessage("Password reset failed. The link may be expired or invalid.")
      console.error("Password reset failed:", err)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <AuthLayout
      title="Reset Your Password"
      subtitle="Enter your new password below"
    >
      {status === "idle" && token && (
        <motion.form
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-4"
          onSubmit={handleSubmit}
        >
          <div className="space-y-2">
            <Label htmlFor="new-password">New Password</Label>
            <div className="relative">
              <Input
                id="new-password"
                type={showPassword ? "text" : "password"}
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                required
                className="pr-10"
              />
              <button
                type="button"
                className="absolute right-3 top-1/2 -translate-y-1/2"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
              </button>
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="confirm-password">Confirm Password</Label>
            <Input
              id="confirm-password"
              type={showPassword ? "text" : "password"}
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
          </div>

          <Button type="submit" className="w-full" disabled={isLoading}>
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Resetting Password
              </>
            ) : (
              "Reset Password"
            )}
          </Button>
        </motion.form>
      )}

      {status === "success" && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-4 text-center"
        >
          <CheckCircle2 className="mx-auto h-12 w-12 text-green-500" />
          <h3 className="text-xl font-semibold">Password Reset Successful</h3>
          <p>{message}</p>
          <Button asChild className="w-full">
            <Link href="/account">Log In</Link>
          </Button>
        </motion.div>
      )}

      {status === "error" && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-4 text-center"
        >
          <XCircle className="mx-auto h-12 w-12 text-red-500" />
          <h3 className="text-xl font-semibold">Password Reset Failed</h3>
          <p>{message}</p>
          <Button asChild variant="outline" className="w-full">
            <Link href="/account/forgot-password">Try Again</Link>
          </Button>
        </motion.div>
      )}
    </AuthLayout>
  )
}
