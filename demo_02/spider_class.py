import csv
import requests
from fake_useragent import FakeUserAgent
from jsonpath import jsonpath
import json
import os
from lxml import etree
import random
from retrying import retry
import asyncio
from aiohttp_socks import ProxyConnector
import aiohttp
from DrissionPage import ChromiumPage,ChromiumOptions
import random
from hashlib import md5
import requests
from fontTools.ttLib import TTFont
import re
import ddddocr
from PIL import ImageDraw, ImageFont,Image



class GetProxies:
    """
    获取与使用代理ip
    """
    def __init__(self):
        self.headers = {
            'User-Agent': FakeUserAgent(platforms='desktop').random,
        }
        self.headers_generator = FakeUserAgent(platforms='desktop')

    def save_proxies(self,url):
        response = requests.get(url, headers=self.headers)
        with open('./proxies/proxies_ip.txt', 'w', encoding='utf_8') as f:
            f.write(response.text)

    def get_proxies_list(self):
        with open('./proxies/proxies_ip.txt', 'r', encoding='utf-8') as f:
            # 将每一行转化为一个元素，去除多余的\n，返回代理ip列表
            proxies_list = f.readlines()
            for i in range(len(proxies_list)):
                proxies_list[i] = proxies_list[i].strip()
        return proxies_list



class SpiderToGuaziershouche:

    def __init__(self):
        self.headers = {
            'User-Agent': FakeUserAgent(platforms='desktop').random,
        }
        self.headers_generator = FakeUserAgent(platforms='desktop')

    def __get_headers(self):
        """
        :return: 返回headers请求头字典字典
        """
        return {'User-Agent': self.headers_generator.random}

    def get_car_research_id(self,url,page=None,proxies_list=None):
        """
        :param url: 此参数url为已经确定好车辆品牌型号的url
        :return: 返回车辆详细页id -- type-list
        """
        car_research_id = []
        if page:
            for i in range(1,page):
                tmp_url = url + f'?page={i}'
                response = requests.get(tmp_url, headers=self.__get_headers())
                html = etree.HTML(response.text)
                data = html.xpath('//div/a[@class="car-item-img" and @target="_blank"]/@href')
                car_research_id.extend(data)
        else:
            response = requests.get(url,headers=self.__get_headers())
            # print(response.text)
            html = etree.HTML(response.text)
            data = html.xpath('//div/a[@class="car-item-img" and @target="_blank"]/@href')
            car_research_id.extend(data)
            # print(data)

        return car_research_id

    def get_car_data(self,car_id_list):
        car_title_list = ['标题','售价(万)','三电质保', '电池容量', '电池类型', '新车续航', '快充功能', '快充', '电池品牌', '驱动电机']
        with open('./data/carlist_01.csv','w',encoding='utf-8',newline='') as f:
            writer = csv.DictWriter(f,fieldnames=car_title_list)
            writer.writeheader()
            for car_id in car_id_list:
                url = 'https://www.guazi.com' + car_id
                response = requests.get(url,headers=self.__get_headers())
                html = etree.HTML(response.text)
                data_01_value = html.xpath('//div[@class="car-condition__functional-configuration"]/div[@class="car-info-item"]/div[@class="car-info-item-value"]/text()')
                data_01_title = html.xpath('//div[@class="car-condition__functional-configuration"]/div[@class="car-info-item"]/div[@class="car-info-item-label"]/text()')
                data_02_value = html.xpath('//div[@class="right-box"]/div[@class="car-base-info"]/h1[@class="title"]/text()')
                data_03_value = html.xpath('//div[@class="right-box"]/div[@class="car-base-info"]/div[@class="price-info"]/div/div/span[@class="values"]/text()')
                data_dic = dict(zip(data_01_title,data_01_value))
                data_dic['标题'] = data_02_value[0]
                data_dic['售价(万)'] = data_03_value[0]
                writer.writerow(data_dic)
                print('数据写入完毕')


    @retry(stop_max_attempt_number=5)
    def __proxy_request(self,url,proxy):
        response = requests.get(url, headers=self.__get_headers(), proxies=proxy)
        html = etree.HTML(response.text)
        data_01_value = html.xpath('//div[@class="car-condition__functional-configuration"]/div[@class="car-info-item"]/div[@class="car-info-item-value"]/text()')
        data_01_title = html.xpath('//div[@class="car-condition__functional-configuration"]/div[@class="car-info-item"]/div[@class="car-info-item-label"]/text()')
        data_02_value = html.xpath('//div[@class="right-box"]/div[@class="car-base-info"]/h1[@class="title"]/text()')
        data_03_value = html.xpath('//div[@class="right-box"]/div[@class="car-base-info"]/div[@class="price-info"]/div/div/span[@class="values"]/text()')
        data_dic = dict(zip(data_01_title, data_01_value))
        data_dic['标题'] = data_02_value[0]
        data_dic['售价(万)'] = data_03_value[0]
        return data_dic

    def get_car_data_by_proxy(self, car_id_list, proxies_list):
        car_title_list = ['标题','售价(万)','三电质保', '电池容量', '电池类型', '新车续航', '快充功能', '快充', '电池品牌', '驱动电机']
        with open('./data/carlist_01.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=car_title_list)
            writer.writeheader()
            for car_id in car_id_list:
                proxy = {
                    'https': random.choice(proxies_list)
                }
                url = 'https://www.guazi.com' + car_id
                try:
                    data_dic = self.__proxy_request(url,proxy)
                    if data_dic.keys() is None or list(data_dic.keys())[0] is None:
                        pass
                    else:
                        writer.writerow(data_dic)
                        print('数据写入完毕')
                except Exception as e:
                    print(e,'数据使用代理ip请求失败')


    async def __get_car_data_by_async(self, url, proxies_list,semaphore_count = 8):
        semaphore = asyncio.Semaphore(semaphore_count)
        async with semaphore:
            try:
                headers = self.__get_headers()
                ip = 'http://' + random.choice(proxies_list)
                print(f'本次使用的ip：{ip}')
                connector = ProxyConnector.from_url(ip, ssl=False)
                async with aiohttp.ClientSession(connector=connector) as session:
                    async with session.get(url, headers=headers) as response:
                        data = await response.content.read()
                        return data
            except Exception as e:
                print('发生错误', e)

    async def get_car_requests_by_async(self,car_research_id, proxies_list):
        tasks = []
        for car_id in car_research_id:
            url = 'https://www.guazi.com' + car_id
            tasks.append(asyncio.create_task(self.__get_car_data_by_async(url,proxies_list)))
        all_data = await asyncio.gather(*tasks)
        car_title_list = ['标题','售价(万)','三电质保', '电池容量', '电池类型', '新车续航', '快充功能', '快充', '电池品牌', '驱动电机']
        with open('./data/carlist_02.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=car_title_list)
            writer.writeheader()
            for data in all_data:
                try:
                    html = etree.HTML(data)
                    data_01_value = html.xpath('//div[@class="car-condition__functional-configuration"]/div[@class="car-info-item"]/div[@class="car-info-item-value"]/text()')
                    data_01_title = html.xpath('//div[@class="car-condition__functional-configuration"]/div[@class="car-info-item"]/div[@class="car-info-item-label"]/text()')
                    data_02_value = html.xpath('//div[@class="right-box"]/div[@class="car-base-info"]/h1[@class="title"]/text()')
                    data_03_value = html.xpath('//div[@class="right-box"]/div[@class="car-base-info"]/div[@class="price-info"]/div/div/span[@class="values"]/text()')
                    data_dic = dict(zip(data_01_title, data_01_value))
                    data_dic['标题'] = data_02_value[0]
                    data_dic['售价(万)'] = data_03_value[0]
                    if data_dic.keys() is None or list(data_dic.keys())[0] is None:
                        pass
                    else:
                        writer.writerow(data_dic)
                        print('数据写入完毕')
                except Exception as e:
                    print('get_car_requests_by_async数据解析发生错误')
        return


class XiaohongshuSpiader:

    def __init__(self):
        self.headers = {
            'User-Agent': FakeUserAgent(platforms='desktop').random,
        }
        self.headers_generator = FakeUserAgent(platforms='desktop')


    def spider_by_key_by_driver(self):

        option = ChromiumOptions()
        option.headless()
        page = ChromiumPage(option)

        # page.listen.start('https://www.xiaohongshu.com')

        page.get('https://www.xiaohongshu.com/')
        page.listen.start('https://edith.xiaohongshu.com/api/sns/web/v2/comment/page')
        # page.set.window.max()
        page.wait(2)

        def get_data(page):
            title = page.ele(
                'xpath=//div[@class="note-scroller"]/div[@class="note-content"]/div[@id="detail-title"]').text
            # print(title)

            user_name = page.ele('xpath=//div[@class="info"]/a[@class="name"]/span[@class="username"]').text
            # print(user_name)

            content_ly = page.eles('xpath=//div[@id="detail-desc"]/span[@class="note-text"]/span')
            content = ''
            for i in content_ly:
                content = content + i.text
            # print(content)

            keywords_ly = page.eles('xpath=//div[@id="detail-desc"]/span[@class="note-text"]/a[@id="hash-tag"]')
            keywords = ''
            for i in keywords_ly:
                keywords = keywords + i.text
            # print(keywords)

            age = page.ele('xpath=//div[@class="bottom-container"]/span[@class="date"]').text
            # print(age)

            like_num = page.ele(
                'xpath=//div[@class="left"]/span[@class="like-wrapper like-active"]/span[@class="count"]').text
            # print(like_num)

            collect_num = page.ele(
                'xpath=//div[@class="left"]/span[@class="collect-wrapper"]/span[@class="count"]').text
            # print(collect_num)

            comment_num = page.ele('xpath=//div[@class="left"]/span[@class="chat-wrapper"]/span[@class="count"]').text
            # print(comment_num)

            return [title, user_name, content, keywords, age, like_num, collect_num, comment_num]

        researchs = input('请输入你要搜寻的关键词：')

        with open('./set_01/guangdong_05.csv', 'a', encoding='GBK', newline='', errors='replace') as f:
            writer = csv.writer(f)
            hashset = set()

            for research in researchs:
                input_ele = page.ele('xpath=//div[@class="input-box"]/input[@id="search-input"]')
                input_ele.clear()
                input_ele.input(research)
                page.wait(5)
                button_ele = page.ele('xpath=//div[@class="input-button"]/div[@class="search-icon"]')
                button_ele.click()
                page.wait(2)

                y = 0

                num_count = set()
                num_ly = []

                while True:

                    aaa_list = page.eles(
                        'xpath=//div[@class="feeds-container"]/section[@class="note-item" and @data-width]')

                    for aaa in aaa_list:
                        num = aaa.attr('data-index')
                        if num not in num_count:
                            num_count.add(num)
                            num_ly.append(num)

                    if num_ly:
                        for num in num_ly:
                            try:
                                print('正在寻找=============', num)
                                aaa = page.ele(
                                    f'xpath=//div[@class="feeds-container"]/section[@class="note-item" and @data-width and @data-index="{num}"]')
                                aaa.click()
                                page.wait(2)
                                data = list(get_data(page))
                                comments = '###'
                                for dat in page.listen.steps(timeout=2):
                                    all_items = jsonpath(dat.response.body, "$..data.comments[*]")
                                    for item in all_items:
                                        con1 = ''
                                        con2 = ''
                                        try:
                                            tmp = jsonpath(item, "$.sub_comments[0].content")
                                            con1 = tmp[0]
                                        except Exception as e:
                                            pass
                                        try:
                                            tmp = jsonpath(item, "$.content")
                                            con2 = tmp[0]
                                        except Exception as e:
                                            pass
                                        comments = comments + con1 + '###' + con2 + '###'
                                # print(comments)
                                if data[0] not in hashset:
                                    hashset.add(data[0])
                                    data.append(comments)
                                else:
                                    pass
                                # yy = 0
                                # while True:
                                #     high = random.randint(1800, 2200)
                                #     page.run_js(f'window.scrollTo(0,{int(yy) + int(high)});')
                                #     scroll_top = int(page.run_js(
                                #         "return window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop;"))
                                #     print(f"当前垂直滚动位置：{scroll_top} 像素,y{yy}")
                                #     if scroll_top == y:
                                #         yy = 0
                                #         break
                                #     yy= scroll_top
                                #     page.wait(2)
                                print(data)
                                writer.writerow(data)
                                page.wait(random.randint(8, 20))
                                closs_button = page.ele(
                                    'xpath=//div[@class="close-circle"]/div[@class="close close-mask-dark"]')
                                closs_button.click()
                                page.wait(1)
                            except Exception as e:
                                print('发生错误', e)
                                page.wait(random.randint(8, 15))
                                closs_button = page.ele(
                                    'xpath=//div[@class="close-circle"]/div[@class="close close-mask-dark"]')
                                closs_button.click()
                                page.wait(1)

                    high = random.randint(1800, 2200)
                    page.run_js(f'window.scrollTo(0,{int(y) + int(high)});')
                    scroll_top = int(page.run_js(
                        "return window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop;"))
                    print(f"当前垂直滚动位置：{scroll_top} 像素,y{y}")
                    if scroll_top == y:
                        y = 0
                        break
                    y = scroll_top
                    num_ly.clear()
                    page.wait(2)
                num_count.clear()

        def spider_by_cookies_by_proxies():
            def aaa(data_ly, proxies_ly, cookies_ly):
                with open('./set_01/guangdong.csv', 'a', encoding='utf-8-sig', newline="") as file:
                    writer = csv.writer(file)
                    # writer.writerow(['标题','作者','日期','提及的关键字','内容描述','标题','评论','点赞','收藏'])
                    for i in data_ly[248:-1]:
                        headers = {
                            'User-Agent': FakeUserAgent(platforms='desktop').random,
                        }
                        url = f'https://www.xiaohongshu.com/explore/{i[3]}?xsec_token={i[4]}'
                        cookies = random.choice(cookies_list)
                        proxy = {
                            'https': random.choice(proxies_ly),
                        }
                        print('正在发起请求')
                        try:
                            text = bbb(headers, proxy, cookies, url)
                            html = etree.HTML(text)

                            keywords = html.xpath('//meta[@name="keywords"]/@content') or ['']
                            keywords = keywords[0]
                            description = html.xpath('//meta[@name="description"]/@content') or ['']
                            description = description[0]
                            content = html.xpath('//meta[@name="og:title"]/@content') or ['']
                            content = content[0]
                            note_comment = html.xpath('//meta[@name="og:xhs:note_comment"]/@content') or ['']
                            note_comment = note_comment[0]
                            note_like = html.xpath('//meta[@name="og:xhs:note_like"]/@content') or ['']
                            note_like = note_like[0]
                            note_collect = html.xpath('//meta[@name="og:xhs:note_collect"]/@content') or ['']
                            note_collect = note_collect[0]
                            tmp_data = [keywords, description, content, note_comment, note_like, note_collect]
                            # print(tmp_data)
                            all_data = [i[0], i[2], i[5]]
                            print(all_data)
                            all_data.extend(tmp_data)
                            print(all_data)
                            writer.writerow(all_data)
                            print('数据写入完成')
                            time.sleep(random.randint(4, 8))
                        except Exception as e:
                            print('发生错误', e)
                            time.sleep(random.randint(3, 6))
                            continue

            @retry(stop_max_attempt_number=5)
            def bbb(headers, proxies, cookies, url):
                print('代理发起了一次请求')
                response = requests.get(url, headers=headers, proxies=proxies, cookies=cookies)
                # print(response.text)
                time.sleep(random.random() * 2)
                return response.text

            def ccc(data_ly, proxies_ly):
                count = 0
                with open('./set_01/guangdong.csv', 'a', encoding='utf-8-sig', newline="") as file:
                    writer = csv.writer(file)
                    # writer.writerow(['标题','作者','日期','提及的关键字','内容描述','标题','评论','点赞','收藏'])
                    for i in data_ly[165:-1]:
                        headers = {
                            'User-Agent': FakeUserAgent(platforms='desktop').random,
                        }
                        proxy = {
                            'https': random.choice(proxies_ly),
                        }
                        cookies = random.choice(cookies_list)
                        url = f'https://www.xiaohongshu.com/explore/{i[3]}?xsec_token={i[4]}'

                        print('正在发起请求')
                        try:
                            text = bbb(headers, proxy, cookies, url)
                            html = etree.HTML(text)

                            keywords = html.xpath('//meta[@name="keywords"]/@content') or ['']
                            keywords = keywords[0]
                            description = html.xpath('//meta[@name="description"]/@content') or ['']
                            description = description[0]
                            content = html.xpath('//meta[@name="og:title"]/@content') or ['']
                            content = content[0]
                            note_comment = html.xpath('//meta[@name="og:xhs:note_comment"]/@content') or ['']
                            note_comment = note_comment[0]
                            note_like = html.xpath('//meta[@name="og:xhs:note_like"]/@content') or ['']
                            note_like = note_like[0]
                            note_collect = html.xpath('//meta[@name="og:xhs:note_collect"]/@content') or ['']
                            note_collect = note_collect[0]
                            tmp_data = [keywords, description, content, note_comment, note_like, note_collect]
                            # print(tmp_data)
                            all_data = [i[0], i[2], i[5]]
                            print(all_data)
                            all_data.extend(tmp_data)
                            print(all_data)
                            writer.writerow(all_data)
                            print('数据写入完成')
                            count += 1
                            print(f'-------------{count}--------------------')
                            time.sleep(random.randint(2, 4))
                        except Exception as e:
                            print('发生错误', e)
                            time.sleep(random.randint(2, 4))
                            continue

            class GetProxies:
                """
                获取与使用代理ip
                """

                def __init__(self):
                    self.headers = {
                        'User-Agent': FakeUserAgent(platforms='desktop').random,
                    }
                    self.headers_generator = FakeUserAgent(platforms='desktop')

                def save_proxies(self, url):
                    response = requests.get(url, headers=self.headers)
                    with open('./proxies/proxies_ip.txt', 'w', encoding='utf_8') as f:
                        f.write(response.text)

                def get_proxies_list(self):
                    with open('./proxies/proxies_ip.txt', 'r', encoding='utf-8') as f:
                        # 将每一行转化为一个元素，去除多余的\n，返回代理ip列表
                        proxies_list = f.readlines()
                        for i in range(len(proxies_list)):
                            proxies_list[i] = proxies_list[i].strip()
                    return proxies_list

            url = input('ip:')
            proxies_class = GetProxies()
            proxies_class.save_proxies(url=url)
            proxies_list = proxies_class.get_proxies_list()

            data_aaa = input("请输入帖子id（列表）：")
            cookies_list = input("前输入帖子cookies（列表）：")

            aaa(data_aaa, proxies_list, cookies_list)

class Chaojiying_Client(object):

    def __init__(self, username, password, soft_id):
        self.username = username
        password =  password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        return r.json()

    def PostPic_base64(self, base64_str, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
            'file_base64':base64_str
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()


    def main(self):
        chaojiying = Chaojiying_Client('超级鹰用户名', '超级鹰用户名的密码', '96001')  # 用户中心>>软件ID 生成一个替换 96001
        im = open('a.jpg', 'rb').read()  # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
        print(chaojiying.PostPic(im, 1902))

class QidianSpider():
    def __init__(self):
        pass

    def get_url(url):
        """
        获取字体文档地址，并同时获取下一页地址
        :param url:
        :return:
        """
        header_value = FakeUserAgent(platforms='desktop').random
        headers = {
            'User-Agent': header_value,
            'Cookie': 'x-web-secsdk-uid=235d74f9-698a-4fed-a088-e5448e2c77ee; Hm_lvt_2667d29c8e792e6fa9182c20a3013175=1762956320; HMACCOUNT=E6EA64EA32ED02A2; csrf_session_id=f67a1ee8b9d713b329ccf8dedf01be70; s_v_web_id=verify_mhw2obb9_vPbiaWvN_nXk2_4Rpy_9wW1_HL5HN6dDvj5x; novel_web_id=7571839718960383531; Hm_lpvt_2667d29c8e792e6fa9182c20a3013175=1762956391; ttwid=1%7Cc-hDiz2cxGQO7qrLhg6B4svoA-7nyNlT4CAKOywJpGw%7C1762956392%7Cb7f2351fb34b69be96add6c0157c80554a4ff1d22cf01fb66cda600c6d4cd487'
        }
        response = requests.get(url, headers=headers)
        woff2_url_list = re.findall(r'url\((.*?)\)format\("woff2"\),', response.text)
        next_element = re.findall(r',"nextItemId":"(.*?)",', response.text)
        next_url = f'https://fanqienovel.com/reader/{next_element[0]}?enter_from=reader'
        woff2_url = woff2_url_list[0]
        return woff2_url, next_url

    def get_content(url):
        """
        获取并处理小说，转换成二维列表
        :return: list
        """
        header_value = FakeUserAgent(platforms='desktop').random
        headers = {
            'User-Agent': header_value,
            'Cookie': 'x-web-secsdk-uid=235d74f9-698a-4fed-a088-e5448e2c77ee; Hm_lvt_2667d29c8e792e6fa9182c20a3013175=1762956320; HMACCOUNT=E6EA64EA32ED02A2; csrf_session_id=f67a1ee8b9d713b329ccf8dedf01be70; s_v_web_id=verify_mhw2obb9_vPbiaWvN_nXk2_4Rpy_9wW1_HL5HN6dDvj5x; novel_web_id=7571839718960383531; Hm_lpvt_2667d29c8e792e6fa9182c20a3013175=1762956391; ttwid=1%7Cc-hDiz2cxGQO7qrLhg6B4svoA-7nyNlT4CAKOywJpGw%7C1762956392%7Cb7f2351fb34b69be96add6c0157c80554a4ff1d22cf01fb66cda600c6d4cd487'
        }
        response = requests.get(url, headers=headers)
        xpathTree = etree.HTML(response.text)
        content_data = xpathTree.xpath('//div[@class="muye-reader-content noselect"]/div/p/text()')
        content_list = []
        for i in content_data:
            tmp = []
            for j in i:
                tmp.append((j, ord(j)))
            content_list.append(tmp)
        print(content_list)
        return content_list

    def save_woff2(woff2_url, file_name):
        header_value = FakeUserAgent(platforms='desktop').random
        headers = {
            'User-Agent': header_value,
            'Cookie': 'x-web-secsdk-uid=235d74f9-698a-4fed-a088-e5448e2c77ee; Hm_lvt_2667d29c8e792e6fa9182c20a3013175=1762956320; HMACCOUNT=E6EA64EA32ED02A2; csrf_session_id=f67a1ee8b9d713b329ccf8dedf01be70; s_v_web_id=verify_mhw2obb9_vPbiaWvN_nXk2_4Rpy_9wW1_HL5HN6dDvj5x; novel_web_id=7571839718960383531; Hm_lpvt_2667d29c8e792e6fa9182c20a3013175=1762956391; ttwid=1%7Cc-hDiz2cxGQO7qrLhg6B4svoA-7nyNlT4CAKOywJpGw%7C1762956392%7Cb7f2351fb34b69be96add6c0157c80554a4ff1d22cf01fb66cda600c6d4cd487'
        }
        response = requests.get(woff2_url, headers=headers)
        with open(f'{file_name}.woff2', 'wb') as f:
            f.write(response.content)

    def get_real_dict(file_path):
        """
        获取点码值与字符的映射
        :return: dict
        """
        # 实例化文字图片识别
        real_dict = {}
        font_woff = TTFont(file_path)
        fake_dict = font_woff.getBestCmap()
        ddc = ddddocr.DdddOcr(show_ad=False)

        for key in fake_dict:
            image = Image.new('RGB', size=(100, 100), color='white')
            # 实例化绘制字体的对象
            draw_01 = ImageDraw.Draw(image)
            # 打开字体文件，此时font所储存的内容为加密的字体信息，包含其笔画
            font = ImageFont.truetype(file_path, size=50)
            draw_01.text((25, 25), chr(key), font=font, fill='black')
            real_str = ddc.classification(image)
            if real_str is None:
                image.save(f'images/{key}.png')
            real_dict[key] = real_str
        # print(real_dict)
        del fake_dict
        print(real_dict)
        return real_dict

    def convert_txt(content_list, map):
        """
        小说内容二位列表转换解密
        :param content_list: 小说的二维列表
        :param map: 电码字符映射表映射表
        :return: 二维list
        """
        for i in range(len(content_list)):
            for j in range(len(content_list[i])):
                if content_list[i][j][1] in map:
                    content_list[i][j] = map[content_list[i][j][1]]
                else:
                    content_list[i][j] = content_list[i][j][0]
        return content_list

    def save_story(file_name, lyst):
        with open(f'story/{file_name}.txt', 'w', encoding='utf-8') as f:
            for i in lyst:
                i.append('\n')
                a = ''.join(i)
                f.write(a)



if __name__ == '__main__':

    """
    此段主程序为提取代理ip的程序
    """
    # url = input('ip:')
    proxies_class = GetProxies()
    # proxies_class.save_proxies(url=url)
    proxies_list = proxies_class.get_proxies_list()


    """
    此程序为瓜子二手车api的调用
    """
    ###定义类
    Spider_Car = SpiderToGuaziershouche()

    ### 当只抓取少量数据，不用异步化
    car_research_id = Spider_Car.get_car_research_id('https://www.guazi.com/wei/tesila/model-y/')
    # Spider_Car.get_car_data(car_research_id)
    Spider_Car.get_car_data_by_proxy(car_research_id,proxies_list)

    ### 抓取大量数据的方案，使用异步化协同
    # car_research_id = Spider_Car.get_car_research_id('https://www.guazi.com/wei/tesila/model-y/',page = 10)
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # asyncio.run(Spider_Car.get_car_requests_by_async(car_research_id, proxies_list))


