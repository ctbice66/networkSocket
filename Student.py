import random
import socket
import ssl
import sys
import time

#check for arguments passed to client
if (len(sys.argv) > 1):
	if sys.argv[1] == "-s":
		
		#context and hostname for SSL
		context = ssl.create_default_context()
		context.load_verify_locations("cert.pem")
		context.check_hostname = False
		
		#create first socket and wrap in SSL context
		s_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		secure_s_1 = context.wrap_socket(s_1, server_hostname="127.0.0.1")
		
		#connect and send BlazerID to server
		secure_s_1.connect(("127.0.0.1", 27994))
		print("Verified server using certificate: {}".format(secure_s_1.getpeercert()))
		print("Connected to server on port 27994")
		secure_s_1.send(bytes("ctbice66", "utf-8"))
		print("Sending BlazerID to server on port 27994")
		
		#create second socket, bind and listen for connection from server; set 5 second timeout on socket
		s_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s_2.settimeout(5.0)
		
		#remove comment to work with instructor-provided ROBOT executable
		#s_2_port = int(s_1.recv(1024).decode("utf-8"))
		
		s_2_port = int.from_bytes(secure_s_1.recv(1024), byteorder="big")
		s_2.bind(("127.0.0.1", s_2_port))
		s_2.listen()
		print("Listening on port {}".format(s_2_port))
		connection, address = s_2.accept()
		
		#close first socket
		secure_s_1.close()
		
		#remove comment to work with instructor-provided ROBOT executable
		#ports = connection.recv(1024).decode("utf-8").split(",")
		#server_port = int(ports[0])
		#client_port = int(ports[1])
		
		#when server connects, extract ports
		ports = str(connection.recv(1024), "utf-8").split(",")
		server_port = int(ports[0])
		client_port = int(ports[1].split(".")[0])
		
		#close second socket
		s_2.close()
		
		#create third socket - UDP
		s_3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		
		#bind UDP socket to client port, set 5 second timeout
		s_3.bind(("127.0.0.1", client_port))
		s_3.settimeout(5.0)
		
		#connect to server via UDP
		s_3.connect(("127.0.0.1", server_port))
		print("Connected to server on port {}".format(server_port))
		
		#wait for 1 second, then send random int to server
		time.sleep(1.0)
		s_3.send(bytes(random.randint(6, 9).to_bytes(10, byteorder="big")))
		print("Sent random integer to server on port {}".format(server_port))
		
		#send random characters received as a response back to server five times; once per second
		for i in range(5):
			time.sleep(1.0)
			s_3.send(s_3.recv(1024))
			print("Sending random string of characters back to server on {}".format(server_port))
			
			#if server responds with success message, break from loop
			if (str(s_3.recv(1024), "utf-8") == "success"):
				print("Server confirmed matching character string")
				
				#close third socket
				s_3.close()
				
				break
	else:
		print("Invalid argument, please use '-s' to connect via SSL")

#user did not provide any arguments
else:
	
	#create first socket, connect and send BlazerID to server
	s_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s_1.connect(("127.0.0.1", 3310))
	print("Connected to server on port 3310")
	s_1.send(bytes("ctbice66", "utf-8"))
	print("Sending BlazerID to server on port 3310")
	
	#create second socket, bind and listen for connection from server; set 5 second timeout on socket
	s_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s_2.settimeout(5.0)
	
	#remove comment to work with instructor-provided ROBOT executable
	#s_2_port = int(s_1.recv(1024).decode("utf-8"))
	
	s_2_port = int.from_bytes(s_1.recv(1024), byteorder="big")
	s_2.bind(("127.0.0.1", s_2_port))
	s_2.listen()
	print("Listening on port {}".format(s_2_port))
	connection, address = s_2.accept()
	
	#when server connects, extract ports
	#if connection:
	
	#close first socket
	s_1.close()
	#remove comment to work with instructor-provided ROBOT executable
	#ports = connection.recv(1024).decode("utf-8").split(",")
	#server_port = int(ports[0])
	#client_port = int(ports[1])
	
	ports = str(connection.recv(1024), "utf-8").split(",")
	server_port = int(ports[0])
	client_port = int(ports[1].split(".")[0])
	
	#close second socket
	s_2.close()
	
	#create third socket - UDP
	s_3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	
	#bind UDP socket to client port, set 5 second timeout
	s_3.bind(("127.0.0.1", client_port))
	s_3.settimeout(5.0)
	
	#connect to server via UDP
	s_3.connect(("127.0.0.1", server_port))
	print("Connected to server on port {}".format(server_port))
	
	#wait for 1 second, then send random int to server
	time.sleep(1.0)
	s_3.send(bytes(random.randint(6, 9).to_bytes(10, byteorder="big")))
	print("Sent random integer to server on port {}".format(server_port))
	
	#send random characters received as a response back to server five times; once per second
	for i in range(5):
		time.sleep(1.0)
		s_3.send(s_3.recv(1024))
		print("Sending random string of characters back to server on {}".format(server_port))
		
		#if server responds with success message, break from loop
		if (str(s_3.recv(1024), "utf-8") == "success"):
			print("Server confirmed matching character string")
			
			#close third socket
			s_3.close()
			
			break