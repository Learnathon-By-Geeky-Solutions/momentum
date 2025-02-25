"use client"

import { useState } from "react"
import { Heart, Share2, ShoppingCart } from "lucide-react"

import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { ProductGallery } from "@/components/brand/products/product-gallery"
import { RelatedProducts } from "@/components/brand/products/related-product"

const product = {
  id: "1",
  title: "2020 Apple MacBook Pro with Apple M1 Chip (13-inch, 8GB RAM, 256GB SSD Storage) - Space Gray",
  sku: "SKU567",
  brand: "Apple",
  category: "Electronics",
  price: 1699,
  originalPrice: 1999,
  discount: 21,
  rating: 4.8,
  reviews: 21671,
  stock: true,
  images: [
    "https://www.digitaltrends.com/wp-content/uploads/2024/10/m4-mac-pro-8.jpg?resize=1000%2C600&p=1",
    "https://www.digitaltrends.com/wp-content/uploads/2024/10/m4-mac-pro-8.jpg?resize=1000%2C600&p=1",
    "https://www.digitaltrends.com/wp-content/uploads/2024/10/m4-mac-pro-8.jpg?resize=1000%2C600&p=1",
    "https://www.digitaltrends.com/wp-content/uploads/2024/10/m4-mac-pro-8.jpg?resize=1000%2C600&p=1",
    "https://www.digitaltrends.com/wp-content/uploads/2024/10/m4-mac-pro-8.jpg?resize=1000%2C600&p=1",
    "https://www.digitaltrends.com/wp-content/uploads/2024/10/m4-mac-pro-8.jpg?resize=1000%2C600&p=1",
  ],
  colors: ["Space Gray", "Silver"],
  displayOptions: ["14-inch Liquid Retina XDR display", "16-inch Liquid Retina XDR display"],
  memoryOptions: ["16GB unified memory", "32GB unified memory"],
  storageOptions: ["512GB SSD", "1TB SSD", "2TB SSD"],
  description: `The most powerful MacBook Pro ever is here. With the blazing-fast M1 Pro or M1 Max 
    chip — the first Apple silicon designed for pros — you get groundbreaking performance and amazing 
    battery life. Add to that a stunning Liquid Retina XDR display, the best camera and audio ever in 
    a Mac notebook, and all the ports you need. The first notebook of its kind, this MacBook Pro is a 
    beast. M1 Pro takes the exceptional performance of the M1 architecture to a whole new level for pro users.`,
  features: [
    "Free 1 Year Warranty",
    "Free Shipping & Fastest Delivery",
    "100% Money-back guarantee",
    "24/7 Customer support",
    "Secure payment method",
  ],
  shipping: {
    courier: "2-4 days, free shipping",
    local: "up to one week, $19.00",
    ground: "4-6 days, $29.00",
    express: "3-4 days, $39.00",
  },
}

export default function ProductPage() {
  const [selectedColor, setSelectedColor] = useState(product.colors[0])
  const [quantity, setQuantity] = useState(1)
  const [isWishlisted, setIsWishlisted] = useState(false)

  return (
    <div className="container py-10">
      <div className="lg:grid lg:grid-cols-2 lg:gap-x-8">
        <ProductGallery images={product.images} />

        {/* Product info */}
        <div className="mt-10 px-4 sm:mt-16 sm:px-0 lg:mt-0">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-1">
              {[...Array(5)].map((_, i) => (
                <svg
                  key={i}
                  className={cn(
                    "h-5 w-5",
                    i < Math.floor(product.rating) ? "fill-primary" : "fill-muted stroke-muted-foreground",
                  )}
                  viewBox="0 0 24 24"
                >
                  <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z" />
                </svg>
              ))}
            </div>
            <p className="text-sm text-muted-foreground">({product.reviews} User feedback)</p>
          </div>

          <h1 className="mt-4 text-2xl font-bold tracking-tight sm:text-3xl">{product.title}</h1>

          <div className="mt-4">
            <div className="flex items-center gap-4">
              <p className="text-3xl font-bold">${product.price}</p>
              {product.originalPrice && (
                <>
                  <p className="text-lg text-muted-foreground line-through">${product.originalPrice}</p>
                  <Badge variant="secondary">{product.discount}% OFF</Badge>
                </>
              )}
            </div>
            <div className="mt-4 space-y-6">
              <div className="flex items-center gap-4">
                <p className="text-sm text-muted-foreground">SKU: {product.sku}</p>
                <Separator orientation="vertical" className="h-4" />
                <p className="text-sm text-muted-foreground">Brand: {product.brand}</p>
                <Separator orientation="vertical" className="h-4" />
                <p className="text-sm text-muted-foreground">Category: {product.category}</p>
              </div>

              <div className="space-y-4">
                <div className="flex items-center gap-4">
                  <span className="text-sm font-medium">Color:</span>
                  <div className="flex gap-2">
                    {product.colors.map((color) => (
                      <button
                        key={color}
                        onClick={() => setSelectedColor(color)}
                        className={cn(
                          "h-8 w-8 rounded-full border-2",
                          color === "Space Gray" ? "bg-gray-900" : "bg-gray-100",
                          selectedColor === color ? "ring-2 ring-primary ring-offset-2" : "border-transparent",
                        )}
                      >
                        <span className="sr-only">{color}</span>
                      </button>
                    ))}
                  </div>
                </div>

                <div className="space-y-2">
                  <span className="text-sm font-medium">Display:</span>
                  <Select>
                    <SelectTrigger>
                      <SelectValue placeholder="Select display" />
                    </SelectTrigger>
                    <SelectContent>
                      {product.displayOptions.map((option) => (
                        <SelectItem key={option} value={option}>
                          {option}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <span className="text-sm font-medium">Memory:</span>
                  <Select>
                    <SelectTrigger>
                      <SelectValue placeholder="Select memory" />
                    </SelectTrigger>
                    <SelectContent>
                      {product.memoryOptions.map((option) => (
                        <SelectItem key={option} value={option}>
                          {option}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <span className="text-sm font-medium">Storage:</span>
                  <Select>
                    <SelectTrigger>
                      <SelectValue placeholder="Select storage" />
                    </SelectTrigger>
                    <SelectContent>
                      {product.storageOptions.map((option) => (
                        <SelectItem key={option} value={option}>
                          {option}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="flex items-center gap-4">
                  <div className="flex items-center">
                    <Button variant="outline" size="icon" onClick={() => setQuantity(Math.max(1, quantity - 1))}>
                      -
                    </Button>
                    <input
                      type="number"
                      value={quantity}
                      onChange={(e) => setQuantity(Math.max(1, Number.parseInt(e.target.value) || 1))}
                      className="w-16 border-y border-input bg-transparent px-3 py-2 text-center text-sm"
                    />
                    <Button variant="outline" size="icon" onClick={() => setQuantity(quantity + 1)}>
                      +
                    </Button>
                  </div>
                  <p className="text-sm text-muted-foreground">
                    {product.stock ? (
                      <span className="text-green-600">In Stock</span>
                    ) : (
                      <span className="text-red-600">Out of Stock</span>
                    )}
                  </p>
                </div>
              </div>

              <div className="flex flex-col gap-4 sm:flex-row">
                <Button className="flex-1 gap-2">
                  <ShoppingCart className="h-4 w-4" />
                  Add to Cart
                </Button>
                <Button variant="secondary" className="flex-1">
                  Buy Now
                </Button>
              </div>

              <div className="flex items-center gap-4">
                <Button variant="outline" size="sm" className="gap-2" onClick={() => setIsWishlisted(!isWishlisted)}>
                  <Heart className={cn("h-4 w-4", isWishlisted && "fill-red-500 text-red-500")} />
                  Add to Wishlist
                </Button>
                <Button variant="outline" size="sm" className="gap-2">
                  <Share2 className="h-4 w-4" />
                  Share
                </Button>
              </div>
            </div>
          </div>

          <Tabs defaultValue="description" className="mt-8">
            <TabsList className="grid w-full grid-cols-4">
              <TabsTrigger value="description">Description</TabsTrigger>
              <TabsTrigger value="features">Features</TabsTrigger>
              <TabsTrigger value="shipping">Shipping</TabsTrigger>
              <TabsTrigger value="reviews">Reviews</TabsTrigger>
            </TabsList>
            <TabsContent value="description" className="mt-4">
              <div className="prose max-w-none">
                <p>{product.description}</p>
              </div>
            </TabsContent>
            <TabsContent value="features" className="mt-4">
              <ul className="space-y-4">
                {product.features.map((feature) => (
                  <li key={feature} className="flex items-center gap-2">
                    <svg
                      className="h-5 w-5 text-green-500"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                    >
                      <path d="M20 6L9 17l-5-5" />
                    </svg>
                    {feature}
                  </li>
                ))}
              </ul>
            </TabsContent>
            <TabsContent value="shipping" className="mt-4">
              <div className="space-y-4">
                <div className="grid gap-4 sm:grid-cols-2">
                  {Object.entries(product.shipping).map(([method, info]) => (
                    <Card key={method} className="p-4">
                      <h3 className="font-medium capitalize">{method.replace("_", " ")} Shipping</h3>
                      <p className="text-sm text-muted-foreground">{info}</p>
                    </Card>
                  ))}
                </div>
              </div>
            </TabsContent>
            <TabsContent value="reviews" className="mt-4">
              <div className="text-center text-muted-foreground">Reviews coming soon...</div>
            </TabsContent>
          </Tabs>
        </div>
      </div>

      <div className="mt-16">
        <h2 className="text-xl font-bold">Related Products</h2>
        <RelatedProducts />
      </div>
    </div>
  )
}


