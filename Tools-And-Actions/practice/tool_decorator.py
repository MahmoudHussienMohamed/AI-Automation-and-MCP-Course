import inspect
from functools import wraps
from typing import (
    get_type_hints,
    get_origin,
    get_args,
    Callable,
    Union
)

TOOLS_REGISTRY = {}

def openai_tool(function: Callable = None, *, name: str = None, description: str = None):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            formatted_args = ", ".join(
                [repr(arg) for arg in args]
            )

            if kwargs:
                if formatted_args:
                    formatted_args += ", "

                formatted_args += ", ".join(
                    f"{k}={v!r}" for k, v in kwargs.items()
                )

            print(f"calling tool [{func.__name__}({formatted_args})]")

            return func(*args, **kwargs)

        sig = inspect.signature(func)
        type_hints = get_type_hints(func)

        docstring = func.__doc__ or ""
        first_line = docstring.strip().split("\n")[0] if docstring else ""

        tool_description = (
            description
            or first_line
            or f"Tool for {func.__name__}"
        )

        param_descriptions = {}

        for line in docstring.split("\n")[1:]:
            line = line.strip()

            if ":" not in line:
                continue

            param_name, param_desc = line.split(":", 1)

            param_descriptions[param_name.strip()] = param_desc.strip()

        primitive_mapping = {
            str: "string",
            int: "integer",
            float: "number",
            bool: "boolean",
            dict: "object"
        }

        def python_type_to_schema(annotation):
            """
            Convert Python typing annotations
            into OpenAI-compatible JSON schema.
            """

            origin = get_origin(annotation)
            args = get_args(annotation)

            # Primitive types
            if annotation in primitive_mapping:
                return {
                    "type": primitive_mapping[annotation]
                }

            # list[T]
            if origin is list:
                item_type = args[0] if args else str

                return {
                    "type": "array",
                    "items": python_type_to_schema(item_type)
                }

            # dict[K, V]
            if origin is dict:
                return {
                    "type": "object"
                }

            # Optional[T] or Union
            if origin is Union:
                non_none = [
                    arg for arg in args
                    if arg is not type(None)
                ]

                if len(non_none) == 1:
                    return python_type_to_schema(non_none[0])

                return {
                    "anyOf": [
                        python_type_to_schema(arg)
                        for arg in non_none
                    ]
                }

            # fallback
            return {
                "type": "string"
            }

        properties = {}
        required = []

        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue

            annotation = type_hints.get(param_name, str)

            schema = python_type_to_schema(annotation)

            schema["description"] = param_descriptions.get(
                param_name,
                f"The {param_name}"
            )

            properties[param_name] = schema

            if param.default == inspect.Parameter.empty:
                required.append(param_name)

        params_schema = {
            "type": "object",
            "properties": properties
        }

        if required:
            params_schema["required"] = required

        openai_schema = {
            "type": "function",
            "name": name or func.__name__,
            "description": tool_description,
            "parameters": params_schema,
        }

        tool_name = name or func.__name__

        TOOLS_REGISTRY[tool_name] = {
            "function": wrapper,
            "schema": openai_schema,
            "description": func.__doc__
        }

        wrapper.openai_schema = openai_schema
        wrapper.tool_name = tool_name

        return wrapper

    if function is not None:
        return decorator(function)

    return decorator


def get_all_tools_schemas():
    return [
        tool["schema"]
        for tool in TOOLS_REGISTRY.values()
    ]


def get_tool_function(tool_name: str):
    return TOOLS_REGISTRY.get(tool_name, {}).get("function")