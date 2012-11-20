union_file=open("union_insecure", "w")
def main():
  link_hash = {}
  file_one=tuple(open("crawled_links", "r"))
  file_two=tuple(open("crawled_links2", "r"))
  for site in file_one:
    if site not in link_hash:
      link_hash[site]=True
  for site in file_two:
    if site not in link_hash:
      link_hash[site]=True
  for link in link_hash:
    union_file.write("%s" % (link))

main()

