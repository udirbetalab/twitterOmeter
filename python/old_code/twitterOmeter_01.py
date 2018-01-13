# -*- coding: utf-8 -*-

import time
from time import sleep
from TwitterAPI import TwitterAPI
import struct
import os
from serial import Serial
import httplib
from httplib import IncompleteRead

from auth_romforlek import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)


availableMicrobit = True # Debugging without an micro:bit
testSerial = False # Debugging without Twitter connection
microbitPort = '/dev/ttyACM0' # USB port address for the micro:bit /dev/ttyACM0 eller /dev/ttyACM1
microbitBaud = '115200' # Baud for serial communication
microbitWaitTime = 0.01 # The length of time Python wait before attemping to issue commands to the micro:bit
stringToTrack = "#trump" # Change this to the search term you wish to track from Twitter
tweet_number = 0

if availableMicrobit:
	ser = Serial(microbitPort, microbitBaud, timeout=3)

sleep(microbitWaitTime)

if testSerial:
	print "Send to micro:bit"
	sleep(2)
	ser.write('\r\n')

else:
	print 'Twitter connection!'
	try:
		api = TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)

		print 'Twitter ready!'

		r = api.request('statuses/filter', {'track':stringToTrack})

		for item in r.get_iterator():
			if 'text' in item:
				#print item['user']['screen_name'].encode('utf-8') + ' tweeted: ' + item['text'].encode('utf-8')
				
				if availableMicrobit:
					#print "New tweet send to micro:bit with " + stringToTrack
					#ser.write(bytes(1)) # The command is a simple byte intepretation of the integer 1
					tweet = item['text'].encode('utf-8').strip(stringToTrack) + '\r\n'
					#ser.write(tweet)
					ser.write("\n")
					tweet_number = tweet_number + 1
					print tweet_number
					#print tweet
					#ser.write(item['text'].encode('utf-8') + '\r\n')
					sleep(microbitWaitTime) # Wait before sending next command
					#ser.write(bytes(0))
					#sleep(microbitWaitTime) # Wait before sending next command
	except IncompleteRead:
		# Oh well, reconnect and keep trucking
		print "IncompleteRead occurred"
	except KeyboardInterrupt:
		# Or however you want to exit this loop
		api.disconnect()
		exit()
