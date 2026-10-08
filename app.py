import os
import json
from fastapi import FastAPI
from pydantic import BaseModel
from openai import AzureOpenAI
from dotenv import load_dotenv
from tools import get_order_status

load_dotenv()

app = FastAPI()

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION")
)

MODEL = os.getenv("AZURE_OPENAI_DEPLOYMENT")


class ChatRequest(BaseModel):
    message: str


tools = [{
    "type": "function",
    "function": {
        "name": "get_order_status",
        "description": "Get order status",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string"}
            },
            "required": ["order_id"]
        }
    }
}]


@app.post("/chat")
def chat(request: ChatRequest):
    messages = [
        {"role": "user", "content": request.message}
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools
    )

    message = response.choices[0].message

    if message.tool_calls:
        call = message.tool_calls[0]
        args = json.loads(call.function.arguments)
        result = get_order_status(args["order_id"])

        messages.append(message)
        messages.append({
            "role": "tool",
            "tool_call_id": call.id,
            "content": result
        })

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )
        return {"answer": response.choices[0].message.content}

    return {"answer": message.content}
