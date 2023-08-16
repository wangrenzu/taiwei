import asyncio
import json
import time

import requests
from asgiref.sync import async_to_sync
from bs4 import BeautifulSoup
from celery import shared_task
from channels.layers import get_channel_layer
from django_redis import get_redis_connection

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def getGoods(ip, room_id, getUrl):
    # chrome.exe --remote-debugging-port=9531 --user-data-dir=“D:\S姐直播间”
    # chrome.exe --remote-debugging-port=9532 --user-data-dir=“D:\悦仓直播间”
    # chrome.exe --remote-debugging-port=9533 --user-data-dir=“D:\S姐直播间2”
    # chrome.exe --remote-debugging-port=9534 --user-data-dir=“D:\悦仓直播间2”

    options = Options()
    options.add_experimental_option("debuggerAddress", ip)
    chrome_driver_path = "D:/chromedriver.exe"  # 替换为实际的驱动程序路径
    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)
    driver.implicitly_wait(5)
    url = f'https://compass.jinritemai.com/screen/talent/main?source=baiying_home&live_room_id={room_id}&live_app_id=1128'
    if getUrl:
        driver.get(url)
    selenium_cookies = driver.get_cookies()

    # 将Selenium的Cookie转换为Requests库可接受的格式
    cookies = {cookie['name']: cookie['value'] for cookie in selenium_cookies}

    # 使用Requests库发送请求并设置Cookie
    response = requests.get(
        f'https://compass.jinritemai.com/compass_api/content_live/author/live_screen/product_list?category_id=0&product_filter_type=0&explained_filter_type=0&index_selected=product_click_pay_ucnt_ratio,pay_cnt,unpay_cnt,product_show_click_ucnt_ratio,pay_amt,product_show_ucnt&room_id={room_id}&_lid=168683929&msToken=wtYB-UNASZT59fEOFxwc6SuG3Mycl6SVfNwC9G1c4Fgq12wHN-UZDZSoP2vAa9FN7h-im_lpDVZ5KYYQpEU-WQSURu31IiBZdVPDT42rsXGyPS4odO4IVUbTLfFJTNha&X-Bogus=DFSzswVuwAxANjeqtrtVjl9WX7jz',
        cookies=cookies, headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'})

    # 解码为UTF-8字符串
    try:
        response_content = response.content.decode('utf-8')
        # 解析为字典
        response_data = json.loads(response_content).get("data").get("data_result")
    except Exception as e:
        driver.get(url)
    result = []
    # 获取"data"字段

    for data in response_data:
        row_data = []
        # 序号
        product_id = data.get('room_cart_num')
        row_data.append(product_id)
        # 图片
        img = data.get('image_uri')
        row_data.append(img)
        # 款号
        code = data.get('title')[-5:]
        row_data.append(code)
        # 特征
        characteristic = data.get('feature')
        characteristic2 = ''
        for c in characteristic:
            characteristic2 += c.get('label') + ' '
        characteristic = characteristic2.replace('库存告急', '').replace('压单商品', '')
        row_data.append(characteristic)
        # 曝光量
        exposure = data.get('product_show_ucnt').get('value')
        row_data.append(exposure)
        # 曝光点击率
        clickExposure = round(data.get('product_show_click_ucnt_ratio').get('value'), 4)
        row_data.append(clickExposure)
        # 成交转化率
        clickDeal = round(data.get('product_click_pay_ucnt_ratio').get('value'), 4)
        row_data.append(clickDeal)
        # 金额
        salesPrice = data.get('pay_amt').get('value') / 100
        row_data.append(salesPrice)
        # 单数
        salesNum = data.get('pay_cnt').get('value')
        row_data.append(salesNum)
        result.append(row_data)
    return result


def getGoodsSencode(ip, room_id):
    options = Options()
    options.add_experimental_option("debuggerAddress", ip)
    chrome_driver_path = "D:/chromedriver.exe"  # 替换为实际的驱动程序路径
    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)
    driver.implicitly_wait(5)

    selenium_cookies = driver.get_cookies()

    # 将Selenium的Cookie转换为Requests库可接受的格式
    cookies = {cookie['name']: cookie['value'] for cookie in selenium_cookies}

    # 使用Requests库发送请求并设置Cookie
    response = requests.get(
        f'https://compass.jinritemai.com/ad/marketing/data/api/v1/board/get_product_list?roomId={room_id}&metrics=live_order_settle_count_7d%2Cad_live_order_settle_cost_per_product_7d%2Clive_order_settle_count_rate_7d%2Cproduct_click_pay_ucnt_ratio%2Ctotal_live_pay_order_gpm_ecom&explainStatus=2&page=1&pageSize=10&page_type=19001&statsAuthority=-1&msToken=ORnkQ6dWOoTdlzJBtKveiNL9Ap_PelNaYTXB4YCa82E3g4QP5OfTCEwMlAs3WTV1kmroMrr0u2A29_sYKWrUXpzeyUrFL7gpoa0mcmrojY1r3C_1e9U4LeWBqqYE9Ae-&a_bogus=QXMOXOh5Msm1HDVO4wDz9cim2t80YWRQgZEFdhe2WzLD',
        cookies=cookies, headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'})

    # 解码为UTF-8字符串
    response_content = response.content.decode('utf-8')
    # 解析为字典
    response_data = json.loads(response_content).get('data').get('products')
    result = []
    for data in response_data:
        row_data = append_data(data)
        result.append(row_data)
    response_data = json.loads(response_content).get('data').get('topProduct')
    row_data = append_data(response_data)
    response = requests.get(
        'https://buyin.jinritemai.com/api/author/livepc/prompt_board?in_explain_ab=true&verifyFp=f1acf483b9fdfb40be34aaa2882c9b02638bb38e695493a913&fp=f1acf483b9fdfb40be34aaa2882c9b02638bb38e695493a913&msToken=YzKoIBKL7r5kbifuo6EgEwvgQ8Sa2i1gBay7Hv_kwhoDQ2eCSDplPBm7_0ZOXdzrxRmQdGHhda5pOUfKV7VpszgYL_EdCeHdQ3CfZvw_lBcutcOxgWAZfKA%3D&a_bogus=Q7-Q6OgiMsm1UDvo07kz9GhmSlW0YWRMgZENWjaxltqr',
        cookies=cookies, headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'})
    # 解码为UTF-8字符串
    response_content = response.content.decode('utf-8')

    # 解析为字典
    response_data = json.loads(response_content).get('data').get("title")[-5:]

    row_data[0] = response_data

    result.insert(0, row_data)
    return result


def append_data(data):
    row_data = []
    # 名称
    name = data.get('title')[-5:]
    row_data.append(name)
    # 广告结算订单数
    order_number = data.get('metrics').get('liveOrderSettleCount7D').get('value')
    row_data.append(order_number)
    # 广告直接结算成本
    order_rate = round(data.get('metrics').get('adLiveOrderSettleCostPerProduct7D').get('value') / 100000, 2)
    row_data.append(order_rate)
    # 广告直接订单结算率
    back_rate = round(data.get('metrics').get('liveOrderSettleCountRate7D').get('value') / 100, 4)
    row_data.append(back_rate)
    # 点击成交率
    clickDeal = round(data.get('metrics').get('productClickPayUcntRatio').get('value') / 100, 4)
    row_data.append(clickDeal)
    # GPM
    GPM = round(data.get('metrics').get('totalLivePayOrderGpmEcom').get('value') / 100000, 2)
    row_data.append(GPM)

    return row_data


def getLive(ip, room_id):
    options = Options()
    options.add_experimental_option("debuggerAddress", ip)
    chrome_driver_path = "D:/chromedriver.exe"  # 替换为实际的驱动程序路径
    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)
    driver.implicitly_wait(5)
    # 获取Selenium的Cookie
    selenium_cookies = driver.get_cookies()

    # 将Selenium的Cookie转换为Requests库可接受的格式
    cookies = {cookie['name']: cookie['value'] for cookie in selenium_cookies}
    net_url = get_net_url(driver, 'https://compass.jinritemai.com/compass_api/author/live/basic_live_screen/base_info')
    # 使用Requests库发送请求并设置Cookie
    response = requests.get(
        net_url[-1],
        cookies=cookies, headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'})
    try:
        result = {}
        # 解码为UTF-8字符串
        response_content = response.content.decode('utf-8')
        # 解析为字典
        response_data = json.loads(response_content).get('data')
        # 直播间成交金额
        price = response_data.get('gmv') / 100

        result['price'] = price
        # 成交件数
        pay_cnt = response_data.get('pay_cnt').get('value')
        result['pay_cnt'] = pay_cnt
        # 成交人数
        pay_ucnt = response_data.get('pay_ucnt').get('value')
        result['pay_ucnt'] = pay_ucnt
        # 点击-成交转化率
        product_click_to_pay_rate = round(response_data.get('product_click_to_pay_rate').get('value'), 4)
        result['product_click_to_pay_rate'] = product_click_to_pay_rate
        # 千次观看成交金额
        gpm = round(response_data.get('gpm').get('value') / 100, 2)
        result['gpm'] = gpm
        # 成交粉丝占比
        pay_fans_ratio = round(response_data.get('pay_fans_ratio').get('value'), 4)
        result['pay_fans_ratio'] = pay_fans_ratio
        # 平均在线人数
        online_user_cnt = response_data.get('online_user_cnt').get('value')
        result['online_user_cnt'] = online_user_cnt
        # 累计观看人数
        online_user_ucnt = response_data.get('online_user_ucnt').get('value')
        result['online_user_ucnt'] = online_user_ucnt
        # 新加直播团人数
        fans_club_ucnt = response_data.get('fans_club_ucnt').get('value')
        result['fans_club_ucnt'] = fans_club_ucnt
        # 新增粉丝数
        incr_fans_cnt = response_data.get('incr_fans_cnt').get('value')
        result['incr_fans_cnt'] = incr_fans_cnt
        # 数据摘要
        net_url = get_net_url(driver,
                              'https://compass.jinritemai.com/compass_api/author/live/basic_live_screen/data_digest')
        response = requests.get(
            net_url[-1],
            cookies=cookies, headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'})
        # 解码为UTF-8字符串
        response_content = response.content.decode('utf-8')
        # 解析为字典
        response_data = json.loads(response_content).get('data').get('digests')
        # 进入直播间人数
        in_live = response_data[0].get('value').get('value')
        result['in_live'] = in_live
        # 离开直播间人数
        out_live = response_data[1].get('value').get('value')
        result['out_live'] = out_live
        # 新增粉丝数
        add_fan = response_data[2].get('value').get('value')
        result['add_fan'] = add_fan
        # 评论次数
        comment_num = response_data[3].get('value').get('value')
        result['comment_num'] = comment_num
        net_url = get_net_url(driver,
                              'https://compass.jinritemai.com/compass_api/content_live/author/basic_live_screen/product_list')
        net_url[-1] = net_url[-1].replace('index_selected=',
                                          'index_selected=market_price,product_click_ucnt,product_show_ucnt,stock_cnt,pay_combo_cnt')
        response = requests.get(
            net_url[-1],
            cookies=cookies, headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'})
        # 解码为UTF-8字符串
        response_content = response.content.decode('utf-8')
        # 解析为字典

        response_data = json.loads(response_content).get('data').get('data_result')[0]
        # 库存
        stock_cnt = response_data.get('stock_cnt').get('value')
        result['stock_cnt'] = stock_cnt
        # 销量
        pay_combo_cnt = response_data.get('pay_combo_cnt').get('value')
        result['pay_combo_cnt'] = pay_combo_cnt
        # 曝光量
        product_show_ucnt = response_data.get('product_show_ucnt').get('value')
        result['product_show_ucnt'] = product_show_ucnt
        # 点击人数
        product_click_ucnt = response_data.get('product_click_ucnt').get('value')
        result['product_click_ucnt'] = product_click_ucnt
        # 金额
        market_price = response_data.get('pay_amt').get('value')
        result['market_price'] = market_price

        # 直播间曝光人数 和进入直播间人数
        response = requests.get(
            f'https://compass.jinritemai.com/ad/marketing/data/api/v1/board/get_funnel?RoomID={room_id}&StatsAuthority=-1&verifyFp=f1fa57d58cd5059c49a1c21629edf3c6e16aab45eecb68a2a4&fp=f1fa57d58cd5059c49a1c21629edf3c6e16aab45eecb68a2a4&msToken=BT1qpl5sqsDTjccsTDw-6Kqt5lE0MTagTvtsIgPF0JcOWLg6YFOqYxC9OxMx_Ny-0gZcNvRAs84D3K7mkIXLcgSwvN1Ue17mJOgoKej9_lKq5Rfwtb-eMiw%3D&a_bogus=mvsODO2UMsm1oDVO-hDz9JTm2jW0YW4UgZEFr76VBUqC',
            cookies=cookies, headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'})
        # 解码为UTF-8字符串
        response_content = response.content.decode('utf-8')
        # 解析为字典

        response_data = json.loads(response_content).get('data')
        # 总曝光人数
        room_live_exposure_sum = response_data.get('adFlowDistribution').get('convertDistribution0').get("value")
        result['room_live_exposure_sum'] = room_live_exposure_sum
        # 进入直播间人数
        in_room_live1 = response_data.get('adFlowDistribution').get('convertDistribution1').get("value")
        in_room_live2 = response_data.get('natureFlowDistribution').get('convertDistribution1').get("value")
        result['in_room_live'] = in_room_live1 + in_room_live2
        result['in_room_live1'] = in_room_live1
        result['in_room_live2'] = in_room_live2
        # 商品点击
        click_product_ad1 = response_data.get('adFlowDistribution').get('convertDistribution2').get("value")
        click_product_ad2 = response_data.get('natureFlowDistribution').get('convertDistribution2').get("value")
        result['click_product_ad1'] = click_product_ad1
        result['click_product_ad2'] = click_product_ad2
        # 创建订单
        create_order_ad1 = response_data.get('adFlowDistribution').get('convertDistribution3').get("value")
        create_order_ad2 = response_data.get('natureFlowDistribution').get('convertDistribution3').get("value")
        result['create_order_ad1'] = create_order_ad1
        result['create_order_ad2'] = create_order_ad2
        # 成交
        deal_order_ad1 = response_data.get('adFlowDistribution').get('convertDistribution4').get("value")
        deal_order_ad2 = response_data.get('natureFlowDistribution').get('convertDistribution4').get("value")
        result['deal_order_ad1'] = deal_order_ad1
        result['deal_order_ad2'] = deal_order_ad2

        return result
    except Exception as e:

        return None


def get_net_url(driver, url):
    url_list = []
    while len(url_list) == 0:
        network = driver.execute_script("return window.performance.getEntries()")
        for entry in network:
            if entry['name'].startswith(url):
                url_list.append(entry['name'])
    return url_list


@shared_task(bind=True, default_retry_delay=30 * 60)
def fetch_barrage(self, ip, room_id, room_name):
    print("celery开始运行")
    channel_layer = get_channel_layer()
    options = Options()
    options.add_experimental_option("debuggerAddress", ip)
    chrome_driver_path = "D:/chromedriver.exe"  # 替换为实际的驱动程序路径
    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)
    driver.implicitly_wait(5)
    # 获取Selenium的Cookie
    selenium_cookies = driver.get_cookies()
    # 将Selenium的Cookie转换为Requests库可接受的格式
    cookies = {cookie['name']: cookie['value'] for cookie in selenium_cookies}
    url = 'https://buyin.jinritemai.com/dashboard/live/control'
    comment_id_list = []
    while True:
        conn = get_redis_connection("default")
        val = int(conn.get(room_name).decode())
        if val == 0:
            return
        response = requests.get(
            f'https://buyin.jinritemai.com/api/anchor/comment/info?comment_query_type=7&cursor=t-1687828497354_r-7249168195871867869_rdc-1_d-1_u-7249168152922161745_h-7249166862247498811&internal_ext=internal_src:dim%7Cwss_push_room_id:{room_id}%7Cwss_push_did:2075499671065928%7Cdim_log_id:202306270914579D6656B5186D5D658AD8%7Cfetch_time:1687828497354%7Cseq:62%7Cwss_info:0-0-0-0&request_source=2&similar_comment_enable=true&msToken=KMkbK0mBXom5w7EC-G_zZ2kUpErkRZ0A8mfck_1z1ba3FPN23VvNiRs6zHcF5vs_TAsZ2wh_SlGhZN0hJIAPCR2LoYA4Bf8DamZ0yXFtmVKcV0TldC-qzw==&X-Bogus=DFSzswVE6o0ANru7tnaSIl9WX7JK&_signature=_02B4Z6wo00001.A02lgAAIDDcDYgGLb6L7vwNN7AAJigev1NDp8ggl85N8uC69sC9-5IQif1wg5AXUc8ME6KHozw0Dx9UY2A7nNJhsxDZQQ6ea4-CvnfQ5am9H0qyM6WB5njbYNfEfO.vGIdc1',
            cookies=cookies, headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'})
        # 解码为UTF-8字符串
        response_content = response.content.decode('utf-8')
        # 解析为字典
        response_data = json.loads(response_content).get('data')
        if response_data.get("next_fetch_interval") == 2000:
            continue
        try:
            content = response_data.get("comment_infos")[0]
            comment_id = content.get("comment_id")
            if comment_id in comment_id_list:
                continue
            comment_id_list.append(comment_id)
            # 发送消息到Channels层
            group = ''
            if room_name == 'S姐直播间':
                group = "barrage_group_1"
            if room_name == '悦仓直播间':
                group = "barrage_group_2"
            if room_name == '星露直播间':
                group = "barrage_group_3"
            async_to_sync(channel_layer.group_send)(group, {
                'type': 'send_comment',
                'content': content,
            })

        except Exception as e:
            time.sleep(5)
            driver.get(url)
            # 获取Selenium的Cookie
            selenium_cookies = driver.get_cookies()
            # 将Selenium的Cookie转换为Requests库可接受的格式
            cookies = {cookie['name']: cookie['value'] for cookie in selenium_cookies}
            raise self.retry(exc=e, countdown=5)


def get_douyin_user():
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9534")
    chrome_driver_path = "D:/chromedriver.exe"  # 替换为实际的驱动程序路径
    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)
    response_data = ''
    try:
        driver.implicitly_wait(5)
        # 获取Selenium的Cookie
        selenium_cookies = driver.get_cookies()
        cookies = {cookie['name']: cookie['value'] for cookie in selenium_cookies}
        net_url = get_net_url(driver, 'https://live.douyin.com/webcast/ranklist/audience/?aid=')
        response = requests.get(
            net_url[-1],
            cookies=cookies, headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'})
        response_content = response.content.decode('utf-8')
        # 解析为字典
        response_data = json.loads(response_content).get('data')
    except Exception as e:
        driver.refresh()
    return response_data


if __name__ == '__main__':
    # getGoods("127.0.0.1:9531", '7245051119288748856', False)  # S姐直播间
    # getLive("127.0.0.1:9532", '7246532033483180837')  # 悦仓直播间
    # fetch_barrage("127.0.0.1:9531", '7249134356038437687')
    response = get_douyin_user()
