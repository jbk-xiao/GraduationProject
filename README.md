# GraduationProject

## 目录结构

```terminal
GraduationProject
├─scrapy    //爬虫部分
│   └─src
│       ├─DATA.csv          //2020-01-01至2022-01-01广州市各领导收到的留言数据
│       ├─testDATA.csv      //部分留言数据用于测试
│       ├─url_fid.txt       //广州市所有领导的fid，用于形成url
│       ├─single_thread_with_selenium.py        //单线程+selenium
│       ├─multiple_thread_with_selenium.py      //多线程+selenium
│       └─multiple_process_with_selenium.py     //多进程+selenium
├─lda_model //LDA主题模型部分
│   ├─stop_words//中文停用词
│   │   ├─mystopword.txt
│   │   ├─中文停用词库.txt
│   │   ├─哈工大停用词表.txt
│   │   ├─四川大学机器智能实验室停用词库.txt
│   │   └─百度停用词列表.txt
│   ├─LDA_Topic_Select.py
│   └─setting.py
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
   > 多进程+selenium版，按理来说应该比较安全，但是像上边一样出现了某领导的全部数据缺失，难道是触发了反爬机制？
### LDA模型
1. Python：3.X
2. 所需库：
    - jieba
    - pandas
    - numpy
    - matplotlib
    - gensim
    - scikit-learn
3. 代码说明
    `setting.py`为部分模型参数
    `LDA_Topic_Select.py`包括切词和LDA主题模型的选取与运行两个部分