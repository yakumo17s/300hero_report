300英雄战绩查询
=========

一个爬虫+一个GUI

把数据下载下来，找个方法展示一下。

scrapy PyQt matplotlib

尚未完成。

### 运行方式

python 300hero.py



### TODO

* 防止爬取重复信息

* 数据存入本地库，查询时优先从本地库获取

* 点击某一场次时，会弹出一个对话框，显示该场的详细数据

* 把数据显示规整一些 （也许需要pandas和matplotlib）

* 加点图表（团分变化图……）

* 多窗口（点击显示详细战况）

* 再来个Web端

* 具体场次的数据，不再使用爬虫，改用api获取

### Bug

* ~~重复查询会报错 twisted.internet.error.ReactorNotRestartable （考虑一下多进程）~~
    使用subprocess调用命令行命令执行爬虫

* 长时间没打会不显示表格，导致缺少团分信息而无法显示整个个人信息


