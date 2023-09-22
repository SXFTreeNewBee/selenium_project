import asyncio
import re
import linecache
import os
import aiofiles
from scripts import process
async def run(file_dir):
    like_pattern=re.compile(r'xlink:href="#like">.+?</span>')
    collect_pattern = re.compile(r'xlink:href="#collect">.+?</span>')
    chat_pattern = re.compile(r'xlink:href="#chat">.+?</span>')

    pattern=re.compile(r'>\d+\D?\d*\w*<')

    async def get_files():
        for fn in os.listdir(file_dir):
            yield fn

    async for fname in get_files():
        async with aiofiles.open(f'{file_dir}\\{fname}', "r", encoding='utf-8') as f:
            content = await f.read()
        like,collect,chat=re.findall(like_pattern,content),re.findall(collect_pattern,content),re.findall(chat_pattern,content)
        print(fname)
        print(like)
        print(collect)
        print(chat)
        print("============")
        # print(re.findall(pattern,like[-1])[0].strip(">").strip("<"))
        # print(re.findall(pattern, collect[0])[0].strip(">").strip("<"))
        # print(re.findall(pattern, chat[0])[0].strip(">").strip("<"))



if __name__ == '__main__':
    asyncio.run(run("data\\detail_page\\高考"))