
"""Receiver"""

import socket   #for sockets
import sys      #for exit
import os.path  #for checking filename
import pickle   #for converting packet to and from bytes
import packet
import select

HOST = "127.0.0.1"  #localhost
MAGIC_NO = 0x497E
DATA_PACKET = 0
ACK_PACKET = 1



def check_port_num(port_num):
    """Requests port number from user and checks it conforms to requirements"""
    if port_num <= 1024 or port_num  >= 64000:
        sys.exit()

            
    
try:
    port_r_in = int(sys.argv[1])
    port_r_out = int(sys.argv[2])
    port_cr_in = int(sys.argv[3])  
    filename = sys.argv[4]

except ValueError:
    sys.exit()
    
check_port_num(port_r_in)
check_port_num(port_r_out)
check_port_num(port_cr_in)


# Creating dgram udp sockets:
try:
    r_in =socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    r_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print("Failed to create socket")
    sys.exit()

# Binding both ports:
r_in.bind((HOST, port_r_in))
r_out.bind((HOST, port_r_out))

# Connecting s_out to cs_in:
r_out.connect((HOST, port_cr_in))

# Getting filename of file to be copied to and checking it doesn't already exist:

if os.path.isfile(filename) is True:
    print("File already exists. Exiting Receiver program.\n")
    sys.exit()

# Opening new file:
new_file = open(filename, 'wb')

exp_seq_no = 0
input_sockets = [r_in]

# Entering loop:
while 1:
    input_ready, output_ready, except_ready = select.select(input_sockets,[],[])
    d_new = r_in.recvfrom(1024)
    rcvd = pickle.loads(d_new[0])
    if rcvd.magicno == MAGIC_NO and rcvd.packType == DATA_PACKET:
        new_packet = packet.Packet(MAGIC_NO, ACK_PACKET, rcvd.seqno, 0, None)
        packet_buffer = pickle.dumps(new_packet)
        r_out.send(packet_buffer)
        if rcvd.seqno == exp_seq_no:
            exp_seq_no = 1 - exp_seq_no
            if rcvd.dataLen > 0:
                new_data = rcvd.data
                new_file.write(new_data)
            else:
                new_file.close()
                r_in.close()
                r_out.close()
                sys.exit()