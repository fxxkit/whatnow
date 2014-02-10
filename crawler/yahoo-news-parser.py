# -*- coding: utf-8 -*-
#! /usr/bin/env python

import urllib2
from bs4 import BeautifulSoup

class y_newsParser():
	def __init__(self):
		self.url = None
		return

	def setURL(self,url):
		self.url = url
		return

	def startFetch(self):
		htmlContent = None
		if self.url is not None:
			htmlContent = urllib2.urlopen(self.url).read()
			result = self.__parser(htmlContent)
			return result
		else:
			return None

	'''
	### Private method for news parser ###
	Fetch : content, time, title, category
	'''
	def __parser(self,content):
		soup = BeautifulSoup(content)

		#DS prototype = {u'content': u'2014-02-09T16:00:00Z', u'itemprop': u'datePublished'}
		date = soup.find(attrs={'itemprop':'datePublished'}).attrs['content']
		title = soup.find(attrs={'itemprop':'headline'}).attrs['content'].encode('utf-8')

		#Extract the main article content
		mainContentList = soup.find(id='mediaarticlebody').find_all('p')
		contentStr = ''
		for eachObj in mainContentList:
			try:
				line = eachObj.string.encode('utf-8')
				#print line.encode('utf-8')
				contentStr += line
			except:
				break

		print 'date: ', date
		print 'title: ',title
		print 'contentStr: ', contentStr
		#print 'soup ', type(soup)
		return 

	def __JSONConvertor(self):
		return

def main():
	url = 'http://tw.news.yahoo.com/%E9%98%BF%E5%9F%BA%E5%B8%AB%E5%88%86%E4%BA%AB%E8%AA%8D%E9%8C%AF%E5%93%B2%E5%AD%B8-160000246.html' # write the url here
	#url = 'http://tw.news.yahoo.com/%E6%89%93%E5%B7%A5%E5%A5%BD%E7%B4%AF-%E7%BE%8E%E5%A5%B3%E5%A4%A7%E7%94%9F%E7%98%8B%E6%89%BE-%E7%94%9C%E5%BF%83%E7%88%B9%E5%9C%B0-%E5%8C%85%E9%A4%8A-044412338.html'
	yParser = y_newsParser()
	yParser.setURL(url)
	yParser.startFetch()

	return

if __name__ == '__main__':
	main()