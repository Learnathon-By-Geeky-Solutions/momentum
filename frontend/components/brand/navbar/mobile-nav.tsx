"use client"

import {
  Menu,
  X,
  ShoppingCart,
  User,
  Package,
  ListChecks,
  HeadphonesIcon,
  HelpCircle,
} from "lucide-react"
import Link from "next/link"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"
import { MobileCategoryMenu } from "./mobile-category-menu"

export function MobileNav() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <Sheet open={isOpen} onOpenChange={setIsOpen}>
      <SheetTrigger asChild>
        <Button variant="ghost" size="icon" className="md:hidden">
          <Menu className="h-6 w-6" />
          <span className="sr-only">Toggle menu</span>
        </Button>
      </SheetTrigger>
      <SheetContent side="left" className="w-[min(calc(100vw-2rem),350px)] p-0">
        <div className="flex flex-col h-full bg-white">
          <div className="p-4 border-b bg-primary text-primary-foreground">
            <div className="flex items-center justify-between">
              <span className="text-lg font-bold">Menu</span>
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setIsOpen(false)}
                className="text-primary-foreground hover:text-primary-foreground/90"
              >
                <X className="h-6 w-6" />
              </Button>
            </div>
          </div>
          <div className="flex-grow overflow-auto">
            <div className="p-4 border-b">
              <h2 className="font-semibold mb-2">Categories</h2>
              <MobileCategoryMenu />
            </div>
            <nav className="p-4 space-y-2">
              <Link
                href="/track"
                className="flex items-center gap-3 p-2 hover:bg-gray-100 rounded-lg transition-colors duration-200"
              >
                <Package className="h-5 w-5 text-gray-500" />
                <span>Track Order</span>
              </Link>
              <Link
                href="/compare"
                className="flex items-center gap-3 p-2 hover:bg-gray-100 rounded-lg transition-colors duration-200"
              >
                <ListChecks className="h-5 w-5 text-gray-500" />
                <span>Compare</span>
              </Link>
              <Link
                href="/support"
                className="flex items-center gap-3 p-2 hover:bg-gray-100 rounded-lg transition-colors duration-200"
              >
                <HeadphonesIcon className="h-5 w-5 text-gray-500" />
                <span>Customer Support</span>
              </Link>
              <Link
                href="/help"
                className="flex items-center gap-3 p-2 hover:bg-gray-100 rounded-lg transition-colors duration-200"
              >
                <HelpCircle className="h-5 w-5 text-gray-500" />
                <span>Need Help</span>
              </Link>
            </nav>
          </div>
          <div className="border-t p-4 bg-gray-50">
            <div className="flex justify-around">
              <Link
                href="/cart"
                className="flex flex-col items-center text-sm text-gray-600 hover:text-primary transition-colors duration-200"
              >
                <ShoppingCart className="h-6 w-6 mb-1" />
                Cart
              </Link>
              <Link
                href="/account"
                className="flex flex-col items-center text-sm text-gray-600 hover:text-primary transition-colors duration-200"
              >
                <User className="h-6 w-6 mb-1" />
                Account
              </Link>
            </div>
          </div>
        </div>
      </SheetContent>
    </Sheet>
  )
}
