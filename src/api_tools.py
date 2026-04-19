import os
import requests

def search_ticketmaster(keywords: list[str], city: str, radius: int = 25) -> list[dict]:
    """
    Search Ticketmaster for events matching the keywords in the given city.
    Presently returns mock data pending API keys.
    """
    tm_api_key = os.environ.get("TICKETMASTER_API_KEY")
    if not tm_api_key:
        return [
            {
                "title": f"Mock Ticketmaster Event: {city} {keywords[0].capitalize()} Fest",
                "date": "2026-05-10T19:00:00Z",
                "description": f"A wonderful {keywords[0]} event happening soon in {city}.",
                "url": "https://ticketmaster.mock/event/123",
                "venue": f"{city} Arena",
                "price_range": "$50 - $150"
            }
        ]
    
    # Real implementation would go here:
    # url = f"https://app.ticketmaster.com/discovery/v2/events.json?apikey={tm_api_key}&city={city}&keyword={keywords[0]}&radius={radius}"
    # response = requests.get(url)
    # return response.json()
    return []

def search_eventbrite(keywords: list[str], city: str) -> list[dict]:
    """
    Search Eventbrite for events matching the keywords in the given city.
    Presently returns mock data pending API keys.
    """
    eb_api_key = os.environ.get("EVENTBRITE_API_KEY")
    if not eb_api_key:
        return [
            {
                "title": f"Mock Eventbrite gathering: {city} {keywords[-1].capitalize()} Workshop",
                "date": "2026-05-15T10:00:00Z",
                "description": f"Join us for an interactive {keywords[-1]} workshop in {city}.",
                "url": "https://eventbrite.mock/e/456",
                "venue": f"Downtown {city} Center",
                "price": "Free"
            }
        ]
    
    # Real implementation would go here
    return []

def get_map_link(address: str) -> str:
    """
    Generate a Google Maps URL for the given address.
    """
    # Simply URL encode the address for Google Maps
    import urllib.parse
    encoded_address = urllib.parse.quote(address)
    return f"https://www.google.com/maps/search/?api=1&query={encoded_address}"

def scrape_local_events(city: str) -> list[dict]:
    """
    Mock scraper for local social media events.
    """
    return [
        {
            "title": f"Local {city} Indie Concert",
            "date": "2026-04-20T20:00:00Z",
            "description": "Found via social media scraping. Support local bands!",
            "url": "https://instagram.mock/p/789",
            "venue": "Underground Pub",
            "source": "Social Media"
        }
    ]
