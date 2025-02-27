from pydantic import BaseModel, Field
from typing import Optional
import json
import re
import ast


class Filter:
    class Valves(BaseModel):
        pass

    class UserValves(BaseModel):
        pass

    def __init__(self):
        pass

    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        return body

    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        # Modify the response body after processing by the API.
        # This function modify the json-format output to be more understandable for user interface
        # print(f"outlet:body:{body}")

        def format_json(json_str):
            # Remove markdown json formatting
            match = re.search(r"\{.*\}", json_str, re.DOTALL)
            if match:
                json_str = match.group(0)
            data = ast.literal_eval(json_str)

            def format_entry(key, value, indent=0):
                if isinstance(value, dict):
                    formatted = f"{'  ' if indent else ''}**{key}:**\n"
                    for sub_key, sub_value in value.items():
                        formatted += format_entry(sub_key, sub_value, indent=1)
                    return formatted
                elif isinstance(value, list):
                    if all(isinstance(item, str) for item in value):
                        return f"{'  ' if indent else ''}**{key}:**\n " + "\n ".join(value) + "\n"
                    else:
                        formatted = f"{'  ' if indent else ''}**{key}:**\n"
                        for item in value:
                            if isinstance(item, dict):
                                for sub_key, sub_value in item.items():
                                    formatted += format_entry(sub_key, sub_value, indent=1)
                            else:
                                formatted += f" {item}\n"
                        return formatted
                elif value:
                    return f"{'  ' if indent else ''}**{key}:**\n {value}\n"
                return ""

            try:
                formatted_output = "".join(format_entry(key, value) for key, value in data.items() if value)
            except Exception as e:
                raise e

            return formatted_output

        for message in body["messages"]:
            if message["role"] == "assistant":  # Target model response
                json_content = message["content"]
                formatted_content = format_json(json_content)
                message["content"] = formatted_content + json_content

        return body
