from fastapi import FastAPI, Request
import requests

app = FastAPI()

@app.post("/get_company_kpis")
async def get_company_kpis(request: Request):
    data = await request.json()
    ticker = data.get("ticker")
    api_key = "your_fiscal_api_key"  # Replace with your real API key

    url = f"https://datafeed.finchat.io/company/{ticker}/kpis"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers)

    return response.json() if response.ok else {
        "error": f"Status {response.status_code}",
        "details": response.text
    }
