# from bs4 import BeautifulSoup
# import urllib3
#
#
# def run():
# 	url = "https://www.google.com/search?q=curly+hairs&source=lnms&tbm=isch"
# 	# content = urllib3.urlopen(url).read()
# 	import urllib3
#
# 	# url = 'http://urllib3.readthedocs.org/'
# 	http_pool = urllib3.connection_from_url(url)
# 	r = http_pool.urlopen('GET', url)
#
# 	# print(r.data)
# 	soup = BeautifulSoup(r.data,features="html.parser")
# 	for link in soup.find_all('img'):
# 		print(link.get('class'))
# 	# print(content)
#
# run()

