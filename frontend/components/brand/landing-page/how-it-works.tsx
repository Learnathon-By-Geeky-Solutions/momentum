import {
  Search,
  ShoppingCart,
  Truck,
  Smile,
  UserPlus,
  Package,
  DollarSign,
  TrendingUp,
} from "lucide-react"
import { Button } from "@/components/ui/button"

const buyerSteps = [
  {
    id: 1,
    icon: Search,
    text: "Browse unique items",
    description: "Find handcrafted items that speak to you",
  },
  {
    id: 2,
    icon: ShoppingCart,
    text: "Add to cart",
    description: "Select your favorite pieces",
  },
  {
    id: 3,
    icon: Truck,
    text: "Fast shipping",
    description: "Quick and secure delivery to your door",
  },
  {
    id: 4,
    icon: Smile,
    text: "Enjoy your craft",
    description: "Experience the joy of artisanal products",
  },
]

const sellerSteps = [
  {
    id: 1,
    icon: UserPlus,
    text: "Create account",
    description: "Join our community of artisans",
  },
  {
    id: 2,
    icon: Package,
    text: "List your products",
    description: "Showcase your unique creations",
  },
  {
    id: 3,
    icon: DollarSign,
    text: "Receive orders",
    description: "Start selling to eager customers",
  },
  {
    id: 4,
    icon: TrendingUp,
    text: "Grow your business",
    description: "Expand your creative enterprise",
  },
]

export function HowItWorks() {
  return (
    <section className="py-16 bg-muted">
      <div className="max-w-6xl mx-auto px-4">
        <h2 className="text-3xl font-serif font-bold text-center mb-12 animate-fade-in-up">
          How It Works
        </h2>
        <div className="grid md:grid-cols-2 gap-12">
          <div>
            <h3 className="text-2xl font-semibold mb-8 text-center">
              For Buyers
            </h3>
            <div className="relative">
              {buyerSteps.map((step, index) => (
                <div key={step.id} className="flex mb-8 relative">
                  <div className="flex-none">
                    <div className="bg-background w-12 h-12 rounded-full flex items-center justify-center z-10 relative border-2 border-primary">
                      <step.icon className="h-6 w-6 text-primary" />
                    </div>
                    {index !== buyerSteps.length - 1 && (
                      <div className="absolute h-full w-0.5 bg-primary/20 left-6 top-12 -translate-x-1/2" />
                    )}
                  </div>
                  <div className="ml-4 flex-1">
                    <h4 className="font-semibold text-lg mb-1">{step.text}</h4>
                    <p className="text-muted-foreground">{step.description}</p>
                  </div>
                </div>
              ))}
              <div className="mt-8 text-center">
                <Button>Start Shopping</Button>
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-2xl font-semibold mb-8 text-center">
              For Artisans
            </h3>
            <div className="relative">
              {sellerSteps.map((step, index) => (
                <div key={step.id} className="flex mb-8 relative">
                  <div className="flex-none">
                    <div className="bg-primary w-12 h-12 rounded-full flex items-center justify-center z-10 relative border-2 border-secondary">
                      <step.icon className="h-6 w-6 text-secondary" />
                    </div>
                    {index !== sellerSteps.length - 1 && (
                      <div className="absolute h-full w-0.5 bg-secondary/20 left-6 top-12 -translate-x-1/2" />
                    )}
                  </div>
                  <div className="ml-4 flex-1">
                    <h4 className="font-semibold text-lg mb-1">{step.text} </h4>
                    <p className="text-muted-foreground">{step.description}</p>
                  </div>
                </div>
              ))}
              <div className="mt-8 text-center">
                <Button variant="outline">Become an Artisan</Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
