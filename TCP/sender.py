"""Sender"""

import socket   #for sockets
import sys      #for exit
import os.path  #for checking filename
import pickle   #for converting packet to and from bytes
import packet

HOST = "127.0.0.1"  #localhost
MAGIC_NO = 0x497E
DATA_PACKET = 0
ACK_PACKET = 1



def check_port_num(port_num):
    """Requests port number from user and checks it conforms to requirements"""
    if port_num <= 1024 or port_num  >= 64000:
        sys.exit()
                
try:
    port_s_in = int(sys.argv[1])
    port_s_out = int(sys.argv[2])
    port_cs_in = int(sys.argv[3])
    filename = sys.argv[4]
except ValueError:
    sys.exit()
    
check_port_num(port_s_in)
check_port_num(port_s_out)
check_port_num(port_cs_in)

# Getting filename of file to be sent and checking it exists:
if os.path.isfile(filename) is False:
    print("File does not exist. Exiting Sender program.\n")
    sys.exit()
 
 
    # Creating dgram udp sockets:
try:
    s_in =socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print("Failed to create socket")
    sys.exit()

# Binding both ports:
s_in.bind((HOST, port_s_in))
s_out.bind((HOST, port_s_out))

# Connecting s_out to cs_in:
s_out.connect((HOST, port_cs_in))

# Setting timeout:
s_in.settimeout(1.0)



# Converting file into bytes:
original_file = open(filename, 'rb')
remaining_bytes = original_file.read()

# Initialising local variables:
next_seq_no = 0
packets_sent = 0
exitFlag = False

# Processing file, 512 bytes at a time and placing into packets
while 1:
    if len(remaining_bytes) >= 512:
        n = 512
    else:
        n = len(remaining_bytes)
    if n == 0:
        new_packet = packet.Packet(MAGIC_NO, DATA_PACKET, next_seq_no, 0, None)
        exitFlag = True
    else:
        data_buffer = remaining_bytes[:n]
        new_packet = packet.Packet(MAGIC_NO, DATA_PACKET, next_seq_no, n, data_buffer)
        remaining_bytes = remaining_bytes[n:]

    # Sending each packet:
    packet_buffer = pickle.dumps(new_packet)
    acknowledged = False
    while acknowledged is False:
        s_out.send(packet_buffer)
        packets_sent += 1
        try:
            rcvd_tuple = s_in.recvfrom(1024)
            rcvd = pickle.loads(rcvd_tuple[0])
            if rcvd.magicno == MAGIC_NO and rcvd.packType == ACK_PACKET and rcvd.dataLen == 0:
                if rcvd.seqno == next_seq_no:
                    next_seq_no = 1 - next_seq_no
                    acknowledged = True
                    if exitFlag is True:
                        original_file.close()
                        s_in.close()
                        s_out.close()
                        print("Number of packets sent is: " + str(packets_sent))
                        sys.exit()
        except socket.timeout:
            continue
