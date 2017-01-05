"""Channel"""
 
import socket
import sys
import random
import select
import pickle
import packet
 
HOST = "127.0.0.1"  #localhost
MAGIC_NO = 0x497E



def check_port_num(port_num):
    """Requests port number from user and checks it conforms to requirements"""
    if port_num <= 1024 or port_num  >= 64000:
        sys.exit()
       
            
    
try:
    port_cs_in = int(sys.argv[1])
    port_cs_out = int(sys.argv[2])
    port_cr_in = int(sys.argv[3])
    port_cr_out = int(sys.argv[4])
    port_s_in = int(sys.argv[5])
    port_r_in = int(sys.argv[6])   
    P = float(sys.argv[7])

except ValueError:
    sys.exit()
    
check_port_num(port_cs_in)
check_port_num(port_cs_out)
check_port_num(port_cr_in)
check_port_num(port_cr_out)
check_port_num(port_s_in)
check_port_num(port_r_in)

# Getting P value
signal = 0
while signal == 0:
    if P >= 0 and P < 1:
        signal = 1

# Creating sockets:
try :
    cs_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cs_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cr_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cr_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error as err_msg :
    print("Failed to create a socket. Error Code : " + str(err_msg[0]) + " Message " + err_msg[1])
    sys.exit()
    
# Binding sockets:
cs_in.bind((HOST, port_cs_in))
cs_out.bind((HOST, port_cs_out))
cr_in.bind((HOST, port_cr_in))
cr_out.bind((HOST, port_cr_out))

# Connecting sockets:
cs_out.connect((HOST, port_s_in))
cr_out.connect((HOST, port_r_in))

input_sockets = [cs_in, cr_in]

# Entering infinite loop:
while 1:
    input_ready, output_ready, except_ready = select.select(input_sockets,[],[])
    for sock in input_ready:
        if sock == cs_in:
            rcvd_tuple = cs_in.recvfrom(1024)
            rcvd = pickle.loads(rcvd_tuple[0])
            if rcvd.magicno == MAGIC_NO:
                u = random.random()
                if u < P:
                    continue
                else:
                    cr_out.send(rcvd_tuple[0])
        elif sock == cr_in:
            rcvd_tuple = cr_in.recvfrom(1024)
            rcvd = pickle.loads(rcvd_tuple[0])
            if rcvd.magicno == MAGIC_NO:
                u = random.random()
                if u < P:
                    continue
                else:
                    cs_out.send(rcvd_tuple[0])