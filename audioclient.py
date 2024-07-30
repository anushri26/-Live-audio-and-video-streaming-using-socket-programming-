import socket,cv2, pickle,struct
import pyshine as ps

#pyshine : contains various audio and video processing utilities
#pickle lib : converting a Python object into a byte stream to store it in a file/database
#socket lib : The 'socket' module defines how server and client machines can communicate at hardware level using socket endpoints on top of the operating system. The 'socket' API supports both connection-oriented and connectionless network protocols.
#struct lib : interpret bytes as packed binary data

mode =  'get' #mode of audio capture is set to 'get'
name = 'CLIENT RECEIVING AUDIO'
audio,context = ps.audioCapture(mode=mode)#audiocapture function to capture audio , returns a tuple containing the audio data and context 
ps.showPlot(context,name)#to display a plot of the audio waveform 

# create socket
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#creates a socket object using socket lib
host_ip = '192.168.56.1'#ip address of the server to connect to
port = 4982# sets the port number of the server to connect to.

socket_address = (host_ip,port)
client_socket.connect(socket_address) 
print("CLIENT CONNECTED TO",socket_address)
data = b""#emprt bytes obj to hold the received data
payload_size = struct.calcsize("Q")#cal the size of the payload using the struct module,8 byte unsigned int
while True:#starts an infinite loop to receive data from the server.
	while len(data) < payload_size:
		packet = client_socket.recv(4*1024) # 4K , receive data in chunks of 4kb until the size of the recieved data matches the payload size
		if not packet: break
		data+=packet #adds recieved data the data variable 
	packed_msg_size = data[:payload_size]
	data = data[payload_size:]
	msg_size = struct.unpack("Q",packed_msg_size)[0]
	
	
	while len(data) < msg_size:
		data += client_socket.recv(4*1024)
	frame_data = data[:msg_size]
	data  = data[msg_size:]
	frame = pickle.loads(frame_data)
	audio.put(frame)

client_socket.close()
