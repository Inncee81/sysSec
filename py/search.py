import requests
from bing_search_api import BingSearchAPI 

my_key = "lijZiS7uFCLkkj8wKJ3EqwDC9sZzk/Qm3e7j5fosTh8="
bing = BingSearchAPI(my_key)
params = {'ImageFilters':'"Face:Face"','$format': 'json','$top': 10,'$skip': 0}


output=open("searchresults",'wr')

lines = tuple(open("trending", 'r'))

res=[]

for line in lines:
  r = bing.search("web",line,params)
  #print r
  res.append(r)
  #print("Appended an Entry!!!!!!!!")
  #res.append(bing.search("web",line,params))

websites_list=[]

for result in res:
  for elem in result['d']['results'][0]['Web']:
    websites_list.append(elem['DisplayUrl'])

for site in websites_list:
  output.write("%s\n" % site)

#print websites_list









