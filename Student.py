import random
import socket
import ssl
import sys
import time

#check for arguments passed to client
try:
	if sys.argv[1] == "-s":
		
		#context and hostname for SSL
		context = ssl.create_default_context()
		context.load_verify_locations("cert.pem")
		context.check_hostname = False
		
		#create first socket and wrap in SSL context
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_1:
			with context.wrap_socket(s_1, server_hostname="127.0.0.1") as secure_s_1:
				
				#connect and send BlazerID to server
				secure_s_1.connect(("127.0.0.1", 27994))
				print("Connected to server on port 27994")
				secure_s_1.send(bytes("ctbice66", "utf-8"))
				print("Sending BlazerID to server on port 27994")
				
				#create second socket, bind and listen for connection from server
				with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_2:
					
					#remove comment to work with instructor-provided ROBOT executable
					#s_2_port = int(s_1.recv(1024).decode("utf-8"))
					
					s_2_port = int.from_bytes(secure_s_1.recv(1024), byteorder="big")
					s_2.bind(("127.0.0.1", s_2_port))
					s_2.listen()
					print("Listening on port {}".format(s_2_port))
					connection, address = s_2.accept()
					
					#when server connects, extract ports
					with connection:
						
						#remove comment to work with instructor-provided ROBOT executable
						#ports = connection.recv(1024).decode("utf-8").split(",")
						#server_port = int(ports[0])
						#client_port = int(ports[1])
						
						ports = str(connection.recv(1024), "utf-8").split(",")
						server_port = int(ports[0])
						client_port = int(ports[1].split(".")[0])
						
						#create third socket - UDP, bind to port selected by server
						with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s_3:
							s_3.bind(("127.0.0.1", client_port))
							
							#create fourth socket - UDP, connect to Server
							s_4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
							s_4.connect(("127.0.0.1", server_port))
							print("Connected to server on port {}".format(server_port))
							
							#send random int to server
							s_4.send(bytes(random.randint(6, 9).to_bytes(10, byteorder="big")))
							print("Sending random integer to server on port {}".format(server_port))
							
							#send random characters received back as a response back to server five times; once per second
							for i in range(5):
								time.sleep(1.0)
								s_4.send(s_3.recv(1024))
								print("Sending random string of characters back to server on {}".format(server_port))
								
								#if server responds with success message, break from loop
								if (str(s_3.recv(1024), "utf-8") == "success"):
									print("Server confirmed matching character string")
									break
	else:
		print("Invalid argument, please use '-s' to connect via SSL")

#user did not provide any arguments
except IndexError:
	
	#create first socket, connect and send BlazerID to server
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_1:
		s_1.connect(("127.0.0.1", 3310))
		print("Connected to server on port 3310")
		s_1.send(bytes("ctbice66", "utf-8"))
		print("Sending BlazerID to server on port 3310")
		
		#create second socket, bind and listen for connection from server
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_2:
			
			#remove comment to work with instructor-provided ROBOT executable
			#s_2_port = int(s_1.recv(1024).decode("utf-8"))
			
			s_2_port = int.from_bytes(s_1.recv(1024), byteorder="big")
			s_2.bind(("127.0.0.1", s_2_port))
			s_2.listen()
			print("Listening on port {}".format(s_2_port))
			connection, address = s_2.accept()
			
			#when server connects, extract ports
			with connection:
				
				#remove comment to work with instructor-provided ROBOT executable
				#ports = connection.recv(1024).decode("utf-8").split(",")
				#server_port = int(ports[0])
				#client_port = int(ports[1])
				
				ports = str(connection.recv(1024), "utf-8").split(",")
				server_port = int(ports[0])
				client_port = int(ports[1].split(".")[0])
				
				#create third socket - UDP, bind to port selected by server
				with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s_3:
					s_3.bind(("127.0.0.1", client_port))
					
					#create fourth socket - UDP, connect to Server
					s_4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
					s_4.connect(("127.0.0.1", server_port))
					print("Connected to server on port {}".format(server_port))
					
					#send random int to server
					s_4.send(bytes(random.randint(6, 9).to_bytes(10, byteorder="big")))
					print("Sending random integer to server on port {}".format(server_port))
					
					#send random characters received as a response back to server five times; once per second
					for i in range(5):
						time.sleep(1.0)
						s_4.send(s_3.recv(1024))
						print("Sending random string of characters back to server on {}".format(server_port))
						
						#if server responds with success message, break from loop
						if (str(s_3.recv(1024), "utf-8") == "success"):
							print("Server confirmed matching character string")
							break