'''
Author: GanJianWen
Date: 2021-02-22 17:26:05
LastEditors: GanJianWen
LastEditTime: 2021-03-04 20:00:17
QQ: 1727949032
GitHub: https://github.com/1727949032a/
Gitee: https://gitee.com/gan_jian_wen_main
'''
import json
import re
import threading
import zhconv
import requests
from lxml import etree
from os.path import exists, abspath
from os import makedirs, listdir
from datetime import datetime
from os import system
from novel3.novel_yunlin.image_to_str_map import ImageToStr
from novel3.novel_yunlin.config import Config
from novel3.novel_yunlin.utils.regex import RegexUtils


class YuLinZhanYeScrapy:

    def __init__(self, db="sqlite") -> None:
        self.novel_config = Config.read_config()
        self.domain = self.novel_config.get('novel_domain')
        self.total_page = self.novel_config.get('total_page')
        self.novel_path = self.novel_config.get('novel_path')
        self.threading_lock = threading.Lock()
        self.DEFAULT_REQUEST_HEADERS = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
        }
        self.BOOK_LISTS = []
        module_name = "novel3.novel_yunlin.db.{}".format(db)
        module_meta = __import__(
            module_name, globals(), locals(), [db.capitalize()])
        class_meta = getattr(module_meta, db.capitalize())
        self.database = class_meta()
        self.image_tool = ImageToStr()
        print(self.database)

    def aks_url(self, url, timeout=5):
        while True:
            try:
                print(f"正在请求:{url}")
                response = requests.get(
                    url, headers=self.DEFAULT_REQUEST_HEADERS, timeout=timeout)
                break
            except:
                continue
        return response.text

    def generate_book_list(self):
        self.novel_config = Config.read_config()
        self.domain = self.novel_config.get('novel_domain')
        self.total_page = int(self.novel_config.get('total_page'))
        self.novel_path = self.novel_config.get('novel_path')
        print(self.domain)
        self.BOOK_LISTS = [
            f"{self.domain}/shuku/0-lastupdate-0-%d.html" % i for i in range(0, self.total_page + 1)]

    def set_domain(self, domain: str):
        with open(f"{abspath(__file__)}/../config/novel.json", "r", encoding="utf-8") as fp:
            novel_config = json.load(fp)
        novel_config['novel_domain'] = domain
        with open(f"{abspath(__file__)}/../config/novel.json", "w", encoding="utf-8") as fp:
            json.dump(novel_config, fp, ensure_ascii=False, indent=4)

    def get_total_page(self):
        sku_url = f"{self.domain}/shuku/"
        print(sku_url)
        content = self.aks_url(sku_url)
        self.total_page = RegexUtils.regex_search(content, r'第1/(\d+?)页', 1)
        self.novel_config['total_page'] = self.total_page
        with open(f"{abspath(__file__)}/../config/novel.json", "w", encoding="utf-8") as fp:
            json.dump(self.novel_config, fp, ensure_ascii=False, indent=4)

    def filter_summary(self, summary: str) -> str:
        if not summary:
            return str()
        summary = re.sub(r"<[\s]*?script[^>]*?>[\s\S]*?<[\s]*?\/[\s]*?script[\s]*?>", "", summary)
        summary = re.sub(r"<[\s]*?SCRIPT[^>]*?>[\s\S]*?<[\s]*?\/[\s]*?SCRIPT[\s]*?>", "", summary)
        summary = re.sub(r"(\r|\n|\t|<p>|</p>|<br/>|<P>|</P>|<br>)", "&br", summary)
        summary = re.sub(r"[*|/]*", "", summary)
        summary = re.sub(r"(&nbp;)+?", "", summary)
        summary = re.sub(r"(&nbsp;)+?", "", summary)
        summary = re.sub(r"<[^>]+>", "", summary)
        summary = re.sub(r"[video,uuid\-(.+?)]", "", summary)
        summary = re.sub(r"(\w|&br){1,40}?\([\w,]{1,200}?\)\{(.)+?;}", "", summary)
        summary = re.sub(r"\$[^;]+;", "", summary)
        summary = re.sub(r"(\w|&br){1,40}?\([\w,]{1,200}?\)\{(.)+?;}", "", summary)
        summary = re.sub(r"(&br)+", "\n", summary)
        summary = re.sub(r"(&ldquo;|&rdquo;)", "\"", summary)
        summary = re.sub(r"(&gt;)", ">", summary)
        summary = re.sub(r"&amp;ldquo;", "“", summary)
        summary = re.sub(r"&amp;rdquo;", "”", summary)
        summary = re.sub(r"&amp;mdah;", "—", summary)
        summary = re.sub(r"&amp;lquo;", "‘", summary)
        summary = re.sub(r"amp;rquo;", "’", summary)
        summary = summary.replace("\n", "\n\n")
        summary = re.sub(r"[\n]{2,}", "\n\n", summary)
        summary = summary.strip()
        return summary

    def check_domain_valid(self):
        content = self.aks_url(self.domain)
        str_url = RegexUtils.regex_search(content, r"strU=\"(.+?)\"", 1)
        if str_url:
            to_url = f"{str_url}{self.domain}/&p=/"
            content = self.aks_url(to_url)
            content = etree.HTML(content)
            self.domain = content.xpath('//div[@class="line"]//p//a[1]/@href')[0]
            self.set_domain(self.domain)

    def book_scrapyed(self, book_name, word_number):
        select_sql = "select book_name,word_number from book where book_name='%s' and word_number=%d;" % (
            book_name, word_number)
        self.threading_lock.acquire()
        book_list = self.database.get_datas(select_sql)
        self.threading_lock.release()
        if len(book_list) > 0:
            return True
        else:
            return False

    def visit_book_one_lists(self, url):
        print("list_url:", url)
        book_list = list()
        html = self.aks_url(url)
        html = etree.HTML(html)
        li_list = html.xpath('//div[@class="bd"]/ul/li')
        for li in li_list:
            book_name = li.xpath(
                'div[@class="right"]/a/text()')[0].replace(':', " ").replace('?', ' ').replace('*', 'x')
            book_link = self.domain + \
                        li.xpath('div[@class="right"]/a/@href')[0]
            author = li.xpath(
                '//a[@class="author"]/text()')[0]
            word_numbers = li.xpath(
                'div[@class="right"]//p[@class="info"]/span/text()')[0].replace('字数：', '')
            print(book_name)
            try:
                update_date = li.xpath(
                    'div[@class="right"]//p[@class="info"]/font/text()')[0]
            except:
                # print("book_name=", book_name)
                update_date = li.xpath(
                    'div[@class="right"]//p[3]/text()')[0].replace('\n更新：', '').strip()
                # print("update_date=", update_date)

            if self.book_scrapyed(book_name, int(word_numbers)):
                continue
            item = dict()
            item['book_name'] = book_name
            item['author'] = author
            item['book_link'] = book_link
            item['word_numbers'] = word_numbers
            item['update_date'] = update_date
            book_list.append(item)

        thread_list = []
        for book in book_list:
            t = threading.Thread(target=self.visit_book_detail, args=(book,))
            thread_list.append(t)
        for t in thread_list:
            t.start()
        for t in thread_list:
            t.join()

    def book_exist_and_not_updated(self, book_name, chapter_number):
        select = "select * from book where book_name='%s';" % book_name
        self.threading_lock.acquire()
        book_list = self.database.get_datas(select)
        self.threading_lock.release()
        if len(book_list) > 0 and book_list[0][-2] < chapter_number:
            return True
        else:
            return False

    def update_book_message(self, book_name, word_number, popularity, update_time, status, chapter_number):
        if self.book_exist_and_not_updated(book_name, chapter_number):
            update_sql = "update book set word_number=%d,popularity=%d,update_time='%s',status='%s',chapter_number=%d,latest=0 where book_name='%s';" % (
                int(word_number), int(popularity), update_time, status, int(chapter_number), book_name)
            # print("update_sql:", update_sql)
            self.threading_lock.acquire()
            self.database.query(update_sql)
            self.threading_lock.release()

    def visit_book_detail(self, book):
        print('当前子线程: {}'.format(threading.current_thread().name))
        begin, count = 1, 0
        print("开始获取%s的详细信息" % book['book_name'])
        self.database.log.info(
            "{}\t正在爬取小说<<{}>>".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), book['book_name']))
        intro = str()
        print("对应链接为%s" % book['book_link'])
        html = self.aks_url(book['book_link'])
        html = etree.HTML(html)
        content = html.xpath(
            '//div[@class="right"]//p[@class="info"]/text()')
        status = html.xpath(
            '//div[@class="right"]/span/text()')[0]
        # print(content)
        type = content[1].replace('\n类型：', '')
        pupular = content[-1].replace('\n', '').replace('人气：', '').strip()
        # print(book["book_name"])
        try:
            intro = html.xpath(
                '//div[@class="mod book-intro"]/div/text()')[0]
        except:
            pass

        try:
            end_page = int(html.xpath(
                '//div[@class="pagelistbox"]//a[@class="endPage"]/@href')[0].split('/')[-2].split('_')[-1])
        except:
            return
            # print("type=", type)
            # print("popular=", pupular)
            # print("status=", status)
            # print("intro=", intro)
        page_list = [book['book_link'][:-1] + "_%d/" %
                     i for i in range(1, end_page + 1)]
        # pprint(page_list)
        chapter_number = 0
        file_path = f"{self.novel_path}/第一版主/{book['book_name']}"
        if exists(file_path):
            begin = len(listdir(file_path)) + 1

        for page in page_list:
            html_page = self.aks_url(page)
            html_page = etree.HTML(html_page)
            li_list = html_page.xpath(
                '//div[@class="mod block update chapter-list"]')[1].xpath('div[@class="bd"]/ul//li')
            chapter_number += len(li_list)
            self.update_book_message(book['book_name'], book['word_numbers'], int(
                pupular), update_time=book['update_date'], status=status, chapter_number=chapter_number)
            for li in li_list:
                count += 1
                if count < begin:
                    continue
                if count % 10 == 0:
                    system("cls")
                chapter_header = li.xpath('a/text()')[0]
                chapter_link = self.domain + \
                               li.xpath('a/@href')[0]
                # print('chapter_header=', chapter_header)
                # print('chapter_link=', chapter_link)
                self.visit_chapter(
                    book['book_name'], chapter_header, chapter_link)

        insert = "insert into book values(NULL,'%s','%s','%s',%d,%d,'%s','%s','%s',%d,0);" % (
            book['book_name'], book['author'], type, int(
                book['word_numbers']), int(pupular), book['update_date'],
            intro, status, chapter_number)
        self.threading_lock.acquire()
        self.database.query(insert)
        self.threading_lock.release()
        print("插入完成")

    def visit_chapter(self, book_name, chapter_name, chapter_link, first=True) -> str:
        file_path = f"{self.novel_path}/第一版主/{book_name}"
        if not exists(file_path):
            makedirs(file_path)
        html = self.aks_url(chapter_link)
        tree = etree.HTML(html)
        content = str()
        for each in tree.xpath('//p[@class="neirong"]'):
            temp = etree.tostring(each, encoding='unicode').replace(' ', ' ')
            temp = temp.replace('<p class="neirong">', '').replace('</p>', '').strip()
            content += temp

        if first:
            contents = content
            page_links = [page.xpath("@href")[0] for page in tree.xpath('//center[@class="chapterPages"]/a')]
            for i in range(1, len(page_links)):
                next_page_link = re.sub(r"\d+.html", page_links[i], chapter_link)
                print(next_page_link)
                chapter_content = self.visit_chapter(book_name, chapter_name, next_page_link, False)
                contents += chapter_content
            contents = self.image_tool.image_to_str_each_chapter(html=contents)
            chapter_name = chapter_name.replace(
                '?', '').replace('2u2u2u', '').replace('/', '-').replace('*', 'x').replace(':', '：').replace('|', '')
            contents = self.filter_summary(contents)
            contents = zhconv.convert(contents, 'zh-hans')
            print(contents)
            with open("%s/%s.txt" % (file_path, chapter_name), "w", encoding='utf-8') as fp:
                fp.write(contents)

        else:
            return content

    def main(self):
        self.database.log.info(
            "{}\t开始爬取小说".format(
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        )
        self.check_domain_valid()
        self.get_total_page()
        self.generate_book_list()
        for url in self.BOOK_LISTS:
            self.visit_book_one_lists(url)


if __name__ == "__main__":
    spider = YuLinZhanYeScrapy()
    #spider.visit_chapter("test", "test", "http://www.01bz9999.xyz/1/1975/280369.html")
