import time

from scripts import process
import asyncio
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import config
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress",f'{config.CHORME_REMOTE_ADDR}:{config.CHROME_REMOTE_PORT}')
chrome_handler=webdriver.Chrome(options=chrome_options)
def run_scripts():
    chrome_handler.get("https://www.xiaohongshu.com/search_result/?keyword=%E9%94%81%E9%AA%A8%E6%89%8B%E9%93%BE&source=web_search_result_notes&type=51")
    time.sleep(3)
    end=2000
    start=0
    while 1:
        chrome_handler.execute_script("window.scrollTo(0, window.scrollY + 100);")
        time.sleep(0.5) #滑动频率
        if start>=end:
            break
        start+=100
        print("向下滚动了")
run_scripts()

