# import time
# import random
#
# from urllib import request
# import cv2
# import pandas as pd
# from selenium import webdriver
#
# from selenium.webdriver import ActionChains
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait
#
#
# def get_img():
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 以键值对的形式加入参数
#     chrome_options.add_experimental_option('useAutomationExtension', False)
#     chrome_options.add_experimental_option("detach", True)
#
#     chrome_options.binary_location = "D:\Google\Chrome\Application\chrome.exe"  # 使用实际的Chrome二进制文件路径进行更新
#
#     driver = webdriver.Chrome(executable_path="D:\chromedriver.exe", chrome_options=chrome_options)
#     driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
#         'source': 'Object.defineProperty(navigator,"webdriver",{get:() => undefined})'
#     })
#
#     df = pd.read_excel('1.xlsx')
#     urls = df['英文名'].tolist()
#     wait = WebDriverWait(driver, 10)
#
#     for index, url in enumerate(urls):
#         if index == len(urls):
#             break
#         if len(str(url)) > 80:
#             continue
#         if str(url) != 'nan':
#             driver.get(str(url))
#         else:
#             continue
#         try:
#             while True:
#                 try:
#                     captcha = wait.until(EC.presence_of_element_located((By.ID, 'captcha-verify-image')))
#                 except Exception as e:
#                     captcha = None
#                 if captcha is None:
#                     break
#                 big = driver.find_element(By.ID, 'captcha-verify-image').get_attribute('src')
#                 request.urlretrieve(big, 'bigImage.png')
#                 bigs = driver.find_element(By.CLASS_NAME, 'captcha_verify_img_slide').get_attribute('src')
#                 request.urlretrieve(bigs, 'bigImages.png')
#                 big_gray = cv2.imread('bigImage.png', 0)
#                 small_gray = cv2.imread('bigImages.png', 0)
#                 res = cv2.matchTemplate(big_gray, small_gray, cv2.TM_CCORR_NORMED)
#                 value = cv2.minMaxLoc(res)
#                 x = value[2][0]
#                 # 缩放比列   原图552px   实际340px
#                 xx = int(x * 340 / 552)
#                 bt = driver.find_element(By.CLASS_NAME, 'secsdk-captcha-drag-icon')
#                 ac = ActionChains(driver)
#                 ac.click_and_hold(bt).perform()
#                 moved = 0
#                 while moved < xx:
#                     x = random.randint(22, 40)
#                     moved += x
#                     ac.move_by_offset(xoffset=x, yoffset=0).perform()
#                     if moved > xx:
#                         time.sleep(0.5)
#                         zcz = moved - xx
#                         cz = zcz * 2
#                         ac.move_by_offset(xoffset=-cz, yoffset=0).perform()
#                         time.sleep(0.3)
#                         ac.move_by_offset(xoffset=zcz, yoffset=0).perform()
#                     # 释放鼠标
#
#                 ac.release().perform()
#             try:
#                 url = driver.find_element(By.XPATH, '(//div[contains(@class, "carousel-wrap__img")])[1]').get_attribute(
#                     'style')
#                 start_index = url.index('("') + 2
#                 end_index = url.index('")')
#                 image_url = url[start_index:end_index]
#                 df.loc[index, '英文名'] = image_url
#                 df.to_excel('1.xlsx', index=False)
#             except Exception as e:
#                 continue
#         except Exception as e:
#             driver.quit()
#             get_img()
#
#
# if __name__ == '__main__':
#     get_img()
# import pandas as pd
#
# df = pd.read_excel('1.xlsx', header=0)
# phone_list = []
# name_list = []
#
# for index, row in df.iterrows():
#     phone = str(row['电话'])
#     name = str(row['姓名/名称'])
#     if ';' in phone:
#         phone = phone.replace(';', ' ')
#     if '，' in phone:
#         phone = phone.replace('，', ' ')
#     if len(phone) < 10:
#         continue
#     if len(str(phone)) > 15:
#         phones = phone.split(" ")
#         for p in phones:
#             if p.startswith('0') or '*' in p:
#                 continue
#             if len(p) < 10:
#                 continue
#             phone_list.append(p)
#             name_list.append(name)
#         continue
#     if phone.startswith('0'):
#         continue
#     if '*' in phone:
#         continue
#     phone_list.append(phone)
#     name_list.append(name)
#
#
# df = pd.DataFrame({
#    '手机号': phone_list,
#    '姓名': name_list,
# })
#
# # 将DataFrame写入一个Excel文件
# df.to_excel('11.xlsx', index=False)

# import unittest
from datetime import datetime

# from celery import Celery
# from util.getGood import fetch_barrage


# class CeleryTaskTest(unittest.TestCase):
#
#     def tearDown(self):
#         pass
#
#     def test_celery_task(self):
#         # 使用Celery应用程序实例调用任务
#         result = fetch_barrage.delay("127.0.0.1:9531", "7249505129118976823", "S姐直播间")  # 传递任务参数
#
#
# if __name__ == '__main__':
#     unittest.main()
#
# date_time_str = datetime.now().strftime("%Y-%m-%d")
# status_time_str = datetime(2023, 6, 28).strftime("%Y-%m-%d")
#
# date_time = datetime.strptime(date_time_str, "%Y-%m-%d")
# status_time = datetime.strptime(status_time_str, "%Y-%m-%d")
#
# difference = date_time - status_time
# difference_in_days = difference.days
# print("两个日期的差异为:", difference_in_days, "天")


normal_tags = '采购面料,采购辅料,没到车间,刚到车间,车间加工中,在后道,入仓,到档口,新款,翻单'
tags = '采购面料,没到车间'



print(tags in normal_tags)

