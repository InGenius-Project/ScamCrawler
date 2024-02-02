import asyncio
import requests
from src.websites import TaiwanFactCheck


SERVER_IP = "localhost"
PORT = 8003
API = f"{SERVER_IP}:{PORT}"


def post_result(data):
    res = requests.post(API, json=data)
    res.raise_for_status()
    print("[POST] Succeed!")


async def main():
    tfc = TaiwanFactCheck()
    tfc.get_sub_links()
    results = tfc.get_result()
    print(len(results))
    tfc.save("result.json")


if __name__ == "__main__":
    asyncio.run(main())
