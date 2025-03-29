import { Heart, Search, ShoppingCart, User } from "lucide-react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

export function MainHeader() {
  return (
    <div className="bg-primary text-white p-4">
      <div className="container mx-auto flex items-center justify-between gap-4">
        <Link href="/" className="text-2xl font-bold whitespace-nowrap">
          HANDICRAFT
        </Link>
        <div className="flex-1 max-w-xl">
          <div className="relative">
            <Input
              type="search"
              placeholder="Search for anything..."
              className="w-full pl-4 pr-10 py-2 rounded bg-white text-black"
            />
            <Button
              size="icon"
              variant="ghost"
              className="absolute right-0 top-0 h-full text-gray-400 hover:text-gray-600"
            >
              <Search className="h-4 w-4" />
            </Button>
          </div>
        </div>
        <div className="flex items-center gap-4">
          <Link href="/wishlist" className="hover:text-gray-200">
            <Heart className="h-6 w-6" />
          </Link>
          <Link href="/cart" className="relative hover:text-gray-200">
            <ShoppingCart className="h-6 w-6" />
            <span className="absolute -top-2 -right-2 bg-white text-blue-900 rounded-full w-5 h-5 flex items-center justify-center text-xs">
              0
            </span>
          </Link>
          <Link href="/account" className="hover:text-gray-200">
            <User className="h-6 w-6" />
          </Link>
        </div>
      </div>
    </div>
  )
}
