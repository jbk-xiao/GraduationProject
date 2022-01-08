import csv
import os
import random
import re
import time
import threading

import dateutil.parser as dparser
from random import choice
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

# 全局变量和参数配置
# 时间节点
start_date = dparser.parse('2021-12-07')
# 控制同时运行的线程数
sem = threading.Semaphore(3)
# 浏览器设置选项
chrome_options = Options()
chrome_options.add_argument('blink-settings=imagesEnabled=false')
chrome_options.add_argument("--headless")  # 为浏览器配置无头模式 后台运行
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')


def get_time():
    """获取随机时间"""
    return round(random.uniform(2, 4), 1)


def get_user_agent():
    """获取随机用户代理"""
    user_agents = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        # "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
        # "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        # "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1",
        # "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36",
        # "Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20",
        # "Mozilla/5.0 (Linux;u;Android 4.2.2;zh-cn;) AppleWebKit/534.46 (KHTML,like Gecko) Version/5.1 Mobile Safari/10600.6.3 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
        "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html）"
    ]
    # 在user_agent列表中随机产生一个代理，作为模拟的浏览器
    user_agent = choice(user_agents)
    return user_agent
    # 产生随机时间并随机模拟浏览器用于访问网页，降低被服务器识别出是爬虫而被禁的可能。


def get_fid():
    """获取所有领导id"""
    with open('url_fid.txt', 'r') as f:  # TODO 需要外部文件
        content = f.read()
        fids = content.split()
    return fids


def get_detail_urls(leader_name, list_url):
    """获取每个领导的所有留言链接"""
    user_agent = get_user_agent()
    chrome_options.add_argument('user-agent=%s' % user_agent)
    drivertemp = webdriver.Chrome(options=chrome_options)
    drivertemp.maximize_window()
    drivertemp.get(list_url)
    time.sleep(2)
    # 循环加载页面
    try:
        while WebDriverWait(drivertemp, 50, 2).until(EC.element_to_be_clickable((By.ID, "show_more"))):
            datestr = WebDriverWait(drivertemp, 10).until(
                lambda driver: driver.find_element(
                    By.XPATH, '//*[@id="list_content"]/li[position()=last()]/h3/span')
            ).text.strip()
            datestr = re.search(r'\d{4}-\d{2}-\d{2}', datestr).group()
            date = dparser.parse(datestr, fuzzy=True)
            print('正在爬取链接 --', leader_name, '--', date)
            if date < start_date:
                break
            # 模拟点击加载
            drivertemp.find_element(By.XPATH, '//*[@id="show_more"]').click()
            time.sleep(get_time())
        detail_elements = drivertemp.find_elements(By.XPATH, '//*[@id="list_content"]/li/h2/b/a')
        # 获取所有链接
        for element in detail_elements:
            detail_url = element.get_attribute('href')
            yield detail_url
        drivertemp.quit()
    except TimeoutException:  # 超时时递归调用
        drivertemp.quit()
        get_detail_urls(leader_name, list_url)


def get_message_detail(driver, detail_url, writer, leader_name, i):
    """获取留言详情"""
    if i % 50 == 0:
        print('正在爬取第{}留言 --{}--{}'.format(i, leader_name, detail_url))
    driver.get(detail_url)
    message_date_temp = WebDriverWait(driver, 1.5).until(
        lambda driver: driver.find_element(By.XPATH, "/html/body/div[6]/h3/span")).text
    message_date = re.search(r'\d{4}-\d{2}-\d{2}', message_date_temp).group()
    message_datetime = dparser.parse(message_date, fuzzy=True)
    if message_datetime < start_date:
        return
    message_time = re.search(r'\d{2}:\d{2}', message_date_temp).group()
    tid = re.search(r'\d+', detail_url).group()
    # print("detail_url::: {}, tid::: {}".format(detail_url, tid))
    message_title = WebDriverWait(driver, 1.5).until(
        lambda driver: driver.find_element(By.CLASS_NAME, "context-title-text")).text.strip()
    label_elements = WebDriverWait(driver, 1.5).until(lambda driver: driver.find_elements(By.CLASS_NAME, "domainType"))
    try:
        label1 = label_elements[0].text.strip()
        label2 = label_elements[1].text.strip()
    except:
        label1 = ''
        label2 = label_elements[0].text.strip()
    message_content = WebDriverWait(driver, 1.5).until(
        lambda driver: driver.find_element(By.XPATH, "/html/body/div[6]/p")).text.strip()
    # 存入CSV文件
    writer.writerow(
        [leader_name, tid, message_title, label1, label2, message_date, message_time,
         message_content.replace(',', '，').replace('\n', '').replace('\r', '')]  # 替换掉逗号、换行等易出错字符
    )


def get_officer_messages(index, fid):
    """获取并保存领导的所有留言"""
    user_agent = get_user_agent()
    chrome_options.add_argument('user-agent=%s' % user_agent)
    driver = webdriver.Chrome(options=chrome_options)
    list_url = "http://liuyan.people.com.cn/threads/list?fid={}#state=1".format(fid)
    try:
        driver.get(list_url)
        leader_name = WebDriverWait(driver, 10).until(
            lambda driver: driver.find_element(By.XPATH, "/html/body/div[4]/i")).text
        # time.sleep(get_time())
        print(index, '-- 正在爬取 --', leader_name)
        start_time = time.time()
        # encoding='gb18030'
        csv_name = leader_name + '.csv'
        # 文件存在则删除重新创建
        if os.path.exists(csv_name):
            os.remove(csv_name)
        with open(csv_name, 'a+', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, dialect="excel")
            writer.writerow(
                ['leader_name', 'tid', 'message_title', 'label1',
                 'label2', 'message_date', 'message_time', 'message_content']
            )
            i = 0
            for detail_url in get_detail_urls(leader_name, list_url):
                i += 1
                get_message_detail(driver, detail_url, writer, leader_name, i)
                if i % 50 == 0:
                    print("第{}条，当前时间是{}".format(i, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
                    time.sleep(get_time())
        end_time = time.time()
        crawl_time = int(end_time - start_time)
        crawl_minute = crawl_time // 60
        crawl_second = crawl_time % 60
        print(leader_name, '已爬取结束！！！共', i, '条')
        print('共计用时：{}分钟{}秒。'.format(crawl_minute, crawl_second))
        driver.quit()
        time.sleep(5)
    except:
        driver.quit();
        get_officer_messages(index, fid)


def merge_csv():
    """将所有文件合并"""
    file_list = os.listdir('.')
    csv_list = []
    for file in file_list:
        if file.endswith('.csv'):
            csv_list.append(file)
    # 文件存在则删除重新创建
    if os.path.exists('DATA.csv'):
        os.remove('DATA.csv')
    with open('DATA.csv', 'a+', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, dialect="excel")
        writer.writerow(
            ['leader_name', 'tid', 'message_title', 'label1',
             'label2', 'message_date', 'message_time', 'message_content']
        )
        for csv_file in csv_list:
            with open(csv_file, 'r', encoding='utf-8') as csv_f:
                reader = csv.reader(csv_f)
                line_count = 0
                for line in reader:
                    line_count += 1
                    if line_count != 1:
                        writer.writerow(
                            (line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7])
                        )  # TODO 可能有多余元素


def main():
    """主函数"""
    fids = get_fid()
    print('爬虫程序开始执行：')
    s_time = time.time()
    thread_list = []
    # 将所有线程加入线程列表，便于控制同时执行的线程数量
    for index, fid in enumerate(fids):
        t = threading.Thread(target=get_officer_messages, args=(index + 1, fid))
        thread_list.append([t, fid])
    for thread, fid in thread_list:
        # 5层嵌套进行异常处理
        try:
            thread.start()
        except:
            try:
                thread.start()
            except:
                try:
                    thread.start()
                except:
                    try:
                        thread.start()
                    except:
                        try:
                            thread.start()
                        except:
                            # 如果仍出现异常加入失败名单
                            print('该leader爬取失败，已存入失败名单，以备再爬')
                            if not os.path.exists('fid_not_success.txt'):
                                with open('fid_not_success.txt', 'a+') as f:
                                    f.write(fid)
                            else:
                                with open('fid_not_success.txt', 'a+') as f:
                                    f.write('\n' + fid)
                            continue
    for thread, fid in thread_list:
        thread.join()
    print('爬虫程序执行结束！！！')
    print('开始合成文件：')
    merge_csv()
    print('文件合成结束！！！')
    e_time = time.time()
    c_time = int(e_time - s_time)
    c_minute = c_time // 60
    c_second = c_time % 60
    print('{}位领导共计用时：{}分钟{}秒。'.format(len(fids), c_minute, c_second))


if __name__ == '__main__':
    '''执行主函数'''
    main()
