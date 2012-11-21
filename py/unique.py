def unique(infile, outfile):
  inputrecords = tuple(open(infile, 'r'))
  outhandle = open(outfile, 'w')
  dict = {}
  for link in inputrecords:
    if link not in dict:
      dict[link] = True
  
  for link in dict:
    outhandle.write("%s" %(link))

def main():
  unique("newdata/union_gray", "newdata/gray_malware")
  unique("newdata/union_insecure", "newdata/insecure_malware")

main()
