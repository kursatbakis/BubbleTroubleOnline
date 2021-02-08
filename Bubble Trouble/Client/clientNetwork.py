import socket
from threading import Thread
import json
from window import setPlayerId, matchFound, forceEnd, levelStart, rivalDied


serverIp = '192.168.1.35'
port = 2181
udpSock = None
playerId = None

def send_tcp_packet(packet):
    sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sck.settimeout(3.0)
    sck.connect((serverIp, port))
    sck.send(packet)
    sck.close()


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


def send_udp_packet(packet):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 0))
    sock.sendto(packet, (serverIp, port))
    sock.close()


def send_match_request():
    send_tcp_packet(searchForMatchPacket(id))


def send_connect_packet(username):
    send_tcp_packet(connectPacket(username))

def listenByUdp():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(('', port))
        # s.setblocking(0)
        result = select.select([s], [], [])
        while True:
            msg = result[0][0].recv(1024)
            data = json.loads(msg.decode('utf8'))
            if data['type'] == 'level':
                rivallives = data['r_lives']
                balls = data['balls']
                noOfBalls = data['noOfBalls']
                initialX = data['initialX']
                r_initialX = data['r_initialX']
                wait = data['wait']
                levelStart(rivallives, balls, noOfBalls, initialX, r_initialX, wait)
            elif data['type'] == 'dead':
                id = data['id']
                remaining = data['remaining']
                if id == playerId:
                    continue

            elif data['type'] == 's_update':
                pass
            elif data['type'] == 's_shoot':
                pass
            elif data['type'] == 'balls':
                pass


def listenByTcp():
    global playerId
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', port))
        s.listen()
        conn, addr = s.accept()
        while True:
            content = conn.recv(1024).decode('utf-8')
            if content:
                content = json.loads(content)
                if 'success' in content: # basari ile servera baglandik demektir.match request atilacak
                    send_match_request(content['id'])
                    setPlayerId(content['id'])
                    playerId = content['id']
                elif content['type'] == 'match': # match bulundu oyuna basla demektir
                    matchFound(content['name'], content['port'], content['withId'])
                    print('match arrives')
                elif content['type'] == 'forceEnd':
                    forceEnd()



####  WITH TCP ####
def searchForMatchPacket(id1):
    pack = {"id": id1, "type": "enqueue"}
    return bytes(json.dumps(pack) + '\n', 'utf8')


def connectPacket(username):
    pack = {'ip': get_ip(), 'name': username, 'type': 'connect'}
    return bytes(json.dumps(pack) + '\n', 'utf8')


def goodbyePacket(id):
    pack = {'id': id, 'type': 'goodbye'}
    return bytes(json.dumps(pack) + '\n', 'utf8')


#### WITH UDP (GAME MECHANICS) ####

def coordinatesPacket(id, gameId, x, dir):
    packet = {'id': id, 'gameId': gameId, 'x': x, 'dir': dir, type: 'update'}
    return bytes(json.dumps(packet) + '\n', 'utf8')


def deadPacket(id):
    packet = {'id': id, 'type': 'dead'}
    return bytes(json.dumps(packet) + '\n', 'utf8')


def shootPacket(id, x):
    packet = {'id': id, 'x': x, 'type': 'shoot'}
    return bytes(json.dumps(packet) + '\n', 'utf8')



