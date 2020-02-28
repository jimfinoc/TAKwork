# ----- An UDP server in Python that receives temperature values from clients-----
import socket
import datetime

# Define the IP address and the Port Number
ip      = "127.0.0.1";
port    = 14550;
listeningAddress = (ip, port);

# Create a datagram based server socket that uses IPv4 addressing scheme
datagramSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
datagramSocket.bind(listeningAddress);

while(True):
    gpsMessage, sourceAddress = datagramSocket.recvfrom(128);
    # print("Temperature at %s is %s"%(sourceAddress, gpsMessage.decode()));
    # print("GPS Code from %s is %s"%(sourceAddress, gpsMessage.decode()));
    # response = "Received at: %s"%datetime.datetime.now();
    # datagramSocket.sendto(response.encode(), sourceAddress);
    gpsText = str(gpsMessage.decode())
    textArray = gpsText.split(',')
    if textArray[0] == "$GPGGA":
        # print(textArray[0])
        print (gpsText)
        # print (gpsText.split(','))
