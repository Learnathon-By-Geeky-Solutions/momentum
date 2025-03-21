"use client"

import { useState } from "react"
import Image from "next/image"
import { ChevronLeft, ChevronRight } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"

const artisans = [
  {
    id: 1,
    name: "Emma Craft",
    specialty: "Textile Artist",
    bio: "Creating beautiful handwoven textiles for over 20 years.",
    image: "/placeholder.svg?height=100&width=100",
  },
  {
    id: 2,
    name: "John Potter",
    specialty: "Ceramic Artist",
    bio: "Specializing in unique, functional pottery inspired by nature.",
    image: "/placeholder.svg?height=100&width=100",
  },
  {
    id: 3,
    name: "Sarah Woodwork",
    specialty: "Woodcarver",
    bio: "Crafting intricate wooden sculptures and home decor items.",
    image: "/placeholder.svg?height=100&width=100",
  },
  {
    id: 4,
    name: "Michael Silver",
    specialty: "Jewelry Maker",
    bio: "Designing and creating bespoke silver jewelry pieces.",
    image: "/placeholder.svg?height=100&width=100",
  },
]

export function FeaturedArtisans() {
  const [currentIndex, setCurrentIndex] = useState(0)

  const nextSlide = () => {
    setCurrentIndex((prevIndex) => (prevIndex + 1) % artisans.length)
  }

  const prevSlide = () => {
    setCurrentIndex((prevIndex) => (prevIndex - 1 + artisans.length) % artisans.length)
  }

  return (
    <section className="py-16">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl font-serif font-bold text-center mb-12">Meet Our Talented Artisans</h2>
        <div className="relative">
          <div className="flex overflow-hidden">
            {artisans.map((artisan, index) => (
              <Card
                key={artisan.id}
                className={`flex-shrink-0 w-full md:w-1/2 lg:w-1/4 p-4 transition-all duration-300 ease-in-out transform ${
                  index === currentIndex ? "scale-100 opacity-100" : "scale-95 opacity-60"
                }`}
              >
                <CardContent className="flex flex-col items-center text-center">
                  <Image
                    src={artisan.image || "/placeholder.svg"}
                    alt={artisan.name}
                    width={100}
                    height={100}
                    className="rounded-full mb-4"
                  />
                  <h3 className="font-semibold text-lg mb-1">{artisan.name}</h3>
                  <p className="text-primary text-sm mb-2">{artisan.specialty}</p>
                  <p className="text-sm text-muted-foreground mb-4">{artisan.bio}</p>
                  <Button variant="outline" size="sm">
                    View Shop
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
          <Button
            variant="ghost"
            size="icon"
            className="absolute top-1/2 left-4 transform -translate-y-1/2"
            onClick={prevSlide}
          >
            <ChevronLeft className="h-6 w-6" />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            className="absolute top-1/2 right-4 transform -translate-y-1/2"
            onClick={nextSlide}
          >
            <ChevronRight className="h-6 w-6" />
          </Button>
        </div>
      </div>
    </section>
  )
}

