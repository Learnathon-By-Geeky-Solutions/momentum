"use client"

import { useState } from "react"
import Image from "next/image"
import { ChevronLeft, ChevronRight } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"

const testimonials = [
  {
    id: 1,
    type: "buyer",
    name: "Alice Johnson",
    location: "New York, USA",
    text: "I found the perfect handmade gift for my sister. The quality is amazing!",
    image: "/placeholder.svg?height=60&width=60",
  },
  {
    id: 2,
    type: "artisan",
    name: "Carlos Rodriguez",
    location: "Barcelona, Spain",
    text: "ArtisanMarket has helped me reach customers worldwide. My business has grown significantly.",
    image: "/placeholder.svg?height=60&width=60",
  },
  {
    id: 3,
    type: "buyer",
    name: "Emily Chen",
    location: "Toronto, Canada",
    text: "The variety of unique items is incredible. I always find something special here.",
    image: "/placeholder.svg?height=60&width=60",
  },
  {
    id: 4,
    type: "artisan",
    name: "Aisha Patel",
    location: "Mumbai, India",
    text: "The platform is user-friendly and has given me the tools to showcase my traditional crafts globally.",
    image: "/placeholder.svg?height=60&width=60",
  },
]

export function Testimonials() {
  const [currentIndex, setCurrentIndex] = useState(0)

  const nextSlide = () => {
    setCurrentIndex((prevIndex) => (prevIndex + 1) % testimonials.length)
  }

  const prevSlide = () => {
    setCurrentIndex((prevIndex) => (prevIndex - 1 + testimonials.length) % testimonials.length)
  }

  return (
    <section className="py-16 bg-white">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl font-serif font-bold text-center mb-12">What Our Community Says</h2>
        <div className="relative">
          <div className="flex overflow-hidden">
            {testimonials.map((testimonial, index) => (
              <Card
                key={testimonial.id}
                className={`flex-shrink-0 w-full md:w-1/2 p-4 transition-all duration-300 ease-in-out transform ${
                  index === currentIndex ? "scale-100 opacity-100" : "scale-95 opacity-60"
                }`}
              >
                <CardContent className="flex flex-col items-center text-center">
                  <Image
                    src={testimonial.image || "/placeholder.svg"}
                    alt={testimonial.name}
                    width={60}
                    height={60}
                    className="rounded-full mb-4"
                  />
                  <p className="text-sm text-muted-foreground mb-4">&ldquo;{testimonial.text}&rdquo;</p>
                  <h3 className="font-semibold">{testimonial.name}</h3>
                  <p className="text-sm text-muted-foreground">{testimonial.location}</p>
                  <span className="mt-2 inline-block px-2 py-1 text-xs font-semibold rounded-full bg-primary text-primary-foreground">
                    {testimonial.type === "buyer" ? "Happy Customer" : "Successful Artisan"}
                  </span>
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

