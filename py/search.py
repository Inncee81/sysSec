import urlparse
import requests
from bing_search_api import BingSearchAPI 

#definitions and declarations.

my_key = ""
bing = BingSearchAPI(my_key)
params = {'ImageFilters':'"Face:Face"','$format': 'json','$top': 10,'$skip': 0}
lines = tuple(open("trending", 'r'))

raw_search_results=[] #raw search results

edited_links=[]
websites_list=[]
search_results_from_file=[]

def download_raw_results():
  search_results=open("searchresults",'wr')
  
  for line in lines:
    r = bing.search("web",line,params)
    #print r
    raw_search_results.append(r)
    #print("Appended an Entry!!!!!!!!")
    #res.append(bing.search("web",line,params))
  for result in raw_search_results:
    for elem in result['d']['results'][0]['Web']:
      websites_list.append(elem['DisplayUrl'])
  #Extract the links, and write to file so we don't have
  for link in websites_list:
    search_results.write("%s\n" % link)

#Process websites list
def process_links():
  output = open("output",'wr')
  search_results_from_file = tuple(open("searchresults",'r'))
  for site in search_results_from_file:
    if not site.startswith('https') and not site.startswith(unicode('https')) and not site.startswith(unicode('http')) and not site.startswith('http'): 
      if not site.startswith('www'):
        site = "%s%s" % ('http://www.',site) 
        edited_links.append(site)
        #print "Doesn't start with http://wwww"
        #print "site %s" % (site)
        continue

      if site.startswith('www'):
        #print "Starts with www : %s" % (site)
        site = "%s%s" % ('http://',site)
        edited_links.append(site)
        continue

  for site in edited_links:
    p = urlparse.urlparse(site)
    output.write("%s\n" % p.netloc)

def check_safe_url():

  edited_links = tuple(open("output",'r'))
  for site in edited_links:  
    payload = {'apikey':'ABQIAAAAIK_XOS9WwzZndzj7983ENxRsRnAzCcE57y43-GwaNHKyNjL5jg','pver':'3.0','appver':'1.0','url':site}
    r = requests.get("https://sb-ssl.google.com/safebrowsing/api/lookup?client=api",params=payload)
    if r.text == "":
      continue
    print "%s: %s" % (r.text,site)

def main():
  #download_raw_results()
  #process_links()
  check_safe_url()
main()

