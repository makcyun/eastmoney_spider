from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import pandas as pd
import os

# 先chrome，后phantomjs
# browser = webdriver.Chrome()

# 添加无头headlesss
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)

# browser = webdriver.PhantomJS() # 会报警高提示不建议使用phantomjs，建议chrome添加无头
browser.maximize_window()  # 最大化窗口
wait = WebDriverWait(browser, 10)


def index_page(page):
    try:
        print('正在爬取第： %s 页' % page)
        wait.until(
            EC.presence_of_element_located((By.ID, "dt_1")))
        # 判断是否是第1页，如果大于1就输入跳转，否则等待加载完成。
        if page > 1:
            # 确定页数输入框
            input = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="PageContgopage"]')))
            input.click()
            input.clear()
            input.send_keys(page)
            submit = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#PageCont > a.btn_link')))
            submit.click()
            time.sleep(2)
        # 确认成功跳转到输入框中的指定页
        wait.until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, '#PageCont > span.at'), str(page)))
    except Exception:
        return None


def parse_table():
    # 提取表格第一种方法
    # element = wait.until(EC.presence_of_element_located((By.ID, "dt_1")))
    # 第二种方法
    element = browser.find_element_by_css_selector('#dt_1')

    # 提取表格内容td
    td_content = element.find_elements_by_tag_name("td")
    lst = []
    for td in td_content:
        # print(type(td.text)) # str
        lst.append(td.text)

    # 确定表格列数
    col = len(element.find_elements_by_css_selector('tr:nth-child(1) td'))
    # 通过定位一行td的数量，可获得表格的列数，然后将list拆分为对应列数的子list
    lst = [lst[i:i + col] for i in range(0, len(lst), col)]

    # 原网页中打开"详细"链接，可以查看更详细的数据，这里我们把url提取出来，方便后期查看
    lst_link = []
    links = element.find_elements_by_css_selector('#dt_1 a.red')
    for link in links:
        url = link.get_attribute('href')
        lst_link.append(url)

    lst_link = pd.Series(lst_link)
    # list转为dataframe
    df_table = pd.DataFrame(lst)
    # 添加url列
    df_table['url'] = lst_link

    # print(df_table.head())
    return df_table


# 写入文件
def write_to_file(df_table, category):
    # 设置文件保存在D盘eastmoney文件夹下
    file_path = 'D:\\eastmoney'
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    os.chdir(file_path)
    df_table.to_csv('{}.csv' .format(category), mode='a',
                    encoding='utf_8_sig', index=0, header=0)


# 设置表格获取时间、类型
def set_table():
    print('*' * 80)
    print('\t\t\t\t东方财富网报表下载')
    print('作者：高级农民工  2018.10.6')
    print('--------------')

    # 1 设置财务报表获取时期
    year = int(float(input('请输入要查询的年份(四位数2007-2018)：\n')))
    # int表示取整，里面加float是因为输入的是str，直接int会报错，float则不会
    # https://stackoverflow.com/questions/1841565/valueerror-invalid-literal-for-int-with-base-10
    while (year < 2007 or year > 2018):
        year = int(float(input('年份数值输入错误，请重新输入：\n')))

    quarter = int(float(input('请输入小写数字季度(1:1季报，2-年中报，3：3季报，4-年报)：\n')))
    while (quarter < 1 or quarter > 4):
        quarter = int(float(input('季度数值输入错误，请重新输入：\n')))

    # 转换为所需的quarter 两种方法,2表示两位数，0表示不满2位用0补充，
    # http://www.runoob.com/python/att-string-format.html
    quarter = '{:02d}'.format(quarter * 3)
    # quarter = '%02d' %(int(month)*3)
    date = '{}{}' .format(year, quarter)
    # print(date) 测试日期 ok

    # 2 设置财务报表种类
    tables = int(
        input('请输入查询的报表种类对应的数字(1-业绩报表；2-业绩快报表：3-业绩预告表；4-预约披露时间表；5-资产负债表；6-利润表；7-现金流量表): \n'))

    dict_tables = {1: '业绩报表', 2: '业绩快报表', 3: '业绩预告表',
                   4: '预约披露时间表', 5: '资产负债表', 6: '利润表', 7: '现金流量表'}
    dict = {1: 'yjbb', 2: 'yjkb/13', 3: 'yjyg',
            4: 'yysj', 5: 'zcfz', 6: 'lrb', 7: 'xjll'}
    category = dict[tables]

    # 3 设置url
    # url = 'http://data.eastmoney.com/bbsj/201803/lrb.html' eg.
    url = 'http://data.eastmoney.com/{}/{}/{}.html' .format(
        'bbsj', date, category)

    # # 4 选择爬取页数范围
    start_page = int(input('请输入下载起始页数：\n'))
    nums = input('请输入要下载的页数，（若需下载全部则按回车）：\n')
    print('*' * 80)

    # 确定网页中的最后一页
    browser.get(url)
    # 确定最后一页页数不直接用数字而是采用定位，因为不同时间段的页码会不一样
    try:
        page = browser.find_element_by_css_selector('.next+ a')  # next节点后面的a节点
    except:
        page = browser.find_element_by_css_selector('.at+ a')
    # else:
    #     print('没有找到该节点')
    # 上面用try.except是因为绝大多数页码定位可用'.next+ a'，但是业绩快报表有的只有2页，无'.next+ a'节点
    end_page = int(page.text)

    if nums.isdigit():
        end_page = start_page + int(nums)
    elif nums == '':
        end_page = end_page
    else:
        print('页数输入错误')

    # 输入准备下载表格类型
    print('准备下载:{}-{}' .format(date, dict_tables[tables]))
    print(url)

    yield{
        'url': url,
        'category': dict_tables[tables],
        'start_page': start_page,
        'end_page': end_page
    }


def main(category, page):
    try:
        index_page(page)
        # parse_table() #测试print
        df_table = parse_table()
        write_to_file(df_table, category)
        print('第 %s 页抓取完成' % page)
        print('--------------')
    except Exception:
        print('网页爬取失败，请检查网页中表格内容是否存在')

# 单进程
if __name__ == '__main__':

    for i in set_table():
        # url = i.get('url')
        category = i.get('category')
        start_page = i.get('start_page')
        end_page = i.get('end_page')

    for page in range(start_page, end_page):
        # for page in range(44,pageall+1): # 如果下载中断，可以尝试手动更改网页继续下载
        main(category, page)
    print('全部抓取完成')
