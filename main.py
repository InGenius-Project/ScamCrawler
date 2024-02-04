import asyncio
import requests
from src.websites import TaiwanFactCheck, HumanBank104


SERVER_IP = "150.117.18.40"
PORT = 8000
API = f"{SERVER_IP}:{PORT}"


def post_result(data):
    res = requests.post(API, json=data)
    res.raise_for_status()
    print("[POST] Succeed!")


async def main():
    tfc = TaiwanFactCheck()
    tfc.start_and_save(label=1)

    hb104 = HumanBank104()
    hb104.debug = False
    hb104.start_and_save()


if __name__ == "__main__":
    asyncio.run(main())
