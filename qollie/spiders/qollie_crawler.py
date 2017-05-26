# -*- coding: utf-8 -*-
import scrapy
import json
import re
from bs4 import BeautifulSoup
from qollie.items import RateItem, CommentItem, JobItem

class qollie(scrapy.Spider):
	name = "qollie"

	# search and get the link form qollie
	def start_requests(self):
		print("=============================================================================================")

		# with open('/Users/pg/Desktop/illegal.txt', 'r') as f:
		# 	company = [line.strip() for line in f]
			

		# company = ['資誠聯合會計師事務所','台積電','永采烘培坊惠文營業所','東立出版社有限公司','國泰金控_國泰金融控股股份有限公司']
		company = ['聯發科']

		pattern = re.compile(r'\w+')

		for x in range(0,len(company)):
			string = str(company[x])
			match = re.search(pattern, string)
			company[x]=match.group()

			company_json = {
				"keyword":str(company[x]),"page":1,"limit":10
			}
			payload_search = {
				"query":"\n  \nfragment commonFields on Company {\n  _id\n  name\n  category\n  webSite\n  introduction\n  sourcesLinks\n  createdAt\n  comments\n  jobs {\n    _id\n    jobTitle\n  }\n}\n\n  query search(\n    $keyword: String\n    $page: Int\n    $limit: Int\n  ) {\n    searchCompanies(query: {\n      name: $keyword\n      limit: $limit\n      page: $page\n    }) {\n      ... commonFields\n    }\n  }\n  "
				,"variables":{"keyword":str(company[x]),"page":1,"limit":10}
			}
			url = 'https://www.qollie.com/graphql'
			yield scrapy.Request( url, method='POST', body=json.dumps(payload_search), headers={'Content-Type':'application/json'}, callback=self.parse)

	def parse(self, response):

		print("=============================================================================================")

		url = 'https://www.qollie.com/graphql'

		res = BeautifulSoup(response.text,'lxml')
		# print(res)
		jsondata_search = json.loads(res.text, encoding="utf-8")

		jsondata_search = jsondata_search['data']
		for item in jsondata_search['searchCompanies']:

			print(item['name'])
			print(item['_id'])

			# Company Rate
			url_rate = 'https://www.qollie.com/companies/'+item['_id']
			yield scrapy.Request(url_rate,method='GET', callback=self.parse_rate)

			# Company Comment
			payload_comment = {
				"query":"\n\nfragment commonFields on Comment {\n  _id\n  status\n  checked\n  kind\n  content\n  anonymous\n  likes\n  dislikes\n  judge\n  createdAt\n  category\n  pros\n  cons\n  shareType\n  isSysDelete\n  replies {\n    _id\n  }\n  author {\n    _id\n    nickname\n    picture\n    showComments\n    showAvatar\n  }\n}\n\n\nfragment jobCommentFields on JobComment {\n  job {\n    _id\n    jobTitle\n    company {\n      _id\n      name\n      jobs {\n        _id\n        jobTitle\n      }\n    }\n    sourcesLinks\n  }\n}\n\n\nfragment companyCommentFields on CompanyComment{\n  company {\n    _id\n    name\n    taxId\n    introduction\n    webSite\n    sourcesLinks\n    jobs {\n      _id\n      jobTitle\n    }\n  }\n}\n\n\nquery search(\n  $kind: String\n  $companyId: ID\n  $jobId: ID\n  $keyword: String\n  $page: Int\n  $limit: Int\n) {\n  searchComments(query: {\n    kind: $kind\n    companyId: $companyId\n    jobId: $jobId\n    keyword: $keyword\n    page: $page\n    limit: $limit\n  }) {\n    ... commonFields\n    ... jobCommentFields\n    ... companyCommentFields\n  }\n}\n\n",
				"variables":{"companyId":item['_id'],"page":1,"limit":10}
			}
			yield scrapy.Request(url,method='POST', body=json.dumps(payload_comment), headers={'Content-Type':'application/json'}, callback=self.parse_comment)

			# Jobs Comment
			if len(item['jobs'])!=0:
				for k in range(0,len(item['jobs'])):
					print(item['jobs'][k]['_id'])
			
					payload_job_comment = {
						"query":"\n\nfragment commonFields on Comment {\n  _id\n  status\n  checked\n  kind\n  content\n  anonymous\n  likes\n  dislikes\n  judge\n  createdAt\n  category\n  pros\n  cons\n  shareType\n  isSysDelete\n  replies {\n    _id\n  }\n  author {\n    _id\n    nickname\n    picture\n    showComments\n    showAvatar\n  }\n}\n\n\nfragment jobCommentFields on JobComment {\n  job {\n    _id\n    jobTitle\n    company {\n      _id\n      name\n      jobs {\n        _id\n        jobTitle\n      }\n    }\n    sourcesLinks\n  }\n}\n\n\nfragment companyCommentFields on CompanyComment{\n  company {\n    _id\n    name\n    taxId\n    introduction\n    webSite\n    sourcesLinks\n    jobs {\n      _id\n      jobTitle\n    }\n  }\n}\n\n\nquery search(\n  $kind: String\n  $companyId: ID\n  $jobId: ID\n  $keyword: String\n  $page: Int\n  $limit: Int\n) {\n  searchComments(query: {\n    kind: $kind\n    companyId: $companyId\n    jobId: $jobId\n    keyword: $keyword\n    page: $page\n    limit: $limit\n  }) {\n    ... commonFields\n    ... jobCommentFields\n    ... companyCommentFields\n  }\n}\n\n",
						"variables":{"jobId":str(item['jobs'][k]['_id']),"page":1,"limit":10}
					}
					yield scrapy.Request(url, method='POST',body=json.dumps(payload_job_comment), headers={'Content-Type':'application/json'}, callback=self.parse_job)
			else:
				print("no jobs")

	def parse_rate(self,response):
		print("========================================= Evaluation ============================================================")
		res = BeautifulSoup(response.text,'lxml')
		# print(res.select('svg g g'))
		# print(res.select('h1')[0].text)
		# for rate in res.select('svg g g'):
		# print(rate.select('text')[0].text)
		# print(res.select('svg g g text')[0].text)
		rate = res.select('svg g g text')
		# print(rate[0].text)

		# item=RateItem()
		# item['company'] = res.select('h1')[0].text

		for x in range(0,3):

			pattern = re.compile(r'\d+[.]\d+')
			match = re.search(pattern,rate[x].text)

			if match != None:
				if x==0:
					# item['good'] = float(match.group())
					print(match.group())
				elif x==1:
					# item['normal'] = float(match.group())
					print(match.group())
				else:
					# item['bad'] = float(match.group())
					print(match.group())
			else:
				pattern = re.compile(r'\d+')
				match = re.search(pattern,rate[x].text)

				if x==0:
					# item['good'] = float(match.group())
					print(match.group())
				elif x==1:
					# item['normal'] = float(match.group())
					print(match.group())
				else:
					# item['bad'] = float(match.group())
					print(match.group())
		# yield item

	def parse_comment(self, response):
		print("====================================== Company Comment ==========================================================")

		res = BeautifulSoup(response.text,'lxml')

		# print(res)
		jsondata = json.loads(res.text, encoding="utf-8")
		jsondata = jsondata['data']

		# print(jsondata['searchComments'])
		for comment in jsondata['searchComments']:
			print("id: "+comment['_id'])
			print("judge: "+comment['judge'])
			print("category: "+comment['category'])
			print("adventage: "+ str(comment['cons']) +"\n" + "disadventage: " + str(comment['pros'])+ "\n" + "content: "+ str(comment['content']))
			# item = CommentItem()

			# item['company'] = comment['company']['name']
			# item['category']=str(comment['category'])
			# item['value'] = str(comment['judge'])
			# item['main_context']= "優點:" + str(comment['pros']) + "缺點:" + str(comment['cons'])+ "內容:" + str(comment['content'])

			# yield item
			
	def parse_job(self, response):
		print("====================================== Jobs Comment ==========================================================")

		res = BeautifulSoup(response.text,'lxml')

		jsondata = json.loads(res.text, encoding="utf-8")
		jsondata = jsondata['data']

		# print(jsondata['searchComments'])
		for comment in jsondata['searchComments']:
			print(comment['job']['company']['name'])
			print(comment['job']['jobTitle'])
			print(comment['category'])
			print(comment['judge'])
			print("優點:" +str(comment['cons']) +"\n" + "缺點: " + str(comment['pros'])+ "\n" + "content: "+ str(comment['content']))

			# item = JobItem()
			# item['company']=comment['job']['company']['name']
			# item['job'] = comment['job']['jobTitle']
			# item['category']=comment['category']
			# item['value'] = comment['judge']
			# item['main_context'] = "優點:" +str(comment['cons']) +"\n" + "缺點: " + str(comment['pros'])+ "\n" + "content: "+ str(comment['content'])

			# yield item




