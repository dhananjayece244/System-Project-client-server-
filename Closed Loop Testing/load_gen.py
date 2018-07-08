#!/usr/bin/python3           
import socket
import sys
from threading import Thread, Lock
import time

total_requests = 0
total_time_taken = 0
all_req = []
def doShopping(i,tc,):
	t1 = time.time()
	global total_requests,total_time_taken
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
			if authentication_status == '1':
				elapsed = 0
				j = 0
				start = time.time()
				#300 seconds request time starts here
				while elapsed<tc:
					
					req_time = time.time()
					order_description = 'Book 1'
					order = s.send(order_description.encode('ascii'))
					try:
						order_status = s.recv(1024)
						order_status = order_status.decode('utf-8')
						delta_t = time.time()-req_time
					except:
						print("ERROR: Thread ",i," could not placed the order.\n")
					total_time_taken = total_time_taken+delta_t	
					total_requests = total_requests+1
					print("-----------------------------")
					print("Total requests = ",total_requests)
					elapsed = time.time()-start
					print("Elapsed time for thread ",i," is = ",elapsed)
					j = j+1
				flag = s.send("$".encode('ascii'))	

			else:
				print("Log-in failed")
		except:
			print("ERROR: Thread ",i," failed to get the authentication status.\n")
	except:
		print("ERROR: Could not get the signal to send the passwd for thread ",i,"\n")

	s.close()

time0 = 0
if __name__ == "__main__":
	n_threads = int(input("No. of threads: "))
	tc = int(input("Time to iterate: "))
	time0 = time.time()
	print("time 0 =",time0)
	for i in range(n_threads):
		thread = Thread(target=doShopping,args=(i,tc))
		thread.start()
	thread.join()