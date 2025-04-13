'use client';

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import api from "@/lib/axios";
import { useMutation } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { toast } from "sonner";

const BecomeArtisan = () => {
    const router = useRouter();

    const mutation = useMutation({
        mutationFn: async () => {
            const response = await api.put("/become-artisan")
            return response.data
        },
        onSuccess: () => {
            toast.success("Successfully became an artisan!");
            router.push('/dashboard');

            const user = localStorage.getItem("user");
            if (user) {
                const userData = JSON.parse(user);
                userData.role = "artisan";
                localStorage.setItem("user", JSON.stringify(userData));
            }
        },
        onError: (error) => {
            toast.error("Failed to become an artisan. Please try again.");
            console.error(error);
        }
    });

    return (
        <div className="container mx-auto py-10">
            {
                mutation.isPending && (
                    <div className="container mx-auto py-10">
                        <div className="flex items-center justify-center">
                            <div className="w-10 h-10 border-t-transparent border-b-transparent border-r-transparent border-l-blue-500 rounded-full animate-spin"></div>
                        </div>
                    </div>
                )


            }

            {
                mutation.isError && (
                    <div className="container mx-auto py-10">
                        <div className="flex items-center justify-center">
                            <div className="w-10 h-10 border-t-transparent border-b-transparent border-r-transparent border-l-blue-500 rounded-full animate-spin"></div>
                        </div>
                    </div>
                )
            }
            <Card className="max-w-3xl mx-auto border-none shadow-lg">
                <CardHeader className="text-center space-y-2">
                    <CardTitle className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-blue-500 bg-clip-text text-transparent">Become an Artisan</CardTitle>
                    <CardDescription className="text-lg">
                        Join our vibrant community of creators and bring your craft to the world
                    </CardDescription>
                </CardHeader>
                <CardContent className="px-8">
                    <div className="space-y-8">
                        <div className="bg-gradient-to-r from-purple-50 to-blue-50 p-6 rounded-xl">
                            <h3 className="text-xl font-semibold flex items-center gap-2 text-purple-700">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-gift"><path d="M20 12v10H4V12" /><path d="M2 7h20v5H2z" /><path d="M12 22V7" /><path d="M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7z" /><path d="M12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z" /></svg>
                                Benefits
                            </h3>
                            <div className="mt-4 grid md:grid-cols-2 gap-4">
                                <div className="flex items-center gap-3 p-3 bg-white rounded-lg shadow-sm">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-purple-500"><path d="M3 11v3a1 1 0 0 0 1 1h16a1 1 0 0 0 1-1v-3" /><path d="M12 19H4a1 1 0 0 1-1-1v-2" /><path d="M20 19h-8" /><path d="M12 19v-3" /><path d="M12 16h8a1 1 0 0 0 1-1v-2" /><path d="M4 13h16" /><path d="M3 8a3 3 0 0 1 3-3h12a3 3 0 0 1 3 3v2a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V8Z" /></svg>
                                    Create your brand
                                </div>
                                <div className="flex items-center gap-3 p-3 bg-white rounded-lg shadow-sm">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-purple-500"><path d="m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l8.57-8.57A4 4 0 1 1 18 8.84l-8.59 8.57a2 2 0 0 1-2.83-2.83l8.49-8.48" /></svg>
                                    Showcase products
                                </div>
                                <div className="flex items-center gap-3 p-3 bg-white rounded-lg shadow-sm">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-purple-500"><path d="M14 9a2 2 0 0 1-2 2H6l-4 4V4c0-1.1.9-2 2-2h8a2 2 0 0 1 2 2v5Z" /><path d="M18 9h2a2 2 0 0 1 2 2v11l-4-4h-6a2 2 0 0 1-2-2v-1" /></svg>
                                    Direct customer connect
                                </div>
                                <div className="flex items-center gap-3 p-3 bg-white rounded-lg shadow-sm">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-purple-500"><path d="M12 2v20" /><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" /></svg>
                                    Flexible pricing
                                </div>
                            </div>
                        </div>

                        <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-6 rounded-xl">
                            <h3 className="text-xl font-semibold flex items-center gap-2 text-blue-700">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-check-circle"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" /><path d="m9 11 3 3L22 4" /></svg>
                                Requirements
                            </h3>
                            <div className="mt-4 grid md:grid-cols-2 gap-4">
                                <div className="flex items-center gap-3 p-3 bg-white rounded-lg shadow-sm">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-blue-500"><rect width="18" height="11" x="3" y="11" rx="2" ry="2" /><path d="M7 11V7a5 5 0 0 1 10 0v4" /></svg>
                                    Valid identification
                                </div>
                                <div className="flex items-center gap-3 p-3 bg-white rounded-lg shadow-sm">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-blue-500"><path d="M12 2l9 4.9V12" /><path d="M12 2 3 6.9V12" /><path d="M12 22v-6" /><path d="M12 13V2" /><path d="m2 12 10 5 10-5" /></svg>
                                    Quality products
                                </div>
                                <div className="flex items-center gap-3 p-3 bg-white rounded-lg shadow-sm">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-blue-500"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z" /></svg>
                                    Customer service
                                </div>
                                <div className="flex items-center gap-3 p-3 bg-white rounded-lg shadow-sm">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-blue-500"><path d="M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8" /><path d="M21 3v5h-5" /></svg>
                                    Regular updates
                                </div>
                            </div>
                        </div>

                        <Button
                            onClick={() => mutation.mutate()}
                            disabled={mutation.isPending}
                            className="w-full bg-gradient-to-r from-purple-600 to-blue-500 hover:from-purple-700 hover:to-blue-600 text-white py-6 text-lg font-semibold rounded-xl transition-all duration-200 transform hover:scale-[1.02]"
                        >
                            {mutation.isPending ? (
                                <div className="flex items-center justify-center gap-2">
                                    <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                    </svg>
                                    Processing...
                                </div>
                            ) : (
                                "Start Your Artisan Journey"
                            )}
                        </Button>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
};

export default BecomeArtisan;