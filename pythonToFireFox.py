###################   A Script to Control the FirFox Settings ################
#
# ------------------------------
#	CHANGELOG:
# ------------------------------ 
#   Version 0.1:
#			 -  Initial Release
#			 -  Uses XML file to update the Firefox Proxy settings by editing
#				the preferences file.
#			 -  Works on WINDOWS Operating System only [Will add MAC,LINUX in 
#				future]
#
#	  Version 0.2:
#			 -	Updated code to function better
#			 -	Used Subprocess to Avoid Firfox Error when not running during
#				terminate.
#			 -	Updated to input the File name directly in the Batch File.(XML
#				file has to be in same folder as python File.)
#
#  Created by Bharath Metpally
#  E Mail -  bharathgdk@gmail.com
#
###############################################################################


import os
import re
import fileinput  # To be used in Future
import sys
import warnings
from xml.dom import minidom
import subprocess

class firefoxPrefMod(object):

	def __init__(self,xmlFile):
		print "Initializing..."
		self.appData = os.getenv('APPDATA')
		self.lookupFileName = 'prefs.js'
		self.xmlLoc = os.path.dirname(os.path.realpath(__file__))
		self.xmlPath = self.xmlLoc+'/'+xmlFile+'.xml'   
		## Update this Path to the XML where its Sourcing all the Proxy Settings from

	def __killFireFox(self):
		try:
			#os.system("TaskKill /F /IM firefox.exe")

			## Updated to Subprocess to Avoid error when Firefox is not open.

			subprocess.Popen("TaskKill /F /IM firefox.exe",stdout=subprocess.PIPE, shell=PIPE)  
		except:
			pass
		
	def __extractFileName(self):
		self.path =  self.appData+'/Mozilla/Firefox/Profiles'
		self.profileList = os.listdir(self.path)

		for each in self.profileList:
			if 'default' in each:
				self.path =  self.path+'/'+each
				#print self.path

		for each in os.listdir(self.path):
			if self.__exactMatch(each,self.lookupFileName):
				self.prefFile =  each
		if self.prefFile == self.lookupFileName:
			#print 'preferences File Name is : ',self.prefFile
			pass
		else:
			warnings.warn("Is Firefox Installed???")
			sys.exit()

		self.filePath = self.path+'/'+self.prefFile
		#print 'Full File Path is : ',self.filePath

	def __exactMatch(self,phrase,word):
	    b = r'(\s|^|$)' 
	    return re.match(b + word + b, phrase, flags=re.IGNORECASE)

	def __replaceAll(self,file,searchExp,replaceExp):  #Will be used in future.
	    for line in fileinput.input(file, inplace=1):
	        if searchExp in line:
	            line = line.replace(searchExp,replaceExp)
	        sys.stdout.write(line)

	def __readingXML(self):
		xmlFile = minidom.parse(self.xmlPath)

		proxyInfo = xmlFile.getElementsByTagName("proxyInfo")

		self.proxyAddress = proxyInfo[0].getAttribute("proxyAddress")
		self.proxyPort = proxyInfo[0].getAttribute("proxyPort")
		self.proxyList = proxyInfo[0].getAttribute("proxyList")

	def __list(self):	
		## Add the Following Lines to the New Code...	

		self.newList = ['user_pref("network.proxy.backup.ftp", "");',
		'user_pref("network.proxy.backup.ftp_port", 0);',
		'user_pref("network.proxy.backup.socks", "");',
		'user_pref("network.proxy.backup.socks_port", 0);',
		'user_pref("network.proxy.backup.ssl", "");',
		'user_pref("network.proxy.backup.ssl_port", 0);',
		'user_pref("network.proxy.ftp","'+self.proxyAddress+'");',
		'user_pref("network.proxy.ftp_port",'+ self.proxyPort+');',
		'user_pref("network.proxy.http", "'+self.proxyAddress+'");',
		'user_pref("network.proxy.http_port",'+self.proxyPort+');',
		'user_pref("network.proxy.no_proxies_on","'+self.proxyList+'");',
		'user_pref("network.proxy.share_proxy_settings", true);',   # This can be changed to False if Sharing is not needed.
		'user_pref("network.proxy.socks","'+self.proxyAddress+'");',
		'user_pref("network.proxy.socks_port",'+self.proxyPort+');',
		'user_pref("network.proxy.ssl","'+self.proxyAddress+'");',
		'user_pref("network.proxy.ssl_port",'+self.proxyPort+');',
		'user_pref("network.proxy.type", 1);'] 
		# Change the number to modify the Proxy Setting betweeen 'NoProxy' = 0,'ManualProxy' = 1,
		#	'autoDetect' = 4,'SystemProxy' = 3
	

	def __loadFile(self):
		self.inFile = open(self.filePath,'r')		
		self.inFileDataDefault = self.inFile.readlines()
		self.inFile.close()
		self.__readingXML()

	def __checkForValues(self):

		self.removeThisList = []

		for each in self.inFileDataDefault:
			if 'network.proxy' in each :
				self.removeThisList.append(each)

	def __writeToFile(self):
		outFile = open(self.filePath,'w')

		outFile.writelines(self.listBeforeAppend)

		outFile.close()

		print 'Firefox Proxy Settings updated Successfully!'

	def __finalize(self):
		os.system()

	def __updateList(self):
		self.listBeforeAppend = [each for each in self.inFileDataDefault if each not in self.removeThisList]
		for each in self.listBeforeAppend:
			if 'network.proxy' in each :
				print each   #Checking if there are any traces left.
				#pass

		self.listBeforeAppend.extend(self.newList)

	def main(self):
		self.__killFireFox()
		self.__extractFileName()
		if self.prefFile == self.lookupFileName:
			self.__loadFile()
			self.__checkForValues()
			self.__list()
			self.__updateList()
			self.__writeToFile()

if __name__ == '__main__':
	run = firefoxPrefMod(sys.argv[1])
	run.main()
