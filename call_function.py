from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from collections.abc import Callable

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
        ]
    )


def call_function(
        function_call: types.FunctionCall, verbose: bool = False 
    ) -> types.Content:
    if verbose:
        print(f"Received function call: {function_call.name} with arguments: {function_call.args}")
    else:
        print(f"Received function call: {function_call.name}")


function_mapping: dict[str, Callable[..., str]] = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file
}
function_name = call_function.name or ""
if function_name not in function_mapping:
    return types.Content(
        role="tool",
        parts=[
        types.Part.from_function_response(
                name=function_name,
                response={"error": f"Unknown function: {function_name}"},
            )
        ],
    )