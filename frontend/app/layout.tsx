import type { Metadata } from "next"
import { Geist, Geist_Mono } from "next/font/google"
import "./globals.css"
import { MainHeader } from "@/components/brand/navbar/main-header"
import { Footer } from "@/components/brand/landing-page/footer"
import QueryProvider from "@/provider/query-provider"
import { AuthProvider } from "@/provider/useAuth"
import { Toaster } from "@/components/ui/sonner"

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
})

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
})

export const metadata: Metadata = {
  title: "Handicraft- A D2C Platform",
  description:
    "Handicraft is a D2C platform for artisans to sell their products.",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <QueryProvider>
        <AuthProvider>
          <body
            className={`${geistSans.variable} ${geistMono.variable} antialiased`}
          >
            <MainHeader />
            {children}
            <Footer />
            <Toaster />
          </body>
        </AuthProvider>
      </QueryProvider>
    </html>
  )
}
