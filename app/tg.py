import httpx
from dotenv import  load_dotenv
from os import getenv

load_dotenv()

TG_TOKEN = getenv("TG_TOKEN")
TG_CHAT_ID = getenv("TG_CHAT_ID")


async def send_tg_notifications(text: str):
    if not TG_CHAT_ID:
        raise ValueError("TG_CHAT_ID is empty!")
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    data =  {
        "chat_id": TG_CHAT_ID,
        "text": text
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(url, json=data)

    print(f"Sending data: {data}")
    if not response.is_success:
        print(response.status_code,response.text)
    return response

