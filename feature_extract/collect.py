#!/bin/python
import BeautifulSoup
import urllib
import sys

if len(sys.argv) < 2:
        print("Please input the repository's URL")
else:
	repo = sys.argv[1]
	urllib.urlretrieve(repo + "index.xml", "index.xml")
	f = open('index.xml', 'r')
	t = f.read()
	f.close()
	soup = BeautifulSoup.BeautifulSoup(t)
	x = soup.findAll('apkname')
	apps =  map(lambda x: x.findAll(text=True)[0], x)
	
	i = 1
	for app in apps:
		print(app + " " + str(i) + "/" + str(len(apps)))
		urllib.urlretrieve (repo + app, app)
		i += 1
