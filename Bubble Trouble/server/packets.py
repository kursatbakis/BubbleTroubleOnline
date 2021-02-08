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
def levelInit(r_lives, balls, x, rivalx, wait=3):
	packet = {
		"bg": "background.jpg",
		"type": "levelInit",
		"r_lives": r_lives,
		"balls": balls,
		"noOfBalls": len(balls),
		"initialX": x,
		"r_initialX": rivalx,
		"wait": wait,
	}
	return bytes(json.dumps(packet), "utf8")


# position update every few milliseconds
def update(x, direction, shooting, shield):
	packet = {
		"type": "s_update",
		"x": x,
		"dir": direction,
		"shooting": shooting,
		"shield": shield
	}
	return bytes(json.dumps(packet), "utf8")


# if someone shoots, send to the peer.
def hitBall(remove, left, right):
	packet = {
		"type": "s_shoot",
		"remove": remove,
		"left": left,
		"right": right
	}
	return bytes(json.dumps(packet), "utf8")


#if someone dies, send to peer.
def dead(remaining):
	packet = {
		"type": "dead",
		"remaining": remaining
	}
	return bytes(json.dumps(packet), "utf8")
