import os
import math
from google import genai

# We initialize these as None and lazily load them upon first tool execution.
# This completely prevents any external boot latency!
KEYWORD_EMBEDDINGS = None
# We use the extremely lightweight cloud-computed embedding dimension API
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
    global KEYWORD_EMBEDDINGS, client
    if client is None:
        gemini_api_key = os.environ.get("GEMINI_API_KEY")
        client = genai.Client(api_key=gemini_api_key)
        
    if KEYWORD_EMBEDDINGS is None:
        print("Fetching Semantic Embeddings via Gemini API...")
        response = client.models.embed_content(
            model="text-embedding-004",
            contents=PREDEFINED_KEYWORDS
        )
        # Store as standard python floats
        KEYWORD_EMBEDDINGS = [emb.values for emb in response.embeddings]

def cosine_similarity(v1: list[float], v2: list[float]) -> float:
    dot_product = sum(a * b for a, b in zip(v1, v2))
    mag1 = math.sqrt(sum(a * a for a in v1))
    mag2 = math.sqrt(sum(b * b for b in v2))
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot_product / (mag1 * mag2)

def run_semantic_algorithm(profile: dict, threshold: float = 0.50) -> list[str]:
    """
    A purely cloud-native semantic search recommender that maps a user's freeform 
    interests to actionable event keywords using Cosine Similarity on Google Text Embeddings.
    """
    load_model_if_needed()
    interests = profile.get("interests", [])
    
    if not interests:
        return ["local events", "entertainment"]
    
    selected_keywords = set()
    
    # Process all user interests via batch request to Gemini Embeddings
    response = client.models.embed_content(
        model="text-embedding-004",
        contents=interests
    )
    interest_embeddings = [emb.values for emb in response.embeddings]
    
    for interest_embedding in interest_embeddings:
        # Calculate cosine similarities purely mathematically natively
        for idx, keyword_embedding in enumerate(KEYWORD_EMBEDDINGS):
            score = cosine_similarity(interest_embedding, keyword_embedding)
            if score >= threshold:
                selected_keywords.add(PREDEFINED_KEYWORDS[idx])
                
    if not selected_keywords:
        # Fallback if no strong semantic matches were found
        selected_keywords.add("local events")
        
    return list(selected_keywords)

if __name__ == "__main__":
    test_profile = {
        "interests": ["gaming and software", "symphony", "baking and desserts"]
    }
    print("Testing Semantic API Recommender...")
    print(run_semantic_algorithm(test_profile))
