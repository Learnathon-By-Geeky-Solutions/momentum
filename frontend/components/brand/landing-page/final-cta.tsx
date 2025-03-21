import { Button } from "@/components/ui/button"

export function FinalCTA() {
  return (
    <section className="py-20 bg-primary text-primary-foreground">
      <div className="container mx-auto px-4 text-center">
        <h2 className="text-4xl font-serif font-bold mb-6">Join Our Global Artisan Marketplace</h2>
        <p className="text-xl mb-8 max-w-2xl mx-auto">
          Whether you`&#39;`re looking for unique handcrafted items or want to share your creations with the world,
          ArtisanMarket is the place for you.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Button size="lg" variant="secondary">
            Shop Unique Crafts
          </Button>
          <Button size="lg" variant="outline">
            Sell Your Creations
          </Button>
        </div>
      </div>
    </section>
  )
}

