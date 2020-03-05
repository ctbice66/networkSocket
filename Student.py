import random
import socket
import time
import sys

#check arguments passed from the command line
try:
	if sys.argv[1] == "-s":
		print("SSL connection")
	else:
		print("Invalid argument, please use '-s' to connect via SSL")

#user did not provide any arguments
except IndexError:
	
	#create first socket, connect and send BlazerID to server
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_1:
		s_1.connect(("127.0.0.1", 3310))
		s_1.send(bytes("ctbice66", "utf-8"))
		
		#create second socket, bind and listen for connection from server
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_2:
			s_2.bind(("127.0.0.1", int.from_bytes(s_1.recv(1024), byteorder="big")))
			s_2.listen()
			connection, address = s_2.accept()
			
			#when server connects, extract ports
			with connection:
				ports = str(connection.recv(1024), "utf-8").split(",")
				server_port = int(ports[0])
				client_port = int(ports[1].split(".")[0])
				
				#create third socket - UDP, bind and then connect to server
				with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s_3:
					s_3.bind(("127.0.0.1", client_port))
					s_3.connect(("127.0.0.1", server_port))
					#send random int to server
					s_3.send(bytes(random.randint(6, 9).to_bytes(10, byteorder="big")))
					
					#send response back to server five times; once per second
					for i in range(5):
						time.sleep(1.0)
						s_3.send(s_3.recv(1024))
						
						#if server responds with success message, break from loop
						if (str(s_3.recv(1024), "utf-8") == "success"):
							print("success")
							break