
class transCookie:
    def __init__(self, cookie):
        self.cookie = cookie

    def stringToDict(self):
        '''
        将从浏览器上Copy来的cookie字符串转化为Scrapy能使用的Dict
        :return:
        '''
        itemDict = {}
        items = self.cookie.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            itemDict[key] = value
        return itemDict

if __name__ == "__main__":
    cookie = "wants_mature_content=1; browserid=1345912399984599383; timezoneOffset=28800,0; _ga=GA1.2.1624844504.1545375155; _gid=GA1.2.1549866948.1570560932; lastagecheckage=1-0-1995; steamCountry=CN%7Cf8f8a95a01392e389bc76225d697121f; sessionid=bc1f5589328e9d60ff34ce2a; app_impressions=10:80@1_5_9__412|300@1_5_9__412|20@1_5_9__412|30@1_5_9__412|40@1_5_9__412|50@1_5_9__412|60@1_5_9__412|70@1_5_9__412|130@1_5_9__412|517630@1_7_15__13|748360@1_7_15__13|446560@1_7_15__13|531510@1_7_15__13|225540@1_7_15__13|8190@1_7_15__13|6880@1_7_15__13|517630@1_7_15__13|748360@1_7_15__13|446560@1_7_15__13|531510@1_7_15__13|225540@1_7_15__13; birthtime=786211201; recentapps=%7B%22225540%22%3A1570609341%2C%22570%22%3A1570609264%2C%22602520%22%3A1570561131%2C%22812140%22%3A1570283705%2C%221083210%22%3A1570282311%2C%2247890%22%3A1570281777%2C%221121560%22%3A1570028505%2C%22750920%22%3A1569297239%2C%22252490%22%3A1569291429%2C%22431960%22%3A1564849524%7D; _gat_app=1"
    trans = transCookie(cookie)
    print(trans.stringToDict())