"use client"

import { ChevronRight } from "lucide-react"
import Image from "next/image"
import Link from "next/link"
import { useState } from "react"
import { categories } from "@/lib/categories"

export function CategoryMenu() {
  const [activeCategory, setActiveCategory] = useState<string | null>(null)

  return (
    <div className="flex bg-white rounded-lg overflow-hidden shadow-lg">
      <div className="w-72 bg-gray-50 border-r border-gray-200 max-h-[calc(100vh-200px)] overflow-y-auto">
        {categories.map((category) => (
            <div
            key={category.name}
            className="relative"
            role="button"
            tabIndex={0}
            onMouseEnter={() => setActiveCategory(category.name)}
            onFocus={() => setActiveCategory(category.name)}
            onKeyDown={(e) => {
              if (e.key === "Enter" || e.key === " ") {
              setActiveCategory(category.name)
              }
            }}
            ><Link
              href={category.href}
              className={`flex items-center justify-between p-4 hover:bg-gray-100 transition-all duration-200 ${
                activeCategory === category.name ? "bg-primary/10 text-primary border-r-2 border-primary" : ""
              }`}
            >
              <div className="flex items-center gap-3">
                <category.icon
                  className={`h-5 w-5 ${activeCategory === category.name ? "text-primary" : "text-gray-500"}`}
                />
                <span className="text-sm font-medium">{category.name}</span>
              </div>
              {category.subcategories && (
                <ChevronRight
                  className={`h-4 w-4 ${activeCategory === category.name ? "text-primary" : "text-gray-400"}`}
                />
              )}
            </Link>
          </div>
        ))}
      </div>
      {activeCategory && (
        <div className="flex-1 p-6 max-h-[calc(100vh-200px)] overflow-y-auto">
          <div className="grid grid-cols-2 gap-8">
            {categories
              .find((c) => c.name === activeCategory)
              ?.subcategories?.map((subcategory) => (
                <div key={subcategory.name} className="space-y-4">
                  <div className="border-b pb-2">
                    <Link
                      href={subcategory.href}
                      className="group flex items-center gap-2 font-medium text-lg hover:text-primary transition-colors duration-200"
                    >
                      {subcategory.icon && (
                        <subcategory.icon className="h-5 w-5 text-gray-500 group-hover:text-primary transition-colors duration-200" />
                      )}
                      {subcategory.name}
                    </Link>
                    {subcategory.description && <p className="text-sm text-gray-500 mt-1">{subcategory.description}</p>}
                  </div>
                  {subcategory.brands && (
                    <div className="grid grid-cols-2 gap-3">
                      {subcategory.brands.map((brand) => (
                        <Link
                          key={brand.name}
                          href={brand.href}
                          className="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-50 transition-all duration-200 group"
                        >
                          <div className="relative w-8 h-8 bg-gray-100 rounded-md overflow-hidden">
                            <Image
                              src={brand.image || "/placeholder.svg"}
                              alt={brand.name}
                              fill
                              className="object-contain p-1"
                            />
                          </div>
                          <span className="text-sm text-gray-600 group-hover:text-primary transition-colors duration-200">
                            {brand.name}
                          </span>
                        </Link>
                      ))}
                    </div>
                  )}
                </div>
              ))}
          </div>
        </div>
      )}
    </div>
  )
}

