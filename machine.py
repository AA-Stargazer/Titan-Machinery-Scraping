import scrapy
from scrapy.shell import inspect_response
import logging
import time


from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC

from scrapy.selector import Selector 

class MachineSpider(scrapy.Spider):
    name = 'machine'
    allowed_domains = ['www.titanmachinery.com']

    def start_requests(self):
        a_urls = [f'https://www.titanmachinery.com/equipment/used-equipment/?Condition=Used&Industries=AGRICULTURE&p={i + 1}' for i in range(68)]
        for url in a_urls:
            yield SeleniumRequest(
                url=url,
                wait_time=3,
                screenshot=False,
                callback=self._parse
            )
    
    def _parse(self, response):
        driver = response.meta['driver']
        text = driver.page_source
        driver.quit()
        response = Selector(text=text)
        cards = response.xpath('//div[@class="search-results"]/span/div/div')
        for card in cards:
            yield {
                'category': card.xpath('.//p[@class="card-equipment-category"]/span/text()').get(),
                'name': card.xpath('.//h2/text()').get(),
                'model': card.xpath('.//div/span[@class="specs-label" and text()="Model: "]/following-sibling::span/text()').get(),
                'contidition': card.xpath('.//span[@class="label label-danger text-uppercase"]/text()').get().replace('\n', '').strip(),
                'price': card.xpath('.//p[@class="card-equipment-price"]/span/text()').get(),
                'stock': card.xpath('.//div/span[@class="specs-label" and text()="Stock: "]/following-sibling::span/text()').get()
        }