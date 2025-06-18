import os
import sys
from dotenv import load_dotenv
from google import genai

from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file
from functions.write_file import write_file

def main():
    args_len = len(sys.argv)
    verbose = False
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

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
        available_functions = genai.types.Tool(
            function_declarations = get_function_declarations(),
        )
        messages = [
            genai.types.Content(role="user", parts=[genai.types.Part(text=user_prompt)]),
        ]

        for i in range(20):

            response = client.models.generate_content(
                model=model_name,
                contents=messages,
                config=genai.types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt,
                )
            )
            for candidate in response.candidates:
                messages.append(candidate.content)
            
            function_called = False

            for candidate in response.candidates:
                for part in candidate.content.parts:
                    if part.function_call:
                        function_called = True
                        function_call_result = call_function(part.function_call, verbose)
                        if not function_call_result: raise Exception("There was no result from call_function()")
                        messages.append(function_call_result)

            if function_called and verbose:
                response_dict = function_call_result.parts[0].function_response.response
                if 'result' in response_dict:
                    print(f"-> {response_dict['result']}")
                else:
                    print(f"-> {response_dict}")
            if not function_called:
                print("Final response:")
                print(response.text)
                break
        if verbose:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")
    else:
        print("You must provide a prompt.")
        exit(1)

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    match function_name:
        case "get_files_info":
            result =  get_files_info("./calculator", function_call_part.args.get("directory"))
        case "get_file_content":
            result = get_file_content("./calculator", function_call_part.args["file_path"])
        case "run_python_file":
            result = run_python_file("./calculator", function_call_part.args["file_path"])
        case "write_file":
            result = write_file("./calculator", function_call_part.args["file_path"], function_call_part.args["content"])
        case _:
            return genai.types.Content(
                        role="tool",
                        parts=[
                            genai.types.Part.from_function_response(
                                name=function_name,
                                response={"error": f"Unknown function: {function_name}"},
                            )
                        ],
                    )
    return genai.types.Content(
                role="tool",
                parts=[
                    genai.types.Part.from_function_response(
                        name=function_name,
                        response={"result": result},
                    )
                ],
            )

def get_function_declarations():
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
    schema_get_file_content = genai.types.FunctionDeclaration(
        name="get_file_content",
        description="Reads in the contents of a file from a specified file path, constrained to the working directory.",
        parameters=genai.types.Schema(
            type=genai.types.Type.OBJECT,
            properties={
                "file_path": genai.types.Schema(
                    type=genai.types.Type.STRING,
                    description="The file path for the file that will be read, relative to the working directory.",
                ),
            },
        ),
    )
    schema_run_python_file = genai.types.FunctionDeclaration(
        name="run_python_file",
        description="Executes a python script stored in the file located at a specified file path, constrained to the working directory.",
        parameters=genai.types.Schema(
            type=genai.types.Type.OBJECT,
            properties={
                "file_path": genai.types.Schema(
                    type=genai.types.Type.STRING,
                    description="The file path for the file that will be executed, relative to the working directory.",
                ),
            },
        ),
    )
    schema_write_file = genai.types.FunctionDeclaration(
        name="write_file",
        description="Writes a content string to a file at a specified file path, constrained to the working directory.",
        parameters=genai.types.Schema(
            type=genai.types.Type.OBJECT,
            properties={
                "file_path": genai.types.Schema(
                    type=genai.types.Type.STRING,
                    description="The file path for the file that will be written to, relative to the working directory.",
                ),
                "content": genai.types.Schema(
                    type=genai.types.Type.STRING,
                    description="The string that will be written to the file.",
                ),
            },
        ),
    )
    return [schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file]


if __name__ == "__main__":
    main()