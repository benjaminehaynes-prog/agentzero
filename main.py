import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function
import sys

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
    if args.verbose:
        print("User prompt:", args.user_prompt)
    for _ in range(20):
        final = generate_content(client, messages, args.verbose)
        if final:
            print("Final response:")
            print(final)
            return
        
    print("Maximum iterations reached")
    sys.exit(1)


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt,tools=[available_functions])
    )
    if response.candidates:
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    if not response.function_calls:
        return response.text
    else:
        function_responses = []
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose = verbose)
            if not function_call_result.parts:
                raise Exception ("Result is empty")
            if  not function_call_result.parts[0].function_response:
                raise Exception ("Function Response is empty")
            if not function_call_result.parts[0].function_response.response:
                raise Exception ("Response is empty")
            if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            function_responses.append(function_call_result.parts[0])
        messages.append(types.Content(role="user", parts=function_responses))

if __name__ == "__main__":
    main()
