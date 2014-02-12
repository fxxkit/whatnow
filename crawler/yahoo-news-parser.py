# -*- coding: utf-8 -*-
#! /usr/bin/env python

import urllib2, json
from bs4 import BeautifulSoup, NavigableString

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
				return json.dumps(result,ensure_ascii=False)
			elif type(self.url) is list:
				resultList = []
				for url in self.url:
					htmlContent = urllib2.urlopen(url).read()
					result = self.__parser(htmlContent)
					resultList.append(result)	
				self.url = None #initialize the url parameter
				return json.dumps(resultList,ensure_ascii=False)	
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
		date = date.split('T')[0].encode('utf-8')

		#Extract title
		title = soup.find(attrs={'itemprop':'headline'}).attrs['content'].encode('utf-8')

		#Extract the main article content
		mainContentList = soup.find(id='mediaarticlebody').find_all('p')
		#print mainContentList, '\nlenth: ', len(mainContentList), '\n type: ', type(mainContentList[0])
		contentStr = ''
		for eachObj in mainContentList:
			line = self.__stripAllTags(eachObj).encode('utf-8')
			#print line
			#line = eachObj.extract().encode('utf-8')
			contentStr += line

		#Extract the category
		category = soup.find(class_="navitem selected")
		if category is not None:
			category = category.find('a')['href'].replace('/','').encode('utf-8')

		
		print 'date: ', date
		print 'title: ',title
		print 'contentStr: ', contentStr
		print 'category: ', category
		
		return {'date': date, 'title': title, 'content': contentStr, 'category': category}
	
	def __stripAllTags(self,htmlSoup):
	        if htmlSoup is None:
	                return None
	        return ''.join( htmlSoup.findAll( text = True ) ) 

def main():
	# Read a single url
	#url = 'http://tw.news.yahoo.com/%E6%81%90%E6%80%96%E6%B4%BB%E5%9F%8B-%E6%9A%B4%E5%8A%9B%E9%9B%86%E5%9C%98%E6%8A%BC%E7%84%A1%E8%BE%9C%E8%A2%AB%E5%AE%B3%E4%BA%BA%E6%81%90%E5%9A%87-090400343.html'
	#url = 'http://tw.news.yahoo.com/%E9%A6%96%E5%87%BA%E5%BA%AD-%E7%82%BA%E4%BD%95%E7%94%A9%E5%B7%B4%E6%8E%8C-%E9%99%B3%E5%B7%A7%E6%98%8E-%E6%88%91%E6%98%AF%E6%80%A7%E6%83%85%E4%B8%AD%E4%BA%BA-041000636.html'
	
	# Read a list
	#url = ['http://tw.news.yahoo.com/%E9%98%BF%E5%9F%BA%E5%B8%AB%E5%88%86%E4%BA%AB%E8%AA%8D%E9%8C%AF%E5%93%B2%E5%AD%B8-160000246.html','http://tw.news.yahoo.com/%E5%9F%BA%E9%9A%86%E6%B8%AF%E8%A5%BF%E4%B8%89%E7%A2%BC%E9%A0%AD%E9%96%8B%E6%8B%86-%E4%BF%9D%E7%95%99%E4%BA%94%E7%B5%84%E9%8B%BC%E6%A8%91-040031054.html']
	
	# Read from file
	url = []
	fd = open('dataset/testURLs')
	for line in fd:
		url.append(line.strip())
	
	yParser = y_newsParser()
	yParser.setURL(url)
	jsonResult = yParser.startFetch()
	#print jsonResult

	
	fw = open('dataset/testData.json','w')
	fw.write(jsonResult)
	
	return

if __name__ == '__main__':
	main()