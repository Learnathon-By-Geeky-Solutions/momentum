"use client"

import Image from "next/image"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"

const products = [
  {
    id: 1,
    name: "Handwoven Basket",
    artisan: "Emma Craft",
    price: "$45",
    image: "/placeholder.svg?height=200&width=200",
    category: "Weaving",
  },
  {
    id: 2,
    name: "Ceramic Vase",
    artisan: "Potter John",
    price: "$60",
    image: "/placeholder.svg?height=200&width=200",
    category: "Pottery",
  },
  {
    id: 3,
    name: "Wooden Sculpture",
    artisan: "Carver Mike",
    price: "$120",
    image: "/placeholder.svg?height=200&width=200",
    category: "Woodwork",
  },
  {
    id: 4,
    name: "Macrame Wall Hanging",
    artisan: "Knot Master",
    price: "$80",
    image: "/placeholder.svg?height=200&width=200",
    category: "Textile Arts",
  },
]

export function FeaturedProducts() {
  return (
    <section className="py-16 bg-white">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl font-serif font-bold text-center mb-12 animate-fade-in-up">
          Handpicked Artisanal Treasures
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {products.map((product) => (
            <Card
              key={product.id}
              className="group hover:shadow-lg transition-all duration-300 ease-in-out"
            >
              <CardContent className="p-4">
                <div className="relative h-56 mb-4 overflow-hidden rounded-md">
                  <Image
                    src={product.image || "/placeholder.svg"}
                    alt={product.name}
                    layout="fill"
                    objectFit="cover"
                    className="group-hover:scale-110 transition-transform duration-300"
                  />
                  <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
                    <span className="text-white font-medium text-lg">
                      {product.category}
                    </span>
                  </div>
                </div>
                <h3 className="font-semibold text-lg mb-1">{product.name}</h3>
                <p className="text-muted-foreground text-sm mb-2">
                  {product.artisan}
                </p>
                <div className="flex items-center justify-between">
                  <span className="font-bold text-primary text-lg">
                    {product.price}
                  </span>
                  <Button
                    variant="outline"
                    size="sm"
                    className="opacity-0 group-hover:opacity-100 transition-opacity duration-300"
                  >
                    View Details
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
        <div className="text-center mt-12">
          <Button
            variant="outline"
            size="lg"
            className="hover:bg-primary hover:text-white transition-colors"
          >
            Explore All Categories
          </Button>
        </div>
      </div>
    </section>
  )
}
