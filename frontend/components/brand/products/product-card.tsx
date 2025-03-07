import Image from "next/image"
import { Heart, ShoppingCart } from "lucide-react"

import { cn } from "@/lib/utils"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter } from "@/components/ui/card"

interface Product {
  id: string
  title: string
  price: number
  originalPrice?: number
  rating: number
  reviews: number
  image: string
  badge?:"HOT" | "BEST DEALS" | "SALE" | "NEW" | "TOP RATED"
  discount?: number
}

interface ProductCardProps {
  product: Product
}

export function ProductCard({ product }: ProductCardProps) {
  return (
    <Card className="group relative overflow-hidden">
      <CardContent className="p-0">
        {product.badge && (
          <Badge
            className={cn(
              "absolute left-4 top-4 z-10",
              product.badge === "HOT" && "bg-red-500",
              product.badge === "SALE" && "bg-green-500",
              product.badge === "BEST DEALS" && "bg-blue-500",
            )}
          >
            {product.badge}
          </Badge>
        )}
        {product.discount && (
          <Badge className="absolute right-4 top-4 z-10 bg-orange-500">{product.discount}% OFF</Badge>
        )}
        <div className="relative aspect-square overflow-hidden">
          <Image
            src={product.image || "/placeholder.svg"}
            alt={product.title}
            fill
            className="object-cover transition-transform group-hover:scale-105"
          />
          <div className="absolute inset-0 bg-black/40 opacity-0 transition-opacity group-hover:opacity-100" />
          <div className="absolute inset-0 flex items-center justify-center gap-2 opacity-0 group-hover:opacity-100">
            <Button size="icon" variant="secondary">
              <Heart className="h-4 w-4" />
              <span className="sr-only">Add to wishlist</span>
            </Button>
            <Button size="icon" variant="secondary">
              <ShoppingCart className="h-4 w-4" />
              <span className="sr-only">Add to cart</span>
            </Button>
          </div>
        </div>
      </CardContent>
      <CardFooter className="flex-col items-start gap-2 p-4">
        <div className="flex items-center gap-1">
          {[...Array(5)].map((_, i) => (
            <svg
              key={i}
              className={cn(
                "h-4 w-4",
                i < Math.floor(product.rating) ? "fill-primary" : "fill-muted stroke-muted-foreground",
              )}
              viewBox="0 0 24 24"
            >
              <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z" />
            </svg>
          ))}
          <span className="text-sm text-muted-foreground">({product.reviews})</span>
        </div>
        <h3 className="line-clamp-2 text-sm font-medium">{product.title}</h3>
        <div className="flex items-center gap-2">
          <span className="text-lg font-bold">${product.price}</span>
          {product.originalPrice && (
            <span className="text-sm text-muted-foreground line-through">${product.originalPrice}</span>
          )}
        </div>
      </CardFooter>
    </Card>
  )
}

