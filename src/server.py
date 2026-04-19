import os
import psycopg2
from psycopg2.extras import RealDictCursor
import json
from fastmcp import FastMCP
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# Import the API tools that Gemini will use
from api_tools import (
    search_ticketmaster,
    search_eventbrite,
    get_map_link,
    scrape_local_events
)

# Import the semantic search mechanism
from recommender import run_semantic_algorithm

mcp = FastMCP("Event Recommender MCP Server")

@mcp.resource("user://{email}/profile")
def get_user_profile(email: str) -> str:
    """
    Called by the Orchestrator to read the latest user profile directly 
    from the persistent PostgreSQL database natively.
    """
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        return json.dumps({"error": "DATABASE_URL environment variable is missing in backend."})
        
    try:
        # Natively connect to the remote Postgres database instance
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # In Prisma, the table is called "User"
        cursor.execute('SELECT * FROM "User" WHERE email = %s', (email,))
        row = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if row:
            # We convert datetime objects (if any) to strings for JSON serialization
            return json.dumps(row, default=str)
        return json.dumps({"error": "User not found."})
    except Exception as e:
        return json.dumps({"error": f"Database error: {str(e)}"})

@mcp.tool(description="Analyze deterministic user preferences, find local events using APIs, and formulate a formatted recommendation message.")
def generate_recommendation(
    user_name: str, 
    email: str, 
    location: str, 
    raw_interests: list[str]
) -> str:
    """
    Called by the orchestrating agent with user profile.
    Uses Semantic Algorithm to map interests, then Gemini API to interpret tools and return string.
    """
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_api_key:
        return "Error: GEMINI_API_KEY environment variable is missing."

    client = genai.Client(api_key=gemini_api_key)
    
    # 1. Process freeform text into deterministic keywords
    resolved_keywords = run_semantic_algorithm({"interests": raw_interests})
    
    system_instruction = (
        "You are an expert event curator and assistant. "
        "Use the provided tools to search for real events in the user's city based on their keywords. "
        "Include the event name, date, description, venue, price, sign-up/ticket url, and a Google Maps link (use get_map_link to generate it). "
        "Make it engaging and personalized to the user's name."
        "CONVERSATIONAL STYLE GUIDELINES:"
        "- drop the corporate filter. no \"how can i help you today\" or \"certainly, i can assist with that\""
        "- use all lowercase for everything"
        "- do not use periods at the end of messages"
        "- never use markdown formatting (no bolding, no headings)"
        "- avoid emojis entirely"
        "- speak like a friend who's already in the middle of a conversation with them, not a new assistant introducing themselves"
    )
    
    prompt = (
        f"User Name: {user_name}\n"
        f"Location: {location}\n"
        f"Algorithm-derived Keywords: {', '.join(resolved_keywords)}\n\n"
        "Please find local events matching these keywords and provide a rich formatted recommendation message."
    )

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                tools=[search_ticketmaster, search_eventbrite, get_map_link, scrape_local_events],
            ),
        )
        return response.text
    except Exception as e:
        return f"Error communicating with Gemini: {str(e)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    
    # Render requires explicit binding to 0.0.0.0 so its scanner can detect the open port.
    print(f"Booting FastMCP Server on 0.0.0.0:{port}...")
    
    # We must use transport="sse" to correctly instantiate the ASGI Web Server explicitly.
    mcp.run(
        transport="sse",
        host="0.0.0.0",
        port=port
    )
