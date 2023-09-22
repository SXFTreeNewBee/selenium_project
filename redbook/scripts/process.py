
import linecache
import re
from selenium_project.redbook import config
import asyncio
import aiofiles
import os

class ProcessUrls(object):
    def __init__(self,chrome):
        self.chrome=chrome

    async def page_content(self,url):
        self.chrome.get(url)
        await asyncio.sleep(config.SCRAPE_WAIT)  # 需要等待界面加载
        page_content = self.chrome.page_source

        return page_content
    @staticmethod
    async def storage_page(storage_file,page_content):

        #异步文件写入
        async with aiofiles.open(storage_file,"w",encoding="utf-8") as f:

            await f.write(page_content)
class ProcessPage(object):
    def __init__(self):
        pass
    @classmethod
    async def get_article_suffix(cls,filename):
        location_pattern = re.compile(r'href="/search_result/\S+\s+class="title">')

        next_urls = []#该标题下每个文章的url后缀
        content = linecache.getline(filename, 23)
        # print(content)
        regx_content = re.findall(location_pattern, content)
        get_href_pattern = re.compile(r'href="\S+"')
        for href in regx_content:
            next_urls.append(re.findall(get_href_pattern, href)[0].strip("href=").strip(r'"'))
        return next_urls

class ProcesDetailPage(object):
    def __init__(self):
        pass
    @classmethod
    async def get_detail_page_content(cls,file_dir):

        async def get_files():
            for fn in os.listdir(file_dir):
                yield fn

        async for fname in get_files():
            async with aiofiles.open(f'{file_dir}\\{fname}', "r", encoding='utf-8') as f:
                content =await f.read()

            title=await asyncio.create_task(cls.get_title(content=content))#获取文章标题

            title_detail=await asyncio.create_task(cls.get_title_detail(content=content))#获取文章描述

            tags=await asyncio.create_task(cls.get_title_tag(content=content))

            timestamp,location=await asyncio.create_task(cls.get_timestamp_and_location(content=content))

            print({f'{fname}':{
                       "title":title,
                       "title_desc":title_detail if title_detail else "无描述",
                        "tags":tags,
                        "time":timestamp,
                        "loc":location
                                }
            })
    @classmethod
    async def get_title(cls,content):

        pattern = re.compile(r'class="title".+id="detail-desc"')  # 获取文章标题的正则

        title_pattern = re.compile(r'>.+</')

        regex_title_mix = re.findall(pattern, content)[0]

        title = re.findall(title_pattern, regex_title_mix)[0].replace("<", "").replace(">", "").replace("/", "")

        return title
    @classmethod
    async def get_title_detail(cls,content):
        pattern = re.compile(r'id="detail-desc".+?</span>')  # 获取文章的描述

        title_detail_pattern = re.compile(r'<span .+</')

        title_detail_again_pattern = re.compile(r'>.+')

        regex_mix = re.findall(pattern, content)[0]

        regex_mix_again = re.findall(title_detail_pattern, regex_mix)[0].replace("<br>", " ").replace("</", "")

        title_detail = re.findall(title_detail_again_pattern, regex_mix_again)

        if title_detail:

            return title_detail[0].replace(">", "")
        else:
            return None
    @classmethod
    async def get_title_tag(cls,content):
        tags=[]
        pattern = re.compile(r'source=web_note_detail_r10.+?</a>')  # 获取文章标签的正则

        tag_pattern = re.compile(r'#.+?<')

        regex_mix = re.findall(pattern, content)

        def map_tag(s):
            return re.findall(tag_pattern, s)[0]

        for tag in map(map_tag, regex_mix):

            tags.append(tag.replace("<", "").replace("#", ""))

        return tags
    @classmethod
    async def get_timestamp_and_location(cls,content):
        pattern = re.compile(r'class="date".+?</span>')  # 获取时间与地理位置

        time_pattern = re.compile(r'>.+<')

        regex_mix = re.findall(pattern, content)[0]

        time_info = re.findall(time_pattern, regex_mix)[0].replace(">", "").replace("<", "").split(" ")

        return time_info[0],"未知" if not time_info[1] else time_info[1]

    @classmethod
    async def get_like_collect_chat(cls,content):
        like_pattern = re.compile(r'xlink:href="#like">.+?</span>')

        collect_pattern = re.compile(r'xlink:href="#collect">.+?</span>')

        chat_pattern = re.compile(r'xlink:href="#chat">.+?</span>')


if __name__ == '__main__':
    asyncio.run(ProcesDetailPage.get_detail_page_content("..\\data\detail_page\\高考"))