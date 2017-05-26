# -*- coding: utf-8 -*-
import scrapy 
from bs4 import BeautifulSoup

class GetCompany(scrapy.Spider):
    name="get"
    print("start----------------------------------------------------")

    def start_requests(self):
        for i in range(2,10):
            print(i)
            url = 'https://www.104.com.tw/cust/list/index/?page=1&order=4&mode=l&jobsource=checkc&cpt='+ str(i)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        res = BeautifulSoup(response.body,'lxml')

        with open('/Users/pg/Desktop/all_company.txt','a') as f:
            
            for company in res.select('tbody tr td.ls-name'):
                print(company.select('a')[0].text)
                f.write(company.select('a')[0].text + "\n")

                next_page = response.css('div.page-ctrl > a.page-next ::attr(href)').extract_first()
            if next_page:
                yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

