"use client"

import { useState } from "react"
import Image from "next/image"
import { ChevronLeft, ChevronRight } from "lucide-react"
import { motion, AnimatePresence } from "framer-motion"

import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"

interface ProductGalleryProps {
  images: string[]
}

export function ProductGallery({ images }: ProductGalleryProps) {
  const [currentImage, setCurrentImage] = useState(0)

  const next = () => setCurrentImage((current) => (current === images.length - 1 ? 0 : current + 1))

  const previous = () => setCurrentImage((current) => (current === 0 ? images.length - 1 : current - 1))

  return (
    <div className="flex flex-col-reverse gap-4 lg:grid lg:grid-cols-[100px_1fr] lg:gap-6">
      <div className="flex gap-4 overflow-auto px-1 lg:flex-col">
        {images.map((image, index) => (
          <button
            key={index}
            onClick={() => setCurrentImage(index)}
            className={cn(
              "relative aspect-square h-[100px] overflow-hidden rounded-lg border-2",
              currentImage === index ? "border-primary" : "border-transparent",
            )}
          >
            <Image src={image || "/placeholder.svg"} alt={`Product image ${index + 1}`} fill className="object-cover" />
          </button>
        ))}
      </div>
      <div className="relative aspect-square overflow-hidden rounded-lg bg-muted">
        <div className="absolute inset-0 flex items-center justify-between p-4">
          <Button variant="secondary" size="icon" className="h-8 w-8" onClick={previous}>
            <ChevronLeft className="h-4 w-4" />
            <span className="sr-only">Previous image</span>
          </Button>
          <Button variant="secondary" size="icon" className="h-8 w-8" onClick={next}>
            <ChevronRight className="h-4 w-4" />
            <span className="sr-only">Next image</span>
          </Button>
        </div>
        <AnimatePresence mode="wait">
          <motion.div
            key={currentImage}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="relative h-full"
          >
            <Image
              src={images[currentImage] || "/placeholder.svg"}
              alt={`Product image ${currentImage + 1}`}
              fill
              className="object-contain"
              priority
            />
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  )
}

