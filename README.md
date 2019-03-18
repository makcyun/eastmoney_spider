### 东方财富网爬虫 / eastmoney_spider

爬取东方财富网上市公司的财务报表数据和公告信息

#### 使用说明：

`eastmoney_crawler.py` 采用 Selenium 方法爬取，需要配置好 Selenium，爬取速度比较慢。

`eastmoney_crawler2.py` 采用 Requests方法爬取，速度比 Selenium 快上百倍，推荐用该程序。

#### 运行放式：

- 打开 Cmd 命令窗口运行程序
- 选择要爬取的年份、报表季度、报表类型、爬取起始和结束页数。
- 开始自动爬取，结果为 CSV 格式，保存在 D 盘 estmoney 文件夹下。

#### 效果图：

![](http://media.makcyun.top/selenium%E7%88%AC%E5%8F%96%E6%95%88%E6%9E%9C.gif)



#### 关于我

- 博客：[高级农民工的](https://www.makcyun.top/)
- 公众号：**高级农民工**



