import socket
from threading import Thread
import json

serverIp = '127.0.0.1'
port = 4590


def send_tcp_packet(packet):
    sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sck.settimeout(3.0)
    sck.connect((serverIp, port))
    sck.send(packet)


def connectPacket(username):
    packet = {'ip': get_ip(), 'name': username, 'type': 'connect'}
    return bytes(json.dumps(packet) + '\n', 'utf8')


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


def send_connection(username):
    send_tcp_packet(connectPacket(username))
