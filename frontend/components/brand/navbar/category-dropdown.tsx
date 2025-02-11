"use client"

import { ChevronDown } from "lucide-react"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { DropdownMenu, DropdownMenuContent, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { CategoryMenu } from "./category-menu"

export function CategoryDropdown() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <DropdownMenu open={isOpen} onOpenChange={setIsOpen}>
      <DropdownMenuTrigger asChild>
        <Button
          variant="outline"
          className="gap-2 bg-primary text-primary-foreground hover:bg-primary/90 hover:text-primary-foreground"
        >
          All Category
          <ChevronDown className={`h-4 w-4 transition-transform duration-200 ${isOpen ? "rotate-180" : ""}`} />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent className="w-[min(calc(100vw-2rem),800px)] p-0" align="start" sideOffset={8}>
        <CategoryMenu />
      </DropdownMenuContent>
    </DropdownMenu>
  )
}

