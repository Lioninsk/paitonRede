import os
import socket
import sys
import time
import threading

class Client(threading.Thread):
	# 30 seconds for search_interval
	SEARCH_INTERVAL = 5
	BCAST_IP = '239.255.255.250'
	BCAST_PORT = 1900

	def __init__(self):
		threading.Thread.__init__(self)
		self.interrupted = False
		
	def run(self):
		self.keep_search()

	def stop(self):
		self.interrupted = True
		print("upnp client stop")

	def keep_search(self):
		'''
		run search function every SEARCH_INTERVAL
		'''
		
		try:
			while True:
				self.search()
				for x in range(self.SEARCH_INTERVAL):
					
					time.sleep(1)
					if self.interrupted:
						return
		except Exception as e:
			print('Error in upnp client keep search %s', e)

	def search(self):
		'''
		broadcast SSDP DISCOVER message to LAN network
		filter our protocal and add to network
		'''
		try:
			SSDP_DISCOVER = ('M-SEARCH * HTTP/1.1\r\n' +
							'HOST: 239.255.255.250:1900\r\n' +
							'MAN: "ssdp:discover"\r\n' +
							'MX: 1\r\n' +
							'ST: ssdp:all\r\n' +
							'\r\n')
			
			sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			sock.sendto(SSDP_DISCOVER.encode('ASCII'), (self.BCAST_IP, self.BCAST_PORT))
			sock.settimeout(3)
			while True:
				data, addr = sock.recvfrom(1024)
				print(f"addr:{addr}\n\n")
		except:
			sock.close()
		

client = Client()
client.run()