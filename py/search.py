import urlparse
import requests
from bing_search_api import BingSearchAPI 
import codecs
#definitions and declarations.

my_key = "lijZiS7uFCLkkj8wKJ3EqwDC9sZzk/Qm3e7j5fosTh8="
bing = BingSearchAPI(my_key)
params = {'ImageFilters':'"Face:Face"','$format': 'json','$top': 200,'$skip': 0}
lines = tuple(open("trending", 'r'))


crawled_links=open("crawled_links",'a')

raw_search_results=[] #raw search results

edited_links=[]
websites_list=[]
search_results_from_file=[]

def download_raw_results():
  search_results=open("searchresults",'w+')
  
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
    search_results.write("%s\n" % link.encode('utf-8'))

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

def check_safe_url(filename):

  edited_links = tuple(open(filename,'r'))
  for site in edited_links:  
    payload = {'apikey':'ABQIAAAAIK_XOS9WwzZndzj7983ENxRsRnAzCcE57y43-GwaNHKyNjL5jg','pver':'3.0','appver':'1.0','url':site}
    r = requests.get("https://sb-ssl.google.com/safebrowsing/api/lookup?client=api",params=payload)
    if r.text == "":
      continue
    print "%s: %s" % (r.text,site)

  """payload = {'apikey':'ABQIAAAAIK_XOS9WwzZndzj7983ENxRsRnAzCcE57y43-GwaNHKyNjL5jg','pver':'3.0','appver':'1.0','url':'admincareers.com'}
  r = requests.get("https://sb-ssl.google.com/safebrowsing/api/lookup?client=api",params=payload)
  print "%s: %s" % (r.text,'n')"""


def get_in_url(input_links,outputfilename):
  in_url_file = open(outputfilename,'w')

  for link in input_links:
    query = '%s%s' % ("link:",link)
    payload = {'key':'AIzaSyCfqoEWCqB7_MIqCF0eGKX6lbALUFqbnCE','cx':'002451276590484194388:tlniujq1r_k','q':query,'alt':'json'}
    r = requests.get('https://www.googleapis.com/customsearch/v1?',params=payload)
    result_links=[]
    items = r.json['items'] if 'items' in r.json else None

    print link
    if items:
      for item in items:
        result_links.append(item['link'])
      for link in result_links: 
        in_url_file.write("%s\n" % (link))


def yahoo_extract_bad(depth,link):

  if (depth > 10):
    return
  
  
  query = 'select * from html where url="www.google.com/safebrowsing/diagnostic?site=%s"' % (link) 
  print query


  params= {'q':query,'format':'json','diagnostics':'true'}
  
  print params

  r = requests.get("http://query.yahooapis.com/v1/public/yql?",params=params)

  """if r.json['query']:
    if r.json['query']['results']:
      if r.json['query']['results']['body']:
        if r.json['query']['results']['body']['center']:
          if r.json['query']['results']['body']['center']['div']:
            if r.json['query']['results']['body']['center']['div']['blockquote']:
                if r.json['query']['results']['body']['center']['div']['blockquote'][3]:
                  if r.json['query']['results']['body']['center']['div']['blockquote'][3]['p']:
                    if r.json['query']['results']['body']['center']['div']['blockquote'][3]['p']['a']:
   """


  json_len = len(r.json['query']['results']['body']['center']['div'][0]['div']['blockquote'][3])

  print json_len
  """
    print "Length Greater than 1"
    links = r.json['query']['results']['body']['center']['div'][0]['div']['blockquote'][3]['p']['a'] 
    print "Links Extracted"
    for link in links:
      crawled_links.write("%s\n" % (link['content']))
      print ("%s\n" % (link['content']))
      #yahoo_extract_bad(depth+1,link['content'])  
  
  return
  """
def main():
  #download_raw_results()
  #process_links()
  
  #check_safe_url()
  #input_links=["cs.stonybrook.edu"]
  #get_in_url(input_links)
  """
  file_name = "insecure"
  with open(file_name) as f:
    content = f.readlines()
  """
  #get_in_url(content,"in_url_links")
  #check_safe_url("in_url_links")

  yahoo_extract_bad(0,"diesel-stores.com")


main()

