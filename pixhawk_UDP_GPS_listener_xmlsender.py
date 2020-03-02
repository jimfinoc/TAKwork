
# ----- An UDP server in Python that receives temperature values from clients-----
import socket
import datetime
import re

# Define the IP address and the Port Number
ip      = "127.0.0.1";
port    = 14550;

listeningAddress = (ip, port);
# input of UDP from pixHawk
datagramSocketGPS = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
datagramSocketGPS.bind(listeningAddress);
# output of UDP to TAK
datagramSocketXML = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);

# xml_sender.py
import datetime as dt
import xml.etree.ElementTree as ET
import socket
import time
import xml.etree.ElementTree
import argparse
parser = argparse.ArgumentParser()
# parser.add_argument('--foo', help='foo help')
parser.add_argument('-s', '--staleness', type=int, default=1, help='How long in minutes before an update to TAK goes into the stale state (and gets removed).')
# parser.add_argument('-u', '--event_uid', default="ROS_#", help='Unique identifier for the event.')
parser.add_argument('-cs', '--callsign', default="Baby baby", help='Call sign that displays on the map.')
parser.add_argument('-c', '--color', default="soldier", help='color of object displaying on the map.')
# parser.add_argument('-', '--color', default="soldier", help='color of object displaying on the map.')
args = parser.parse_args()


header = "<?xml version='1.0' standalone='yes'?>"


DATETIME_FMT = "%Y-%m-%dT%H:%M:%SZ"
SERIAL_FMT = "%Y%m%dT%H%M%SZ"

group_attr = {
    # "name":"Cyan",
    # "name":"Yellow",
    "name":args.color
    # "role":"RTO"
    # "role":"Sniper"
    # "role":"Medic"
    # "role":"K9"
    # "role":"Forward Observer"
}
# GET LOCAL IP INSTEAD OF HARDCODED IP
contact_attr = {
    # "endpoint":"192.168.1.235:4242:tcp",
    # "callsign":"E-Maxx 1"
    "callsign":args.callsign
}

ip      = "239.2.3.1";
port    = 6969;
sending_Address_Port1 = (ip, port);

ip      = "127.0.0.1";
port    = 18999;
sending_Address_Port2 = (ip, port);

ip      = "127.0.0.1";
port    = 18000;
sending_Address_Port3 = (ip, port);


while(True):
    gpsMessage, sourceAddress = datagramSocketGPS.recvfrom(128);

    gpsText = str(gpsMessage.decode())
    textArray = gpsText.split(',')
    if textArray[0] != '$':
        if textArray[0] == "$GPGGA":
            latDD = int(float(textArray[2])/100)
            latMM = float(textArray[2]) - latDD * 100
            latDEC = latDD + latMM/60
            lonDD = int(float(textArray[4])/100)
            lonMM = float(textArray[4]) - lonDD * 100
            lonDEC = lonDD + lonMM/60
            if textArray[3] == "S":
                latDEC = -latDEC
            if textArray[5] == "W":
                lonDEC = -lonDEC
            print (latDEC,",", lonDEC)
            # SHOULD I GET TIME FROM THE GPS INSTEAD????
            timer = dt.datetime
            now = timer.utcnow()
            zulu = now.strftime(DATETIME_FMT)
            stale_part = now.minute + args.staleness
            if stale_part > (60-args.staleness):
                stale_part = stale_part - 60
            stale_now = now.replace(minute=stale_part)
            stale = stale_now.strftime(DATETIME_FMT)
            serial = stale_now.strftime(SERIAL_FMT)
            # ///GPS
            evt_attr = {
                "version": "2.0",
                # "uid": "ROS"+serial,
                # "uid": "ROS"+"001",
                # "uid": args.event_uid,
                "uid": args.callsign,
                "time": zulu,
                "start": zulu,
                "stale": stale,
                "how":"h-e",
                "type": "a-f-G-E-W-R-R"
                }
            pt_attr = {
                # "lat": "41.396",
                "lat": str(latDEC),
                # "lon": "-73.984",
                "lon": str(lonDEC),
                "hae": "-42.6",   #unit["hae"],
                "ce": "45.3",    #unit["ce"],
                "le": "99.5"     #unit["le"]1
            }
            cot = ET.Element('event', attrib=evt_attr)
            cot_event = ET.SubElement(cot,'point', attrib=pt_attr)
            cot_detail = ET.SubElement(cot, 'detail')
            ET.SubElement(cot_detail, 'contact', attrib=contact_attr)
            ET.SubElement(cot_detail, '__group', attrib=group_attr)
            print ("cot")
            print (cot)
            print ("")

            xml_message = ET.tostring(cot)

            xml_decoded = header + xml_message.decode("utf-8")

            xml_re_encoded = xml_decoded.encode("utf-8")
            print ("")
            print ("xml_re_encoded")
            print (xml_re_encoded)
            print ("/xml_re_encoded")

            sent = datagramSocketXML.sendto(xml_re_encoded, sending_Address_Port1)
            print ("Sending to " + str(sending_Address_Port1) + " for ATAK")

            sent = datagramSocketXML.sendto(xml_re_encoded, sending_Address_Port2)
            print ("Sending to " + str(sending_Address_Port2) + " for the COT debugger")

            sent = datagramSocketXML.sendto(xml_re_encoded, sending_Address_Port3)
            print ("Sending to " + str(sending_Address_Port3) + " for WinTAK")

            # print ("zulu")
            # print (zulu)
            # print ("stale")
            # print (stale)
            # datagramSocket.close()
