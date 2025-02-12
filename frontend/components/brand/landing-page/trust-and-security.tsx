import { Shield, Lock, CreditCard } from "lucide-react"

const trustPoints = [
  {
    icon: Shield,
    title: "Verified Artisans",
    description: "All artisans are carefully vetted to ensure quality and authenticity.",
  },
  {
    icon: Lock,
    title: "Secure Transactions",
    description: "Your personal and payment information is always protected.",
  },
  {
    icon: CreditCard,
    title: "Buyer Protection",
    description: "Shop with confidence knowing your purchases are covered.",
  },
]

export function TrustAndSecurity() {
  return (
    <section className="py-16 bg-white">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl font-serif font-bold text-center mb-12">Your Trust, Our Priority</h2>
        <div className="grid md:grid-cols-3 gap-8">
          {trustPoints.map((point, index) => (
            <div key={index} className="flex flex-col items-center text-center">
              <div className="bg-primary/10 rounded-full p-4 mb-4">
                <point.icon className="h-8 w-8 text-primary" />
              </div>
              <h3 className="font-semibold mb-2">{point.title}</h3>
              <p className="text-sm text-muted-foreground">{point.description}</p>
            </div>
          ))}
        </div>
        <div className="mt-12 text-center">
          <p className="text-sm text-muted-foreground">
            ArtisanMarket is committed to providing a safe and secure platform for artisans and buyers alike. We
            implement industry-standard security measures and continuously work to enhance our protection systems.
          </p>
        </div>
      </div>
    </section>
  )
}

