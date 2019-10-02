# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

from InputMongodb.items import InputmongodbItem

class IntoMongodbSpiderSpider(scrapy.Spider):

    name = "IntoMongodbSpider"
    allowed_domains = ["store.steampowered.com"]
    str1 = "https://store.steampowered.com/games#p="
    str2 = "&tab=ConcurrentUsers"
    page = 0
    start_urls = []
    for page in range(1,11):
        start_urls.append(str1+str(page)+str2)

    def parse(self, response):
        gameLinkList = response.xpath('//*[@id="ConcurrentUsersRows"]/a')

        for game in gameLinkList:  # 循环所有game的url

            item = InputmongodbItem()
            item['url'] = ""
            item['name'] = ""
            item['price'] = ""
            item['tags'] = ""
            item['comments'] = ""

            detail_url = game.xpath('./@href').extract()[0]
            try:
                item['url'] = detail_url
                print('游戏地址', item['url'])

                item['name'] = game.xpath('./div[3]/div[1]/text()').extract()[0]
                print('游戏名称', item['name'])

                item['price'] = game.xpath('./div[2]/div[1]/div[1]/text()').extract()[0].strip()
                print('游戏售价', item['price'])
                print()
            except Exception as e:
                print('地址、名称、售价缺失')
                print(e)
                print('detail_url', detail_url)
                print()
                continue

            # yield item
            detail_request = scrapy.Request(
                url=detail_url,
                callback=self.get_details,
                headers={"Accept-Language": "zh-CN,zh;q=0.9"},
                meta={"item": item, "detail_url": detail_url},
                dont_filter=True,
            )
            yield detail_request

    def get_details(self, response):
        item = response.meta["item"]
        detail_url = response.meta["detail_url"]
        # 详情页面还没有爬，有必要再去爬评论页面
        yield item
