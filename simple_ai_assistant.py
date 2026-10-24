from openai import OpenAI
from dotenv import load_dotenv
import os
from tools import TOOLS, FUNCTION_NAME_TO_FUNCTION_MAP
import json

load_dotenv() #by default looks for .env file.

client = OpenAI(
    base_url=os.getenv("BASE_URL"), #/v1 is the OpenAI-compatible API path.
    api_key=os.getenv("API_KEY")
)

messages = []

messages.append({
            "role":"system",
            "content":"Always respond under 20 words"  
})



while True:
    user_input = input("\nAvni: ")
    messages.append({
            "role":"user",
            "content":user_input
        })
    
    if user_input.lower() in ["exit", "quit", "bye"]:
        break
        
    
    response = client.chat.completions.create(
    model=os.getenv("MODEL"),
    messages=messages,
    tools= TOOLS
    )
    
    msg = response.choices[0].message
    
    if msg.tool_calls:
        messages.append(msg)
        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name 
            func_args = json.loads(tool_call.function.arguments or "{}")
            
            fn = FUNCTION_NAME_TO_FUNCTION_MAP[func_name]
            result = fn(**func_args)
            
            messages.append({
                "role":"tool",
                "tool_id": tool_call.id,
                "content" : str(result)
            })
        #2nd call to LLM API 
        response = client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=messages,
            tools= TOOLS
        )
        msg = response.choices[0].message

    print("ASSISTANT: " + response.choices[0].message.content)
    # print(response.choices[0].message.role)
    messages.append({
            "role":response.choices[0].message.role,
            "content":response.choices[0].message.content
        })
    




#ollama json mei bhejta response but open ai ka client usse convert kar dega chatcompletion naam ke object me.