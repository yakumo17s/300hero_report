import scrapy
import re
import requests
from scrapy import Selector
from scrapy import Request
from ..items import *
                       

class JumpReport(scrapy.Spider):

    name = "JumpReport"
    host = "http://300report.jumpw.com/"
    
    def __init__(self, user=None, *args, **kwargs):
        super(JumpReport, self).__init__(*args, **kwargs)
        self.user = user
        print(user)
        self.start_urls = [
            "http://300report.jumpw.com/list.html?name=%s" % user
        ]
        
    count = 0

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse_topic)

    def parse_topic(self, response):
        selector = Selector(response)
        info = selector.xpath("/html/body/div/div/div/div/table[@class='info']")
        name = info.xpath("tr[1]/td[2]/text()").extract_first()
        level = info.xpath("tr[2]/td[2]/text()").extract_first()
        win = info.xpath("tr[4]/td[2]/text()").extract_first()
        match_count = info.xpath("tr[5]/td[2]/text()").extract_first()
        update_time = info.xpath("tr[6]/td[2]/text()").extract_first()

        item = Player()
        item['name'] = name
        item['level'] = level
        item['win'] = win
        item['match_count'] = match_count
        item['update_time'] = update_time

        server_rank = selector.xpath("//*[@class='datatable'][1]/tr")
        if server_rank:
            for tr in server_rank:
                if "团队实力" in tr.xpath("string(.)").extract_first():
                    rank = re.search(r'(第\d*名)', tr.xpath("td[2]/text()").extract_first()).group(1)
                    strength = tr.xpath("td[4]/text()").extract_first()
                    item['strength'] = strength
                    item['rank'] = rank
                    break
        else:
            report = selector.xpath(
                "/html/body/div/div/div/div/table[@class='datatable'][last()]/tr[2]")
            uri_js = report.xpath("@onclick").extract_first()

            match_id = re.search(r"id=(\d*)", uri_js).group(1)
            api = requests.get("http://300report.jumpw.com/api/getmatch?id={}".format(match_id))

            if report.xpath("td[3]") == "胜利":
                win_side = api["Match"]["WinSide"]
                for role in win_side:
                    if role["RoleName"] == name:
                        strength = role["ELO"]
                        print(strength)
                        item['strength'] = strength
                        break
            else:
                lose_side = api["Match"]["LoseSide"]
                for role in lose_side:
                    if role["RoleName"] == name:
                        strength = role["ELO"]
                        print(strength)
                        item['strength'] = strength
                        break


        item['rank'] = 'a'
        yield item


        report_list = selector.xpath("/html/body/div/div/div/div/table[@class='datatable'][last()]/tr[position()>1]")
        for report in report_list:
            self.count += 1
            print("my_count" + str(self.count))

            hero_line = report.xpath("td[2]").extract_first()
            hero = re.match(r"(<.+>)(.*)(<.+>)(.*)(<.+>)", hero_line)
            hero_name = re.match(r"(\w*)(.*)", hero.group(4)).group(1)
            hero_level = re.match(r'[^0-9]*([0-9]*).*', re.match(r"(\w*)(.*)", hero.group(4)).group(2)).group(1)
            result_line = report.xpath("td[3]").extract_first()
            result = re.match(r".*>(.*)<.*", result_line).group(1)
            date_line = report.xpath("td[4]").extract_first()
            date = re.match(r'<[^>]*>([^<]*)<[^>]*', date_line).group(1)

            uri_js = report.xpath("@onclick").extract_first()
            match_obj = re.match(r".*\'(.*)\'.*", uri_js, flags=0).group(1)
            match_id = re.search(r"id=(\d*)", uri_js).group(1)
            url = self.host + match_obj

            item = ResultList()
            item["name"] = name
            item["match_id"] = match_id
            item["hero"] = hero_name
            item["date"] = date
            item["result"] = result
            yield item
            yield Request(url=url, callback=self.parse_page)
    
        next_url_line = selector.xpath("/html/body/div/div/div/div/a[last()]")
        str_next_url_line = next_url_line.xpath("text()").extract_first()
        if "下一页" in str_next_url_line:
            url = next_url_line.xpath("@href").extract_first()
            next_url = self.host + url
            yield Request(url=next_url, callback=self.parse_topic)

    def parse_page(self, response):
        selector = Selector(response)
        match_id = re.search(r'id=(\d*)', response.url).group(1)
        datamsg_line = selector.xpath("//div[@class='datamsg']").extract_first()
        head = re.search(r"人头数:(\S*)", datamsg_line).group(1)
        date = re.search(r"时间:(\S*)", datamsg_line).group(1)
        time = re.search(r"用时:(\S*)", datamsg_line).group(1)

        game_list = selector.xpath("//*[@class='datatable']")
        game_line = game_list.xpath("tr")
        for game in game_line:
            str_game = game.xpath("string(.)").extract_first()
            user_name = re.search(r"{}".format(self.user), str_game)
            if user_name:
                manifestation_line = game.xpath("td[3]").extract_first()
                manifestation = re.search(r'(\d*)/(\d*)/(\d*)', manifestation_line)
                kill = manifestation.group(1)
                death = manifestation.group(2)
                support = manifestation.group(3)
                score_line = game.xpath("td[8]").extract_first()
                score = re.match(r"<[^>]*>([^<]*).*", score_line).group(1)

                item = GameResult()
                item["match_id"] = match_id
                item["head"] = head
                item["date"] = date
                item["time"] = time
                item["kill"] = kill
                item["death"] = death
                item["support"] = support
                item["score"] = score
                yield item
                break


#class BatterReport(scrapy.Spider):
#    name = "BatterReport"
#    host = "http://300report.jumpw.com/"
#    start_urls = [
#        "http://300report.jumpw.com/list.html?name=%E8%94%BD%E6%9C%88%E5%85%AB%E4%BA%91"
#    ]
#
#    def start_requests(self):
#        for url in self.start_urls:
#            yield Request(url=url, callback=self.parse)
#
#    def parse(self, response):
#        selector = Selector(response)