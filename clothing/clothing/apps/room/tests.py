import json
import threading

import requests
import time

import requests
from asgiref.sync import sync_to_async
from bs4 import BeautifulSoup
from channels.generic.websocket import AsyncWebsocketConsumer

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from clothing.util.getGood import get_net_url

options = Options()
options.add_experimental_option("debuggerAddress", '127.0.0.1:9531')
chrome_driver_path = "D:/chromedriver.exe"  # 替换为实际的驱动程序路径
driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)
driver.implicitly_wait(5)
url = 'https://compass.jinritemai.com/screen/talent/main?source=baiying_home&live_room_id=7249134356038437687&live_app_id=1128'
# driver.get(url)

# 获取Selenium的Cookie
selenium_cookies = driver.get_cookies()
# 将Selenium的Cookie转换为Requests库可接受的格式
cookies = {cookie['name']: cookie['value'] for cookie in selenium_cookies}
comment_id_list = []

response = requests.get(
    'https://compass.jinritemai.com/ad/marketing/data/api/v1/board/get_funnel?RoomID=7249872670244834105&StatsAuthority=-1&verifyFp=f1fa57d58cd5059c49a1c21629edf3c6e16aab45eecb68a2a4&fp=f1fa57d58cd5059c49a1c21629edf3c6e16aab45eecb68a2a4&msToken=BT1qpl5sqsDTjccsTDw-6Kqt5lE0MTagTvtsIgPF0JcOWLg6YFOqYxC9OxMx_Ny-0gZcNvRAs84D3K7mkIXLcgSwvN1Ue17mJOgoKej9_lKq5Rfwtb-eMiw%3D&a_bogus=mvsODO2UMsm1oDVO-hDz9JTm2jW0YW4UgZEFr76VBUqC',
    cookies=cookies, headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'})
# 解码为UTF-8字符串
response_content = response.content.decode('utf-8')
# 解析为字典

response_data = json.loads(response_content).get('data')
# 直播间曝光人数
room_live_exposure_sum = response_data.get('adFlowDistribution').get('convertDistribution0').get("value")
in_room_live1 = response_data.get('adFlowDistribution').get('convertDistribution1').get("value")
in_room_live2 = response_data.get('natureFlowDistribution').get('convertDistribution1').get("value")
print(room_live_exposure_sum)
print(in_room_live1)
print(in_room_live2)

# from clothing.util.getGood import fetch_barrage
#
# fetch_barrage.delay("127.0.0.1:9531", "7249505129118976823", "S姐直播间")
#
#
# from celery import Celery
#
# # 创建 Celery 应用
# app = Celery('room', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
#
# # 调用任务
# result = app.send_task('clothing.util.getGood.fetch_barrage',args=("127.0.0.1:9531", "7249505129118976823", "S姐直播间"))
#
# # 打印结果
# print(result.get())
