import urllib.request

import re
import os

src = urllib.request.urlopen('http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing=2284')
nexturl = None

url = 'http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing='

count = 0

while True:
	nexturl = src.readline()
	nextid = nexturl[-5:];count=count+1
	try:
		nextid = int(nextid)
	except:
		break
		
	nexturl = url+str(nextid)
	print(count,'next url -->'+nexturl)
	src.close()
	src = urllib.request.urlopen(nexturl)
