
import { MainHeader } from "@/components/brand/navbar/main-header"
import { Navigation } from "@/components/brand/navbar/navigation"

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col">
      <MainHeader />
      <Navigation />
    </div>
  )
}

