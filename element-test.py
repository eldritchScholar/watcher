import re, urllib, sys

site = sys.argv[1]
element = sys.argv[2]

n = urllib.urlopen(site)
page = n.read()
result = re.search(element, page, re.DOTALL)
print result.group(1)


