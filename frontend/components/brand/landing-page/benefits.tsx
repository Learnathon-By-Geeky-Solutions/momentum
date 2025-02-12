import { Shield, Globe, Award, Heart, Users, Gift } from "lucide-react"

const benefits = [
  { icon: Shield, title: "Quality Guaranteed", description: "Every item is vetted for quality" },
  { icon: Globe, title: "Worldwide Shipping", description: "Deliver to doorsteps globally" },
  { icon: Award, title: "Unique Handcrafted Items", description: "One-of-a-kind pieces" },
  { icon: Heart, title: "Support Local Artisans", description: "Empower creators worldwide" },
  { icon: Users, title: "Global Artisan Community", description: "Connect with skilled craftspeople" },
  { icon: Gift, title: "Perfect for Gifts", description: "Find something special for everyone" },
]

export function Benefits() {
  return (
    <section className="py-20 bg-gradient-to-b from-white to-gray-50">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-serif font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-primary to-primary/80 animate-fade-in-up">
            Why Choose ArtisanMarket
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Discover the unique advantages of shopping with our global artisan marketplace
          </p>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {benefits.map((benefit, index) => (
            <div
              key={index}
              className="group relative overflow-hidden rounded-xl bg-white p-8 shadow-sm transition-all duration-300 hover:shadow-xl hover:-translate-y-1"
              style={{ animationDelay: `${index * 150}ms` }}
            >
              <div className="absolute top-0 left-0 h-1 w-full bg-gradient-to-r from-primary to-primary/60 transform origin-left scale-x-0 transition-transform group-hover:scale-x-100" />
              <div className="flex items-start space-x-6">
                <div className="flex-shrink-0 p-3 rounded-lg bg-primary/10 group-hover:bg-primary/20 transition-colors">
                  <benefit.icon className="h-8 w-8 text-primary" />
                </div>
                <div>
                  <h3 className="font-bold text-xl mb-3 text-gray-900">{benefit.title}</h3>
                  <p className="text-muted-foreground leading-relaxed">{benefit.description}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
