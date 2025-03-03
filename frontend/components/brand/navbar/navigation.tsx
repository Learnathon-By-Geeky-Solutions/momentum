import { HeadphonesIcon, HelpCircle, ListChecks, Package } from "lucide-react"
import Link from "next/link"
import { MobileNav } from "./mobile-nav"
import { CategoryDropdown } from "./category-dropdown"

export function Navigation() {
  return (
    <div className="border-b bg-muted sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <div className="flex items-center gap-6">
          <MobileNav />
          <div className="hidden md:block">
            <CategoryDropdown />
          </div>
          <nav className="hidden md:flex items-center gap-6">
            <Link
              href="/track"
              className="flex items-center gap-2 text-sm text-gray-600 hover:text-primary transition-colors duration-200"
            >
              <Package className="h-4 w-4" />
              Track Order
            </Link>
            <Link
              href="/compare"
              className="flex items-center gap-2 text-sm text-gray-600 hover:text-primary transition-colors duration-200"
            >
              <ListChecks className="h-4 w-4" />
              Compare
            </Link>
            <Link
              href="/support"
              className="flex items-center gap-2 text-sm text-gray-600 hover:text-primary transition-colors duration-200"
            >
              <HeadphonesIcon className="h-4 w-4" />
              Customer Support
            </Link>
            <Link
              href="/help"
              className="flex items-center gap-2 text-sm text-gray-600 hover:text-primary transition-colors duration-200"
            >
              <HelpCircle className="h-4 w-4" />
              Need Help
            </Link>
          </nav>
        </div>
        <div className="hidden md:block text-sm font-medium">+1-202-555-0104</div>
      </div>
    </div>
  )
}

