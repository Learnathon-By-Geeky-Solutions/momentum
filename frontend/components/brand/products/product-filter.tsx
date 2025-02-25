"use client"

import { useState } from "react"

import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Slider } from "@/components/ui/slider"

const categories = [
  "Computer & Laptop",
  "Computer Accessories",
  "Smartphone",
  "Headphone",
  "Mobile Accessories",
  "Gaming Console",
  "Camera & Photo",
  "TV & Home Appliances",
  "Watches & Accessories",
  "GPS & Navigation",
  "Portable Technology",
]

const brands = [
  { name: "Apple", count: 150 },
  { name: "Samsung", count: 145 },
  { name: "Google", count: 132 },
  { name: "Microsoft", count: 112 },
  { name: "Dell", count: 98 },
  { name: "HP", count: 87 },
  { name: "Lenovo", count: 76 },
  { name: "Asus", count: 65 },
  { name: "Acer", count: 54 },
  { name: "LG", count: 43 },
]

const popularTags = [
  "Bluetooth",
  "Wireless",
  "USB Type-C",
  "4K",
  "Gaming",
  "Laptop",
  "Desktop",
  "Camera",
  "Smartphone",
  "Audio",
  "Accessories",
  "Graphics Card",
]

export function ProductFilters() {
  const [priceRange, setPriceRange] = useState([0, 1000])

  return (
    <div className="space-y-6 p-1">
      <div>
        <h3 className="mb-4 text-sm font-medium">Categories</h3>
        <div className="space-y-4">
          {categories.map((category) => (
            <div key={category} className="flex items-center gap-2">
              <Checkbox id={category} />
              <Label htmlFor={category} className="text-sm font-normal">
                {category}
              </Label>
            </div>
          ))}
        </div>
      </div>
      <div>
        <h3 className="mb-4 text-sm font-medium">Price Range</h3>
        <div className="space-y-4">
          <Slider value={priceRange} max={1000} step={1} onValueChange={setPriceRange} />
          <div className="flex items-center gap-4">
            <Input
              type="number"
              value={priceRange[0]}
              onChange={(e) => setPriceRange([Number(e.target.value), priceRange[1]])}
              className="h-9"
            />
            <span className="text-muted-foreground">to</span>
            <Input
              type="number"
              value={priceRange[1]}
              onChange={(e) => setPriceRange([priceRange[0], Number(e.target.value)])}
              className="h-9"
            />
          </div>
        </div>
      </div>
      <div>
        <h3 className="mb-4 text-sm font-medium">Brands</h3>
        <div className="space-y-4">
          {brands.map((brand) => (
            <div key={brand.name} className="flex items-center gap-2">
              <Checkbox id={brand.name} />
              <Label htmlFor={brand.name} className="flex flex-1 items-center justify-between text-sm font-normal">
                {brand.name}
                <span className="text-muted-foreground">({brand.count})</span>
              </Label>
            </div>
          ))}
        </div>
      </div>
      <div>
        <h3 className="mb-4 text-sm font-medium">Popular Tags</h3>
        <div className="flex flex-wrap gap-2">
          {popularTags.map((tag) => (
            <Button key={tag} variant="outline" size="sm" className="h-7">
              {tag}
            </Button>
          ))}
        </div>
      </div>
    </div>
  )
}

