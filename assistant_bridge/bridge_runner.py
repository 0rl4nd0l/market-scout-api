import os
import json
import requests
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

BASE_URL = "https://market-scout-api-production.up.railway.app"

ENDPOINTS = {
    "get_company_kpis": "/get_company_kpis"
}

# Your tools setup remains the same...

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Get KPIs for AAPL"}],
    tools=tools,
    tool_choice="auto"
)

tool_calls = response.choices[0].message.tool_calls
if tool_calls:
    tool_call = tool_calls[0]
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)
    ticker = arguments.get("ticker")

    # Check if API key exists before making the API call
    finchat_api_key = os.getenv("FINCHAT_API_KEY")
    if not finchat_api_key:
        api_result = {
            "error": "FINCHAT_API_KEY is missing. Cannot fetch KPIs."
        }
    elif function_name in ENDPOINTS and ticker:
        res = requests.post(BASE_URL + ENDPOINTS[function_name], json={"ticker": ticker})
        api_result = res.json() if res.ok else {
            "error": f"Status {res.status_code}",
            "details": res.text
        }
    else:
        api_result = {"error": "Invalid function name or missing ticker"}

    print("\nAPI Result:\n", api_result)

    # Follow-up chat with the assistant as before
    follow_up = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": "Get KPIs for AAPL"},
            {
                "role": "assistant",
                "tool_calls": [tool_call]
            },
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(api_result)
            }
        ]
    )
    print("\nAssistant Response:\n", follow_up.choices[0].message.content)
else:
    print("\nAssistant Response:\n", response.choices[0].message.content)
