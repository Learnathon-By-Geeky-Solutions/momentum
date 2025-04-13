"use client"
import ShowBrand from "@/components/brand/artisan/brand/show-brand"
import { useAuth } from "@/provider/useAuth"
import React from "react"

export default function Dashboard() {
  const { userRole } = useAuth();
  return (
    <div>
      {userRole === "artisan" && <ShowBrand />}
    </div>
  )
}
