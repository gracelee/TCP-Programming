import sys
import packet
import pickle
import pac

MAGIC_NO = 0x497E
DATA_PACKET = 0

the_file = open("copy",'rb')
data = the_file.read(512)


#myPack = packet.Packet(MAGIC_NO, DATA_PACKET, 0, 512, data)
tupled = (0x497E,0,0,512,data)
dPack = pickle.dumps(tupled)



print("Size of bytes:")
print(sys.getsizeof(tupled))
print("Size of packet:")
print(sys.getsizeof(dPack))

