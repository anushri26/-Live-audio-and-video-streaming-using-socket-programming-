import socket, cv2, pickle,struct,time
import pyshine as ps

mode =  'send'#set the mode to send to capture audio data 
name = 'SERVER TRANSMITTING AUDIO'
audio,context= ps.audioCapture(mode=mode)
#ps.showPlot(context,name)

# Socket Create
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '192.168.56.1'
port = 4982
backlog = 5#which is the number of incoming connections that can be queued up.
socket_address = (host_ip,port)
print('STARTING SERVER AT',socket_address,'...')
server_socket.bind(socket_address)#Bind the socket to the socket_address.
server_socket.listen(backlog)#Listen for incoming connections using server_socket.listen().


while True:
	client_socket,addr = server_socket.accept()#accept a new client conncetion to the server 
	print('GOT CONNECTION FROM:',addr)
	if client_socket:

		while(True):
			frame = audio.get()#get a frame of audio data using audio.get()
			
			a = pickle.dumps(frame)#convert object to a byte stream
			message = struct.pack("Q",len(a))+a#pack the serialized data using struct.pack()
			client_socket.sendall(message)#send the packed data to the client
			
	else:
		break#if client_socket obj is none break out of the loop

client_socket.close()
