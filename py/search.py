import urlparse
import requests
from bing_search_api import BingSearchAPI 
import codecs
import lxml.html

#definitions and declarations.

my_key = "lijZiS7uFCLkkj8wKJ3EqwDC9sZzk/Qm3e7j5fosTh8="
#safebrowsing keys
keys=["ABQIAAAAa9ySd1q2lVZ1i6YIbbBsmRQMBcUpG57DaV2QrXMD7lvATY1OOA", "ABQIAAAAIK_XOS9WwzZndzj7983ENxRsRnAzCcE57y43-GwaNHKyNjL5jg", "ABQIAAAA_I2izgfxGlryfYwIYS70BRT8pqafTW6P1gbCnH6IroX5vaHj9Q", "ABQIAAAAM30iSdq9L0RaY09v-I3v-BRQLLLh9yXUsM_l0tCicoEmuqxaPA", "ABQIAAAA_sNdKf1_e-MEkpldPtBaVRTbnk67_GT0JJy109c0XKua5PQfkQ", "ABQIAAAAtDUdZrhDe7q6u9-VluKVKhTpSiylglYA4QImwO8UrkxN4l0E2w", "ABQIAAAAGb6WoNSUhxdLbDMS3NFOUBQv6N1BCev7kRN9dA_We0l968p_lg", "ABQIAAAAAiiIKkKiMJy8RYSj7fwJARRKoDf9zZKOWopZE-Ci8oJDJ7H27Q", "ABQIAAAA9sWbFwniL2ugge2OAY6h8RS_yXU4MELPsAj_AhrxQYBzqwWl4Q", "ABQIAAAAS2Pro4qHrOPRqjGd-qpeXRR0-ViiOQegzz-T4DV8ptJNFC_5EA"]

#customsearch keys
custom_keys=["AIzaSyBoDOnPuj88KvEMLvA8B4iTiwkC7BiIaXI", "AIzaSyDmK23bkt9sjyVOaniQZDfVlTreKHkaSTY","AIzaSyCfqoEWCqB7_MIqCF0eGKX6lbALUFqbnCE", "AIzaSyB7gUgM7ooGX8js06rugugJb9ZjNAUQZRI"]
crawled_links=open("crawled_links",'a')

#bing search keys
bing_keys=["5HK7cliwLpZfbXedOpOMmB5je9j75olGADVNX82zLTI=", "xaGM3hcKEWMx00/z9tB71zIDIuvtr/hkYEMP5oNr6G0=", "SvIQ3+T2nf6G3zmGp4FUSvOSPbFcD50nccyNOHnyhrU=", "eZ30y35Yb9dCvB1Og9uBNG71UuqlS6AEwCDpW6zXnhQ=", "a2tmb4ICANZf7WTCh4qPJa4F9XrNB41tq0zu53ai2v8=", "xihmWXBodlfGQ4h9ID/ndFM/W9m1/f3KyJq2vxnvPO4=", "ohDHagAb7Xi3Kt0GB+mvH64Yv7fXKdxLkpMU8gHJh1c="]

raw_search_results=[] #raw search results

edited_links=[]
websites_list=[]
search_results_from_file=[]

def generate_domain_chart(filename):
  domain_hash = {}
  links = tuple(open(filename, "r"))
  for link in links:
    lastindex = link.rindex('.')
    last = len(link)
    domain = link[lastindex:last-1]
    if domain not in domain_hash:
      domain_hash[domain] = 0
    domain_hash[domain] = domain_hash[domain] + 1
  domain_chart=open("domain_chart", "w")
  for domain in domain_hash:
   print "%s %s" %(domain, domain_hash[domain])
   domain_chart.write("%s %s\n" %(domain, domain_hash[domain]))


def download_raw_results(infile, outfile):
  skip = 0
  params = {'ImageFilters':'"Face:Face"','$format': 'json','$top': 50,'$skip': skip}
  lines = tuple(open(infile, 'r'))
  search_results=open(outfile,'w+')
  i = 1
  for line in lines:
    bing = BingSearchAPI(bing_keys[i])
    i = i + 1
    if ( i == 7):
      i = 0
    print line
    r = bing.search("web",line,params)
    if r.status_code == 200:
    #print r
      raw_search_results.append(r.json)
    #print("Appended an Entry!!!!!!!!")
    #res.append(bing.search("web",line,params))
  
  for result in raw_search_results:
    for elem in result['d']['results'][0]['Web']:
      websites_list.append(elem['DisplayUrl'])
  #Extract the links, and write to file so we don't have
  for link in websites_list:
    search_results.write("%s\n" % link.encode('utf-8'))

#Process websites list
def process_links(infile, outfile):
  output = open(outfile,'wr')
  search_results_from_file = tuple(open(infile,'r'))
  for site in search_results_from_file:
    print site
    site = site.decode('utf-8')
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

def check_safe_url(infile, outfile):

  malware_links=open(outfile, "w")
  edited_links = tuple(open(infile,'r'))
  i=0
  for site in edited_links:  
    
    payload = {'apikey':keys[i],'pver':'3.0','appver':'1.0','url':site}
    r = requests.get("https://sb-ssl.google.com/safebrowsing/api/lookup?client=api",params=payload)
    if r.text == "":
      continue
    malware_links.write("%s" % (site))
    print "%s: %s" % (r.text,site)
    i = i + 1
    if i == 9:
      i=0
  """payload = {'apikey':'ABQIAAAAIK_XOS9WwzZndzj7983ENxRsRnAzCcE57y43-GwaNHKyNjL5jg','pver':'3.0','appver':'1.0','url':'admincareers.com'}
  r = requests.get("https://sb-ssl.google.com/safebrowsing/api/lookup?client=api",params=payload)
  print "%s: %s" % (r.text,'n')"""


def get_in_url(input_links,outputfilename):
  in_url_file = open(outputfilename,'w')
  i = 0
  for link in input_links:
    query = '%s%s' % ("link:",link)
    payload = {'key':custom_keys[i],'cx':'002451276590484194388:tlniujq1r_k','q':query,'alt':'json'}
    r = requests.get('https://www.googleapis.com/customsearch/v1?',params=payload)
    result_links=[]
    items = r.json['items'] if 'items' in r.json else None
    i = i + 1
    print link
    if items:
      for item in items:
        result_links.append(item['link'])
      for link in result_links: 
        in_url_file.write("%s\n" % (link))
    if i == 4:
      i = 0

def extractMiddleWord(filename):
  pair_name = tuple(open(filename, "r"))
  out_file = open("pornkeys", "w")
  for name in pair_name:
    sp1 = name.index('\t')
    sp2 = name.rindex('\t')
    name1 = name[sp1:sp2]
    out_file.write("%s\n" %(name1))
 

def spiltDash(filename):
  pair_name = tuple(open(filename, "r"))
  out_file = open("celebrity_list", "w")
  for name in pair_name:
    dashindex = name.find('-')
    name1 = name[0:dashindex]
    out_file.write("%s\n" %(name1))
 
  

def yahoo_extract_bad(depth,link, link_hash):

  if (depth > 15):
    return
  query = "http://www.google.com/safebrowsing/diagnostic?site=%s" % (link)
#  print query
  parser = lxml.html.parse(query)
  hrefs = parser.xpath("//a/@href")
#  print hrefs
  for alink in hrefs:
    index = alink.find('site=')
    if(index is not -1):
      if(alink[index+5:][0] is not 'A'):
        parsed_link = alink[index+5:]
        if (parsed_link not in link_hash): 
          crawled_links.write("%s\n" % (parsed_link))
          link_hash[parsed_link] = True
          print ("%s\n" % (parsed_link))
          yahoo_extract_bad(depth+1, parsed_link, link_hash)

  
  """ print "Length Greater than 1"
    links = r.json['query']['results']['body']['center']['div'][0]['div']['blockquote'][3]['p']['a'] 
    print "Links Extracted"
    for link in links:
      crawled_links.write("%s\n" % (link['content']))
      print ("%s\n" % (link['content']))
      #yahoo_extract_bad(depth+1,link['content'])  
  
  return
  """
def main():
#  spiltDash("celebrities")
#  extractMiddleWord("porn_keywords")
  #iownload_raw_results()
  #process_links()
  #generate_domain_chart("malware_links")
  #check_safe_url("properinlinks")
  #input_links=["cs.stonybrook.edu"]
  #get_in_url(input_links)
#  download_raw_results("list1", "links1")
  #process_links("links_insecure_keywords", "processed_malware_links")
  #process_links("links_gray", "processed_gray_links")
  #process_links(infile, outfile):

 # download_raw_results("celebrity_list", "links_celebrity")
#  download_raw_results("pornkeys", "links_porn")
#  download_raw_results("grayKeyWords_mal", "links_gray")
#  download_raw_results("insecureKeyWords_mal", "links_insecure_keywords")
  check_safe_url("processed_malware_links", "insecure_malware")
  check_safe_url("processed_gray_links", "gray_malware")
  """
  file_name = "malware_links1"
  with open(file_name) as f:
    content = f.readlines()
  
  get_in_url(content, "malware_inlinks")
  """
  #get_in_url(content,"in_url_links")
  #check_safe_url("in_url_links")
  #ink_hash = {}
  #ahoo_extract_bad(0,"movie2k.to", link_hash)


main()

