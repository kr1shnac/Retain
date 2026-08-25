import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url = "https://openrouter.ai/api/v1",
    api_key = os.environ["OPENROUTER_API_KEY"]
)

history = []


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

        reply = response.choices[0].message.content

        history.append({"role": "assistant", "content": reply})

        print("Retain > ", reply)

    except Exception as e:
        print("Error:", e)

        history.pop()