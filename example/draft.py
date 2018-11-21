import scrapy
import scrapy.crawler as crawler
from multiprocessing import Process, Queue
from twisted.internet import reactor

class get_description(scrapy.Spider):

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


# the wrapper to make it run more times
def run_spider(company):
    def f(q):
        try:
            runner = crawler.CrawlerRunner()
            deferred = runner.crawl(get_description,company)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            q.put(None)
        except Exception as e:
            q.put(e)

    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
#     result = q.get()
    p.join()

#     if result is not None:
#         raise result


# print('run:')
# run_spider()
# print('run:')
# run_spider()