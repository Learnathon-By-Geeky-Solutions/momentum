import Link from "next/link"
import { Facebook, Instagram, Twitter } from "lucide-react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

export function Footer() {
  return (
    <footer className="bg-muted text-muted-foreground">
      <div className="container mx-auto px-6 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-primary">HandiCraft</h3>
            <p className="text-sm">
              Connecting artisans with art lovers worldwide. Discover unique,
              handcrafted treasures and support skilled creators.
            </p>
            <div className="flex space-x-4">
              <a href="#" className="text-muted-foreground hover:text-primary">
                <Facebook size={20} />
              </a>
              <a href="#" className="text-muted-foreground hover:text-primary">
                <Instagram size={20} />
              </a>
              <a href="#" className="text-muted-foreground hover:text-primary">
                <Twitter size={20} />
              </a>
            </div>
          </div>

          <div>
            <h4 className="text-sm font-semibold mb-4">Shop</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <Link href="#" className="hover:text-primary">
                  All Categories
                </Link>
              </li>
              <li>
                <Link href="#" className="hover:text-primary">
                  Featured Products
                </Link>
              </li>
              <li>
                <Link href="#" className="hover:text-primary">
                  New Arrivals
                </Link>
              </li>
              <li>
                <Link href="#" className="hover:text-primary">
                  Best Sellers
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="text-sm font-semibold mb-4">Sell</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <Link href="#" className="hover:text-primary">
                  Become an Artisan
                </Link>
              </li>
              <li>
                <Link href="#" className="hover:text-primary">
                  Seller Guidelines
                </Link>
              </li>
              <li>
                <Link href="#" className="hover:text-primary">
                  Success Stories
                </Link>
              </li>
              <li>
                <Link href="#" className="hover:text-primary">
                  Artisan Resources
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="text-sm font-semibold mb-4">Help</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <Link href="#" className="hover:text-primary">
                  FAQ
                </Link>
              </li>
              <li>
                <Link href="#" className="hover:text-primary">
                  Shipping Info
                </Link>
              </li>
              <li>
                <Link href="#" className="hover:text-primary">
                  Returns & Refunds
                </Link>
              </li>
              <li>
                <Link href="#" className="hover:text-primary">
                  Contact Us
                </Link>
              </li>
            </ul>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-muted-foreground/20">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="text-sm mb-4 md:mb-0">
              &copy; 2025 HandiCraft. All rights reserved.
              <p>
                Developed by{" "}
                <span className="text-primary font-semibold">
                  Team MOMENTUM
                </span>
              </p>
            </div>
            <div className="flex space-x-4 text-sm">
              <Link href="#" className="hover:text-primary">
                Terms of Service
              </Link>
              <Link href="#" className="hover:text-primary">
                Privacy Policy
              </Link>
              <Link href="#" className="hover:text-primary">
                Cookie Policy
              </Link>
            </div>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-muted-foreground/20">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="text-sm mb-4 md:mb-0">
              Stay updated with new artisans and unique crafts
            </div>
            <div className="flex w-full md:w-auto">
              <Input
                type="email"
                placeholder="Enter your email"
                className="rounded-r-none md:w-64"
              />
              <Button type="submit" className="rounded-l-none">
                Subscribe
              </Button>
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}
