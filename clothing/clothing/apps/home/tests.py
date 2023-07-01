# from datetime import datetime
#
# from selenium.webdriver.chrome.service import Service
# import time
# from selenium import webdriver
# from selenium.webdriver import ActionChains
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# # options = Options()
# # options.add_experimental_option("debuggerAddress", "127.0.0.1:9532")
# # options.add_argument("--charset=utf-8")
# #
# # driver = webdriver.Chrome(options=options)
# #
# # driver.implicitly_wait(5)
# # url = 'http://192.168.1.101:8002/List_user/'
# # driver.get(url)
# # while True:
# #     driver.refresh()
#
# time = datetime.now().strftime("%Y-%m-%d")
# print(time)
#
#
#
from datetime import datetime

s = '2023-06-23 00:00:00'
date_object = datetime.strptime(s, "%Y-%m-%d %H:%M:%S")  # 将字符串转化为 datetime 对象

print(date_object.strftime("%Y-%m-%d"))  # 使用 strftime 方法

print(bool(" "))