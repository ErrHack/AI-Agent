import os
import sys
from dotenv import load_dotenv
from google import genai


args_len = len(sys.argv)
verbose = False
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
model_name = 'gemini-2.0-flash-001'

if args_len > 1:
    if args_len > 2:
        if sys.argv[2] == "--verbose":
            verbose = True
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    user_prompt = sys.argv[1]
    schema_get_files_info = genai.types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=genai.types.Schema(
            type=genai.types.Type.OBJECT,
            properties={
                "directory": genai.types.Schema(
                    type=genai.types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )
    available_functions = genai.types.Tool(
        function_declarations = [
            schema_get_files_info,
        ],
    )
    messages = [
        genai.types.Content(role="user", parts=[genai.types.Part(text=user_prompt)]),
    ]
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=genai.types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        )
    )
    if response.function_calls:
        for call in response.function_calls:
            print(f"Calling function: {call.name}({call.args})")
        if response.code_execution_result: print(f"Code execution response: {response.code_execution_result}")
    if response.text: print(f"Response Text:\n\t {response.text}")
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")
else:
    print("You must provide a prompt.")
    exit(1)