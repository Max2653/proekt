from fastapi import FastAPI, HTTPException, Query, Header
import requests

app = FastAPI()

# Секретний ключ для доступу (в продакшені використовуйте змінні оточення)
API_KEYS = ["crypto123", "securekey456"]

# Перевірка API ключа
def verify_api_key(api_key: str = Header(...)):
    if api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return True

@app.get("/crypto/price")
async def get_crypto_price(
    coin: str = Query("bitcoin", description="ID криптовалюти (наприклад bitcoin)"),
    currency: str = Query("usd", description="Валюта для відображення ціни"),
    api_key_valid: bool = Depends(verify_api_key)
):
    """
    Отримати поточну ціну криптовалюти
    """
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies={currency}"
        response = requests.get(url)
        data = response.json()
        return {"status": "ok", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/crypto/top")
async def get_top_cryptos(
    limit: int = Query(10, description="Кількість криптовалют"),
    currency: str = Query("usd", description="Валюта для відображення цін"),
    api_key_valid: bool = Depends(verify_api_key)
):
    """
    Отримати топ криптовалют за ринковою капіталізацією
    """
    try:
        url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={currency}&order=market_cap_desc&per_page={limit}&page=1"
        response = requests.get(url)
        data = response.json()
        
        simplified = []
        for coin in data:
            simplified.append({
                "name": coin["name"],
                "symbol": coin["symbol"].upper(),
                "price": coin["current_price"],
                "change_24h": coin["price_change_percentage_24h"]
            })
        
        return {"status": "ok", "data": simplified}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
