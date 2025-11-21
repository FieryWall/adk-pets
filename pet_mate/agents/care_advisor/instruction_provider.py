import os
import json
from google import genai
from google.genai import types

# --- 1. Subagent Simulation: Instruction Provider (The Tool) ---

# Mock data simulating the "core care instructions generated earlier"
CORE_INSTRUCTIONS_DB = {
    "dog": {
        "emergency": "If your dog is choking or bleeding severely, muzzle the dog first if possible, and transport immediately to the nearest 24hr vet clinic. Keep the wound clean and apply firm pressure.",
        "diet": "Ensure your dog has fresh water access at all times. Feeding guidelines vary by weight; typically 2-3 cups of high-quality kibble divided into two meals. Avoid chocolate, grapes, and onions.",
        "training": "Use positive reinforcement methods. Keep sessions short (5-10 minutes). Focus on consistency for commands like 'sit', 'stay', and 'come'."
    },
    "cat": {
        "emergency": "For sudden lethargy or inability to urinate, seek immediate veterinary care, as this could be a blocked bladder (especially in male cats). Do not attempt home remedies.",
        "diet": "Cats require taurine, found in meat. Ensure commercial food is labeled complete and balanced. Always keep litter box clean and separate from food/water area.",
        "behavior": "Provide scratching posts (vertical and horizontal) and vertical climbing space. Introduce new pets slowly over a period of 1-2 weeks."
    }
}

def get_core_care_instructions(pet_type: str, situation_keywords: str) -> str:
    """
    Retrieves core care instructions for a specific pet type and situation.
    
    This function simulates the 'Instruction Provider' subagent.
    It accesses a specialized knowledge base to supply relevant parts
    of pre-generated core care instructions to the parent agent.

    Args:
        pet_type: The type of pet (e.g., 'dog', 'cat').
        situation_keywords: Keywords describing the current situation (e.g., 'emergency', 'diet', 'behavior').

    Returns:
        A string containing the relevant core instructions, or a message if none are found.
    """
    pet_type = pet_type.lower()
    
    if pet_type in CORE_INSTRUCTIONS_DB:
        # Check if any keyword matches the known instruction types
        for key, instruction in CORE_INSTRUCTIONS_DB[pet_type].items():
            if key in situation_keywords.lower():
                return f"Core Instruction for {pet_type.capitalize()} ({key}): {instruction}"
        
        # If no specific keyword match, return general advice for the pet
        return f"General Core Instruction for {pet_type.capitalize()}: {CORE_INSTRUCTIONS_DB[pet_type].get('diet', 'No specific core instruction found, but general care is always important.')}"
    
    return f"Pet type '{pet_type}' not found in the core knowledge base."
