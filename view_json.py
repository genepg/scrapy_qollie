import requests
import json
from bs4 import BeautifulSoup

url = 'https://www.qollie.com/graphql'

payloads={
    "query":"\n\nfragment commonFields on Comment {\n  _id\n  status\n  checked\n  kind\n  content\n  anonymous\n  likes\n  dislikes\n  judge\n  createdAt\n  category\n  pros\n  cons\n  shareType\n  isSysDelete\n  replies {\n    _id\n  }\n  author {\n    _id\n    nickname\n    picture\n    showComments\n    showAvatar\n  }\n}\n\n\nfragment jobCommentFields on JobComment {\n  job {\n    _id\n    jobTitle\n    company {\n      _id\n      name\n      jobs {\n        _id\n        jobTitle\n      }\n    }\n    sourcesLinks\n  }\n}\n\n\nfragment companyCommentFields on CompanyComment{\n  company {\n    _id\n    name\n    taxId\n    introduction\n    webSite\n    sourcesLinks\n    jobs {\n      _id\n      jobTitle\n    }\n  }\n}\n\n\nquery search(\n  $kind: String\n  $companyId: ID\n  $jobId: ID\n  $keyword: String\n  $page: Int\n  $limit: Int\n) {\n  searchComments(query: {\n    kind: $kind\n    companyId: $companyId\n    jobId: $jobId\n    keyword: $keyword\n    page: $page\n    limit: $limit\n  }) {\n    ... commonFields\n    ... jobCommentFields\n    ... companyCommentFields\n  }\n}\n\n",
    "variables":{"jobId":"5860df1b8dc5ef00750b25cc","page":1,"limit":10}
}

res = requests.post(url,  data = json.dumps(payloads), headers= {'Content-Type': 'application/json'})
parse=json.loads(res.text)
# print (parse)
print (json.dumps(parse, indent=4, sort_keys=True, ensure_ascii=False))
# parse1 = json.dumps(parse, indent=4, sort_keys=True)
# print(json.loads(parse1))
for job in parse['data']['searchComments']:
    print(job['job']['jobTitle'])
    print(job['job']['company']['name'])

    

# payloads={
#     "query":"\n\nfragment commonFields on Comment {\n  _id\n  status\n  checked\n  kind\n  content\n  anonymous\n  likes\n  dislikes\n  judge\n  createdAt\n  category\n  pros\n  cons\n  shareType\n  isSysDelete\n  replies {\n    _id\n  }\n  author {\n    _id\n    nickname\n    picture\n    showComments\n    showAvatar\n  }\n}\n\n\nfragment jobCommentFields on JobComment {\n  job {\n    _id\n    jobTitle\n    company {\n      _id\n      name\n      jobs {\n        _id\n        jobTitle\n      }\n    }\n    sourcesLinks\n  }\n}\n\n\nfragment companyCommentFields on CompanyComment{\n  company {\n    _id\n    name\n    taxId\n    introduction\n    webSite\n    sourcesLinks\n    jobs {\n      _id\n      jobTitle\n    }\n  }\n}\n\n\nquery search(\n  $kind: String\n  $companyId: ID\n  $jobId: ID\n  $keyword: String\n  $page: Int\n  $limit: Int\n) {\n  searchComments(query: {\n    kind: $kind\n    companyId: $companyId\n    jobId: $jobId\n    keyword: $keyword\n    page: $page\n    limit: $limit\n  }) {\n    ... commonFields\n    ... jobCommentFields\n    ... companyCommentFields\n  }\n}\n\n",
#     "variables":{"companyId":"58b1d34ef39d14a4d8845148","page":1,"limit":10}
# }

# res = requests.post(url,  data = json.dumps(payloads), headers= {'Content-Type': 'application/json'})
# parse=json.loads(res.text)
# print (json.dumps(parse, indent=4, sort_keys=True, ensure_ascii=False))

# print(job['company']['name'])

# jsondata = parse['data']['searchCompanies'][0]
# print(len(jsondata['jobs']))

# try:
#     for k in range(0,1):
#         print(k)
#     print(len(jsondata['jobs']))
#     # print(jsondata['jobs'][0])
# except IndexError:
#     print("out of rangeeeeeeeeee")

# for i in range(0,len(jsondata['jobs'])):

#     print(jsondata['jobs'][i])
