# -*- coding: utf-8 -*-
#! /usr/bin/env python

import urllib2, json
from bs4 import BeautifulSoup

class y_newsParser():
	def __init__(self):
		self.url = None
		return

	'''
	### set a single url or a list of urls ###
	'''
	def setURL(self,url):
		self.url = url
		return

	def startFetch(self):
		htmlContent = None
		if self.url is not None:
			if type(self.url) is str:
				htmlContent = urllib2.urlopen(self.url).read()
				result = self.__parser(htmlContent)
				self.url = None #initialize the url parameter
				return json.dumps(result)
			elif type(self.url) is list:
				resultList = []
				for url in self.url:
					htmlContent = urllib2.urlopen(url).read()
					result = self.__parser(htmlContent)
					resultList.append(result)	
				self.url = None #initialize the url parameter
				return json.dumps(resultList)		
		else:
			print 'Please use "setURL" method to set url first'
			return None

	'''
	### Private method for news parser ###
	Fetch : content, time, title, category
	'''
	def __parser(self,content):
		soup = BeautifulSoup(content)

		#Extract date
		#DS prototype = {u'content': u'2014-02-09T16:00:00Z', u'itemprop': u'datePublished'}
		date = soup.find(attrs={'itemprop':'datePublished'}).attrs['content']
		date = date.split('T')[0]

		#Extract title
		title = soup.find(attrs={'itemprop':'headline'}).attrs['content'].encode('utf-8')

		#Extract the main article content
		mainContentList = soup.find(id='mediaarticlebody').find_all('p')
		contentStr = ''
		for eachObj in mainContentList:
			try:
				line = eachObj.string.encode('utf-8')
				contentStr += line
			except:
				break

		#Extract the category
		category = soup.find(class_="navitem selected").find('a')['href'].replace('/','')

		print 'date: ', date
		print 'title: ',title
		print 'contentStr: ', contentStr
		print 'category: ', category
		return {'date': date, 'title': title, 'content': contentStr, 'category': category}

	def __JSONConvertor(self):
		return

def main():
	url = 'http://tw.news.yahoo.com/%E9%98%BF%E5%9F%BA%E5%B8%AB%E5%88%86%E4%BA%AB%E8%AA%8D%E9%8C%AF%E5%93%B2%E5%AD%B8-160000246.html'
	url = ['http://tw.news.yahoo.com/%E9%98%BF%E5%9F%BA%E5%B8%AB%E5%88%86%E4%BA%AB%E8%AA%8D%E9%8C%AF%E5%93%B2%E5%AD%B8-160000246.html','http://tw.news.yahoo.com/%E5%9F%BA%E9%9A%86%E6%B8%AF%E8%A5%BF%E4%B8%89%E7%A2%BC%E9%A0%AD%E9%96%8B%E6%8B%86-%E4%BF%9D%E7%95%99%E4%BA%94%E7%B5%84%E9%8B%BC%E6%A8%91-040031054.html']
	yParser = y_newsParser()
	yParser.setURL(url)
	jsonResult = yParser.startFetch()
	print jsonResult
	return

if __name__ == '__main__':
	main()