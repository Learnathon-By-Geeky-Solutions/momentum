import { Palette, BarChart, ShieldCheck, Megaphone } from "lucide-react"
import { Button } from "@/components/ui/button"

const features = [
  {
    icon: Palette,
    title: "Easy Shop Setup",
    description: "Create your online store in minutes with our intuitive tools.",
  },
  { icon: BarChart, title: "Powerful Analytics", description: "Gain insights into your sales and customer behavior." },
  {
    icon: ShieldCheck,
    title: "Secure Payments",
    description: "Receive payments safely and quickly through our trusted system.",
  },
  { icon: Megaphone, title: "Marketing Tools", description: "Promote your products with built-in marketing features." },
]

export function PlatformFeatures() {
  return (
    <section className="py-16 bg-muted">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl font-serif font-bold text-center mb-12">Empower Your Craft Business</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => (
            <div key={index} className="flex flex-col items-center text-center">
              <div className="bg-primary/10 rounded-full p-4 mb-4">
                <feature.icon className="h-8 w-8 text-primary" />
              </div>
              <h3 className="font-semibold mb-2">{feature.title}</h3>
              <p className="text-sm text-muted-foreground">{feature.description}</p>
            </div>
          ))}
        </div>
        <div className="text-center mt-12">
          <Button size="lg">Start Selling Today</Button>
        </div>
      </div>
    </section>
  )
}

