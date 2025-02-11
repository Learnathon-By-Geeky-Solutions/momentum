"use client"

import { ChevronDown } from "lucide-react"
import Link from "next/link"
import { useState } from "react"
import { cn } from "@/lib/utils"
import { categories } from "@/lib/categories"

export function MobileCategoryMenu() {
  const [expandedCategories, setExpandedCategories] = useState<string[]>([])

  const toggleCategory = (categoryName: string) => {
    setExpandedCategories((prev) =>
      prev.includes(categoryName) ? prev.filter((name) => name !== categoryName) : [...prev, categoryName],
    )
  }

  const isCategoryExpanded = (categoryName: string) => expandedCategories.includes(categoryName)

  return (
    <div className="space-y-1">
      {categories.map((category) => (
        <div key={category.name} className="border-b border-gray-100 last:border-0">
          <button
            onClick={() => toggleCategory(category.name)}
            className={cn(
              "flex items-center justify-between w-full p-2 hover:bg-gray-50 rounded-lg transition-all duration-200",
              isCategoryExpanded(category.name) && "text-primary bg-primary/5",
            )}
          >
            <div className="flex items-center gap-3">
              <category.icon
                className={cn("h-5 w-5", isCategoryExpanded(category.name) ? "text-primary" : "text-gray-500")}
              />
              <span className="font-medium text-sm">{category.name}</span>
            </div>
            <ChevronDown
              className={cn(
                "h-4 w-4 text-gray-400 transition-transform duration-200",
                isCategoryExpanded(category.name) && "rotate-180 text-primary",
              )}
            />
          </button>
          {isCategoryExpanded(category.name) && category.subcategories && (
            <div className="pl-10 pr-2 py-2 space-y-1">
              {category.subcategories.map((subcategory) => (
                <Link
                  key={subcategory.name}
                  href={subcategory.href}
                  className="flex items-center gap-2 p-2 hover:bg-gray-50 rounded-lg transition-colors text-sm"
                >
                  {subcategory.icon && <subcategory.icon className="h-4 w-4 text-gray-500" />}
                  <span>{subcategory.name}</span>
                </Link>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  )
}

