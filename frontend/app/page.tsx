
import { Benefits } from "@/components/brand/landing-page/benefits"
import { CategoriesShowcase } from "@/components/brand/landing-page/categories"
import { Faq } from "@/components/brand/landing-page/faq"
import { FeaturedArtisans } from "@/components/brand/landing-page/featured-artisans"
import { FeaturedProducts } from "@/components/brand/landing-page/featured-products"
import { FinalCTA } from "@/components/brand/landing-page/final-cta"
import { Footer } from "@/components/brand/landing-page/footer"
import Hero from "@/components/brand/landing-page/hero"
import { HowItWorks } from "@/components/brand/landing-page/how-it-works"
import { Newsletter } from "@/components/brand/landing-page/newsletter"
import { PlatformFeatures } from "@/components/brand/landing-page/platform-features"
import { Testimonials } from "@/components/brand/landing-page/testimonial"
import { TrustAndSecurity } from "@/components/brand/landing-page/trust-and-security"
import { MainHeader } from "@/components/brand/navbar/main-header"
import { Navigation } from "@/components/brand/navbar/navigation"

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col">
      <MainHeader />
      <Navigation />
      <Hero/>
      <FeaturedProducts/>
      <HowItWorks/>
      <Benefits/>
      <FeaturedArtisans/>
      <Testimonials/>
      <CategoriesShowcase/>
      <PlatformFeatures/>
      <TrustAndSecurity/>
      <Faq/>
      <Newsletter/>
      <FinalCTA/>
      <Footer/>
    </div>
  )
}

