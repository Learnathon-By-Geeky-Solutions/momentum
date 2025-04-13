import { z } from "zod";

export const brandFormSchema = z.object({
    brand_name: z.string().min(2, "Brand name must be at least 2 characters"),
    brand_description: z.string().min(10, "Description must be at least 10 characters"),
    logo: z.instanceof(File).optional(),
  });
  
  export type BrandFormValues = z.infer<typeof brandFormSchema>;