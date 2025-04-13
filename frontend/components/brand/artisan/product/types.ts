import { z } from "zod";
import { productCategories, quantityUnits } from "./lib";


export const productFormSchema = z.object({
    product_name: z.string().min(3, "Product name must be at least 3 characters"),
    product_pic: z.array(z.string()).min(1, "At least one product image is required"),
    product_video: z.array(z.string()).optional(),
    category: z.enum(productCategories),
    description: z.string().min(20, "Description must be at least 20 characters"),
    order_size: z.string().min(1, "Minimum order size is required"),
    order_quantity: z.number().positive("Quantity must be positive"),
    quantity_unit: z.enum(quantityUnits),
    price: z.number().positive("Price must be positive"),
  });
  
  export type ProductFormValues = z.infer<typeof productFormSchema>;