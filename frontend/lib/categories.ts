import { Laptop, Monitor, Gamepad, ComputerIcon as Desktop, type LucideIcon } from "lucide-react"

export interface CategoryBrand {
  name: string
  href: string
  image: string
}

export interface SubCategory {
  name: string
  href: string
  icon?: LucideIcon
  brands?: CategoryBrand[]
  description?: string
}

export interface Category {
  name: string
  href: string
  icon: LucideIcon
  subcategories?: SubCategory[]
}

export const categories: Category[] = [
  {
    name: "Desktop",
    href: "/category/desktop",
    icon: Desktop,
    subcategories: [
      {
        name: "Gaming Desktop",
        href: "/category/gaming-desktop",
        icon: Gamepad,
        brands: [
          { name: "Alienware", href: "/brand/alienware", image: "/placeholder.svg?height=40&width=40" },
          { name: "ROG", href: "/brand/rog", image: "/placeholder.svg?height=40&width=40" },
          { name: "MSI", href: "/brand/msi", image: "/placeholder.svg?height=40&width=40" },
        ],
      },
    ],
  },
  {
    name: "Laptop",
    href: "/category/laptop",
    icon: Laptop,
    subcategories: [
      {
        name: "All Laptop",
        href: "/category/all-laptop",
        icon: Laptop,
      },
      {
        name: "Gaming Laptop",
        href: "/category/gaming-laptop",
        icon: Gamepad,
        brands: [
          { name: "Lenovo", href: "/brand/lenovo", image: "/placeholder.svg?height=40&width=40" },
          { name: "Asus", href: "/brand/asus", image: "/placeholder.svg?height=40&width=40" },
          { name: "MSI", href: "/brand/msi", image: "/placeholder.svg?height=40&width=40" },
          { name: "HP", href: "/brand/hp", image: "/placeholder.svg?height=40&width=40" },
          { name: "Acer", href: "/brand/acer", image: "/placeholder.svg?height=40&width=40" },
          { name: "Gigabyte", href: "/brand/gigabyte", image: "/placeholder.svg?height=40&width=40" },
          { name: "Thunderobot", href: "/brand/thunderobot", image: "/placeholder.svg?height=40&width=40" },
          { name: "Dell", href: "/brand/dell", image: "/placeholder.svg?height=40&width=40" },
        ],
      },
      {
        name: "Premium Ultrabook",
        href: "/category/premium-ultrabook",
        icon: Laptop,
      },
    ],
  },
  {
    name: "Laptop Accessories",
    href: "/category/laptop-accessories",
    icon: Monitor,
    subcategories: [
      {
        name: "Laptop Bag",
        href: "/category/laptop-bag",
      },
      {
        name: "Laptop Accessories",
        href: "/category/accessories",
      },
    ],
  },
]

