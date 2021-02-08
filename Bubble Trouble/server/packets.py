import json

# send to everyone who connects to server
def success(uniqueId):
	packet = {"success": True, "id": uniqueId}
	return bytes(json.dumps(packet), "utf8")


# send to both players
def matchFound(withId, name, port):
	packet = {"withId": withId, "name": name, "type": "match", "port": port}
	return bytes(json.dumps(packet), "utf8")


# if a player loses connection or leaves the game, send to the peer.
def forceEnd(withId):
	packet = {"withId": withId, "type": "forceEnd"}
	return bytes(json.dumps(packet), "utf8")


# send before the match starts to BOTH players.
def levelInit(level, r_lives, balls, x, rivalx, wait, minX, maxX):
	packet = {
		"bg": "bg" + level + ".jpg",
		"time": 60,
		"type": "levelInit",
		"level": level,
		"r_lives": r_lives,
		"balls": balls,
		"noOfBalls": len(balls),
		"initialX": x,
		"r_initialX": rivalx,
		"wait": wait,
		"minX": minX,
		"maxX": maxX
	}
	return bytes(json.dumps(packet), "utf8")


# position update every few milliseconds

def update(id, x, direction, shooting, shield):
	packet = {
		"type": "s_update",
		"id": id,
		"x": x,
		"dir": direction
	}
	return bytes(json.dumps(packet), "utf8")


# if someone shoots, send to the peer.
def shoot(x):
	packet = {
		"type": "s_shoot",
		"x": x
	}
	return bytes(json.dumps(packet), "utf8")


# balls
def balls(_balls):
	packet = {
		"type": "balls",
		"balls": _balls,
		"noOfBalls": len(_balls)
	}
	return bytes(json.dumps(packet), "utf8")

#if someone dies, send to peer.

def dead(id, remaining):
	packet = {
		"type": "dead",
		"id": id,
		"remaining": remaining
	}
	return bytes(json.dumps(packet), "utf8")
