from flask import Flask, request
from flask_restful import Resource, Api
import json

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


s = 'adfad'

process = CrawlerProcess(get_project_settings())
process.crawl('description',s)
process.start()
