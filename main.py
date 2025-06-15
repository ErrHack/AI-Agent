import os
import sys
from dotenv import load_dotenv
from google import genai


args_len = len(sys.argv)
verbose = False
system_prompt = 'Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'
model_name = 'gemini-2.0-flash-001'

if args_len > 1:
    if args_len > 2:
        if sys.argv[2] == "--verbose":
            verbose = True
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    user_prompt = sys.argv[1]
    messages = [
    genai.types.Content(role="user", parts=[genai.types.Part(text=user_prompt)]),
    ]
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=genai.types.GenerateContentConfig(system_instruction=system_prompt)
    )
    print(f"Response Text:\n\t {response.text}")
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")
else:
    print("You must provide a prompt.")
    exit(1)