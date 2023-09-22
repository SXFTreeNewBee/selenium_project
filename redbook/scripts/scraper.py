import re
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium_project.redbook.scripts import process
import asyncio
import time
import os
import sys
from urllib.parse import quote,unquote
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
sys.path.append('..')
from utils import url_pool
import config


chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress",f'{config.CHORME_REMOTE_ADDR}:{config.CHROME_REMOTE_PORT}')
chrome_handler=webdriver.Chrome(options=chrome_options)

process_urls=process.ProcessUrls(chrome=chrome_handler)

process_page=process.ProcessPage()

async def extract_urls(filename):

    urls_prefix=url_pool.main_page_url

    urls_suffix=await asyncio.create_task(process_page.get_article_suffix(filename=filename))

    full_urls=[]
    def get_full_url(suffix:str):
        return urls_prefix+suffix

    for i in map(get_full_url,urls_suffix):
        full_urls.append(i)
    return full_urls

async def save_detail_page_content(url,title_name):
    unique_name=url.strip(f'{url_pool.main_page_url}/search_result/')

    dst_file_dir=f'{config.DETAIL_PAGE_DIR}\\{title_name}'
    if not os.path.exists(dst_file_dir):
        # 如果目录不存在，创建目录
        os.makedirs(dst_file_dir)
        print(f"该关键词 ’{title_name}‘ 未被创建过，'{dst_file_dir}' 不存在，已创建。")

    storage_file=f"{dst_file_dir}\\{unique_name}"#存储目录

    print(f'即将访问{url}')
    page_content=await asyncio.create_task(process_urls.page_content(url=url))#获取主页的html代码

    print(f'正在存储至{storage_file}')
    await asyncio.create_task(process_urls.storage_page(storage_file=storage_file,page_content=page_content))#将h5代码存入到data目录中

    print(f'该url:{url} 爬取完成')
async def save_search_page_content(search_keyword:str):

    search_template=url_pool.search_page_url

    search_url=search_template.format(kw=search_keyword)

    storage_file="{main_page}\\{filename}".format(main_page=config.MAIN_PAGE_DIR,filename=search_keyword)

    search_content=await asyncio.create_task(process_urls.page_content(search_url))#拿到搜索的结果页面

    await asyncio.create_task(process_urls.storage_page(storage_file=storage_file,page_content=search_content))

async def scroll_page():
    end = 2000
    start = 0
    while 1:
        chrome_handler.execute_script("window.scrollTo(0, window.scrollY + 100);")
        await asyncio.sleep(0.5)  # 滑动频率
        if start >= end:
            break
        start += 100

async def start_search(keyword:str):

    await asyncio.create_task(save_search_page_content(keyword))

    data_dir=f'{config.MAIN_PAGE_DIR}\\{keyword}'

    urls=await asyncio.create_task(extract_urls(data_dir))

    for url in urls:

        await asyncio.create_task(save_detail_page_content(url=url,title_name=keyword))

        await asyncio.sleep(config.SCRAPE_FREQUENCY)#设置爬取频率
    print("爬取完成")
if __name__ == '__main__':
    asyncio.run(start_search("高考"))