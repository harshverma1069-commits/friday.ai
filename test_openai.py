#!/usr/bin/env python
"""Test script to verify OpenAI API connection."""

import os
import sys

try:
    from dotenv import load_dotenv
except ImportError:
    print("Error: python-dotenv is not installed. Run: pip install -r requirements.txt")
    sys.exit(1)

try:
    import openai
except ImportError:
    print("Error: openai package is not installed. Run: pip install -r requirements.txt")
    sys.exit(1)

# Load environment variables from .env
load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")

if not api_key or api_key == "your_api_key_here":
    print("[X] OPENAI_API_KEY is not set or is still the placeholder value.")
    print("\nTo fix this:")
    print("1. Get your API key from https://platform.openai.com/account/api-keys")
    print("2. Edit .env and replace 'your_api_key_here' with your actual key")
    print("3. Save the file and run this test again")
    sys.exit(1)

try:
    print("[*] Testing OpenAI API connection...")
    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Friday, a helpful AI assistant. Always address the user as Boss, and call them Boss in every message."},
                {"role": "user", "content": "Say hello to Boss in one sentence."},
            ],
            max_tokens=100,
            temperature=0.7,
        )
    except AttributeError:
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Friday, a helpful AI assistant. Always address the user as Boss, and call them Boss in every message."},
                {"role": "user", "content": "Say hello to Boss in one sentence."}
            ],
            temperature=0.7,
        )

    reply = response.choices[0].message.content.strip()
    print(f"[OK] OpenAI API connection successful!")
    print(f"\nFriday says: {reply}")

except Exception as exc:
    print(f"[X] OpenAI API connection failed: {exc}")
    sys.exit(1)
