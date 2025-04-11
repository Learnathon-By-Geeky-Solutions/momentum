import { Box, Cog, Home, ShoppingCart, User, ChartBar } from "lucide-react"

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
    role: ["artisan"],
  },
  {
    label: "Inventory",
    href: "/dashboard/inventory",
    icon: Box,
    role: ["artisan"],
  },
  {
    label: "Analytics",
    href: "/dashboard/analytics",
    icon: ChartBar,
    role: ["artisan"],
  },
  {
    label: "Discounts & Coupons",
    href: "/dashboard/discounts",
    icon: ChartBar,
    role: ["artisan"],
  },
  {
    label: "Reviews & Feedback",
    href: "/dashboard/reviews",
    icon: ChartBar,
    role: ["artisan"],
  },
  {
    label: "Settings",
    href: "/dashboard/settings",
    icon: Cog,
    role: ["customer", "artisan"],
  },
]
