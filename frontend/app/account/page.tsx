"use client"

import { useState } from "react"
import { AnimatePresence, motion } from "framer-motion"
import { AuthLayout } from "@/components/brand/account/auth-layout"
import { LoginForm } from "@/components/brand/account/login-form"
import SignupForm from "@/components/brand/account/signup-form"


export default function AccountPage() {
  const [isLogin, setIsLogin] = useState(true)

  return (
    <AuthLayout
      title={isLogin ? "Welcome Back" : "Create Account"}
      subtitle={
        isLogin ? "Enter your credentials to access your account" : "Enter your information to create an account"
      }
    >
      <AnimatePresence mode="wait">
        <motion.div
          key={isLogin ? "login" : "signup"}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.2 }}
        >
          {isLogin ? (
            <LoginForm onToggleForm={() => setIsLogin(false)} />
          ) : (
            <SignupForm onToggleForm={() => setIsLogin(true)} />
          )}
        </motion.div>
      </AnimatePresence>
    </AuthLayout>
  )
}

