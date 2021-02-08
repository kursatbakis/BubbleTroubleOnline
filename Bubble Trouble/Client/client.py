import select, socket
import json
from threading import Thread

port = 2181

def connectPacket():
	d = {"ip": my_ip, "name": username, "type": "connect"}
	return bytes(json.dumps(d), "utf8")

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def broadcastPacket(packet):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(('', 0))
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	sock.sendto(packet, ('<broadcast>', port))
	sock.close()

def listen_udp():


my_ip = get_ip()
username = 'tester'
print(my_ip)
broadcastPacket(connectPacket())

listen_udp()