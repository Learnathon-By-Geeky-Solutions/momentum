"use client"

import { useState, useEffect } from "react"
import { Filter, Search, SlidersHorizontal } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"
import { ProductFilters } from "@/components/brand/products/product-filter"
import { ProductCard } from "@/components/brand/products/product-card"

interface Product {
  product_id: number
  product_name: string
  product_pic: string[]
  product_video: string[]
  category: string
  description: string
  order_size: string
  order_quantity: number
  quantity_unit: string
  price: number
  rating: number
  approved: boolean
}

export default function ProductsPage() {
  const [openFilter, setOpenFilter] = useState(false)
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchProducts() {
      try {
        const response = await fetch("/products/get-all-producs")
        if (!response.ok) {
          throw new Error("Failed to fetch products")
        }
        const data = await response.json()
        setProducts(data)
        setLoading(false)
      } catch (err) {
        setError(
          err instanceof Error ? err.message : "An unknown error occurred",
        )
        setLoading(false)
      }
    }

    fetchProducts()
  }, [])

  return (
    <div className="flex min-h-screen flex-col">
      <header className="sticky top-0 z-50 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-16 items-center gap-4">
          <div className="flex flex-1 items-center gap-4">
            <Sheet open={openFilter} onOpenChange={setOpenFilter}>
              <SheetTrigger asChild>
                <Button
                  variant="outline"
                  size="icon"
                  className="shrink-0 lg:hidden"
                >
                  <SlidersHorizontal className="h-5 w-5" />
                  <span className="sr-only">Filter products</span>
                </Button>
              </SheetTrigger>
              <SheetContent
                side="left"
                className="w-full border-r pr-0 sm:max-w-lg overflow-auto"
              >
                <ProductFilters />
              </SheetContent>
            </Sheet>
            <div className="flex w-full items-center gap-2">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                <Input
                  placeholder="Search products..."
                  className="w-full pl-9"
                />
              </div>
              <Button variant="outline" size="icon" className="shrink-0">
                <Filter className="h-4 w-4" />
                <span className="sr-only">Sort products</span>
              </Button>
            </div>
          </div>
        </div>
      </header>
      <div className="container flex-1 items-start py-6 lg:grid lg:grid-cols-[240px_1fr] lg:gap-10">
        <aside className="hidden lg:block">
          <ProductFilters />
        </aside>
        <div className="flex-1">
          <div className="flex items-center justify-between">
            <div className="flex gap-2">
              {["Electronics Devices", "5 Star Rating"].map((filter) => (
                <Button
                  key={filter}
                  variant="secondary"
                  size="sm"
                  className="h-7"
                >
                  {filter}
                  <span className="sr-only">Remove filter</span>
                </Button>
              ))}
            </div>
            <div className="text-sm text-muted-foreground">
              {products.length} Results found
            </div>
          </div>
          {loading ? (
            <div className="flex justify-center items-center h-64">
              <p>Loading products...</p>
            </div>
          ) : error ? (
            <div className="flex justify-center items-center h-64">
              <p className="text-red-500">Error: {error}</p>
            </div>
          ) : (
            <div className="mt-6 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
              {products.map((product) => (
                <ProductCard
                  key={product.product_id}
                  product={{
                    id: product.product_id.toString(),
                    product_name: product.product_name,
                    price: product.price,
                    category: product.category,
                    description: product.description,
                    rating: product.rating,
                    product_pic: product.product_pic,
                    product_video: product.product_video,
                    order_size: product.order_size,
                    order_quantity: product.order_quantity,
                    quantity_unit: product.quantity_unit,
                    approved: product.approved,
                  }}
                />
              ))}
            </div>
          )}
          {!loading && !error && products.length > 0 && (
            <Button className="mt-8 w-full" size="lg">
              Load More Products
            </Button>
          )}
        </div>
      </div>
    </div>
  )
}
