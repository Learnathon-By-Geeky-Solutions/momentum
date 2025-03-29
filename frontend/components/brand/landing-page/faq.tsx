"use client"

import { useState } from "react"
import { ChevronDown, ChevronUp } from "lucide-react"

const faqs = [
  {
    id: 1,
    question: "How do I become a seller on ArtisanMarket?",
    answer:
      "To become a seller, create an account, verify your email, and complete your artisan profile. Once approved, you can start listing your handcrafted items.",
  },
  {
    id: 2,
    question: "What types of products can I sell on ArtisanMarket?",
    answer:
      "ArtisanMarket welcomes a wide range of handcrafted items, including but not limited to jewelry, pottery, textiles, woodwork, and artwork. All items must be handmade or significantly altered by you.",
  },
  {
    id: 3,
    question: "How does shipping work for buyers?",
    answer:
      "Sellers are responsible for shipping their items. As a buyer, you'll see shipping costs and estimated delivery times on each product page before making a purchase.",
  },
  {
    id: 4,
    question: "What if I'm not satisfied with my purchase?",
    answer:
      "We have a buyer protection policy. If you're not satisfied, contact the seller first. If you can't resolve the issue, our customer support team will assist you with returns or refunds.",
  },
]

export function Faq() {
  const [openIndex, setOpenIndex] = useState<number | null>(null)

  const toggleFAQ = (index: number) => {
    setOpenIndex(openIndex === index ? null : index)
  }

  return (
    <section className="py-16 bg-background">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl font-serif font-bold text-center mb-12">
          Frequently Asked Questions
        </h2>
        <div className="max-w-3xl mx-auto">
          {faqs.map((faq, index) => (
            <div key={faq.id} className="mb-4">
              <button
                className="flex justify-between items-center w-full text-left p-4 bg-muted rounded-lg focus:outline-none"
                onClick={() => toggleFAQ(index)}
              >
                <span className="font-semibold">{faq.question}</span>
                {openIndex === index ? (
                  <ChevronUp className="h-5 w-5 text-primary" />
                ) : (
                  <ChevronDown className="h-5 w-5 text-primary" />
                )}
              </button>
              {openIndex === index && (
                <div className="mt-2 p-4 bg-muted/50 rounded-lg">
                  <p className="text-sm text-muted-foreground">{faq.answer}</p>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
