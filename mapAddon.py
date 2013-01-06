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

addonDict={}
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
				print addons	
				addonList = addons.split(',')
				print len(addonList)
				print "\n"
				count=count+1
				if count>4:
					break
		except:
			print("Exception occured\nEither the attribute \"addon\" or \"firstPaint\" is not present\n")
		#break
print "The total count and count for startup time > 5 are"
print tcount
print count
print "Probablity that startupTime > 5s is %.2f" %(count/tcount)

