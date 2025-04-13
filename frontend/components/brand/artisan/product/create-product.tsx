"use client";

import {  useMutation } from "@tanstack/react-query";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { Loader2, Plus, X, ImagePlus, HelpCircle } from "lucide-react";
import { useState } from "react";
import api from "@/lib/axios";
import { toast } from "sonner";

import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { productFormSchema, ProductFormValues } from "./types";
import { productCategories, quantityUnits } from "./lib";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { AlertCircle } from "lucide-react";

export default function CreateProduct() {
  const [imageFiles, setImageFiles] = useState<File[]>([]);
  const [videoFiles, setVideoFiles] = useState<File[]>([]);
  const [imageUrls, setImageUrls] = useState<string[]>([]);
  const [videoUrls, setVideoUrls] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [uploadProgress, setUploadProgress] = useState<{
    images: boolean;
    videos: boolean;
    creating: boolean;
  }>({
    images: false,
    videos: false,
    creating: false
  });

  const form = useForm<ProductFormValues>({
    resolver: zodResolver(productFormSchema),
    defaultValues: {
      product_name: "",
      category: "Pottery & Ceramics",
      description: "",
      order_size: "",
      quantity_unit: "Piece",
      order_quantity: 0,
      price: 0,
      product_pic: [],
      product_video: [],
    },
    mode: "onChange",
  });

  const uploadFiles = async (files: File[], type: "product photo" | "product video") => {
    if (!files.length) return [];
    
    const formData = new FormData();
    formData.append("upload_type", type);
    files.forEach(file => {
      formData.append("files", file);
    });

    try {
      if (type === "product photo") {
        setUploadProgress(prev => ({ ...prev, images: true }));
      } else {
        setUploadProgress(prev => ({ ...prev, videos: true }));
      }

      const response = await api.post("/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      if (type === "product photo") {
        setUploadProgress(prev => ({ ...prev, images: false }));
      } else {
        setUploadProgress(prev => ({ ...prev, videos: false }));
      }

      return response.data.urls;
    } catch (error) {
      const errorMessage = `Failed to upload ${type}s`;
      setError(errorMessage);
      toast.error(errorMessage);
      setUploadProgress({
        images: false,
        videos: false,
        creating: false
      });
      throw error;
    }
  };

  const createProductMutation = useMutation({
    mutationFn: async (data: ProductFormValues) => {
      setUploadProgress(prev => ({ ...prev, creating: true }));
      const response = await api.post("/products", data);
      return response.data;
    },
    onSuccess: () => {
      setError(null);
      toast.success("Product created successfully!");
      form.reset();
      setImageFiles([]);
      setVideoFiles([]);
      setImageUrls([]);
      setVideoUrls([]);
      setIsSubmitting(false);
      setUploadProgress({
        images: false,
        videos: false,
        creating: false
      });
    },
    onError: (error: any) => {
      const errorMessage = error?.response?.data?.message || "Failed to create product";
      setError(errorMessage);
      toast.error(errorMessage);
      setIsSubmitting(false);
      setUploadProgress({
        images: false,
        videos: false,
        creating: false
      });
    },
  });

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>, type: "image" | "video") => {
    const files = Array.from(event.target.files || []);
    if (type === "image") {
      setImageFiles(prev => [...prev, ...files]);
      const newUrls = files.map(file => URL.createObjectURL(file));
      setImageUrls(prev => [...prev, ...newUrls]);
    } else {
      setVideoFiles(prev => [...prev, ...files]);
      const newUrls = files.map(file => URL.createObjectURL(file));
      setVideoUrls(prev => [...prev, ...newUrls]);
    }
  };

  const removeFile = (index: number, type: "image" | "video") => {
    if (type === "image") {
      setImageFiles(prev => prev.filter((_, i) => i !== index));
      setImageUrls(prev => {
        const newUrls = prev.filter((_, i) => i !== index);
        return newUrls;
      });
    } else {
      setVideoFiles(prev => prev.filter((_, i) => i !== index));
      setVideoUrls(prev => {
        const newUrls = prev.filter((_, i) => i !== index);
        return newUrls;
      });
    }
  };

  const onSubmit = async (data: ProductFormValues) => {
    try {
      if (isSubmitting) return;
      setIsSubmitting(true);
      setError(null);

      // Validate the form data
      const result = productFormSchema.safeParse(data);
      if (!result.success) {
        setError("Please fill in all required fields correctly");
        setIsSubmitting(false);
        return;
      }

      const uploadedImageUrls = await uploadFiles(imageFiles, "product photo");
      const uploadedVideoUrls = await uploadFiles(videoFiles, "product video");

      const productData = {
        ...data,
        product_pic: uploadedImageUrls,
        product_video: uploadedVideoUrls,
        order_quantity: Number(data.order_quantity),
        price: Number(data.price),
        order_size: data.order_size,
      };

      await createProductMutation.mutateAsync(productData);
    } catch (error: any) {
      const errorMessage = error?.response?.data?.message || "Error creating product";
      setError(errorMessage);
      setIsSubmitting(false);
      setUploadProgress({
        images: false,
        videos: false,
        creating: false
      });
      console.error("Error creating product:", error);
    }
  };

  return (
    <div className="container mx-auto p-6">
      <Card className="max-w-6xl mx-auto">
        <CardHeader>
          <CardTitle className="text-2xl font-bold">Create New Product</CardTitle>
          <CardDescription>Fill in the details below to create your new product listing</CardDescription>
          {error && (
            <Alert variant="destructive" className="mt-4">
              <AlertCircle className="h-4 w-4" />
              <AlertTitle>Error</AlertTitle>
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}
          {(uploadProgress.images || uploadProgress.videos || uploadProgress.creating) && (
            <Alert className="mt-4">
              <Loader2 className="h-4 w-4 animate-spin" />
              <AlertTitle>Progress</AlertTitle>
              <AlertDescription>
                {uploadProgress.images && "Uploading images..."}
                {uploadProgress.videos && "Uploading videos..."}
                {uploadProgress.creating && "Creating product..."}
              </AlertDescription>
            </Alert>
          )}
        </CardHeader>
        <CardContent>
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Left Column */}
                <div className="space-y-6">
                  <FormField
                    control={form.control}
                    name="product_name"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Product Name</FormLabel>
                        <FormControl>
                          <Input placeholder="Enter your product name" {...field} />
                        </FormControl>
                          <FormDescription>Choose a clear and descriptive name</FormDescription>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="category"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Category</FormLabel>
                        <Select onValueChange={field.onChange} defaultValue={field.value}>
                          <FormControl>
                            <SelectTrigger>
                              <SelectValue placeholder="Select product category" />
                            </SelectTrigger>
                          </FormControl>
                          <SelectContent>
                            {productCategories.map((category) => (
                              <SelectItem key={category} value={category}>
                                {category}
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                        <FormDescription>Choose the most relevant category</FormDescription>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="description"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Description</FormLabel>
                        <FormControl>
                          <Textarea 
                            placeholder="Describe your product's features, materials, and unique selling points"
                            className="min-h-[120px]"
                            {...field} 
                          />
                        </FormControl>
                        <FormDescription>Provide detailed information about your product</FormDescription>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <div className="space-y-4">
                    <FormLabel>Product Images</FormLabel>
                    <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
                      {imageUrls.map((url, index) => (
                        <div key={index} className="relative group">
                          <img src={url} alt="preview" className="w-full aspect-square object-cover rounded-lg" />
                          <Button
                            type="button"
                            variant="destructive"
                            size="icon"
                            className="absolute -top-2 -right-2 h-6 w-6 opacity-0 group-hover:opacity-100 transition-opacity"
                            onClick={() => removeFile(index, "image")}
                          >
                            <X className="h-4 w-4" />
                          </Button>
                        </div>
                      ))}
                      <label className="aspect-square border-2 border-dashed rounded-lg flex flex-col items-center justify-center cursor-pointer hover:border-primary hover:bg-secondary/50 transition-colors">
                        <input
                          type="file"
                          accept="image/*"
                          multiple
                          className="hidden"
                          onChange={(e) => handleFileChange(e, "image")}
                        />
                        <ImagePlus className="h-8 w-8 mb-2" />
                        <span className="text-sm text-muted-foreground">Add Images</span>
                      </label>
                    </div>
                    <FormDescription>Upload clear, high-quality product images</FormDescription>
                  </div>
                </div>

                {/* Right Column */}
                <div className="space-y-6">
                  <div className="grid grid-cols-2 gap-4">
                    <FormField
                      control={form.control}
                      name="order_size"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Minimum Order Size</FormLabel>
                          <FormControl>
                            <Input type="number" placeholder="e.g. 100" {...field} onChange={(e) => field.onChange(e.target.value)} />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />

                    <FormField
                      control={form.control}
                      name="quantity_unit"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Quantity Unit</FormLabel>
                          <Select onValueChange={field.onChange} defaultValue={field.value}>
                            <FormControl>
                              <SelectTrigger>
                                <SelectValue placeholder="Select unit" />
                              </SelectTrigger>
                            </FormControl>
                            <SelectContent>
                              {quantityUnits.map((unit) => (
                                <SelectItem key={unit} value={unit}>
                                  {unit}
                                </SelectItem>
                              ))}
                            </SelectContent>
                          </Select>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <FormField
                      control={form.control}
                      name="order_quantity"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Available Stock</FormLabel>
                          <FormControl>
                            <Input
                              type="number"
                              placeholder="e.g. 1000"
                              {...field}
                              onChange={(e) => field.onChange(Number(e.target.value))}
                            />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />

                    <FormField
                      control={form.control}
                      name="price"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Price</FormLabel>
                          <FormControl>
                            <Input
                              type="number"
                              placeholder="Enter price"
                              {...field}
                              onChange={(e) => field.onChange(Number(e.target.value))}
                            />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                  </div>

                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <FormLabel>Product Videos (Optional)</FormLabel>
                      <HelpCircle className="h-4 w-4 text-muted-foreground" />
                    </div>
                    <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
                      {videoUrls.map((url, index) => (
                        <div key={index} className="relative group">
                          <video src={url} className="w-full aspect-square object-cover rounded-lg" />
                          <Button
                            type="button"
                            variant="destructive"
                            size="icon"
                            className="absolute -top-2 -right-2 h-6 w-6 opacity-0 group-hover:opacity-100 transition-opacity"
                            onClick={() => removeFile(index, "video")}
                          >
                            <X className="h-4 w-4" />
                          </Button>
                        </div>
                      ))}
                      <label className="aspect-square border-2 border-dashed rounded-lg flex flex-col items-center justify-center cursor-pointer hover:border-primary hover:bg-secondary/50 transition-colors">
                        <input
                          type="file"
                          accept="video/*"
                          multiple
                          className="hidden"
                          onChange={(e) => handleFileChange(e, "video")}
                        />
                        <Plus className="h-8 w-8 mb-2" />
                        <span className="text-sm text-muted-foreground">Add Videos</span>
                      </label>
                    </div>
                    <FormDescription>Upload product videos to showcase features and usage</FormDescription>
                  </div>
                </div>
              </div>

              <div className="flex justify-end gap-4 pt-6">
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => {
                    form.reset();
                    setImageFiles([]);
                    setVideoFiles([]);
                    setImageUrls([]);
                    setVideoUrls([]);
                  }}
                  className="w-32"
                >
                  Reset
                </Button>
                <Button
                  type="submit"
                  className="w-32"
                  disabled={isSubmitting}
                >
                  {isSubmitting && (
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  )}
                  {isSubmitting ? "Creating..." : "Create"}
                </Button>
              </div>
            </form>
          </Form>
        </CardContent>
      </Card>
    </div>
  );
}
