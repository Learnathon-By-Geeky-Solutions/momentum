"use client"
import React, { useState } from "react"
import { dashboardMenu } from "./menu"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import { useAuth } from "@/provider/useAuth"
import { Menu, X } from "lucide-react"

export default function DashboardNavbar() {
  const pathname = usePathname()
  const { userRole } = useAuth()
  const [isOpen, setIsOpen] = useState(false)

  return (
    <div className="bg-white border-b shadow-sm">
      <div className="container mx-auto">
        <nav className="relative">
          {/* Mobile menu button */}
          <div className="flex items-center justify-between h-16 md:hidden">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="p-2 text-gray-600 hover:text-primary"
            >
              {isOpen ? (
                <X className="h-6 w-6" />
              ) : (
                <Menu className="h-6 w-6" />
              )}
            </button>
          </div>

          {/* Desktop menu */}
          <div className="hidden md:flex md:items-center h-16">
            <div className="flex items-center space-x-4 overflow-x-auto scrollbar-hide">
              {dashboardMenu
                .filter((item) => item.role.includes(userRole!))
                .map((item) => (
                  <Link
                    key={item.label}
                    href={item.href}
                    className={cn(
                      "flex items-center gap-3 px-3 py-2 text-sm font-medium transition-colors whitespace-nowrap",
                      pathname === item.href
                        ? "text-primary border-b-2 border-primary"
                        : "text-gray-600 hover:text-primary hover:border-b-2 hover:border-primary/50"
                    )}
                  >
                    <item.icon className="h-4 w-4" />
                    <span>{item.label}</span>
                  </Link>
                ))}
            </div>
          </div>

          {/* Mobile menu */}
          {isOpen && (
            <div className="absolute top-16 left-0 right-0 bg-white border-b shadow-sm md:hidden">
              <div className="flex flex-col py-2">
                {dashboardMenu
                  .filter((item) => item.role.includes(userRole!))
                  .map((item) => (
                    <Link
                      key={item.label}
                      href={item.href}
                      onClick={() => setIsOpen(false)}
                      className={cn(
                        "flex items-center gap-3 px-4 py-3 text-sm font-medium transition-colors",
                        pathname === item.href
                          ? "text-primary bg-primary/5"
                          : "text-gray-600 hover:text-primary hover:bg-primary/5"
                      )}
                    >
                      <item.icon className="h-4 w-4" />
                      <span>{item.label}</span>
                    </Link>
                  ))}
              </div>
            </div>
          )}
        </nav>
      </div>
    </div>
  )
}
