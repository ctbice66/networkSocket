import random
import socket
import ssl
import sys
import time

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

def firstSocket_client(address, socket_1_port, ssl):
	#create first socket and wrap in SSL context
	socket_1 = getSocket(address, socket_1_port, True, False, True, ssl, False, 5.0)
	
	#connection successful
	print("Connected to server on port 27994")
	if ssl == True:
		print("Verified server using certificate: {}".format(socket_1.getpeercert()))
	
	socket_1.send(bytes("ctbice66", "utf-8"))
	print("Sending BlazerID to server on port 27994")
	
	#get socket 2 port from server
	socket_2_port = int.from_bytes(socket_1.recv(1024), byteorder="big")
	socket_1.close()
	
	return socket_2_port

def secondSocket_client(address, socket_2_port, ssl):
	#create second socket, bind and listen for connection from server; set 5 second timeout on socket
	socket_2 = getSocket(address, socket_2_port, True, True, False, ssl, True, 5.0)
	
	#remove comment to work with instructor-provided ROBOT executable
	#s_2_port = int(s_1.recv(1024).decode("utf-8"))
	
	#wait for server connection
	connection, address = socket_2.accept()
	
	#when server connects, extract ports
	ports = str(connection.recv(1024), "utf-8").split(",")
	server_port = int(ports[0])
	client_port = int(ports[1].split(".")[0])
	
	#close second socket
	socket_2.close()
	
	return server_port, client_port

def thirdSocket_client(address, server_port, client_port):
	#create third socket - UDP
	socket_3 = getSocket(address, client_port, False, True, False, False, False, 5.0)
	
	#connect to server via UDP
	socket_3.connect((address, server_port))
	print("Connected to server on port {}".format(server_port))
	
	#wait for 1 second, then send random int to server
	time.sleep(1.0)
	socket_3.send(bytes(random.randint(6, 9).to_bytes(10, byteorder="big")))
	print("Sent random integer to server on port {}".format(server_port))
	
	#send random characters received as a response back to server five times; once per second
	for i in range(5):
		time.sleep(1.0)
		socket_3.send(socket_3.recv(1024))
		print("Sending random string of characters back to server on {}".format(server_port))
		
		#if server responds with success message, break from loop
		if (str(socket_3.recv(1024), "utf-8") == "success"):
			print("Server confirmed matching character string")
			
			#close third socket
			socket_3.close()
			
			break
def main():
	#IP address to use
	address = "127.0.0.1"
	
	#check for arguments passed to client
	if (len(sys.argv) > 1):
		#check for correct parameter
		if sys.argv[1] == "-s":
			
			#start message
			print('STUDENT IS STARTED with SSL')
			
			socket_2_port = firstSocket_client(address, 27994, True)
			
			server_port, client_port = secondSocket_client(address, socket_2_port, True)
			
			thirdSocket_client(address, server_port, client_port)
			
		else:
			print("Use the -s parameter for SSL")

	#user did not provide any arguments
	else:
		
		#start message
		print('STUDENT IS STARTED without SSL')
		
		socket_2_port = firstSocket_client(address, 3310, False)
		
		server_port, client_port = secondSocket_client(address, socket_2_port, False)
		
		thirdSocket_client(address, server_port, client_port)
#start program
main()