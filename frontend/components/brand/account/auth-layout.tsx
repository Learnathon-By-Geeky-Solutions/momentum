import type React from "react"

interface AuthLayoutProps {
  children: React.ReactNode
  title: string
  subtitle: string
  showImage?: boolean
}

export function AuthLayout({
  children,
  title,
  subtitle,
  showImage = true,
}: Readonly<AuthLayoutProps>) {
  return (
    <div className="grid min-h-[90vh] w-full lg:grid-cols-2">
      <div className="flex items-center justify-center px-8 py-12 lg:px-12">
        <div className="mx-auto w-full max-w-7xl">
          <div className="mb-8">
            <div className="h-8 w-8">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="h-full w-full"
              >
                <path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z" />
                <path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z" />
              </svg>
            </div>
            <h1 className="mt-6 text-3xl font-bold">{title}</h1>
            <p className="mt-2 text-sm text-muted-foreground">{subtitle}</p>
          </div>
          {children}
        </div>
      </div>
      {showImage && (
        <div className="hidden bg-secondary lg:block">
          <div className="flex h-full flex-col justify-between p-12">
            <div className="space-y-2">
              <h2 className="text-3xl font-bold">
                The simplest way to manage your workforce
              </h2>
              <p className="text-primary">
                Enter your credentials to access your account
              </p>
            </div>
            <div className="h-100">
              <img src="/hero-craft-1.jpg" alt="Auth" />
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
