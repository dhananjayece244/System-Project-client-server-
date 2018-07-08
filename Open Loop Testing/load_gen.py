#!/usr/bin/python3           
import socket
import sys
from threading import Thread, Lock
import time
from decimal import Decimal

total_requests = 0
total_time = 0
all_req = []
def doShopping(i,time0):
	global total_requests,total_time
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	host = sys.argv[1]                           
	port = int(sys.argv[2])
	s.connect((host, port))
	username = s.send('debanjan'.encode('ascii'))
	try:
		flag = s.recv(1024)
		flag = flag.decode("utf-8")
		if flag=='1':
			password = s.send('abcd'.encode('ascii'))
		try:
			authentication_status = s.recv(1024)
			authentication_status = authentication_status.decode('utf-8')
			#print("Thread ",i," recieved the authentication status.\n")
			if authentication_status == '1':
				order_description = 'Book 1'
				order = s.send(order_description.encode('ascii'))
				try:
					order_status = s.recv(1024)
					order_status = order_status.decode('utf-8')
					total_time=time.time()-time0
					total_requests = total_requests+1

					print("Request ",total_requests, "completes at ",total_time)
					#print("User ", i,"completes at ",total_time)
				except:
					print("ERROR: Thread ",i," could not placed the order.\n")
					
			else:
				print("Log-in failed")
		except:
			print("ERROR: Thread ",i," failed to get the authentication status.\n")
	except:
		print("ERROR: Could not get the signal to send the passwd for thread ",i,"\n")
	s.close()

time0 = 0

if __name__ == "__main__":
	#n_threads = int(input("No. of threads: "))
	#tc = int(input("Time to iterate: "))
	time0 = time.time()
	i=0
	#lembda=Decimal(sys.argv[2])
	#print(type(lembda))
	elapsed=0
	while (elapsed<1):
		i=i+1
		thread = Thread(target=doShopping,args=(i,time0))
		thread.start()
		time.sleep(0.0666667)
		elapsed=time.time()-time0
	
	thread.join()
	print("Throughput = ",total_requests/total_time)