import ServerSide
import json


def success():
	packet = {"success": True, "id": ServerSide.uniqueIdCounter}
	ServerSide.uniqueIdCounter += 1
	return bytes(json.dumps(packet), "utf8")


def matchFound(withId, name):
	packet = {"withId": withId, "name": name, "type": "match", "port": getAvailablePort()}
	return bytes(json.dumps(packet), "utf8")


def forceEnd(withId):
	packet = {"withId": withId, "result": "win", "type": "forceEnd"}
	return bytes(json.dumps(packet), "utf8")


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

def update(x, direction):
	packet = {
		"type": "s_update",
		"x": x,
		"dir": direction
	}
	return bytes(json.dumps(packet), "utf8")

def shoot(x):
	packet = {
		"type": "s_shoot",
		"x": x
	}
	return bytes(json.dumps(packet), "utf8")

def balls(balls):
	packet = {
		"type": "balls",
		"balls": balls,
		"noOfBalls": len(balls)
	}
	return bytes(json.dumps(packet), "utf8")