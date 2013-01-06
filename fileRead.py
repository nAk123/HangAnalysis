from __future__ import division
import json

#Read  the Chrome hang data for Oct 1st

f=open("/home/arjun/MoData/Chromehang/chrome-hangs-20121002.out", 'rb')
print f
#Read the telemetry pings (JSON)
f.seek(0)
#Total count - Sample Space
tcount=0
#Count of readings with firstPaint > 5seconds
count=0
#Unique addonlist
uaddon=set() 

for line in f:
	if "info" in line:
		try:
			jsonObj = json.loads(line)
			#Print simple addon measurements
			fPaint = jsonObj["simpleMeasurements"]["firstPaint"]
			tcount=tcount+1
			#addons = jsonObj["info"]["addons"]
			#print measurements
			#first paint time for the the telemetry pings
			#print fPaint
			if fPaint>5000:
				print fPaint
				addons = jsonObj["info"]["addons"]
				#print addons	
				addonList = addons.split(',')
				print len(addonList)
				tempset=set(addonList)
				#print tempset
				uaddon=uaddon.union(tempset)
				#print uaddon
				print "\n"
				count=count+1
		except:
			print("Exception occured\nEither the attribute \"addon\" or \"firstPaint\" is not present\n")
		#break
		
print "The Unique addons are"
print uaddon
print "Number of Unique addons"
print len(uaddon)
print "The total count and count for startup time > 5 are"
print tcount
print count
pStartup=count/tcount
print "Probablity that startupTime > 5s is {0}".format(pStartup)
