# Foundry LLM Tool Calling with FastAPI (Module 3)

A small FastAPI app that shows how an LLM on Microsoft Foundry (Azure OpenAI) **calls a Python function as a tool**.

The user asks about an order. The model decides to call `get_order_status`. Python runs the function, and the model turns the result into a reply.

## How it works

```
FastAPI  →  Foundry  →  Tool call  →  Python function  →  Foundry  →  Answer
```

1. `POST /chat` receives the user's message.
2. The message and the tool definition are sent to the model.
3. The model replies with a **tool call**, for example `get_order_status(order_id="ORD101")`.
4. Python runs the function in `tools.py`.
5. The function result goes back to the model, which writes the final answer.

## Project structure

```
foundry-llm-tool-calling-fastapi/
├── app.py            # FastAPI app, tool definition, tool-calling flow
├── tools.py          # The Python function the model can call
├── requirements.txt
├── .env              # Your Azure keys (not committed)
└── .gitignore
```

## Prerequisites

- Python 3.10+
- An Azure OpenAI / Microsoft Foundry resource with a chat model deployed (for example `gpt-4o`)

## Setup

1. **Clone the repo and open the folder in VS Code**

   ```powershell
   git clone https://github.com/satyajeetbackendai-crypto/Foundry-LLM-Tool.git
   cd Foundry-LLM-Tool
   ```

2. **Create and activate a virtual environment**

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   On macOS/Linux, use `source .venv/bin/activate`.

3. **Install the dependencies**

   ```powershell
   pip install -r requirements.txt
   ```

4. **Create a `.env` file** in the project folder:

   ```env
   AZURE_OPENAI_ENDPOINT=https://YOUR-RESOURCE.openai.azure.com/
   AZURE_OPENAI_API_KEY=YOUR_KEY
   AZURE_OPENAI_API_VERSION=2024-10-21
   AZURE_OPENAI_DEPLOYMENT=gpt-4o
   ```

   `AZURE_OPENAI_DEPLOYMENT` is the **deployment name** in Foundry, which may differ from the model name.

## Run

```powershell
uvicorn app:app --reload
```

Open **http://127.0.0.1:8000/docs**, select **POST /chat**, then click **Try it out**.

## Try it

Request body:

```json
{
  "message": "What is the status of ORD101?"
}
```

Response:

```json
{
  "answer": "Order ORD101 has been shipped."
}
```

Or use curl:

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the status of ORD101?"}'
```

### Sample orders

| Order ID | Status     |
|----------|------------|
| ORD101   | Shipped    |
| ORD102   | Delivered  |
| ORD103   | Processing |

Any other ID returns `Order not found`.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `404 Not Found` on `/chat` | A different app is running on port 8000. Stop it with Ctrl+C and start this one. |
| The model answers without calling the tool | Ask a clear question, such as "What is the status of ORD101?", instead of only "ORD101". |
| `401` / `Access denied` | Check `AZURE_OPENAI_API_KEY` and `AZURE_OPENAI_ENDPOINT` in `.env`. |
| `DeploymentNotFound` | `AZURE_OPENAI_DEPLOYMENT` must match the deployment name in Foundry. |
