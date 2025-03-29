import { Button } from "@/components/ui/button"
import Image from "next/image"
import Link from "next/link"

const categories = [
  { id: 1, name: "Jewelry", image: "/momentum/hero-craft-1.jpg" },
  { id: 2, name: "Pottery", image: "/momentum/hero-craft-1.jpg" },
  { id: 3, name: "Textiles", image: "/momentum/hero-craft-1.jpg" },
  {
    id: 4,
    name: "Wood Crafts",
    image: "/momentum/hero-craft-1.jpg",
  },
  { id: 5, name: "Paintings", image: "/momentum/hero-craft-1.jpg" },
  { id: 6, name: "Sculptures", image: "/momentum/hero-craft-1.jpg" },
]

export function CategoriesShowcase() {
  return (
    <section className="py-16">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl font-serif font-bold text-center mb-12">
          Discover Artisanal Categories
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          {categories.map((category) => (
            <div
              key={category.id}
              className="group relative overflow-hidden rounded-lg"
            >
              <Image
                src={category.image || "/momentum/hero-craft-1.jpg"}
                alt={category.name}
                width={200}
                height={200}
                className="w-full h-48 object-cover transition-transform duration-300 group-hover:scale-110"
              />
              <div className="absolute inset-0 bg-black bg-opacity-40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                <h3 className="text-white font-semibold text-lg">
                  {category.name}
                </h3>
              </div>
            </div>
          ))}
        </div>
        <div className="text-center mt-8">
          <Button variant="outline" asChild>
            <Link href="/products">Explore All Categories</Link>
          </Button>
        </div>
      </div>
    </section>
  )
}
