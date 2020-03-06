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
s_3_port = randomPort()
s_4_port = randomPort()

#check for arguments passed to server
try:
	if sys.argv[1] == "-s":
		
		
		#create context for SSL and initialize certificate chain
		context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
		context.load_cert_chain('cert.pem')
		
		#create first SSL socket and listen for a connection from client
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_1:
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
			
			#wait 1 second, create second socket connection to client at the port number we sent
			time.sleep(1.0)
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_2:
				s_2.connect(("127.0.0.1", s_2_port))
				print("Connected to client at port {}".format(s_2_port))
				
				#send ports selected at random to client
				s_2.send(bytes(str(s_3_port) + "," + str(s_4_port) + ".", "utf-8"))
				print("Sending server port {} and client port {}".format(s_3_port, s_4_port))
			
			#create third socket - UDP, then bind
			with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s_3:
				s_3.bind(("127.0.0.1", s_3_port))
				print("Waiting for random int from client on port {}".format(s_3_port))
				
				#translate random number received from client into a string
				random_int = int.from_bytes(s_3.recv(1024), byteorder="big")*10
				random_char_string = str(random.choices(char_set, k=random_int))
				print("Random character string selected: {}".format(random_char_string))
				
				#create fourth socket - UDP, then connect to Client
				s_4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				s_4.connect(("127.0.0.1", s_4_port))
				print("Connected to client at port {}".format(s_4_port))
				
				#for 5 iterations, wait 1 second, then send char string to client
				for i in range(5):
					time.sleep(1.0)
					s_4.send(bytes(random_char_string, "utf-8"))
					print("Sending random character string to client on port {}".format(s_4_port))
					
					#if the client responds with a matching string, break from loop
					if (random_char_string == str(s_3.recv(1024), "utf-8")):
						s_4.send(bytes("success", "utf-8"))
						print("Client has responded with a matching string")
						break

	else:
		print("Invalid argument, please use '-s' to connect via SSL")

except IndexError:

	#create first socket and listen for a connection from client
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_1:
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

		#wait 1 second, create second socket connection to client at the port number we sent
		time.sleep(1.0)
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_2:
			s_2.connect(("127.0.0.1", s_2_port))
			print("Connected to client at port {}".format(s_2_port))
			
			#send ports selected at random to client
			s_2.send(bytes(str(s_3_port) + "," + str(s_4_port) + ".", "utf-8"))
			print("Sending server port {} and client port {}".format(s_3_port, s_4_port))
			
		#create third socket - UDP, then bind
		with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s_3:
			s_3.bind(("127.0.0.1", s_3_port))
			print("Waiting for random int from client on port {}".format(s_3_port))
			
			#translate random number received from client into a string
			random_int = int.from_bytes(s_3.recv(1024), byteorder="big")*10
			random_char_string = str(random.choices(char_set, k=random_int))
			print("Random character string selected: {}".format(random_char_string))
			
			#create fourth socket - UDP, then connect to Client
			s_4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			s_4.connect(("127.0.0.1", s_4_port))
			print("Connected to client at port {}".format(s_4_port))
			
			#for 5 iterations, wait 1 second, then send char string to client
			for i in range(5):
				time.sleep(1.0)
				s_4.send(bytes(random_char_string, "utf-8"))
				print("Sending random character string to client on port {}".format(s_4_port))
				
				#if the client responds with a matching string, break from loop
				if (random_char_string == str(s_3.recv(1024), "utf-8")):
					s_4.send(bytes("success", "utf-8"))
					print("Client has responded with a matching string")
					break