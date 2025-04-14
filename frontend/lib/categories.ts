import {
  Brush,
  Gem,
  Home,
  Shirt,
  Leaf,
  Utensils,
  Baby,
  FileText,
  Globe,
  type LucideIcon,
} from "lucide-react"

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
    name: "Handmade Crafts",
    href: "/category/handmade-crafts",
    icon: Brush,
    subcategories: [
      {
        name: "Pottery & Ceramics",
        href: "/category/pottery-ceramics",
        icon: Brush,
        brands: [
          {
            name: "Pottery",
            href: "/category/pottery",
            image: "/images/pottery.png",
          },
          {
            name: "Ceramics",
            href: "/category/ceramics",
            image: "/images/ceramics.png",
          },
        ],
      },
      {
        name: "Woodworking & Carving",
        href: "/category/woodworking",
        icon: Brush,
        brands: [
          {
            name: "Woodworking",
            href: "/category/woodworking",
            image: "/images/woodworking.png",
          },
          {
            name: "Carving",
            href: "/category/carving",
            image: "/images/carving.png",
          },
        ],
      },
      {
        name: "Glass Art",
        href: "/category/glass-art",
        icon: Brush,
        brands: [
          {
            name: "Glass Art",
            href: "/category/glass-art",
            image: "/images/glass-art.png",
          },
        ],
      },
    ],
  },
  {
    name: "Jewelry & Accessories",
    href: "/category/jewelry",
    icon: Gem,
    subcategories: [
      {
        name: "Handmade Necklaces",
        href: "/category/necklaces",
        icon: Gem,
        brands: [
          {
            name: "Necklaces",
            href: "/category/necklaces",
            image: "/images/necklaces.png",
          },
        ],
      },
      {
        name: "Earrings",
        href: "/category/earrings",
        icon: Gem,
      },
      {
        name: "Bracelets & Bangles",
        href: "/category/bracelets",
        icon: Gem,
      },
    ],
  },
  {
    name: "Home Décor",
    href: "/category/home-decor",
    icon: Home,
    subcategories: [
      {
        name: "Handmade Candles",
        href: "/category/handmade-candles",
        icon: Home,
      },
      {
        name: "Wall Art & Paintings",
        href: "/category/wall-art",
        icon: Home,
      },
      {
        name: "Decorative Lamps",
        href: "/category/decorative-lamps",
        icon: Home,
      },
    ],
  },
  {
    name: "Fashion & Apparel",
    href: "/category/fashion",
    icon: Shirt,
    subcategories: [
      {
        name: "Handwoven Fabrics",
        href: "/category/handwoven-fabrics",
        icon: Shirt,
      },
      {
        name: "Knitted & Crocheted Items",
        href: "/category/knitted-items",
        icon: Shirt,
      },
    ],
  },
  {
    name: "Beauty & Personal Care",
    href: "/category/beauty",
    icon: Leaf,
    subcategories: [
      {
        name: "Handmade Soaps",
        href: "/category/handmade-soaps",
        icon: Leaf,
      },
      {
        name: "Essential Oils & Perfumes",
        href: "/category/essential-oils",
        icon: Leaf,
      },
    ],
  },
  {
    name: "Food & Beverages",
    href: "/category/food",
    icon: Utensils,
    subcategories: [
      {
        name: "Artisanal Chocolates",
        href: "/category/chocolates",
        icon: Utensils,
      },
      {
        name: "Handmade Baked Goods",
        href: "/category/baked-goods",
        icon: Utensils,
      },
    ],
  },
  {
    name: "Furniture & Home Essentials",
    href: "/category/furniture",
    icon: Home,
    subcategories: [
      {
        name: "Custom Wooden Furniture",
        href: "/category/wooden-furniture",
        icon: Home,
      },
      {
        name: "Handwoven Baskets",
        href: "/category/baskets",
        icon: Home,
      },
    ],
  },
  {
    name: "Toys & Kids’ Items",
    href: "/category/toys",
    icon: Baby,
    subcategories: [
      {
        name: "Handmade Plush Toys",
        href: "/category/plush-toys",
        icon: Baby,
      },
      {
        name: "Wooden Toys",
        href: "/category/wooden-toys",
        icon: Baby,
      },
    ],
  },
  {
    name: "Stationery & Office Supplies",
    href: "/category/stationery",
    icon: FileText,
    subcategories: [
      {
        name: "Handmade Journals",
        href: "/category/journals",
        icon: FileText,
      },
      {
        name: "Custom Wax Seals",
        href: "/category/wax-seals",
        icon: FileText,
      },
    ],
  },
  {
    name: "Cultural & Traditional Art",
    href: "/category/cultural-art",
    icon: Globe,
    subcategories: [
      {
        name: "Tribal & Indigenous Crafts",
        href: "/category/tribal-crafts",
        icon: Globe,
      },
      {
        name: "Ethnic Accessories",
        href: "/category/ethnic-accessories",
        icon: Globe,
      },
    ],
  },
]
