"use client"
import React from "react"
import { dashboardMenu } from "./menu"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"

export default function DashboardNavbar() {
  const pathname = usePathname()
  return (
    <div className="bg-gray-50 py-4 border-b">
      <nav className="flex items-center gap-4 container mx-auto p-2">
        {dashboardMenu.map((item) => (
          <Link
            key={item.label}
            href={item.href}
            className={cn(
              "flex items-center gap-2 text-sm text-gray-600 px-4 py-2 rounded-lg hover:bg-primary hover:text-white",
              pathname === item.href && "bg-primary text-white",
            )}
          >
            <item.icon className="h-4 w-4 " />
            {item.label}
          </Link>
        ))}
      </nav>
    </div>
  )
}
