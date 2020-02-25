# xml_sender.py
import datetime as dt
import xml.etree.ElementTree as ET
import socket
import time
import xml.etree.ElementTree

header = "<?xml version='1.0' standalone='yes'?>"


DATETIME_FMT = "%Y-%m-%dT%H:%M:%SZ"
SERIAL_FMT = "%Y%m%dT%H%M%SZ"

timer = dt.datetime
now = timer.utcnow()
zulu = now.strftime(DATETIME_FMT)
stale_part = now.minute + 1
if stale_part > 59:
    stale_part = stale_part - 60
stale_now = now.replace(minute=stale_part)
stale = stale_now.strftime(DATETIME_FMT)
serial = stale_now.strftime(SERIAL_FMT)



evt_attr = {
    "version": "2.0",
    # "uid": "ROS"+serial,
    "uid": "ROS"+"001",
    "time": zulu,
    "start": zulu,
    "stale": stale,
    "how":"h-e",
    "type": "a-f-G-E-W-R-R"
}


pt_attr = {
    "lat": "41.396",
    "lon": "-73.984",
    "hae": "-42.6",   #unit["hae"],
    "ce": "45.3",    #unit["ce"],
    "le": "99.5"     #unit["le"]1
}

cot = ET.Element('event', attrib=evt_attr)
cot_event = ET.SubElement(cot,'point', attrib=pt_attr)
cot_detail = ET.SubElement(cot, 'detail')

contact_attr = {
    "endpoint":"192.168.1.235:4242:tcp",
    "callsign":"E-Maxx 1"
}
ET.SubElement(cot_detail, 'contact', attrib=contact_attr)

group_attr = {
    # "name":"Cyan",
    "name":"Yellow",
    # "role":"RTO"
    # "role":"Sniper"
    # "role":"Medic"
    # "role":"K9"
    # "role":"Forward Observer"
}
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


ip      = "239.2.3.1";
port    = 6969;
sending_Address_Port1 = (ip, port);

ip      = "127.0.0.1";
port    = 18999;
sending_Address_Port2 = (ip, port);

ip      = "127.0.0.1";
port    = 18000;
sending_Address_Port3 = (ip, port);


datagramSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);

sent = datagramSocket.sendto(xml_re_encoded, sending_Address_Port1)
print ("Sending to " + str(sending_Address_Port1) + " for ATAK")

sent = datagramSocket.sendto(xml_re_encoded, sending_Address_Port2)
print ("Sending to " + str(sending_Address_Port2) + " for the COT debugger")

sent = datagramSocket.sendto(xml_re_encoded, sending_Address_Port3)
print ("Sending to " + str(sending_Address_Port3) + " for WinTAK")

datagramSocket.close()
