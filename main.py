import asyncio
from src.websites import TaiwanFactCheck

async def main():
    tfc = TaiwanFactCheck()
    tfc.get_raw_content()
    tfc.get_parsed_json()
    tfc.get_sub_links()
    tfc.get_result()
    tfc.save("result.json")

if __name__ == "__main__":
    asyncio.run(main())