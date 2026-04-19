#!/usr/bin/env python3
import os
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

mcp = FastMCP("Event Recommender MCP Server")

@mcp.tool(description="Analyze deterministic user preferences, find local events using APIs, and formulate a formatted recommendation message.")
def generate_recommendation(
    user_name: str, 
    email: str, 
    location: str, 
    deterministic_keywords: list[str]
) -> str:
    """
    Called by the orchestrating agent with user profile and deterministic keywords.
    Uses Gemini API to interpret tools and return the completed string.
    """
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_api_key:
        return "Error: GEMINI_API_KEY environment variable is missing."

    client = genai.Client(api_key=gemini_api_key)
    
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
        f"Algorithm-derived Keywords: {', '.join(deterministic_keywords)}\n\n"
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
    host = "0.0.0.0"
    
    print(f"Starting FastMCP server on {host}:{port}")

    
    mcp.run(
        transport="http",
        host=host,
        port=port,
        stateless_http=True
    )
