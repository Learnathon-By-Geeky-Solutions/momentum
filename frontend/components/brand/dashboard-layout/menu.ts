import { Box, Cog, Home, ShoppingCart, User } from "lucide-react"

export const dashboardMenu = [
  {
    label: "Dashboard",
    href: "/dashboard",
    icon: Home,
    role: ["customer", "artisan"],
  },
  {
    label: "Products",
    href: "/dashboard/products",
    icon: Box,
    role: ["customer", "artisan"],
  },
  {
    label: "Orders",
    href: "/dashboard/orders",
    icon: ShoppingCart,
    role: ["customer", "artisan"],
  },
  {
    label: "Customers",
    href: "/dashboard/customers",
    icon: User,
    role: ["customer", "artisan"],
  },
  {
    label: "Settings",
    href: "/dashboard/settings",
    icon: Cog,
    role: ["customer", "artisan"],
  },
]
