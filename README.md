# GraduationProject

## 目录结构

```terminal
GraduationProject
├─scrapy    //爬虫部分
│   └─src
│       ├─url_fid.txt       //广州市所有领导的fid，用于形成url
│       ├─single_thread_with_selenium.py        //单线程+selenium
│       └─multiple_thread_with_selenium.py      //多线程+selenium
└─README.md
```

## 环境依赖

### 爬虫

1. Python：3.X
2. 所需库：
   - dateutil
     - 安装方法：`pip install python-dateutil`
   - selenium
     - 安装方法：`pip install selenium`
3. 模拟驱动：chromedriver或edgedriver或firfoxdriver等。到官网下载与浏览器对应的版本，放在Python安装路径下的Scripts目录下。（目测chrome是最快的）
4. 代码对比
   > 单线程+selenium版，运行较慢但数据不易出错\
   > 多线程+selenium版，当线程池设置为3时，由于多个fid对应的链接可同时进行爬取，因此速度较快\
   > 但由于多个线程之间数据不安全，以及会出现线程饥饿，容易发生数据缺失\
   > 