import Image from "next/image"
import { Search, Star, ArrowRight } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

export default function Hero() {
  return (
    <div className="relative min-h-screen bg-[#F7F3F0] overflow-hidden">
      {/* Decorative Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-0 left-1/2 w-[800px] h-[800px] -translate-x-1/2 -translate-y-1/2 bg-[#E07A5F] opacity-5 rounded-full blur-3xl" />
        <div className="absolute bottom-0 right-0 w-[600px] h-[600px] bg-[#81B29A] opacity-5 rounded-full blur-3xl" />
      </div>

      {/* Pattern Overlay */}
      <div
        className="absolute inset-0 opacity-[0.02]"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23000000' fill-opacity='1'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
        }}
      />

      <div className="container mx-auto px-4 py-12 relative z-10">
        <div className="grid lg:grid-cols-2 gap-16 items-center">
          <div className="relative z-10 text-center lg:text-left space-y-8">
            {/* Social Proof */}
            <div className="inline-flex items-center rounded-full border border-gray-200 bg-white/50 backdrop-blur-sm px-3 py-1 text-sm text-gray-600">
              <div className="flex -space-x-2 mr-2">
                {[1, 2, 3, 4, 5].map((i) => (
                  <div
                    key={i}
                    className="w-6 h-6 rounded-full border-2 border-white overflow-hidden"
                  >
                    <Image
                      src="https://avatars.githubusercontent.com/u/58410798?v=4"
                      alt={`Artisan ${i}`}
                      width={24}
                      height={24}
                      className="object-cover"
                    />
                  </div>
                ))}
              </div>
              <div className="flex items-center gap-1">
                <Star className="w-3.5 h-3.5 text-[#F2CC8F] fill-current" />
                <span>4.9</span>
                <span className="mx-1">•</span>
                <span>10k+ Artisans</span>
              </div>
            </div>

            {/* Main Content */}
            <div className="space-y-6">
              <h1 className="text-5xl md:text-6xl lg:text-7xl font-serif tracking-tight text-gray-900">
                <span className="block">Discover</span>
                <span className="block mt-2 text-[#E07A5F]">
                  Artisan Treasures
                </span>
              </h1>

              <p className="text-xl text-gray-600 max-w-xl">
                Connect with skilled artisans worldwide. Find unique handcrafted
                pieces that tell a story.
              </p>

              {/* Search Bar */}
              <div className="relative max-w-md mx-auto lg:mx-0">
                <Input
                  type="search"
                  placeholder="Search for handcrafted items..."
                  className="w-full h-14 pl-5 pr-12 rounded-full border-2 border-gray-200 focus:border-[#E07A5F] transition-colors"
                />
                <Button
                  size="icon"
                  className="absolute right-2 top-2 h-10 w-10 rounded-full bg-[#E07A5F] hover:bg-[#c86a51] transition-colors"
                >
                  <Search className="h-4 w-4 text-white" />
                </Button>
              </div>

              {/* CTA Buttons */}
              <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
                <Button
                  size="lg"
                  className="text-lg px-8 bg-[#E07A5F] hover:bg-[#c86a51] text-white rounded-full group transition-all duration-300 transform hover:translate-x-1"
                >
                  Start Shopping
                  <ArrowRight className="ml-2 h-5 w-5 transition-transform group-hover:translate-x-1" />
                </Button>
                <Button
                  size="lg"
                  variant="outline"
                  className="text-lg px-8 border-2 border-[#E07A5F] text-[#E07A5F] hover:bg-[#E07A5F] hover:text-white rounded-full transition-all duration-300"
                >
                  Become an Artisan
                </Button>
              </div>
            </div>

            {/* Feature Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-12">
              {[
                {
                  title: "Verified Artisans",
                  desc: "Quality assured craftsmanship",
                  gradient: "from-[#E07A5F]/10 to-[#E07A5F]/5",
                },
                {
                  title: "Secure Payments",
                  desc: "Safe & protected transactions",
                  gradient: "from-[#81B29A]/10 to-[#81B29A]/5",
                },
                {
                  title: "Global Shipping",
                  desc: "Worldwide delivery options",
                  gradient: "from-[#F2CC8F]/10 to-[#F2CC8F]/5",
                },
              ].map((feature) => (
                <div
                  key={feature.title}
                  className={`p-6 rounded-2xl bg-gradient-to-br ${feature.gradient} backdrop-blur-sm border border-white/20 transition-transform duration-300 hover:scale-105`}
                >
                  <h3 className="font-semibold text-gray-900 mb-1">
                    {feature.title}
                  </h3>
                  <p className="text-sm text-gray-600">{feature.desc}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Hero Images Grid */}
          <div className="relative lg:h-[700px] grid grid-cols-2 gap-4 p-4">
            <div className="space-y-4">
              <div className="rounded-2xl overflow-hidden shadow-lg transform hover:scale-105 transition-transform duration-300">
                <Image
                  src="/momentum/hero-craft-1.jpg"
                  alt="Artisan craft 1"
                  width={300}
                  height={300}
                  className="object-cover w-full h-[200px]"
                />
              </div>
              <div className="rounded-2xl overflow-hidden shadow-lg transform hover:scale-105 transition-transform duration-300">
                <Image
                  src="/momentum/hero-craft2.jpg"
                  alt="Artisan craft 2"
                  width={300}
                  height={300}
                  className="object-cover w-full h-[300px]"
                />
              </div>
            </div>
            <div className="space-y-4 pt-8">
              <div className="rounded-2xl overflow-hidden shadow-lg transform hover:scale-105 transition-transform duration-300">
                <Image
                  src="/momentum/hero-craft3.jpg"
                  alt="Artisan craft 3"
                  width={300}
                  height={300}
                  className="object-cover w-full h-[300px]"
                />
              </div>
              <div className="rounded-2xl overflow-hidden shadow-lg transform hover:scale-105 transition-transform duration-300">
                <Image
                  src="/momentum/hero-craft-1.jpg"
                  alt="Artisan craft 4"
                  width={300}
                  height={300}
                  className="object-cover w-full h-[200px]"
                />
              </div>
            </div>

            {/* Floating Stats Card */}
            <div className="absolute -bottom-6 left-1/2 transform -translate-x-1/2 bg-white rounded-2xl shadow-xl p-6 w-[80%] border border-gray-100">
              <div className="grid grid-cols-3 gap-4">
                {[
                  { number: "10k+", label: "Artisans" },
                  { number: "50k+", label: "Products" },
                  { number: "120+", label: "Countries" },
                ].map((stat) => (
                  <div key={stat.label} className="text-center">
                    <div className="text-xl font-bold text-[#E07A5F]">
                      {stat.number}
                    </div>
                    <div className="text-sm text-gray-600">{stat.label}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
