import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url = "https://openrouter.ai/api/v1",
    api_key = os.environ["OPENROUTER_API_KEY"]
)

history = []


#TOOL Definition
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "write the content to the file which user request",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path where file exist and perform write operation"
                    },
                    "content":{
                        "type": "string",
                        "description": "The conetent which user requested and returned by AI as text will be written to file"
                    }
                }
                "required": ["file_path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "edit_file",
            "description": "To edit the existing file content or makeing changes",
            "properties": {
                "type": "object",
                "parameters" : {
                    "file_path": {
                        "type": "string",
                        "description": "It is the path where the file is present and to navigate to the file edit. This will help."
                    },
                    "old_text": {
                        "type": "string",
                        "description": "This is where the old text is present in the content like which is already present before so that we can modify it further into new text"
                    },
                    "new_text": {
                        "type": "string",
                        "description": "This is where the modified like the content which need to be modified where we replace the old text or and add the new text for the file."
                    }
                },
                "required": ["file_path", "old_text", "new_text"]
            }
        }
    }
]


#TOOL EXECUTOR



while True:
    try:
        user_input = input("You > ") 

        if not user_input:
            continue
        
        if user_input == "/quit":
            print("Bye Bye, Miss you")
            break

        history.append({"role": "user", 
        "content": user_input})
        
        response = client.chat.completions.create(
            model = "poolside/laguna-s-2.1",
            messages = [
                {"role" : "system", "content": "I am Retain, I am an helpful AI agent"}
            ] + history
        )

        reply = response.choices[0].message

        if reply.tool_calls:
            tool_calls_list = []

            for tc in reply.tool_calls:
                one_item = {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": "tc.function.name",
                        "arguments": "tc.function.arguments"
                    }
                }

                tool_calls_list.append(one_item)

            
            history.append(
                "role": "assistent",
                "content": "reply.conetent",
                "tool_calls": "tool_calls_list"
            )

        for tc in reply.tool_calls:
            "tool_name": "tc.function.name",
            "args": json.load("tc.function.arguments")

            result = tool_dispatch["tool_name", "args"]

        preview = result

        print(preview)

        history.append(
            "role": "tool",
            "tool_call_id": "id",
            "content": result
        )


        else:
            history.append({"role": "assistant", "content": reply})

            print("Retain > ", reply)

    except Exception as e:
        print("Error:", e)

        history.pop()