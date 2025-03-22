"use client"

import {
  ChevronRight,
  Laptop,
  Smartphone,
  Headphones,
  Gamepad,
  Camera,
  Tv,
  Watch,
  Navigation,
  WatchIcon as Watch2,
} from "lucide-react"
import Link from "next/link"
import { cn } from "@/lib/utils"

const categories = [
  {
    name: "Computer & Laptop",
    icon: Laptop,
    href: "/category/computer-laptop",
  },
  {
    name: "Computer Accessories",
    icon: Laptop,
    href: "/category/computer-accessories",
  },
  { name: "SmartPhone", icon: Smartphone, href: "/category/smartphone" },
  { name: "Headphone", icon: Headphones, href: "/category/headphone" },
  {
    name: "Mobile Accessories",
    icon: Smartphone,
    href: "/category/mobile-accessories",
  },
  { name: "Gaming Console", icon: Gamepad, href: "/category/gaming-console" },
  { name: "Camera & Photo", icon: Camera, href: "/category/camera-photo" },
  { name: "TV & Homes Appliances", icon: Tv, href: "/category/tv-appliances" },
  { name: "Watchs & Accessories", icon: Watch, href: "/category/watches" },
  {
    name: "GPS & Navigation",
    icon: Navigation,
    href: "/category/gps-navigation",
  },
  {
    name: "Wearable Technology",
    icon: Watch2,
    href: "/category/wearable-tech",
  },
]

interface CategoryListProps {
  className?: string
}

export function CategoryList({ className }: Readonly<CategoryListProps>) {
  return (
    <div className={cn("flex flex-col", className)}>
      {categories.map((category) => (
        <Link
          key={category.name}
          href={category.href}
          className="flex items-center justify-between p-2 hover:bg-gray-100 rounded-lg group"
        >
          <div className="flex items-center gap-3">
            <category.icon className="h-5 w-5" />
            <span>{category.name}</span>
          </div>
          <ChevronRight className="h-4 w-4 opacity-0 group-hover:opacity-100 transition-opacity" />
        </Link>
      ))}
    </div>
  )
}
