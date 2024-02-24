import asyncio
import requests
from src.websites import TaiwanFactCheck, HumanBank104
import os
import json
from time import sleep
from typing import List, Dict
from dotenv import load_dotenv


# load environment variables
load_dotenv()

SERVER_IP = os.getenv("SERVER_IP")
PORT = os.getenv("PORT")
API = f"http://{SERVER_IP}:{PORT}/"
RESULT_PATH = "results/"
PASS_CRAW = False


def get_uploaded_id_list() -> List[str]:
    ID_API = API + "id"
    r = requests.get(ID_API)
    return json.loads(r.text)


def is_new(entity: Dict, id_list: List[str]) -> bool:
    return entity["id"] not in id_list


def post_json_results():
    subfiles = os.listdir(RESULT_PATH)
    for filename in subfiles:
        fullpath = os.path.join(RESULT_PATH, filename)
        with open(fullpath, "r", encoding="utf-8") as jf:
            id_list = get_uploaded_id_list()
            data = json.load(jf)
            data = list(filter(lambda e: is_new(e, id_list), data))
            if len(data) == 0:
                print(f"[warning] {filename} no new data.")
                continue
            res = requests.post(
                API, headers={"Content-Type": "application/json"}, json=data
            )
            res.raise_for_status()
            print(f"[OK] {filename} posted.")

        sleep(1)
    print("[POST] Succeed!")


async def main():
    if PASS_CRAW:
        post_json_results()
        return

    # tfc = TaiwanFactCheck()
    # tfc.start_and_save(label=1)

    hb104 = HumanBank104()
    hb104.debug = False 
    hb104.start_and_save()

    post_json_results()


if __name__ == "__main__":
    asyncio.run(main())
