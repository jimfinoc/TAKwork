
# ----- An UDP server in Python that receives temperature values from clients-----
import socket
import datetime
import re

# Define the IP address and the Port Number
ip      = "127.0.0.1";
port    = 14550;
listeningAddress = (ip, port);
#testDMS = [0,0,3137.36664,'N',00212.21149,'W',0]
# Create a datagram based server socket that uses IPv4 addressing scheme
datagramSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
datagramSocket.bind(listeningAddress);

while(True):
    gpsMessage, sourceAddress = datagramSocket.recvfrom(128);
    # print("Temperature at %s is %s"%(sourceAddress, gpsMessage.decode()));
    # print("GPS Code from %s is %s"%(sourceAddress, gpsMessage.decode()));
    # response = "Received at: %s"%datetime.datetime.now();
    # datagramSocket.sendto(response.encode(), sourceAddress);
    #GPGGA first portion of message::
    # GGA          Global Positioning System Fix Data
    # 123519       Fix taken at 12:35:19 UTC
    # 4807.038,N   Latitude 48 deg 07.038' N
    # 01131.000,E  Longitude 11 deg 31.000' E
    #EXAMPLE####################
    #Lat : 3137.36664 becomes 31 degrees and 37.26664 seconds = 31 + 37.36664/60 = 31.6227773
    #Lon : 00212.21149 becomes 2 degrees and 12.21149 seconds = 2 + 12.21149/60 = 2.20352483
    #So as latitude is in format DDSS.SSSSS
    #DD = int(float(Lat)/100) = int(3137.36664/100) = int(31.3736664) = 31
    #SS = float(lat) - DD * 100 = 3137.36664 - 31 * 100 = 3137.36664 - 3100 = 37.36664
    #LatDec = DD + SS/60 = 31 + 37.36664/60 = 31 + 0.6227773333333333 = 31.6227773333333333
    #Don't forget that data[4] will be your North/South indicator, i.e. "S" or "N".
    #If this is "S" you need to negate your LatDec value.
    #The processing for the longitude will be very similar. This time data[6] will be your East/West indicator. So negate if "W".

    gpsText = str(gpsMessage.decode())
    textArray = gpsText.split(',')
    if textArray[0] != '$':
        #print ("found dollar sign")
        if textArray[0] == "$GPGGA":
            #print ("processing nmea gps message")
            #print (type(testDMS[2]))
            latDD = int(float(textArray[2])/100)
            #print ("DD= ", (latDD))
            latMM = float(textArray[2]) - latDD * 100
            #print ("MM= ", (latMM))
            latDEC = latDD + latMM/60
            #print ("latDEC= ", (latDEC))
            lonDD = int(float(textArray[4])/100)
            lonMM = float(textArray[4]) - lonDD * 100
            lonDEC = lonDD + lonMM/60
            if textArray[3] == "S":
                latDEC = -latDEC
            if textArray[5] == "W":
                lonDEC = -lonDEC

            # print(textArray[0])
            #print (gpsText)
            print (latDEC,",", lonDEC)
            # print (gpsText.split(','))
