from html import parser
import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_function import available_functions

def main():
    load_dotenv()
    api_key= os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("API key not found")
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User Prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args=parser.parse_args()
    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
        ]
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt,tools=[available_functions])
    )
    
    if args.verbose:
        print("User prompt:", args.user_prompt)
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    if not response.function_calls:
        print(response.text)
    else:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")

if __name__ == "__main__":
    main()
