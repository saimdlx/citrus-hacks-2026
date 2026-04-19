import numpy as np
import torch
from sentence_transformers import SentenceTransformer, util

# We initialize these as None and lazily load them upon first tool execution.
# This prevents the 400MB HuggingFace download from completely blocking Render's boot cycle!
model = None
KEYWORD_EMBEDDINGS = None

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
    global model, KEYWORD_EMBEDDINGS
    if model is None:
        print("Downloading/Loading Semantic Model...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        KEYWORD_EMBEDDINGS = model.encode(PREDEFINED_KEYWORDS, convert_to_tensor=True)

def run_semantic_algorithm(profile: dict, threshold: float = 0.40) -> list[str]:
    """
    A semantic search recommender that maps a user's freeform interests
    to actionable event keywords using Cosine Similarity on text embeddings.
    """
    load_model_if_needed()
    interests = profile.get("interests", [])
    
    if not interests:
        return ["local events", "entertainment"]
    
    # Optional weighting based on age or other demographics could go here
    age = profile.get("age", 25)
    
    selected_keywords = set()
    
    for interest in interests:
        interest_embedding = model.encode(interest, convert_to_tensor=True)
        # Calculate cosine similarities
        cosine_scores = util.cos_sim(interest_embedding, KEYWORD_EMBEDDINGS)[0]
        
        # Find keywords above threshold
        for idx, score in enumerate(cosine_scores):
            if score.item() >= threshold:
                selected_keywords.add(PREDEFINED_KEYWORDS[idx])
                
    if not selected_keywords:
        # Fallback if no strong semantic matches were found
        selected_keywords.add("local events")
        
    return list(selected_keywords)

if __name__ == "__main__":
    test_profile = {
        "name": "Jane",
        "email": "jane@example.com",
        "location": "Los Angeles",
        "age": 22,
        # "gaming and software" strongly relates to "tech meetup" and "hackathon"
        # "symphony" relates to "classical music" and "concert"
        "interests": ["gaming and software", "symphony", "baking and desserts"]
    }
    
    print("Testing Semantic Search Recommender...")
    print(f"Profile Interests: {test_profile['interests']}")
    extracted = run_semantic_algorithm(test_profile)
    print(f"Semantic Algorithm Output: {extracted}")
