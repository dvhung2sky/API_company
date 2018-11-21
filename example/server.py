from flask import Flask, request
from flask_restful import Resource, Api
import json
import scrapy
import scrapy.crawler as crawler
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from multiprocessing import Process, Queue
from twisted.internet import reactor


import re
import pickle
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import LabelEncoder
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from keras.models import load_model


from predictor import predict_multi


app = Flask(__name__)
api = Api(app)

APP_PORT = '5008'
GET_RESPONSE_MES = 'Hello my friend !'



DICT_PATH = './extra_prebuilt/corpus.npy'
TFIDF_PATH = './extra_prebuilt/tfidf.pkl'
PREBUILD_MODEL_PATH = './prebuilt_model/mpl.h5'
LABELS_PATH = './extra_prebuilt/classes.npy'

porter = PorterStemmer()
stop = stopwords.words('english')



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
            for i in range(1, 4):                
                result = "".join(response.xpath('//*[@id="ires"]/ol/div[' + str(i) + ']/div/span//text()').extract())
                f.write('{0}. {1}\n'.format(i, result))


# the wrapper to make it run more times
def run_spider(company):
    def f(q):
        try:
            runner = crawler.CrawlerRunner()
            deferred = runner.crawl(get_company,company)
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


class Prediction(Resource):
    def get(self):
        return GET_RESPONSE_MES


    def post(self):
        request_data = request.get_data()
        data_json = json.loads(request_data)
        list_company = data_json["company"]
        list_txt =[]
        for company in list_company:            
            s= company["Name"]
            run_spider(s)       
            with open('company.txt','r') as f:
                txt = f.read()

            list_txt.append(txt)

        industry = predict_multi(list_txt)

        list_industry = []
        for indus in industry:
            list_industry.append({'Industry':indus[0:-4]})


        return {"company_industry": list_industry}


api.add_resource(Prediction, '/prediction')

if __name__ == '__main__':
     app.run(port=APP_PORT)