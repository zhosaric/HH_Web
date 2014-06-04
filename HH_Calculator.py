import sys
import string
import re
import os
import matplotlib.pyplot as plt

class HandParse(object):
	def __init__(self, filename):
		self.filename = filename
	
	def parseFile(self):
		with open(self.filename, "r") as f:
			text = f.read().replace("\n","")
			m = re.findall('\[ME\] \(\$(.+?) in chips', text)
			return m
	
	def calcProfit(self):
		values = self.parseFile()
		profit = 0.00
		for i in range(0,len(values) - 1):
			profit += float(values[i+1]) - float(values[i])
		return profit
	
	def profitList(self):
		values = self.parseFile()
		profLi= []
		profit = 0.00
		for i in range(0,len(values) - 1):
			profit += float(values[i+1]) - float(values[i])
			profLi.append(profit)
		return profLi
	
	def plotProfits(self):
		profLi = self.profitList()
		plt.plot(profLi)
		plt.ylabel("Profit")
		plt.xlabel("Hands")
		plt.show()
	

''' class Tracker(object):
    def __init__(self, handparse):
		self.hp = handparse
		
	def iterateList(self):
		pass
'''	


def main():
	hHist = HandParse(sys.argv[1])
	hHist.plotProfits()
	
if __name__ == "__main__":
	main()