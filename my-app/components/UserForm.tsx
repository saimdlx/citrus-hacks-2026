"use client";

import React, { useState } from "react";
import { useForm } from "react-hook-form";
// import { zodResolver } from "@hookform/resolvers/zod";
// import * as z from "zod";

// NOTE: Uncomment specific Zod resolver lines after running:
// npm install react-hook-form zod @hookform/resolvers lucide-react framer-motion clsx tailwind-merge

// Fallback types if Zod is not installed temporarily
type FormValues = {
  name: string;
  email: string;
  location: string;
  interests: string;
};

export default function UserForm() {
  const [recommendation, setRecommendation] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  // Zod can be integrated by adding the resolver back in
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormValues>();

  const onSubmit = async (data: FormValues) => {
    setLoading(true);
    setRecommendation(null);
    
    // In a real application, this sends data to the External Orchestrator
    try {
      const response = await fetch("/api/orchestrator", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...data,
          interests: data.interests.split(",").map(i => i.trim()),
        }),
      });
      
      const result = await response.json();
      setRecommendation(result.message);
    } catch (err) {
      console.error(err);
      // For demonstration purposes, we show a mock output if the fetch fails
      setTimeout(() => {
        setRecommendation("🎉 Found 3 local indie concerts happening near you this weekend!\n\n[Google Maps route attached]");
        setLoading(false);
      }, 1500);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-[#1a1a2e] to-[#16213e] p-6 text-white font-sans w-full">
      <div className="w-full max-w-md bg-white/5 backdrop-blur-xl border border-white/10 p-8 rounded-3xl shadow-2xl relative overflow-hidden">
        {/* Decorative elements */}
        <div className="absolute top-0 right-0 w-32 h-32 bg-teal-500/20 rounded-full blur-3xl -mr-10 -mt-10"></div>
        <div className="absolute bottom-0 left-0 w-32 h-32 bg-blue-500/20 rounded-full blur-3xl -ml-10 -mb-10"></div>
        
        <div className="relative z-10">
          <h1 className="text-4xl font-extrabold mb-3 bg-clip-text text-transparent bg-gradient-to-r from-teal-400 to-blue-500 tracking-tight">
            Find Your Vibe.
          </h1>
          <p className="text-gray-400 mb-8 text-sm">
            Tell us about yourself and let our AI orchestrator curate the perfect local events just for you.
          </p>

          <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-5">
            {/* Name Field */}
            <div>
              <label className="block text-sm font-medium mb-1.5 text-gray-300">Name</label>
              <input
                {...register("name", { required: "Name is required" })}
                placeholder="Alex Doe"
                className="w-full px-4 py-3 bg-black/20 border border-white/10 rounded-xl focus:outline-none focus:ring-2 focus:ring-teal-400/50 transition-all text-white placeholder-gray-500"
              />
              {errors.name && <span className="text-red-400 text-xs mt-1.5 block">{errors.name.message}</span>}
            </div>

            {/* Email Field */}
            <div>
              <label className="block text-sm font-medium mb-1.5 text-gray-300">Email</label>
              <input
                {...register("email", { required: "Email is required" })}
                type="email"
                placeholder="alex@example.com"
                className="w-full px-4 py-3 bg-black/20 border border-white/10 rounded-xl focus:outline-none focus:ring-2 focus:ring-teal-400/50 transition-all text-white placeholder-gray-500"
              />
              {errors.email && <span className="text-red-400 text-xs mt-1.5 block">{errors.email.message}</span>}
            </div>

            {/* Location Field */}
            <div>
              <label className="block text-sm font-medium mb-1.5 text-gray-300">Location</label>
              <input
                {...register("location", { required: "Location is required" })}
                placeholder="Los Angeles, CA"
                className="w-full px-4 py-3 bg-black/20 border border-white/10 rounded-xl focus:outline-none focus:ring-2 focus:ring-teal-400/50 transition-all text-white placeholder-gray-500"
              />
              {errors.location && <span className="text-red-400 text-xs mt-1.5 block">{errors.location.message}</span>}
            </div>

            {/* Interests Field */}
            <div>
              <label className="block text-sm font-medium mb-1.5 text-gray-300">Interests</label>
              <textarea
                {...register("interests", { required: "Please tell us your interests" })}
                placeholder="e.g. Indie music, tech networking, food festivals"
                rows={3}
                className="w-full px-4 py-3 bg-black/20 border border-white/10 rounded-xl focus:outline-none focus:ring-2 focus:ring-teal-400/50 transition-all text-white placeholder-gray-500 resize-none"
              />
              {errors.interests && <span className="text-red-400 text-xs mt-1.5 block">{errors.interests.message}</span>}
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="mt-4 w-full py-3.5 bg-gradient-to-r from-teal-400/80 to-blue-500/80 hover:from-teal-400 hover:to-blue-500 text-white font-semibold rounded-xl shadow-lg transform transition-all active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed border border-white/10"
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <svg className="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Curating Events...
                </span>
              ) : (
                "Discover local events"
              )}
            </button>
          </form>
        </div>
      </div>

      {/* Results Display Area */}
      {recommendation && (
        <div className="w-full max-w-md mt-6 bg-black/30 border border-teal-500/20 p-6 rounded-2xl animate-in fade-in slide-in-from-bottom-4 duration-700 shadow-xl backdrop-blur-md">
          <h2 className="text-lg font-semibold mb-3 text-teal-300 flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-teal-400 animate-pulse"></span>
            Your AI Curated Events
          </h2>
          <div className="prose prose-invert max-w-none text-sm text-gray-300 leading-relaxed whitespace-pre-line">
            {recommendation}
          </div>
        </div>
      )}
    </div>
  );
}
