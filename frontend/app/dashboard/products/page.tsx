"use client"

import type React from "react"
import { useState, useRef, useEffect } from "react"
import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { z } from "zod"
import {
  CalendarIcon,
  ChevronLeft,
  ChevronRight,
  HelpCircle,
  ImagePlus,
  Info,
  Loader2,
  Plus,
  X,
} from "lucide-react"
import { format } from "date-fns"

import { Button } from "@/components/ui/button"
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Tabs, TabsList, TabsContent, TabsTrigger } from "@/components/ui/tabs"
import { Checkbox } from "@/components/ui/checkbox"
import { Separator } from "@/components/ui/separator"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"
import { Calendar } from "@/components/ui/calendar"
import { Badge } from "@/components/ui/badge"
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip"
import { Progress } from "@/components/ui/progress"

const MAX_FILE_SIZE = 5 * 1024 * 1024 // 5MB
const ACCEPTED_IMAGE_TYPES = [
  "image/jpeg",
  "image/jpg",
  "image/png",
  "image/webp",
]

const productFormSchema = z.object({
  // Basic Information
  name: z
    .string()
    .min(3, {
      message: "Product name must be at least 3 characters.",
    })
    .max(100, {
      message: "Product name must not exceed 100 characters.",
    }),
  description: z
    .string()
    .min(20, {
      message: "Description must be at least 20 characters.",
    })
    .max(2000, {
      message: "Description must not exceed 2000 characters.",
    }),
  price: z.coerce.number().positive({
    message: "Price must be a positive number.",
  }),
  compareAtPrice: z.coerce
    .number()
    .positive({
      message: "Compare at price must be a positive number.",
    })
    .optional(),

  // Category and Tags
  category: z.string({
    required_error: "Please select a category.",
  }),
  subcategory: z.string().optional(),
  tags: z.array(z.string()).optional(),

  // Inventory
  sku: z.string().optional(),
  barcode: z.string().optional(),
  quantity: z.coerce.number().int().nonnegative({
    message: "Quantity must be a non-negative integer.",
  }),
  trackInventory: z.boolean().default(true),

  // Dimensions and Weight
  dimensions: z.any().optional(), // For the heading
  weight: z.coerce
    .number()
    .positive({
      message: "Weight must be a positive number.",
    })
    .optional(),
  weightUnit: z.enum(["kg", "g", "lb", "oz"]).default("g"),
  length: z.coerce.number().positive().optional(),
  width: z.coerce.number().positive().optional(),
  height: z.coerce.number().positive().optional(),
  dimensionUnit: z.enum(["cm", "m", "in", "ft"]).default("cm"),

  // Shipping
  requiresShipping: z.boolean().default(true),
  isFreeShipping: z.boolean().default(false),

  // Dates
  availability: z.any().optional(), // For the heading
  availableFrom: z.date().optional(),
  availableUntil: z.date().optional(),

  // Variants
  hasVariants: z.boolean().default(false),

  // Images
  images: z.any().optional(), // For the images heading

  // SEO
  seoInfo: z.any().optional(), // For the heading
  seoTitle: z.string().max(60).optional(),
  seoDescription: z.string().max(160).optional(),

  // Terms
  termsAccepted: z.boolean().refine((val) => val === true, {
    message: "You must accept the terms and conditions.",
  }),
})

type ProductFormValues = z.infer<typeof productFormSchema>

// Tab order for navigation
const TAB_ORDER = ["basic", "details", "images", "inventory", "shipping"]

export default function ProductForm() {
  const [images, setImages] = useState<File[]>([])
  const [imageUrls, setImageUrls] = useState<string[]>([])
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [currentTag, setCurrentTag] = useState("")
  const [currentTab, setCurrentTab] = useState("basic")
  const [formProgress, setFormProgress] = useState(20)
  const formRef = useRef<HTMLFormElement>(null)

  const form = useForm<ProductFormValues>({
    resolver: zodResolver(productFormSchema),
    defaultValues: {
      name: "",
      description: "",
      price: undefined,
      compareAtPrice: undefined,
      category: "",
      subcategory: "",
      tags: [],
      dimensions: undefined,
      availability: undefined,
      seoInfo: undefined,
      sku: "",
      barcode: "",
      quantity: 1,
      trackInventory: true,
      weight: undefined,
      weightUnit: "g",
      length: undefined,
      width: undefined,
      height: undefined,
      dimensionUnit: "cm",
      requiresShipping: true,
      isFreeShipping: false,
      hasVariants: false,
      images: undefined,
      seoTitle: "",
      seoDescription: "",
      termsAccepted: false,
    },
    mode: "onChange",
  })

  // Update progress based on form completion
  useEffect(() => {
    const values = form.getValues()
    const requiredFields = [
      "name",
      "description",
      "price",
      "category",
      "quantity",
    ]
    const completedFields = requiredFields.filter(
      (field) => !!values[field as keyof ProductFormValues],
    )

    // Calculate progress (20% minimum, 100% maximum)
    const progress =
      20 + Math.floor((completedFields.length / requiredFields.length) * 80)
    setFormProgress(progress)
  }, [form.watch()])

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const newFiles = Array.from(e.target.files)

      // Validate file size and type
      const validFiles = newFiles.filter((file) => {
        if (file.size > MAX_FILE_SIZE) {
          alert(`File ${file.name} is too large. Max size is 5MB.`)
          return false
        }
        if (!ACCEPTED_IMAGE_TYPES.includes(file.type)) {
          alert(
            `File ${file.name} has unsupported format. Please use JPEG, PNG or WebP.`,
          )
          return false
        }
        return true
      })

      if (validFiles.length > 0) {
        setImages((prev) => [...prev, ...validFiles])

        // Create URLs for preview
        const newUrls = validFiles.map((file) => URL.createObjectURL(file))
        setImageUrls((prev) => [...prev, ...newUrls])
      }
    }
  }

  const removeImage = (index: number) => {
    // Revoke the object URL to avoid memory leaks
    URL.revokeObjectURL(imageUrls[index])

    setImages((prev) => prev.filter((_, i) => i !== index))
    setImageUrls((prev) => prev.filter((_, i) => i !== index))
  }

  const addTag = () => {
    if (currentTag.trim() !== "") {
      const currentTags = form.getValues("tags") || []
      if (!currentTags.includes(currentTag.trim())) {
        form.setValue("tags", [...currentTags, currentTag.trim()])
        setCurrentTag("")
      }
    }
  }

  const removeTag = (tag: string) => {
    const currentTags = form.getValues("tags") || []
    form.setValue(
      "tags",
      currentTags.filter((t) => t !== tag),
    )
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      e.preventDefault()
      addTag()
    }
  }

  const navigateTab = (direction: "next" | "prev") => {
    const currentIndex = TAB_ORDER.indexOf(currentTab)
    let newIndex

    if (direction === "next") {
      newIndex = Math.min(currentIndex + 1, TAB_ORDER.length - 1)
    } else {
      newIndex = Math.max(currentIndex - 1, 0)
    }

    setCurrentTab(TAB_ORDER[newIndex])
  }

  async function onSubmit(data: ProductFormValues) {
    setIsSubmitting(true)

    try {
      // Here you would typically upload images and submit the form data to your API
      console.log("Form data:", data)
      console.log("Images:", images)

      // Simulate API call
      await new Promise((resolve) => setTimeout(resolve, 2000))

      alert("Product submitted successfully!")
      // Reset form after successful submission
      form.reset()
      setImages([])
      setImageUrls([])
    } catch (error) {
      console.error("Error submitting product:", error)
      alert("Failed to submit product. Please try again.")
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="max-w-7xl mx-auto py-10 px-4">
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="text-2xl">Publish Your Product</CardTitle>
              <CardDescription>
                Fill out the form below to list your handcrafted item on our
                marketplace.
              </CardDescription>
            </div>
            <div className="hidden md:block">
              <div className="flex items-center gap-2">
                <span className="text-sm text-muted-foreground">
                  Form completion:
                </span>
                <div className="w-40">
                  <Progress value={formProgress} className="h-2" />
                </div>
                <span className="text-sm font-medium">{formProgress}%</span>
              </div>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <Form {...form}>
            <form
              ref={formRef}
              onSubmit={form.handleSubmit(onSubmit)}
              className="space-y-8"
            >
              <Tabs
                value={currentTab}
                onValueChange={setCurrentTab}
                className="w-full"
              >
                <TabsList className="grid grid-cols-2 md:grid-cols-5 w-full mb-4">
                  <TabsTrigger value="basic" aria-label="Basic Information Tab">
                    <span className="hidden md:inline">Basic Info</span>
                    <span className="md:hidden">Basic</span>
                    {form.formState.errors.name ||
                    form.formState.errors.description ||
                    form.formState.errors.price ||
                    form.formState.errors.category ? (
                      <Badge
                        variant="destructive"
                        className="ml-2 h-5 w-5 p-0 flex items-center justify-center"
                      >
                        !
                      </Badge>
                    ) : null}
                  </TabsTrigger>
                  <TabsTrigger value="details" aria-label="Product Details Tab">
                    Details
                  </TabsTrigger>
                  <TabsTrigger value="images" aria-label="Product Images Tab">
                    Images
                  </TabsTrigger>
                  <TabsTrigger value="inventory" aria-label="Inventory Tab">
                    <span className="hidden md:inline">Inventory</span>
                    <span className="md:hidden">Stock</span>
                    {form.formState.errors.quantity ? (
                      <Badge
                        variant="destructive"
                        className="ml-2 h-5 w-5 p-0 flex items-center justify-center"
                      >
                        !
                      </Badge>
                    ) : null}
                  </TabsTrigger>
                  <TabsTrigger value="shipping" aria-label="Shipping Tab">
                    Shipping
                  </TabsTrigger>
                </TabsList>

                {/* Basic Information Tab */}
                <TabsContent value="basic" className="space-y-6 pt-2">
                  <div className="bg-muted/40 p-4 rounded-lg mb-6">
                    <h3 className="text-sm font-medium mb-2 flex items-center">
                      <Info className="h-4 w-4 mr-2" />
                      Getting Started
                    </h3>
                    <p className="text-sm text-muted-foreground">
                      Start by entering the basic information about your
                      product. Fields marked with * are required.
                    </p>
                  </div>

                  <div className="space-y-4">
                    <FormField
                      control={form.control}
                      name="name"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>
                            Product Name*
                            <TooltipProvider>
                              <Tooltip>
                                <TooltipTrigger asChild>
                                  <Button
                                    variant="ghost"
                                    className="px-2 py-0 h-auto"
                                  >
                                    <HelpCircle className="h-4 w-4 text-muted-foreground" />
                                    <span className="sr-only">
                                      Product name help
                                    </span>
                                  </Button>
                                </TooltipTrigger>
                                <TooltipContent>
                                  <p className="max-w-xs">
                                    Choose a clear, descriptive name that will
                                    help customers find your product.
                                  </p>
                                </TooltipContent>
                              </Tooltip>
                            </TooltipProvider>
                          </FormLabel>
                          <FormControl>
                            <Input
                              placeholder="Handcrafted Ceramic Mug"
                              {...field}
                              aria-required="true"
                              aria-invalid={!!form.formState.errors.name}
                            />
                          </FormControl>
                          <FormDescription>
                            Choose a clear, descriptive name for your product.
                          </FormDescription>
                          <FormMessage />
                        </FormItem>
                      )}
                    />

                    <FormField
                      control={form.control}
                      name="description"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Description*</FormLabel>
                          <FormControl>
                            <Textarea
                              placeholder="Describe your product in detail. Include materials, techniques, and what makes it special."
                              className="min-h-32"
                              value={field.value}
                              onChange={field.onChange}
                              onBlur={field.onBlur}
                              name={field.name}
                              ref={field.ref}
                              aria-required="true"
                              aria-invalid={!!form.formState.errors.description}
                            />
                          </FormControl>
                          <FormDescription>
                            A detailed description helps buyers understand your
                            product better.
                            <span className="block mt-1 text-xs">
                              {field.value?.length || 0}/2000 characters
                            </span>
                          </FormDescription>
                          <FormMessage />
                        </FormItem>
                      )}
                    />

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <FormField
                        control={form.control}
                        name="price"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>Price*</FormLabel>
                            <FormControl>
                              <div className="relative">
                                <span className="absolute left-3 top-2.5">
                                  $
                                </span>
                                <Input
                                  className="pl-6"
                                  placeholder="29.99"
                                  {...field}
                                  type="number"
                                  step="0.01"
                                  min="0"
                                  aria-required="true"
                                  aria-invalid={!!form.formState.errors.price}
                                />
                              </div>
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />

                      <FormField
                        control={form.control}
                        name="compareAtPrice"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>
                              Compare-at Price
                              <TooltipProvider>
                                <Tooltip>
                                  <TooltipTrigger asChild>
                                    <Button
                                      variant="ghost"
                                      className="px-2 py-0 h-auto"
                                    >
                                      <HelpCircle className="h-4 w-4 text-muted-foreground" />
                                      <span className="sr-only">
                                        Compare-at price help
                                      </span>
                                    </Button>
                                  </TooltipTrigger>
                                  <TooltipContent>
                                    <p className="max-w-xs">
                                      Original price for showing discounts.
                                      Leave empty if not applicable.
                                    </p>
                                  </TooltipContent>
                                </Tooltip>
                              </TooltipProvider>
                            </FormLabel>
                            <FormControl>
                              <div className="relative">
                                <span className="absolute left-3 top-2.5">
                                  $
                                </span>
                                <Input
                                  className="pl-6"
                                  placeholder="39.99"
                                  {...field}
                                  type="number"
                                  step="0.01"
                                  min="0"
                                  value={
                                    field.value === undefined ? "" : field.value
                                  }
                                  onChange={(e) => {
                                    const value =
                                      e.target.value === ""
                                        ? undefined
                                        : Number.parseFloat(e.target.value)
                                    field.onChange(value)
                                  }}
                                />
                              </div>
                            </FormControl>
                            <FormDescription>
                              Original price for showing discounts (optional).
                            </FormDescription>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <FormField
                        control={form.control}
                        name="category"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>Category*</FormLabel>
                            <Select
                              onValueChange={field.onChange}
                              defaultValue={field.value}
                              value={field.value}
                            >
                              <FormControl>
                                <SelectTrigger
                                  aria-required="true"
                                  aria-invalid={
                                    !!form.formState.errors.category
                                  }
                                >
                                  <SelectValue placeholder="Select a category" />
                                </SelectTrigger>
                              </FormControl>
                              <SelectContent>
                                <SelectItem value="jewelry">Jewelry</SelectItem>
                                <SelectItem value="clothing">
                                  Clothing
                                </SelectItem>
                                <SelectItem value="home_decor">
                                  Home Decor
                                </SelectItem>
                                <SelectItem value="art">Art</SelectItem>
                                <SelectItem value="ceramics">
                                  Ceramics
                                </SelectItem>
                                <SelectItem value="woodworking">
                                  Woodworking
                                </SelectItem>
                                <SelectItem value="textiles">
                                  Textiles
                                </SelectItem>
                                <SelectItem value="paper_goods">
                                  Paper Goods
                                </SelectItem>
                                <SelectItem value="bath_beauty">
                                  Bath & Beauty
                                </SelectItem>
                                <SelectItem value="other">Other</SelectItem>
                              </SelectContent>
                            </Select>
                            <FormMessage />
                          </FormItem>
                        )}
                      />

                      <FormField
                        control={form.control}
                        name="subcategory"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>Subcategory</FormLabel>
                            <FormControl>
                              <Input
                                placeholder="E.g., Necklaces, Mugs, Wall Art"
                                {...field}
                              />
                            </FormControl>
                            <FormDescription>
                              Specify a subcategory to help buyers find your
                              product.
                            </FormDescription>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                    </div>

                    <FormField
                      control={form.control}
                      name="tags"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Tags</FormLabel>
                          <div className="flex items-center gap-2 mt-1.5">
                            <Input
                              placeholder="Add tags (e.g., handmade, vintage)"
                              value={currentTag}
                              onChange={(e) => setCurrentTag(e.target.value)}
                              onKeyDown={handleKeyDown}
                              aria-label="Add tag"
                            />
                            <Button
                              type="button"
                              size="sm"
                              onClick={addTag}
                              aria-label="Add tag"
                            >
                              <Plus className="h-4 w-4" />
                            </Button>
                          </div>
                          <FormDescription>
                            Tags help buyers find your products. Press Enter to
                            add multiple tags.
                          </FormDescription>

                          <div
                            className="flex flex-wrap gap-2 mt-3"
                            aria-label="Product tags"
                          >
                            {field.value?.map((tag, index) => (
                              <Badge
                                key={index}
                                variant="secondary"
                                className="gap-1"
                              >
                                {tag}
                                <button
                                  type="button"
                                  onClick={() => removeTag(tag)}
                                  className="ml-1 rounded-full hover:bg-muted"
                                  aria-label={`Remove ${tag} tag`}
                                >
                                  <X className="h-3 w-3" />
                                  <span className="sr-only">
                                    Remove {tag} tag
                                  </span>
                                </button>
                              </Badge>
                            ))}
                          </div>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                  </div>
                </TabsContent>

                {/* Details Tab */}
                <TabsContent value="details" className="space-y-6 pt-2">
                  <div className="bg-muted/40 p-4 rounded-lg mb-6">
                    <h3 className="text-sm font-medium mb-2 flex items-center">
                      <Info className="h-4 w-4 mr-2" />
                      Product Details
                    </h3>
                    <p className="text-sm text-muted-foreground">
                      Add detailed specifications about your product to help
                      customers make informed decisions.
                    </p>
                  </div>

                  <div className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <FormField
                        control={form.control}
                        name="weight"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>Weight</FormLabel>
                            <div className="flex gap-2">
                              <FormControl>
                                <Input
                                  type="number"
                                  step="0.01"
                                  min="0"
                                  placeholder="0.5"
                                  {...field}
                                  value={
                                    field.value === undefined ? "" : field.value
                                  }
                                  onChange={(e) => {
                                    const value =
                                      e.target.value === ""
                                        ? undefined
                                        : Number.parseFloat(e.target.value)
                                    field.onChange(value)
                                  }}
                                  aria-label="Product weight"
                                />
                              </FormControl>
                              <FormField
                                control={form.control}
                                name="weightUnit"
                                render={({ field }) => (
                                  <Select
                                    onValueChange={field.onChange}
                                    defaultValue={field.value}
                                  >
                                    <FormControl>
                                      <SelectTrigger
                                        className="w-20"
                                        aria-label="Weight unit"
                                      >
                                        <SelectValue />
                                      </SelectTrigger>
                                    </FormControl>
                                    <SelectContent>
                                      <SelectItem value="g">g</SelectItem>
                                      <SelectItem value="kg">kg</SelectItem>
                                      <SelectItem value="oz">oz</SelectItem>
                                      <SelectItem value="lb">lb</SelectItem>
                                    </SelectContent>
                                  </Select>
                                )}
                              />
                            </div>
                            <FormDescription>
                              Product weight for shipping calculations.
                            </FormDescription>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                    </div>

                    <div>
                      <FormField
                        control={form.control}
                        name="dimensions"
                        render={() => (
                          <FormItem>
                            <FormLabel>Dimensions</FormLabel>
                            <FormDescription>
                              Enter the physical dimensions of your product.
                            </FormDescription>
                          </FormItem>
                        )}
                      />
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-2">
                        <FormField
                          control={form.control}
                          name="length"
                          render={({ field }) => (
                            <FormItem>
                              <FormLabel>Length</FormLabel>
                              <FormControl>
                                <Input
                                  type="number"
                                  step="0.1"
                                  min="0"
                                  placeholder="10"
                                  {...field}
                                  value={
                                    field.value === undefined ? "" : field.value
                                  }
                                  onChange={(e) => {
                                    const value =
                                      e.target.value === ""
                                        ? undefined
                                        : Number.parseFloat(e.target.value)
                                    field.onChange(value)
                                  }}
                                  aria-label="Product length"
                                />
                              </FormControl>
                              <FormMessage />
                            </FormItem>
                          )}
                        />

                        <FormField
                          control={form.control}
                          name="width"
                          render={({ field }) => (
                            <FormItem>
                              <FormLabel>Width</FormLabel>
                              <FormControl>
                                <Input
                                  type="number"
                                  step="0.1"
                                  min="0"
                                  placeholder="5"
                                  {...field}
                                  value={
                                    field.value === undefined ? "" : field.value
                                  }
                                  onChange={(e) => {
                                    const value =
                                      e.target.value === ""
                                        ? undefined
                                        : Number.parseFloat(e.target.value)
                                    field.onChange(value)
                                  }}
                                  aria-label="Product width"
                                />
                              </FormControl>
                              <FormMessage />
                            </FormItem>
                          )}
                        />

                        <FormField
                          control={form.control}
                          name="height"
                          render={({ field }) => (
                            <FormItem>
                              <FormLabel>Height</FormLabel>
                              <FormControl>
                                <Input
                                  type="number"
                                  step="0.1"
                                  min="0"
                                  placeholder="2"
                                  {...field}
                                  value={
                                    field.value === undefined ? "" : field.value
                                  }
                                  onChange={(e) => {
                                    const value =
                                      e.target.value === ""
                                        ? undefined
                                        : Number.parseFloat(e.target.value)
                                    field.onChange(value)
                                  }}
                                  aria-label="Product height"
                                />
                              </FormControl>
                              <FormMessage />
                            </FormItem>
                          )}
                        />
                      </div>

                      <div className="mt-2">
                        <FormField
                          control={form.control}
                          name="dimensionUnit"
                          render={({ field }) => (
                            <FormItem>
                              <FormLabel>Dimension Unit</FormLabel>
                              <Select
                                onValueChange={field.onChange}
                                defaultValue={field.value}
                              >
                                <FormControl>
                                  <SelectTrigger
                                    className="w-24"
                                    aria-label="Dimension unit"
                                  >
                                    <SelectValue />
                                  </SelectTrigger>
                                </FormControl>
                                <SelectContent>
                                  <SelectItem value="cm">cm</SelectItem>
                                  <SelectItem value="m">m</SelectItem>
                                  <SelectItem value="in">in</SelectItem>
                                  <SelectItem value="ft">ft</SelectItem>
                                </SelectContent>
                              </Select>
                              <FormMessage />
                            </FormItem>
                          )}
                        />
                      </div>
                    </div>

                    <div className="space-y-4">
                      <FormField
                        control={form.control}
                        name="availability"
                        render={() => (
                          <FormItem>
                            <FormLabel>Availability</FormLabel>
                            <FormDescription>
                              Set when this product will be available for
                              purchase.
                            </FormDescription>
                          </FormItem>
                        )}
                      />
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-2">
                        <FormField
                          control={form.control}
                          name="availableFrom"
                          render={({ field }) => (
                            <FormItem className="flex flex-col">
                              <FormLabel>Available From</FormLabel>
                              <Popover>
                                <PopoverTrigger asChild>
                                  <FormControl>
                                    <Button
                                      variant={"outline"}
                                      className={`w-full pl-3 text-left font-normal ${!field.value ? "text-muted-foreground" : ""}`}
                                      aria-label="Select available from date"
                                    >
                                      {field.value ? (
                                        format(field.value, "PPP")
                                      ) : (
                                        <span>Pick a date</span>
                                      )}
                                      <CalendarIcon className="ml-auto h-4 w-4 opacity-50" />
                                    </Button>
                                  </FormControl>
                                </PopoverTrigger>
                                <PopoverContent
                                  className="w-auto p-0"
                                  align="start"
                                >
                                  <Calendar
                                    mode="single"
                                    selected={field.value}
                                    onSelect={field.onChange}
                                    initialFocus
                                  />
                                </PopoverContent>
                              </Popover>
                              <FormDescription>
                                When this product becomes available.
                              </FormDescription>
                              <FormMessage />
                            </FormItem>
                          )}
                        />

                        <FormField
                          control={form.control}
                          name="availableUntil"
                          render={({ field }) => (
                            <FormItem className="flex flex-col">
                              <FormLabel>Available Until</FormLabel>
                              <Popover>
                                <PopoverTrigger asChild>
                                  <FormControl>
                                    <Button
                                      variant={"outline"}
                                      className={`w-full pl-3 text-left font-normal ${!field.value ? "text-muted-foreground" : ""}`}
                                      aria-label="Select available until date"
                                    >
                                      {field.value ? (
                                        format(field.value, "PPP")
                                      ) : (
                                        <span>Pick a date</span>
                                      )}
                                      <CalendarIcon className="ml-auto h-4 w-4 opacity-50" />
                                    </Button>
                                  </FormControl>
                                </PopoverTrigger>
                                <PopoverContent
                                  className="w-auto p-0"
                                  align="start"
                                >
                                  <Calendar
                                    mode="single"
                                    selected={field.value}
                                    onSelect={field.onChange}
                                    initialFocus
                                  />
                                </PopoverContent>
                              </Popover>
                              <FormDescription>
                                When this product will no longer be available.
                              </FormDescription>
                              <FormMessage />
                            </FormItem>
                          )}
                        />
                      </div>
                    </div>

                    <div className="space-y-4">
                      <FormField
                        control={form.control}
                        name="seoInfo"
                        render={() => (
                          <FormItem>
                            <FormLabel>SEO Information</FormLabel>
                            <FormDescription>
                              Optimize your product for search engines.
                            </FormDescription>
                          </FormItem>
                        )}
                      />
                      <div className="space-y-4 mt-2">
                        <FormField
                          control={form.control}
                          name="seoTitle"
                          render={({ field }) => (
                            <FormItem>
                              <FormLabel>SEO Title</FormLabel>
                              <FormControl>
                                <Input
                                  placeholder="SEO optimized title (max 60 characters)"
                                  {...field}
                                />
                              </FormControl>
                              <FormDescription>
                                {field.value?.length || 0}/60 characters
                              </FormDescription>
                              <FormMessage />
                            </FormItem>
                          )}
                        />

                        <FormField
                          control={form.control}
                          name="seoDescription"
                          render={({ field }) => (
                            <FormItem>
                              <FormLabel>SEO Description</FormLabel>
                              <FormControl>
                                <Textarea
                                  placeholder="SEO optimized description (max 160 characters)"
                                  value={
                                    field.value === undefined ? "" : field.value
                                  }
                                  onChange={field.onChange}
                                  onBlur={field.onBlur}
                                  name={field.name}
                                  ref={field.ref}
                                />
                              </FormControl>
                              <FormDescription>
                                {field.value?.length || 0}/160 characters
                              </FormDescription>
                              <FormMessage />
                            </FormItem>
                          )}
                        />
                      </div>
                    </div>
                  </div>
                </TabsContent>

                {/* Images Tab */}
                <TabsContent value="images" className="space-y-6 pt-2">
                  <div className="bg-muted/40 p-4 rounded-lg mb-6">
                    <h3 className="text-sm font-medium mb-2 flex items-center">
                      <Info className="h-4 w-4 mr-2" />
                      Product Images
                    </h3>
                    <p className="text-sm text-muted-foreground">
                      High-quality images help sell your product. Add multiple
                      images to show different angles and details.
                    </p>
                  </div>

                  <div className="space-y-4">
                    <FormField
                      control={form.control}
                      name="images"
                      render={() => (
                        <FormItem>
                          <FormLabel className="text-sm font-medium">
                            Product Images
                          </FormLabel>
                          <FormDescription className="mb-4">
                            Upload high-quality images of your product. First
                            image will be the main product image.
                          </FormDescription>
                        </FormItem>
                      )}
                    />

                    <div className="grid grid-cols-1 gap-4">
                      <div className="border-2 border-dashed border-muted-foreground/25 rounded-lg p-6 text-center">
                        <label
                          htmlFor="image-upload"
                          className="cursor-pointer"
                        >
                          <div className="flex flex-col items-center gap-2">
                            <ImagePlus className="h-8 w-8 text-muted-foreground" />
                            <h3 className="text-sm font-medium">
                              Upload Images
                            </h3>
                            <p className="text-xs text-muted-foreground">
                              Drag and drop or click to upload (JPEG, PNG, WebP,
                              max 5MB)
                            </p>
                          </div>
                          <input
                            id="image-upload"
                            type="file"
                            accept="image/jpeg,image/png,image/webp"
                            multiple
                            className="hidden"
                            onChange={handleImageChange}
                            aria-label="Upload product images"
                          />
                        </label>
                      </div>

                      {imageUrls.length > 0 && (
                        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4 mt-4">
                          {imageUrls.map((url, index) => (
                            <div key={index} className="relative group">
                              <img
                                src={url || "/placeholder.svg"}
                                alt={`Product image ${index + 1}`}
                                className="w-full h-32 object-cover rounded-md"
                              />
                              <button
                                type="button"
                                onClick={() => removeImage(index)}
                                className="absolute top-2 right-2 bg-black/50 text-white rounded-full p-1 opacity-0 group-hover:opacity-100 transition-opacity"
                                aria-label={`Remove image ${index + 1}`}
                              >
                                <X className="h-4 w-4" />
                                <span className="sr-only">Remove image</span>
                              </button>
                              {index === 0 && (
                                <Badge className="absolute bottom-2 left-2">
                                  Main Image
                                </Badge>
                              )}
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                </TabsContent>

                {/* Inventory Tab */}
                <TabsContent value="inventory" className="space-y-6 pt-2">
                  <div className="bg-muted/40 p-4 rounded-lg mb-6">
                    <h3 className="text-sm font-medium mb-2 flex items-center">
                      <Info className="h-4 w-4 mr-2" />
                      Inventory Management
                    </h3>
                    <p className="text-sm text-muted-foreground">
                      Set up inventory tracking and stock levels for your
                      product.
                    </p>
                  </div>

                  <div className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <FormField
                        control={form.control}
                        name="sku"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>
                              SKU (Stock Keeping Unit)
                              <TooltipProvider>
                                <Tooltip>
                                  <TooltipTrigger asChild>
                                    <Button
                                      variant="ghost"
                                      className="px-2 py-0 h-auto"
                                    >
                                      <HelpCircle className="h-4 w-4 text-muted-foreground" />
                                      <span className="sr-only">SKU help</span>
                                    </Button>
                                  </TooltipTrigger>
                                  <TooltipContent>
                                    <p className="max-w-xs">
                                      A unique identifier for your product that
                                      helps you track inventory.
                                    </p>
                                  </TooltipContent>
                                </Tooltip>
                              </TooltipProvider>
                            </FormLabel>
                            <FormControl>
                              <Input placeholder="SKU123" {...field} />
                            </FormControl>
                            <FormDescription>
                              Your unique identifier for this product.
                            </FormDescription>
                            <FormMessage />
                          </FormItem>
                        )}
                      />

                      <FormField
                        control={form.control}
                        name="barcode"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>
                              Barcode (ISBN, UPC, GTIN, etc.)
                            </FormLabel>
                            <FormControl>
                              <Input placeholder="123456789012" {...field} />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                    </div>

                    <FormField
                      control={form.control}
                      name="quantity"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Quantity*</FormLabel>
                          <FormControl>
                            <Input
                              type="number"
                              min="0"
                              step="1"
                              {...field}
                              aria-required="true"
                              aria-invalid={!!form.formState.errors.quantity}
                            />
                          </FormControl>
                          <FormDescription>
                            Number of items available for sale.
                          </FormDescription>
                          <FormMessage />
                        </FormItem>
                      )}
                    />

                    <FormField
                      control={form.control}
                      name="trackInventory"
                      render={({ field }) => (
                        <FormItem className="flex flex-row items-start space-x-3 space-y-0 rounded-md border p-4">
                          <FormControl>
                            <Checkbox
                              checked={field.value}
                              onCheckedChange={field.onChange}
                              aria-label="Track inventory"
                            />
                          </FormControl>
                          <div className="space-y-1 leading-none">
                            <FormLabel>Track inventory</FormLabel>
                            <FormDescription>
                              Automatically update stock levels as orders are
                              placed.
                            </FormDescription>
                          </div>
                        </FormItem>
                      )}
                    />

                    <FormField
                      control={form.control}
                      name="hasVariants"
                      render={({ field }) => (
                        <FormItem className="flex flex-row items-start space-x-3 space-y-0 rounded-md border p-4">
                          <FormControl>
                            <Checkbox
                              checked={field.value}
                              onCheckedChange={field.onChange}
                              aria-label="Product has multiple variants"
                            />
                          </FormControl>
                          <div className="space-y-1 leading-none">
                            <FormLabel>
                              This product has multiple variants
                            </FormLabel>
                            <FormDescription>
                              Enable if your product comes in different options
                              like sizes or colors.
                            </FormDescription>
                          </div>
                        </FormItem>
                      )}
                    />

                    {form.watch("hasVariants") && (
                      <div className="rounded-md border p-4">
                        <h3 className="font-medium mb-2">Variant Options</h3>
                        <p className="text-sm text-muted-foreground mb-4">
                          After creating your product, you'll be able to add
                          variants like size, color, material, etc.
                        </p>
                      </div>
                    )}
                  </div>
                </TabsContent>

                {/* Shipping Tab */}
                <TabsContent value="shipping" className="space-y-6 pt-2">
                  <div className="bg-muted/40 p-4 rounded-lg mb-6">
                    <h3 className="text-sm font-medium mb-2 flex items-center">
                      <Info className="h-4 w-4 mr-2" />
                      Shipping Options
                    </h3>
                    <p className="text-sm text-muted-foreground">
                      Configure shipping settings for your product.
                    </p>
                  </div>

                  <div className="space-y-4">
                    <FormField
                      control={form.control}
                      name="requiresShipping"
                      render={({ field }) => (
                        <FormItem className="flex flex-row items-start space-x-3 space-y-0 rounded-md border p-4">
                          <FormControl>
                            <Checkbox
                              checked={field.value}
                              onCheckedChange={field.onChange}
                              aria-label="This is a physical product"
                            />
                          </FormControl>
                          <div className="space-y-1 leading-none">
                            <FormLabel>This is a physical product</FormLabel>
                            <FormDescription>
                              Uncheck for digital or service products that don't
                              require shipping.
                            </FormDescription>
                          </div>
                        </FormItem>
                      )}
                    />

                    {form.watch("requiresShipping") && (
                      <FormField
                        control={form.control}
                        name="isFreeShipping"
                        render={({ field }) => (
                          <FormItem className="flex flex-row items-start space-x-3 space-y-0 rounded-md border p-4">
                            <FormControl>
                              <Checkbox
                                checked={field.value}
                                onCheckedChange={field.onChange}
                                aria-label="Free shipping"
                              />
                            </FormControl>
                            <div className="space-y-1 leading-none">
                              <FormLabel>Free shipping</FormLabel>
                              <FormDescription>
                                Offer free shipping for this product.
                              </FormDescription>
                            </div>
                          </FormItem>
                        )}
                      />
                    )}
                  </div>
                </TabsContent>
              </Tabs>

              <Separator />

              <FormField
                control={form.control}
                name="termsAccepted"
                render={({ field }) => (
                  <FormItem className="flex flex-row items-start space-x-3 space-y-0">
                    <FormControl>
                      <Checkbox
                        checked={field.value}
                        onCheckedChange={field.onChange}
                        aria-required="true"
                        aria-invalid={!!form.formState.errors.termsAccepted}
                      />
                    </FormControl>
                    <div className="space-y-1 leading-none">
                      <FormLabel>Terms and Conditions*</FormLabel>
                      <FormDescription>
                        I agree to the marketplace's terms and conditions, and
                        confirm that my product complies with all applicable
                        laws and regulations.
                      </FormDescription>
                    </div>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </form>
          </Form>
        </CardContent>
        <CardFooter className="flex flex-col sm:flex-row gap-4 items-center justify-between">
          <div className="flex gap-2">
            {currentTab !== TAB_ORDER[0] && (
              <Button
                type="button"
                variant="outline"
                onClick={() => navigateTab("prev")}
                className="flex items-center gap-1"
                aria-label="Previous tab"
              >
                <ChevronLeft className="h-4 w-4" />
                <span className="hidden sm:inline">Previous</span>
              </Button>
            )}
            {currentTab !== TAB_ORDER[TAB_ORDER.length - 1] && (
              <Button
                type="button"
                onClick={() => navigateTab("next")}
                className="flex items-center gap-1"
                aria-label="Next tab"
              >
                <span className="hidden sm:inline">Next</span>
                <ChevronRight className="h-4 w-4" />
              </Button>
            )}
          </div>
          <div className="flex gap-4">
            <Button
              type="button"
              variant="outline"
              onClick={() => form.reset()}
              aria-label="Save as Draft"
            >
              Save as Draft
            </Button>
            <Button
              type="submit"
              disabled={isSubmitting}
              onClick={() => formRef.current?.requestSubmit()}
              aria-label="Publish Product"
            >
              {isSubmitting && (
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              )}
              Publish Product
            </Button>
          </div>
        </CardFooter>
      </Card>
    </div>
  )
}
