"use client";

import { useQuery, useMutation } from "@tanstack/react-query";
import { format } from "date-fns";
import { Loader2, Pencil } from "lucide-react";
import { useAuth } from "@/provider/useAuth";
import api from "@/lib/axios";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import CreateBrand from "./index";
import {
  Dialog,
  DialogContent,
  DialogTrigger,
} from "@/components/ui/dialog";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { toast } from "sonner";
import { brandFormSchema, BrandFormValues } from "./types";

interface Brand {
  brand_id: number;
  user_id: number;
  brand_name: string;
  brand_description: string;
  logo: string;
  created_at: string;
}

export default function ShowBrand() {
  const { userRole } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [previewUrl, setPreviewUrl] = useState<string>("");

  const { data: brand, isLoading, refetch } = useQuery<Brand>({
    queryKey: ["brand"],
    queryFn: async () => {
      const response = await api.get("/brands/me");
      return response.data;
    },
    staleTime: 1000 * 60 * 5, // 5 minutes
  });

  const form = useForm<BrandFormValues>({
    resolver: zodResolver(brandFormSchema),
    defaultValues: {
      brand_name: brand?.brand_name || "",
      brand_description: brand?.brand_description || "",
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

  const updateBrandMutation = useMutation({
    mutationFn: async (data: BrandFormValues) => {
      let logoUrl = brand?.logo || "";
      if (data.logo) {
        logoUrl = await uploadImage(data.logo);
      }

      const brandData = {
        brand_name: data.brand_name,
        brand_description: data.brand_description,
        logo: logoUrl,
      };

      const response = await api.patch(`/brands/me`, brandData);
      return response.data;
    },
    onSuccess: () => {
      toast.success("Brand updated successfully!");
      setIsEditing(false);
      refetch();
    },
    onError: (error) => {
      toast.error("Failed to update brand");
    },
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  if (!brand) {
    return (
      <div className="container mx-auto p-6">
        <Card className="max-w-2xl mx-auto">
          <CardContent className="p-6 flex flex-col items-center gap-4">
            <p className="text-center text-muted-foreground">No brand found</p>
            <Dialog>
              <DialogTrigger asChild>
                <Button variant="default">Create New Brand</Button>
              </DialogTrigger>
              <DialogContent className="sm:max-w-[600px]">
                <CreateBrand />
              </DialogContent>
            </Dialog>
          </CardContent>
        </Card>
      </div>
    );
  }

  const onSubmit = async (data: BrandFormValues) => {
    await updateBrandMutation.mutateAsync(data);
  };

  return (
    userRole === "artisan" && (
      <div className="container mx-auto p-6">
        <h1 className="text-4xl font-bold text-center mb-8">Brand Profile</h1>
        <Card className="max-w-3xl mx-auto overflow-hidden shadow-lg">
          {!isEditing ? (
            <>
              <CardHeader className="border-b bg-gradient-to-r from-blue-50 to-indigo-50 p-8">
                <div className="flex flex-col md:flex-row items-center gap-8">
                  {brand.logo ? (
                    <img
                      src={brand.logo}
                      alt={brand.brand_name}
                      className="h-32 w-32 rounded-xl object-cover border-2 border-indigo-100 shadow-md transition-transform hover:scale-105"
                    />
                  ) : (
                    <div className="h-32 w-32 rounded-xl bg-gradient-to-br from-gray-100 to-gray-200 flex items-center justify-center">
                      <span className="text-4xl text-gray-400">🏢</span>
                    </div>
                  )}
                  <div className="text-center md:text-left">
                    <CardTitle className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600">
                      {brand.brand_name}
                    </CardTitle>
                    <CardDescription className="mt-3 text-lg">
                      Established on{" "}
                      {format(new Date(brand.created_at), "MMMM dd, yyyy")}
                    </CardDescription>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="p-8">
                <div className="space-y-8">
                  <div>
                    <div className="flex justify-between items-center mb-4">
                      <h3 className="text-xl font-semibold text-indigo-700">About Our Brand</h3>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => {
                          setIsEditing(true);
                          form.reset({
                            brand_name: brand.brand_name,
                            brand_description: brand.brand_description,
                          });
                        }}
                      >
                        <Pencil className="h-4 w-4 mr-2" />
                        Edit
                      </Button>
                    </div>
                    <p className="text-gray-600 leading-relaxed text-lg bg-gray-50 p-4 rounded-lg">
                      {brand.brand_description}
                    </p>
                  </div>
                </div>
              </CardContent>
            </>
          ) : (
            <CardContent className="p-8">
              <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                  <FormField
                    control={form.control}
                    name="brand_name"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Brand Name</FormLabel>
                        <FormControl>
                          <Input {...field} />
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
                          <Textarea {...field} className="min-h-[120px]" />
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
                            />
                            {(previewUrl || brand.logo) && (
                              <div className="mt-2">
                                <img
                                  src={previewUrl || brand.logo}
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

                  <div className="flex gap-4">
                    <Button
                      type="submit"
                      disabled={updateBrandMutation.isPending}
                    >
                      {updateBrandMutation.isPending ? "Updating..." : "Update Brand"}
                    </Button>
                    <Button
                      type="button"
                      variant="outline"
                      onClick={() => setIsEditing(false)}
                    >
                      Cancel
                    </Button>
                  </div>
                </form>
              </Form>
            </CardContent>
          )}
        </Card>
      </div>
    )
  );
}
