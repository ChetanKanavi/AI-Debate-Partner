import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import time

import prompts

# Load environment variables from .env file
load_dotenv()

def get_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    return genai.Client(api_key=api_key)

def call_with_retry(client, model, contents, config, max_retries=3):
    """Helper to retry API calls on rate limit errors."""
    for attempt in range(max_retries):
        try:
            return client.models.generate_content(
                model=model,
                contents=contents,
                config=config
            )
        except Exception as e:
            error_str = str(e).lower()
            if "429" in error_str or "quota" in error_str or "rate limit" in error_str:
                if attempt < max_retries - 1:
                    sleep_time = (2 ** attempt) * 5 # 5s, 10s
                    print(f"Rate limited. Retrying in {sleep_time}s...")
                    time.sleep(sleep_time)
                else:
                    raise e
            else:
                raise e

def generate_assessment(current_profile, user_input):
    """Silently assesses the user's input to update their profile."""
    client = get_client()
    if not client:
        return current_profile # Fallback if no API key
        
    system_instruction = prompts.ASSESSOR_SYSTEM_PROMPT.format(
        current_profile=current_profile or "No profile established yet.",
        user_input=user_input
    )
    
    try:
        response = call_with_retry(
            client=client,
            model='gemini-2.5-flash', # using flash for faster/cheaper internal assessment
            contents="Please update the assessment profile based on the system instructions.",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2, # Low temperature for consistent assessment
            )
        )
        return response.text.strip()
    except Exception as e:
        print(f"Assessment Error: {e}")
        return current_profile

def generate_debate_response(persona, topic, assessment_profile, chat_history, latest_input):
    """Generates the persona's response to the user."""
    client = get_client()
    if not client:
        return "Error: GEMINI_API_KEY is missing. Please add it to your .env file."
        
    if persona == "Opponent":
        sys_prompt_template = prompts.OPPONENT_SYSTEM_PROMPT
    else:
        sys_prompt_template = prompts.COACH_SYSTEM_PROMPT
        
    system_instruction = sys_prompt_template.format(
        assessment_profile=assessment_profile or "No profile established yet.",
        topic=topic
    )
    
    # Format chat history for the API
    # genai API expects a list of Content objects for multi-turn
    formatted_contents = []
    for msg in chat_history:
        role = "user" if msg["role"] == "user" else "model"
        formatted_contents.append(
            types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])])
        )
        
    # Add the latest input
    formatted_contents.append(
        types.Content(role="user", parts=[types.Part.from_text(text=latest_input)])
    )
    
    try:
        response = call_with_retry(
            client=client,
            model='gemini-2.5-flash', # Switched to flash due to free tier quota limits
            contents=formatted_contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7, 
            )
        )
        return response.text
    except Exception as e:
        return f"An error occurred while calling the Gemini API: {e}"
