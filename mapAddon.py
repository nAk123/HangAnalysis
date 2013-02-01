from __future__ import division
import json
import numpy as np

#Read  the Chrome hang data for Oct 2nd
f=open("/home/arjun/MoData/Chromehang/chrome-hangs-20121002.out", 'rb')
f.seek(0)
tcount=0									#Total count - Sample Space
count=0										#Count of readings above the cutoff time
addonCount=set()					#Unique set of all addons
uaddon=set() 							#unique set of addons which may have caused startup delay
startupTime=[]						#List of all the different startup times
addonOccurrenceMap = {}		#No. of times of occurence of addon when fPaintTime > CutoffTime
addonMap = {}							#Total no. of times of occurence of addon

for line in f:
	#Load the JSON ping
	if "info" in line:
		try:
			jsonObj = json.loads(line)
		except:
			print "Error in parsing JSON telemetry ping"
		#Omit all machines lower than Windows7
		if jsonObj["info"]["version"]>=6.1:
			#Generate unique set of addons
			if "addons" in line:
				addonSet = jsonObj["info"]["addons"]
				addonSetList = addonSet.split(',')
				tmpset=set(addonSetList)
				addonCount=addonCount.union(tmpset)
			else:
				print "No addons present"
			#Calculate number of occurences of individual addons in the data
			for addon in addonSetList:
				if addon in addonMap:
					addonMap[addon] += 1
				else:
					addonMap[addon]= 1
			#Read and store the Startup Times
			if "firstPaint" in line:
				fPaint = jsonObj["simpleMeasurements"]["firstPaint"]
				startupTime.append(fPaint)
			else:
				print "fPaint attribute is missing"
			#Calculate the sample space
			tcount = tcount + 1
			
print "The startup time is"
print startupTime
cutoffTime = np.percentile(startupTime, 90)	
print "The cutoff time is"
print cutoffTime

f.seek(0)
for line in f:
	if "info" in line:
		try:
			jsonObj = json.loads(line)
		except:
			print "Problem in parsing JSON Telemetry Ping"
		if jsonObj["info"]["version"]>=6.1:
			if "firstPaint" in line:
				fPaint = jsonObj["simpleMeasurements"]["firstPaint"]
				#Check if Startup time is above 90 percentile
				if fPaint>cutoffTime:
					#Generate unique list of addons which occur when Startup time is greater than 90 percentile
					if "addons" in line:
						addons = jsonObj["info"]["addons"]
						addonList = addons.split(',')
						tempset=set(addonList)
						uaddon=uaddon.union(tempset)
						#Calculate how many times an individual addon is read
						for addon in addonList:
							if addon in addonOccurrenceMap:
								addonOccurrenceMap[addon] += addonOccurrenceMap[addon]
							else:
								addonOccurrenceMap[addon] = 1
						#Count of readings in which startup time is greater than 90 percentile
						count = count + 1
			else:
				print "Either the fPaint time or addons attribute are not available"

pStartup=count/tcount
print "Probablity that startupTime > cutofftime is {0}".format(pStartup)
addonProbMap = {}
addonCondProbMap = {}
addonIndProbMap = {}
for addon in uaddon:
	addonProbMap[addon] = addonOccurrenceMap[addon]/tcount
	addonIndProbMap[addon] = addonMap[addon]/tcount
	addonCondProbMap[addon] = addonProbMap[addon]/addonIndProbMap[addon]
	
for addon in uaddon:
	if(addonCondProbMap[addon]>0.01):
		print "Prob that {0} causes startup delay is {1}".format(addon, addonCondProbMap[addon])

print "Total number of addons:"
print len(addonCount)
print "Number of addons which might have caused startup delay:"
print len(uaddon)
