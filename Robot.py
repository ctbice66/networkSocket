import random
import socket
import ssl
import sys
import time

#list of characters to use for building random string
char_set =  ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

#return a random port greater than 1024 but less than or equal to 65535; exclude 3310 and 27994
def randomPort():
	port = random.randint(1025, 65535)
	
	if (port == 3310):
		randomPort()
	elif (port == 27994):
		randomPort()
	else:
		return port

#select 3 random ports for implementation
s_2_port = randomPort()
server_port = randomPort()
client_port = randomPort()

#check for arguments passed to server
if (len(sys.argv) > 1):
	if sys.argv[1] == "-s":
		
		#create context for SSL and initialize certificate chain
		context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
		context.load_cert_chain('cert.pem')
		
		#create first SSL socket and listen for a connection from client; set 5 second timeout on socket
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_1:
			s_1.settimeout(5.0)
			s_1.bind(("127.0.0.1", 27994))
			print("ROBOT IS STARTED with SSL")
			s_1.listen()
			print("Listening on port 27994")
			
			#wrap first socket with an SSL context
			with context.wrap_socket(s_1, server_side=True) as secure_s_1:
				connection, address = secure_s_1.accept()
				
				#when client connects, print BlazerID then send a port number to client
				with connection:
					print("Connection to port 27994 successful")
					print(str(connection.recv(1024), "utf-8"))
					connection.send((s_2_port).to_bytes(10, byteorder="big"))
					
					#close first socket
					secure_s_1.close()
			
			#wait 1 second, create second socket connection to client at the port number we sent
			time.sleep(1.0)
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_2:
				s_2.connect(("127.0.0.1", s_2_port))
				print("Connected to client at port {}".format(s_2_port))
				
				#send ports selected at random to client via second socket
				s_2.send(bytes(str(server_port) + "," + str(client_port) + ".", "utf-8"))
				print("Sending server port {} and client port {}".format(server_port, client_port))
				
				#close second socket
				s_2.close()
				
				#create third socket - UDP, bind to server port, set 5 second timeout
				s_3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				s_3.bind(("127.0.0.1", server_port))
				s_3.settimeout(5.0)
				print("Waiting for random int from client on port {}".format(server_port))
				
				#receive random int value from client, multiply by 10 to generate size of random character string
				random_int = int.from_bytes(s_3.recv(1024), byteorder="big")
				random_string_size = random_int * 10
				print("Received random int from client on port {}".format(server_port))
				
				#translate random number received from client into a character string
				random_char_string = str(random.choices(char_set, k=random_string_size))
				print("Random character string selected: {}".format(random_char_string))
				
				#connect to client via UDP
				s_3.connect(("127.0.0.1", client_port))
				print("Connected to client at port {}".format(client_port))
				
				#for 5 iterations, wait 1 second, then send random character string to client
				for i in range(5):
					time.sleep(1.0)
					s_3.send(bytes(random_char_string, "utf-8"))
					print("Sending random character string to client on port {}".format(client_port))
					
					#if the client responds with a matching string, break from loop
					if (random_char_string == str(s_3.recv(1024), "utf-8")):
						s_3.send(bytes("success", "utf-8"))
						print("Client has responded with a matching string")
						
						#close third socket
						s_3.close()
						
						break
	else:
		print("Invalid argument, please use '-s' to connect via SSL")

else:

		#create first socket and listen for a connection from client; set 5 second timeout on socket
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_1:
			s_1.settimeout(5.0)
			s_1.bind(("127.0.0.1", 3310))
			print("ROBOT IS STARTED")
			s_1.listen()
			print("Listening on port 3310")
			connection, address = s_1.accept()
			
			#when client connects, print BlazerID then send a port number to client
			with connection:
				print("Connection to port 3310 successful")
				print(str(connection.recv(1024), "utf-8"))
				connection.send((s_2_port).to_bytes(10, byteorder="big"))
				
				#close first socket
				s_1.close()
		
		#wait 1 second, create second socket connection to client at the port number we sent
		time.sleep(1.0)
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_2:
			s_2.connect(("127.0.0.1", s_2_port))
			print("Connected to client at port {}".format(s_2_port))
			
			#send ports selected at random to client via second socket
			s_2.send(bytes(str(server_port) + "," + str(client_port) + ".", "utf-8"))
			print("Sending server port {} and client port {}".format(server_port, client_port))
			
			#close second socket
			s_2.close()
			
			#create third socket - UDP, bind to server port, set 5 second timeout
			s_3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			s_3.bind(("127.0.0.1", server_port))
			s_3.settimeout(5.0)
			print("Waiting for random int from client on port {}".format(server_port))
			
			#receive random int value from client, multiply by 10 to generate size of random character string
			random_int = int.from_bytes(s_3.recv(1024), byteorder="big")
			random_string_size = random_int * 10
			print("Received random int from client on port {}".format(server_port))
			
			#translate random number received from client into a character string
			random_char_string = str(random.choices(char_set, k=random_string_size))
			print("Random character string selected: {}".format(random_char_string))
			
			#connect to client via UDP
			s_3.connect(("127.0.0.1", client_port))
			print("Connected to client at port {}".format(client_port))
			
			#for 5 iterations, wait 1 second, then send random character string to client
			for i in range(5):
				time.sleep(1.0)
				s_3.send(bytes(random_char_string, "utf-8"))
				print("Sending random character string to client on port {}".format(client_port))
				
				#if the client responds with a matching string, break from loop
				if (random_char_string == str(s_3.recv(1024), "utf-8")):
					s_3.send(bytes("success", "utf-8"))
					print("Client has responded with a matching string")
					
					#close third socket
					s_3.close()
					
					break