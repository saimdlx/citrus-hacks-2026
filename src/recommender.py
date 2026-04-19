import os
from google import genai
from google.genai import types

client = None

# Predefined categories mapping generic terms to actionable event keywords
PREDEFINED_KEYWORDS = [
    "concert", "indie music", "jazz", "classical music",
    "hackathon", "tech meetup", "coding workshop",
    "food festival", "tasting", "farmers market",
    "art exhibition", "gallery opening",
    "sports event", "marathon", "yoga class",
    "networking", "conference",
    "theater", "comedy show"
]

def load_model_if_needed():
    global client
    if client is None:
        gemini_api_key = os.environ.get("GEMINI_API_KEY")
        client = genai.Client(api_key=gemini_api_key)

def run_semantic_algorithm(profile: dict, threshold: float = 0.50) -> list[str]:
    """
    Acts as a Semantic Filter mapper by leveraging Gemini's core logical similarity mapping
    instead of relying on raw mathematical embedding endpoints which often hit API constraints.
    """
    load_model_if_needed()
    interests = profile.get("interests", [])
    
    if not interests:
        return ["local events", "entertainment"]
    
    prompt = (
        f"User Interests: {', '.join(interests)}\n\n"
        f"Predefined Keywords: {', '.join(PREDEFINED_KEYWORDS)}\n\n"
        "Map the User Interests semantically to the closest matching Predefined Keywords. "
        "Strictly output only a comma-separated list of the matching Predefined Keywords."
    )

    try:
        # We explicitly use the standard text-generation model which undeniably works with your API key
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.0 # Deterministic
            )
        )
        
        # Parse output into clean list
        output_txt = response.text.replace("\n", "").strip()
        matched_keywords = [kw.strip() for kw in output_txt.split(",") if kw.strip()]
        
        if not matched_keywords:
            return ["local events"]
            
        return matched_keywords
        
    except Exception as e:
        print(f"Algorithm failure: {e}", flush=True)
        return ["local events"]

if __name__ == "__main__":
    test_profile = {"interests": ["gaming and software", "symphony", "baking and desserts"]}
    print("Testing Fallback Semantic Recommender...")
    print(run_semantic_algorithm(test_profile))
