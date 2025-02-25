"use client"

import { useRef } from "react"
import { ChevronLeft, ChevronRight } from "lucide-react"

import { Button } from "@/components/ui/button"
import { ProductCard } from "./product-card"


const relatedProducts = [
  {
    id: "1",
    title: "Bose Sport Earbuds - Wireless Earphones",
    price: 1500,
    rating: 4.5,
    reviews: 738,
    image: "https://www.digitaltrends.com/wp-content/uploads/2024/10/m4-mac-pro-8.jpg?resize=1000%2C600&p=1",
  },
  {
    id: "2",
    title: "Samsung Electronics Samsung Galaxy S21 5G",
    price: 1500,
    rating: 4.8,
    reviews: 526,
    image: "https://www.digitaltrends.com/wp-content/uploads/2024/10/m4-mac-pro-8.jpg?resize=1000%2C600&p=1",
  },
  {
    id: "3",
    title: "TOZO T6 True Wireless Earbuds Bluetooth Headphones",
    price: 1500,
    rating: 4.7,
    reviews: 423,
    image: "https://www.digitaltrends.com/wp-content/uploads/2024/10/m4-mac-pro-8.jpg?resize=1000%2C600&p=1",
    badge: "BEST DEALS" as const,
  },
  {
    id: "4",
    title: "Dell Optiplex 7000x7480 All-in-One Computer Monitor",
    price: 1500,
    rating: 4.6,
    reviews: 412,
    image: "https://www.digitaltrends.com/wp-content/uploads/2024/10/m4-mac-pro-8.jpg?resize=1000%2C600&p=1",
  },
  {
    id: "5",
    title: "Sony DSCHX8 High Zoom Point & Shoot Camera",
    price: 1500,
    rating: 4.5,
    reviews: 389,
    image: "https://www.digitaltrends.com/wp-content/uploads/2024/10/m4-mac-pro-8.jpg?resize=1000%2C600&p=1",
  },
]

export function RelatedProducts() {
  const containerRef = useRef<HTMLDivElement>(null)

  const scroll = (direction: "left" | "right") => {
    if (containerRef.current) {
      const { scrollLeft, clientWidth } = containerRef.current
      const scrollTo = direction === "left" ? scrollLeft - clientWidth : scrollLeft + clientWidth

      containerRef.current.scrollTo({
        left: scrollTo,
        behavior: "smooth",
      })
    }
  }

  return (
    <div className="relative mt-6">
      <div className="absolute right-0 top-0 flex gap-2">
        <Button variant="outline" size="icon" onClick={() => scroll("left")}>
          <ChevronLeft className="h-4 w-4" />
          <span className="sr-only">Scroll left</span>
        </Button>
        <Button variant="outline" size="icon" onClick={() => scroll("right")}>
          <ChevronRight className="h-4 w-4" />
          <span className="sr-only">Scroll right</span>
        </Button>
      </div>
      <div ref={containerRef} className="mt-16 flex gap-6 overflow-x-auto pb-4 pt-2 scrollbar-hide">
        {relatedProducts.map((product) => (
          <div key={product.id} className="w-[300px] shrink-0">
            <ProductCard product={product} />
          </div>
        ))}
      </div>
    </div>
  )
}

