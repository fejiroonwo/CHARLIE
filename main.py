from fastapi import FastAPI
from pydantic import BaseModel
import yfinance as yf
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

class TickerInput(BaseModel):
    ticker: str

@app.post("/run_dcf/")
async def run_dcf(data: TickerInput):
    ticker = data.ticker.upper()

    stock = yf.Ticker(ticker)
    info = stock.info
    cashflow = stock.cashflow.to_dict()

    prompt = f"""
    Find 3 comparable companies to {ticker} for a DCF model.
    Suggest WACC, revenue growth rate, and terminal value assumptions.
    """

    chat_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    gpt_output = chat_response['choices'][0]['message']['content']

    return {
        "ticker": ticker,
        "companyName": info.get("longName", "N/A"),
        "cashflow": cashflow,
        "gpt_output": gpt_output
    }