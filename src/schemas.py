from pony.orm import *
import os
import logging

Logger = logging.getLogger()
logging.info(os.getcwd())
sql_debug(True)
## Delete created database
#Check if database exists first.
#Make sure your working directory is insde \src or this will not
#Delete the db correctly.
if os.path.isfile(".\sqlite.db"):
	logging.info("Deleting existing sqlite.db file")
	os.remove("sqlite.db")


db = Database("sqlite", "sqlite.db", create_db=True)

class Game(db.Entity):
	gameID = PrimaryKey(int)
	numOfPlayers = Required(int, default=0)
	StartTime = Optional(str)
	EndTime = Optional(str)
	gameVariant = Required(str, default="Balanced")
	Turns = Set("Turn")
	Players = Set("Player")
	Ships = Set("Ships")
	TradingHouse = Set("TradingHouse")


class Player(db.Entity):
	gameID = Required(Game)
	playerID = Required(int)
	Turn = Set("Turn")
	playerName = Required(str)
	colonists = Required(int, default=0)
	victoryPoints = Required(int, default=0)
	victoryPointChips = Required(int, default=0)
	Doubloons = Required(int, default=0)
	#Implementing crops as an attribute since there is nothing unique about each crop aside from it's type. Craftsman/Captain can be handled with arithmetic.
	#Crop Total/running out of crops is likely handled by internal game logic/is constant
	CornOwned = Required(int, default=0)
	IndigoOwned = Required(int, default=0)
	SugarOwned = Required(int, default=0)
	TobaccoOwned = Required(int, default=0)
	CoffeeOwned = Required(int, default=0)
	Buildings = Set("Building")
	Plantations = Set("Plantation")
	PrimaryKey(gameID,playerID)


#Unavailable roles will have to be stored somewhere, maybe in the Turn table
class Turn(db.Entity):
	gameID = Required(Game)
	ActivePlayer = Required(Player)
	#Ticks up on every distinct game action/subsequent db write
	EventNum = Required(int)
	#Cycles once each new governor round
	RoundNum = Required(int)
	#Cycles once each new role phase/move
	#Changing to Move to be consistent with PR log terminology
	MoveNum = Required(int)
	#Cycles once each new player turn within a role
	TurnNum = Required(int)
	# Keeps track of consecutive actions within a turn, or 
	# in other words, relative actions to turn. 
	# This allows the turnNum attribute to track the passing
	# of the initiative between players within a move.
	ActionNum = Required(int)
	EventType = Required(str)
	Action = Required(str)
	Ships = Set("Ships")
	Building = Set("Building")
	Plantation = Set("Plantation")
	TradingHouse = Set("TradingHouse")
	#Governor = Required(Player, reverse="playerName")
	PrimaryKey(gameID,EventNum)

	

# Game id is included in ownerID Foreign key
class Building(db.Entity):
	ownerID = Required(Player)
	buildingID = Required(int)
	Turn = Required(Turn)
	activated = Required(bool, default=False)
	PrimaryKey(ownerID,buildingID,Turn)
	

# Game id is included in ownerID Foreign key
class Plantation(db.Entity):
	ownerID = Required(Player)
	plantationID = Required(int)
	#Turn should be required, setting to Optional temporarily so I don't break PRParser right now
	Turn = Optional(Turn)
	plantationType = Required(str)
	activated = Required(bool, default=False)
	PrimaryKey(ownerID,plantationID)


class Ships(db.Entity):
	gameID = Required(Game)
	shipID = Required(int)
	Capacity = int
	CropType = str
	CropNum = int
	Turn = Required(Turn)
	PrimaryKey(gameID,shipID,Turn)

class TradingHouse(db.Entity):
	gameID = Required(Game)
	Turn = Required(Turn)
	Crop1 = str
	Crop2 = str
	Crop3 = str
	Crop4 = str


# TURN ON DEBUGGING
sql_debug(False)

db.generate_mapping(create_tables=True)
