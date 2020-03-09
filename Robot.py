import random
import socket
import ssl
import sys
import time

#return a random port greater than 1024 but less than or equal to 65535; exclude 3310, 27994, and any already selected for use
def getRandomPort(usedPorts):
	#random intger between 1025 and 65535
	port = random.randint(1025, 65535)
	
	#check if port is already in use, if not then return port and add it to list of ports in use
	if (port in usedPorts):
		randomPort()
	else:
		usedPorts.append(port)
		return port

def getSocket(address, port, TCP, bind, connect, secure, secureServer, timeout):
	#create new TCP or UDP socket
	if TCP == True:
		newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	elif TCP == False:
		newSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		
	#bind and listen for TCP socket or just bind for UDP
	if bind and TCP == True:
		newSocket.bind((address, port))
		newSocket.listen()
	elif bind and TCP == False:
		newSocket.bind((address, port))
		
	#upgrade new socket to SSL socket
	if secure == True and secureServer == True:
		#create context for SSL and initialize certificate chain
		context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
		context.load_cert_chain('cert.pem')
		
		#wrap new socket with SSL context
		newSocket = context.wrap_socket(newSocket, server_side=True)
	elif secure == True and secureServer == False:
		#context and hostname for SSL
		context = ssl.create_default_context()
		context.load_verify_locations("cert.pem")
		context.check_hostname = False
		
		#wrap new socket with SSL context
		newSocket = context.wrap_socket(newSocket, server_hostname=address)
	
	#give socket a timeout
	if timeout > 0:
		newSocket.settimeout(timeout)
	
	#connect via new socket
	if connect == True:
		newSocket.connect((address, port))
		
	
	return newSocket

def firstSocket_Robot(address, socket_1_port, socket_2_port, ssl):
	#create first SSL socket and listen for a connection from client; set 5 second timeout on socket
	socket_1 = getSocket(address, socket_1_port, True, True, False, ssl, True, 5.0)
	print("Listening on port {}".format(socket_1_port))
	
	#wait for client connection
	connection, client_address = socket_1.accept()
	
	#when client connects, print BlazerID then send a port number to client
	print("Connection to port {} successful".format(socket_1_port))
	print(str(connection.recv(1024), "utf-8"))
	connection.sendall((socket_2_port).to_bytes(10, byteorder="big"))
	
	#close first socket
	socket_1.close()

def secondSocket_Robot(address, socket_2_port, server_port, client_port, ssl):
	#wait 1 second, create second socket connection to client at the port number we sent
	time.sleep(1.0)
	socket_2 = getSocket(address, socket_2_port, True, False, True, ssl, False, 5.00)
	print("Connected to client at port {}".format(socket_2_port))
	if ssl == True:
		print("Verified server using certificate: {}".format(socket_2.getpeercert()))
	
	#send ports selected at random to client via second socket
	socket_2.send(bytes(str(server_port) + "," + str(client_port) + ".", "utf-8"))
	print("Sending server port {} and client port {}".format(server_port, client_port))
	
	#close second socket
	socket_2.close()

def thirdSocket_Robot(address, server_port, client_port, char_set):
	#create third socket - UDP, bind to server port, set 5 second timeout
	socket_3 = getSocket(address, server_port, False, True, False, False, True, 5.0)
	print("Waiting for random int from client on port {}".format(server_port))
	
	#receive random int value from client, multiply by 10 to generate size of random character string
	random_int = int.from_bytes(socket_3.recv(1024), byteorder="big")
	random_string_size = random_int * 10
	print("Received random int from client on port {}".format(server_port))
	
	#translate random number received from client into a character string
	random_char_string = "".join(random.choices(char_set, k=random_string_size))
	print("Random character string selected: {}".format(random_char_string))
	
	#connect to client via UDP
	socket_3.connect((address, client_port))
	print("Connected to client at port {}".format(client_port))
	
	#for 5 iterations, wait 1 second, then send random character string to client
	for i in range(5):
		time.sleep(1.0)
		socket_3.send(bytes(random_char_string, "utf-8"))
		print("Sending random character string to client on port {}".format(client_port))
		
		#if the client responds with a matching string, break from loop
		if (random_char_string == str(socket_3.recv(1024), "utf-8")):
			socket_3.send(bytes("success", "utf-8"))
			print("Client has responded with a matching string")
			
			#close third socket
			socket_3.close()
			
			break

def main():
	
	#IP address to use
	address = "127.0.0.1"

	#list of characters to use for building random string
	char_set =  ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

	#list of ports in use
	usedPorts = [3310, 27994]

	#static port initialization, select 3 random ports for implementation
	socket_1_port = 3310
	secure_socket_1_port = 27994
	socket_2_port = getRandomPort(usedPorts)
	server_port = getRandomPort(usedPorts)
	client_port = getRandomPort(usedPorts)
	
	if (len(sys.argv) > 1):
		#check for correct parameter
		if sys.argv[1] == "-s":
			#start message
			print("ROBOT IS STARTED with SSL")
			
			firstSocket_Robot(address, secure_socket_1_port, socket_2_port, True)
			
			secondSocket_Robot(address, socket_2_port, server_port, client_port, True)
			
			thirdSocket_Robot(address, server_port, client_port, char_set)
		else:
			print('Use the -s parameter for SSL')
	else:
		#start message
		print("ROBOT IS STARTED without SSL")
		
		firstSocket_Robot(address, socket_1_port, socket_2_port, False)
		
		secondSocket_Robot(address, socket_2_port, server_port, client_port, False)
		
		thirdSocket_Robot(address, server_port, client_port, char_set)
		
#start program
main()