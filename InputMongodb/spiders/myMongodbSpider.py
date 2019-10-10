# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from selenium import webdriver

from selenium.common.exceptions import NoSuchElementException


from InputMongodb.items import InputmongodbItem

class IntoMongodbSpiderSpider(scrapy.Spider):
    name = "IntoMongodbSpider"
    allowed_domains = ["store.steampowered.com"]
    str1 = "https://store.steampowered.com/games#p="
    strNew="https://store.steampowered.com/search/?category1=998&page={}"
    str2 = "&tab=ConcurrentUsers"
    start_urls = []
    for page in range(1,1497):
      start_urls.append(strNew.format(page))

    def parse(self, response):
        gameLinkList = response.xpath('//*[@id="search_resultsRows"]/a')

        for game in gameLinkList:  # 循环所有game的url
        #for i in range(0,1):
            item = InputmongodbItem()
            item['url'] = ""
            item['name'] = ""
            item['price'] = ""
            item['release_date'] = ""
            item['developer'] = ""
            item['publisher'] = ""
            item['summary'] = ""
            item['review'] = ""
            item['image'] = ""
            item['tags'] = ""

            item['comments'] = ""

            detail_url = game.xpath('./@href').extract()[0]
            #detail_url="https://store.steampowered.com/app/299740/Miscreated/"
            price=0
            price = game.xpath('./div[2]/div[4]/div[2]/text()').extract()[0].strip()  # 如果是正常价格
            if not price:  # 看看是否是打折价格
                price = game.xpath('./div[2]/div[4]/div[2]/span/strike/text()').extract()[0].strip()
            item["price"] = price

            try:
                item['url'] = detail_url
                print('游戏地址', item['url'])

               # print()
            except Exception as e:
                print('地址、名称、售价缺失')
                print(e)
                print('detail_url', detail_url)
                #print()
                continue

            # yield item
            detail_request = scrapy.Request(
                url=detail_url,
                callback=self.get_details,
                headers={"Accept-Language": "zh-CN,zh;q=0.9"},
                cookies={'birthtime': '786211201'},
                meta={"item": item, "detail_url": detail_url},
                dont_filter=True,
            )
            yield detail_request

    def get_details(self, response):
        item = response.meta["item"]
        detail_url = response.meta["detail_url"]
        try:
            # release_date单页面没问题
            name=response.xpath('//div[@class="apphub_AppName"]/text()').extract()[0]
            '''  try:
                price=response.xpath('//div[@class="game_purchase_price price"]/text()').extract()[0].strip()
             
            except:
                price = response.xpath('//div[@class="discount_original_price"]/text()').extract()[0].strip()'''

            #price=299
            release_date = response.xpath('//div[@class="release_date"]/div[2]/text()').extract()[0].strip()
            # developer单页面没问题
            # 但我不知道可不可以出现多个开发商
            developer = []
            developer_list = response.xpath('//div[@class="user_reviews"]/div[@class="release_date"]/following-sibling::div[1]/div[2]/a/text()').extract()
            for i in developer_list:
                developer.append(i)
            # publisher单页面没问题
            publisher = []
            publisher_list = response.xpath('//div[@class="user_reviews"]/div[@class="release_date"]/following-sibling::div[2]/div[2]/a/text()').extract()
            for i in publisher_list:
                publisher.append(i)
            # summary单页面没问题
            summary = response.xpath('//div[@class="game_description_snippet"]/text()').extract()[0].strip()
            if not summary:
                summary="No summary now"
            # review单页面没问题
            try:
                review = response.xpath('//span[@class="nonresponsive_hidden responsive_reviewdesc"]/text()').extract()[0].strip()
            except Exception as e:
                review="无用户评测"
            # image单页面没问题
            image = response.xpath('//img[@class="game_header_image_full"]/@src').extract()[0]
            # tags单页面没问题
            tag_name_list = []
            tag_raw_list = response.css(".app_tag::text").extract()

            for tag_raw in tag_raw_list:
                tag_name_list.append(tag_raw.strip())
            item["name"]=name

            item["release_date"] = release_date
            item["developer"] = developer
            item["publisher"] = publisher
            item["summary"] = summary
            item["review"] = review
            item["image"] = image
            # 最后一个标签为'+'，去掉
            item["tags"] = tag_name_list[0:-1]
            print()
        except Exception as e:
            print('日期/生产商/发行商/简介/评论/图片/标签　缺失')
            print(e)
            print()

        # 详情页面还没有爬，有必要再去爬评论页面
        yield item
