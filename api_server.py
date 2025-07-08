from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

@app.post("/get_company_kpis")
async def get_company_kpis(request: Request):
    data = await request.json()
    ticker = data.get("ticker")
    api_key = os.getenv("FINCHAT_API_KEY")

    if not ticker:
        return {"error": "Ticker symbol is required."}
    if not api_key:
        return {"error": "FINCHAT_API_KEY is not set in the environment."}

    url = f"https://datafeed.finchat.io/company/{ticker}/kpis"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers)

    if response.ok:
        return response.json()
    else:
        return {
            "error": f"Status {response.status_code}",
            "details": response.text
        }

@app.get("/")
def read_root():
    return {"message": "Market Scout API is running"}
