import { NextResponse } from 'next/server';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

export async function POST(request: Request) {
  try {
    const data = await request.json();

    // 1. Sync User Information to the Persistent Datastore via Prisma
    // We use upsert to create or update the user based on their email.
    const user = await prisma.user.upsert({
      where: { email: data.email },
      update: {
        name: data.name,
        location: data.location,
        interests: data.interests // Raw string mapped via Prisma
      },
      create: {
        name: data.name,
        email: data.email,
        location: data.location,
        interests: data.interests
      }
    });

    // 2. The Next.js Backend acts as a Proxy Webhook.
    // Immediately after the persistent storage is synchronized, it pushes the
    // updated profile state over the MCP protocol to wake the Orchestrator via Python.
    const mcpRequest = {
      jsonrpc: "2.0",
      id: Date.now().toString(),
      method: "tools/call",
      params: {
        name: "generate_recommendation",
        arguments: {
          user_name: user.name,
          email: user.email,
          location: user.location,
          raw_interests: user.interests // Pass the raw comma-separated string
        }
      }
    };

    // In production, this proxies to your hosted Python Render server
    // In development, it defaults to your local FastMCP instance
    const BACKEND_URL = process.env.MCP_BACKEND_URL || "http://localhost:8000";

    const response = await fetch(BACKEND_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(mcpRequest)
    });

    if (!response.ok) {
      return NextResponse.json(
        { error: "Stored in database, but failed to connect to the Python MCP server." },
        { status: response.status }
      );
    }

    const mcpResult = await response.json();
    return NextResponse.json({ success: true, user_id: user.id, mcpResult });

  } catch (error) {
    console.error("Database/MCP Proxy Error:", error);
    return NextResponse.json({ error: "Internal Server Error" }, { status: 500 });
  }
}
