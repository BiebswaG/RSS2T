# RS Seed to Time
print "RS Seed To Time (by Kaphotics)\n"
dseed = int(raw_input("Enter 16Bit Seed: 0x"),16)
etime = int(raw_input("How many extra ingame-minutes for a later-frame seed? (50 Rec): "))
edate = int(raw_input("How many days are you willing to wait for a seed? (50?): "))
print "\nProcessing...\n"
	
# Calculate RS Seed With Given Minutes Past Start:
def makeseed(minutes):	
	# Decompose
	m  = (minutes) % 60
	um = (m % 10)
	tm = (m - um)/10
	h  = ((minutes-m)/60) % 24
	uh = (h % 10)
	th = (h - uh)/10
	d  = (((minutes-m)/60) - h)/24 + 1 # (Jan 1)
    
	# Recompose
	v  = 1440*d + 960*th + 60*uh + 16*tm + um
    
	# Resulting Seed
	return (v >> 16) ^ (v & 0xFFFF)

# RNG Function to reverse Seed:
def randr(seed):
	newseed = seed # hehe
	newseed *= 0xEEB9EB65
	newseed += 0x0A3561A1
	newseed &= 0xFFFFFFFF
	return newseed # nice

# Get a List of Higher Frame Seeds that can still be populated.
def populateprevious(seed):
	array=[seed]
	times,frame,itera=[0],[0],0
	seed=randr(seed)
	while itera < 3600*etime: # Keep extra wait time below 45 minutes.
		if seed < 0x10000:
			array.append(seed)
			times.append(itera/60/60)
			frame.append(itera)
		seed=randr(seed)
		itera +=1
	return (array, times, frame)

# Main
def main(seed):
	c = csv.writer(open("RSS2T - 0x%04X.csv" % (seed), "wb"))
	c.writerow(["exFrame","exMinutes","Seed","sMinutes","sHours","sDays"])
	results=[]
	array, times, frame = populateprevious(seed)
	for item in range(len(array)):
		minute = 0
		while minute < 1440*edate: # edate Days maximum for seed extrapolating.
			while (makeseed(minute) != array[item]):
				minute += 1
			c.writerow([frame[item],times[item],"0x%04X" % array[item],minute,minute/60,minute/3600])
			minute += 1
	print "Done.\n"
	
# Script
import csv
import time
import os
import math
main(dseed)
raw_input("Press Enter to Close.")
