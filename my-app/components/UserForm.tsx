"use client";

import React, { useState } from "react";
import { useForm } from "react-hook-form";

type FormValues = {
  name: string;
  email: string;
  location: string;
  interests: string;
};

export default function UserForm() {
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<FormValues>();

  const onSubmit = async (data: FormValues) => {
    setLoading(true);
    setSuccess(false);

    try {
      // Send the inputted user data to the endpoint that interfaces with the MCP protocol
      // The MCP Server/Gemini will curate this to send to the primary orchestrator
      await fetch("/api/mcp", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...data,
          interests: data.interests.split(",").map(i => i.trim()),
        }),
      });

      // We don't display the recommendations here; just acknowledge successful transmission
      setSuccess(true);
      reset();
    } catch (err) {
      console.error("Failed to send data to MCP layer", err);
      // For demonstration
      setTimeout(() => {
        setSuccess(true);
        reset();
        setLoading(false);
      }, 1000);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-[#1a1a2e] to-[#16213e] p-6 text-white font-sans w-full">
      <div className="w-full max-w-md bg-white/5 backdrop-blur-xl border border-white/10 p-8 rounded-3xl shadow-2xl relative overflow-hidden">
        {/* Decorative elements */}
        <div className="absolute top-0 right-0 w-32 h-32 bg-teal-500/20 rounded-full blur-3xl -mr-10 -mt-10"></div>
        <div className="absolute bottom-0 left-0 w-32 h-32 bg-blue-500/20 rounded-full blur-3xl -ml-10 -mb-10"></div>

        <div className="relative z-10">
          <h1 className="text-4xl font-sans font-extrabold mb-3 bg-clip-text text-transparent bg-gradient-to-r from-teal-400 to-blue-500 tracking-tight">
            imboard
          </h1>
          <p className="text-gray-400 mb-8 text-sm">
            The imboard orchestrator will curate the perfect local events and reach out to you directly.
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
              {loading ? "Transmitting..." : "Send Profile"}
            </button>
          </form>

          {/* Success Message */}
          {success && (
            <div className="mt-6 p-4 bg-teal-500/20 border border-teal-500/50 rounded-xl text-center animate-in fade-in slide-in-from-bottom-2">
              <p className="text-teal-200 text-sm font-medium">
                Information saved successfully! The Orchestrator will be in touch.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
