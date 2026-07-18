import httpx
from dotenv import  load_dotenv
from os import getenv

load_dotenv()

TG_PROXY = getenv("TG_PROXY")
TG_TOKEN = getenv("TG_TOKEN")
TG_CHAT_ID = getenv("TG_CHAT_ID")


async def send_tg_notifications(text: str):
    try:
        if not TG_CHAT_ID or not TG_TOKEN:
            print("TG_CHAT_ID is empty! skipping notification...")
            return
        url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
        data =  {
            "chat_id": TG_CHAT_ID,
            "text": text
        }

        client_kwargs = {
            "timeout": httpx.Timeout(30.0,connect=10.0)
        }
        if TG_PROXY:
            client_kwargs["proxy"] = TG_PROXY
        async with httpx.AsyncClient(**client_kwargs) as client:
            response = await client.post(url, json=data)

        print(f"Sending data: {data}")
        if not response.is_success:
            print(response.status_code,response.text)
        return response
    except Exception as e:
        print(e)

