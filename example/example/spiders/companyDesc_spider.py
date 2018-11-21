import scrapy
import requests
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class get_company(scrapy.Spider):

    def __init__(self,company):
        self.company = company

    def start_requests(self):
        item = self.company.replace(' ','+')
        url = 'https://www.google.com/search?q=' + item + '+company+description'
        req = scrapy.Request(url, callback=self.parse_description, meta={'company': item})
        yield req

    def parse_description(self, response):

        item = response.meta.get('company')
        with open('company.txt', 'w') as f:
            f.write("{}\n".format(item))
            for i in range(1, 4):                
                result = "".join(response.xpath('//*[@id="ires"]/ol/div[' + str(i) + ']/div/span//text()').extract())
                f.write('{0}. {1}\n'.format(i, result))
