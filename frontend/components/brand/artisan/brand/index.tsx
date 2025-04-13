"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { useMutation } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { toast } from "sonner";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/provider/useAuth";
import api from "@/lib/axios";
import { brandFormSchema, BrandFormValues } from "./types";  
import { AxiosError } from "axios";



export default function CreateBrand() {
  const router = useRouter();
  const { userRole } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [previewUrl, setPreviewUrl] = useState<string>("");

  

  const form = useForm<BrandFormValues>({
    resolver: zodResolver(brandFormSchema),
    defaultValues: {
      brand_name: "",
      brand_description: "",
    },
  });

  const uploadImage = async (file: File) => {
    const formData = new FormData();
    formData.append("upload_type", "profile");
    formData.append("files", file); 

    const response = await api.post("/upload", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data.urls[0];
  };

  const createBrandMutation = useMutation({
    mutationFn: async (data: BrandFormValues) => {
      let logoUrl = "";
      if (data.logo) {
        logoUrl = await uploadImage(data.logo);
      }

      const brandData = {
        brand_name: data.brand_name,
        brand_description: data.brand_description,
        logo: logoUrl,
      };

      const response = await api.post("/brands", brandData);
      return response.data;
    },
    onSuccess: () => {
      toast.success("Brand created successfully!");
      router.push("/dashboard/brands");
    },
    onError: (error: AxiosError) => {
     toast.error(error.response?.statusText || "Failed to create brand")
    },
  });

  const onSubmit = async (data: BrandFormValues) => {
    setIsLoading(true);
    try {
      await createBrandMutation.mutateAsync(data);
    } finally {
      setIsLoading(false);
    }
  };

  return (
   userRole === "artisan" && (
    <div >
    <Card >
      <CardHeader>
        <CardTitle className="text-2xl font-bold">Create Your Brand</CardTitle>
        <CardDescription>
          Build your brand identity by providing the details below
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
            <FormField
              control={form.control}
              name="brand_name"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Brand Name</FormLabel>
                  <FormControl>
                    <Input 
                      placeholder="Enter your brand name" 
                      {...field}
                      className="w-full"
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="brand_description"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Brand Description</FormLabel>
                  <FormControl>
                    <Textarea
                      placeholder="Describe your brand"
                      className="min-h-[120px]"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="logo"
              render={({ field: { onChange, ...field } }) => (
                <FormItem>
                  <FormLabel>Logo</FormLabel>
                  <FormControl>
                    <div className="space-y-4">
                      <Input
                        type="file"
                        accept="image/*"
                        onChange={(e) => {
                          const file = e.target.files?.[0];
                          if (file) {
                            onChange(file);
                            const reader = new FileReader();
                            reader.onloadend = () => {
                              setPreviewUrl(reader.result as string);
                            };
                            reader.readAsDataURL(file);
                          }
                        }}
                        className="w-full"
                      />
                      {previewUrl && (
                        <div className="mt-2">
                          <img 
                            src={previewUrl} 
                            alt="Logo preview" 
                            className="max-w-[200px] h-auto"
                          />
                        </div>
                      )}
                    </div>
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <Button
              type="submit"
              className="w-full"
              disabled={isLoading}
            >
              {isLoading ? "Creating..." : "Create Brand"}
            </Button>
          </form>
        </Form>
      </CardContent>
    </Card>
  </div>
   )
  );
}
