import re

import requests
from scrapy import Selector, Request, Spider

from jump_300heroes.items import Player, ResultList, GameResult
from model import PlayerData, GameData


class JumpReport(Spider):
    name = "JumpReport"
    host = "http://300report.jumpw.com/"
    count = 0

    def __init__(self, user=None, *args, **kwargs):

        super(JumpReport, self).__init__(*args, **kwargs)

        self.user = user
        print('cls', self.user)

        self.player_info = False
        self.start_urls = [
            "http://300report.jumpw.com/list.html?name=%s" % user
        ]

    def start_requests(self):
        print('net')
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse_topic)

    def parse_player_info(self, selector):

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
                    elo = tr.xpath("td[4]/text()").extract_first()
                    item['elo'] = elo
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
                        elo = role["ELO"]
                        print(elo)
                        item['elo'] = elo
                        break
            else:
                lose_side = api["Match"]["LoseSide"]
                for role in lose_side:
                    if role["RoleName"] == name:
                        elo = role["ELO"]
                        print(elo)
                        item['elo'] = elo
                        break

        return item

    def parse_topic(self, response):
        print('rp')
        selector = Selector(response)

        # 读取第一页时记录玩家排行
        if not self.player_info:
            item = self.parse_player_info(selector)
            yield item
            self.player_info = True

        report_list = selector.xpath("/html/body/div/div/div/div/table[@class='datatable'][last()]/tr[position()>1]")
        for report in report_list:

            self.count += 1
            print("my_count" + str(self.count))

            hero_line = report.xpath("td[2]").extract_first()
            hero = re.match(r"(<.+>)(.*)(<.+>)(.*)(<.+>)", hero_line)
            hero_name = re.match(r"(\w*)(.*)", hero.group(4)).group(1)
            hero_level = re.match(
                r'[^0-9]*([0-9]*).*', re.match(r"(\w*)(.*)", hero.group(4)).group(2)
            ).group(1)
            result_line = report.xpath("td[3]").extract_first()
            result = re.match(r".*>(.*)<.*", result_line).group(1)
            date_line = report.xpath("td[4]").extract_first()
            date = re.match(r'<[^>]*>([^<]*)<[^>]*', date_line).group(1)

            uri_js = report.xpath("@onclick").extract_first()
            match_obj = re.match(r".*\'(.*)\'.*", uri_js, flags=0).group(1)
            match_id = re.search(r"id=(\d*)", uri_js).group(1)
            url = self.host + match_obj

            item = ResultList()
            item["name"] = self.user
            item["match_id"] = match_id
            item["hero"] = hero_name
            item["date"] = date
            item["result"] = result

            # 如果已记录该玩家数据则跳过
            player_data = PlayerData.select().where(
                (PlayerData.name == self.user) & (PlayerData.match_id == match_id)
            ).execute()

            if len(player_data):
                continue

            yield item

            # 如果已记录过该场次数据则跳过
            game_data = GameData.select().where(
                GameData.match_id == match_id
            ).execute()

            if len(game_data):
                continue

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
        date = re.search(r"时间:(.*)比", datamsg_line).group(1)
        time = re.search(r"用时:(\S*)", datamsg_line).group(1)

        # 获取双方战绩表格
        l_game_table = selector.xpath("//*[@class='datatable']")

        # 选择其中一方的表格
        for table in l_game_table:
            game_line = table.xpath("tr")

            # 去掉标题栏
            for game in game_line[1:]:
                # 获得每位玩家的战绩
                user_data = game.xpath('td[2]/a/text()').extract_first()
                user_name = re.match(r'(.*)\(', user_data).group(1)
                role_data = game.xpath('td[2]/text()').extract_first()
                role_group = re.match(r'(.*)\(lv\.(\d*)\)', role_data)
                role = role_group.group(1)
                level = role_group.group(2)
                manifestation_line = game.xpath("td[3]").extract_first()
                manifestation = re.search(r'(\d*)/(\d*)/(\d*)', manifestation_line)
                kill = manifestation.group(1)
                death = manifestation.group(2)
                support = manifestation.group(3)
                result = game.xpath('td[4]/text()').extract_first()
                score = game.xpath("td[8]/text()").extract_first()

                item = GameResult()
                item['name'] = user_name
                item["match_id"] = match_id
                item["head"] = head
                item["date"] = date
                item["time"] = time
                item["kill"] = kill
                item["death"] = death
                item["support"] = support
                item["score"] = score
                item['role'] = role
                item['level'] = level
                item['result'] = result
                yield item

# class BatterReport(scrapy.Spider):
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
