import random
import socket
import ssl
import sys
import time

#list of characters to use for building random string
char_set =  ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

try:
	if sys.argv[1] == "-s":

		#context for SSL
		context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

		#create first SSL socket and listen for a connection from client
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_1:
			s_1.bind(("127.0.0.1", 27994))
			print("ROBOT IS STARTED with SSL")
			s_1.listen()
			
			#wrap first socket with an SSL context
			with context.wrap_socket(s_1, server_side=True) as secure_s_1:
				connection, address = secure_s_1.accept()
				
				#when client connects, print BlazerID then send a port number to client
				with connection:
					print(str(connection.recv(1024), "utf-8"))
					connection.send((12345).to_bytes(10, byteorder="big"))

	else:
		print("Invalid argument, please use '-s' to connect via SSL")

except IndexError:

	#create first socket and listen for a connection from client
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_1:
			s_1.bind(("127.0.0.1", 3310))
			print("ROBOT IS STARTED")
			s_1.listen()
			connection, address = s_1.accept()
			
			#when client connects, print BlazerID then send a port number to client
			with connection:
				print(str(connection.recv(1024), "utf-8"))
				connection.send((12345).to_bytes(10, byteorder="big"))

		#wait 1 second, create second socket connection to client at the port number we sent
		time.sleep(1.0)
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_2:
			s_2.connect(("127.0.0.1", 12345))
			s_2.send(bytes("23456,65432.", "utf-8"))

		#create third socket, bind, then connect
		with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s_3:
			s_3.bind(("127.0.0.1", 23456))
			s_3.connect(("127.0.0.1", 65432))
			
			#translate random number received from client into a string
			random_int = int.from_bytes(s_3.recv(1024), byteorder="big")*10
			random_char_string = str(random.choices(char_set, k=random_int))
			
			#for 5 iterations, wait 1 second, then send char string to client
			for i in range(5):
				time.sleep(1.0)
				s_3.send(bytes(random_char_string, "utf-8"))
				client_response = str(s_3.recv(1024), "utf-8")
				#if the client responds with a matching string, break from loop
				if (random_char_string == client_response):
					s_3.send(bytes("success", "utf-8"))
					print("success")
					break