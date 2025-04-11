import DashboardNavbar from "@/components/brand/dashboard-layout/dashboard-navbar"
import React from "react"

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div>
      <DashboardNavbar />
      {children}
    </div>
  )
}
