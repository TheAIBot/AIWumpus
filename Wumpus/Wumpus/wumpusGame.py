
from enum import Enum
import random
import re

random.seed(3)

class Action(Enum):
    Forward = 1,
    Turn_Left = 2,
    Turn_Right = 3,
    Grab_Gold = 4,
    Shoot = 5,
    Climb = 6

class Tile:
    def __init__(self, x, y):
        self.posX = x
        self.posY = y
        self.pit = False
        self.breeze = False
        self.wumpus = False
        self.stench = False
        self.gold = False
        self.glitter = False
        self.agent = False

    def makeEffectName(self, effect):
        return effect + str(self.posX + 1) + "," + str(self.posY + 1)

    def getSensorValues(self):
        sensor = []
        if self.stench:
            sensor.append(self.makeEffectName("s"))
        else:
            sensor.append(self.makeEffectName("!s"))

        if self.breeze:
            sensor.append(self.makeEffectName("b"))
        else:
            sensor.append(self.makeEffectName("!b"))

        if self.glitter:
            sensor.append(self.makeEffectName("g"))
        else:
            sensor.append(self.makeEffectName("!g"))
        return sensor

    def toPitString(self):
        if self.pit:
            return "p"
        elif self.breeze:
            return "b"
        else:
            return " "
    def toWumpusString(self):
        if self.wumpus:
            return "w"
        elif self.stench:
            return "s"
        else:
            return " "
    def toGoldString(self):
        if self.gold:
            return "g"
        else:
            return " "
    def toAgentString(self):
        if self.agent:
            return "a"
        else:
            return " "


class WunpusGame:
    def __init__(self):
        self.width = 4
        self.height = 4
        self.agentX = 1
        self.agentY = 1
        self.agentDir = 1
        self.agentHasArrow = True
        self.agentHasGold = False
        self.performance = 0
        self.agentBumpedIntoWall = False
        self.wumpusJustDied = False
        self.generateRandomWorld()

    def generateRandomWorld(self):
        self.world = []
        for x in range(self.width):
            self.world.append([])
            for y in range(self.height):
                self.world[x].append(Tile(x, y))

        for x in range(self.width):
            for y in range(self.height):
                pitX = x + 1
                pitY = y + 1
                #starting pos can't be a pit
                if not (pitX == 1 and pitY == 1):
                    if random.randint(1, 10) <= 2:
                        self.world[x][y].pit = True
                        self.addSurroundingEffects(pitX, pitY, "breeze")

        self.addEntityWithEffectToWorld("gold", "glitter")
        self.addEntityWithEffectToWorld("wumpus", "stench")
        self.addEntityWithEffectToWorld("wumpus", "stench")
        self.addEntityWithEffectToWorld("agent", " ")

    def addEntityWithEffectToWorld(self, entity, effect):
        if (entity == "agent"):
            entityX = self.agentX
            entityY = self.agentY
        else:
            entityX = random.randint(1, self.width)
            entityY = random.randint(1, self.height)
        setattr(self.world[entityX - 1][entityY - 1], entity, True)
        if (entity == "wumpus"):
            self.addSurroundingEffects(entityX, entityY, effect)

    def addSurroundingEffects(self, x, y, effect):
        self.addEffectIfInWorld(x + 1, y + 0, effect)
        self.addEffectIfInWorld(x - 1, y + 0, effect)
        self.addEffectIfInWorld(x + 0, y + 1, effect)
        self.addEffectIfInWorld(x + 0, y - 1, effect)

    def addEffectIfInWorld(self, x, y, effect):
        if x + 1 >= 1 and x <= self.width and y >= 1 and y <= self.height:
            setattr(self.world[x - 1][y - 1], effect, True)

    def action(act):
        pass

    def getSensorValues(self):
        sensorValues = self.world[self.agentX - 1][self.agentY - 1].getSensorValues()
        if self.agentBumpedIntoWall:
            sensorValues.append("Bump")
        else:
            sensorValues.append("!Bump")
        if self.wumpusJustDied:
            sensorValues.append("Scream")
        else:
            sensorValues.append("!Scream")
        return sensorValues

    def tostring(self):
        stringsWorld = []
        for y in range(self.height + 2):
            stringsWorld.append("")

        for i in range(4):
            for x in range(self.width + 2):
                stringsWorld[0] += "#"
            stringsWorld[0] += " "

        for y in range(self.height):
            stringsWorld[y + 1] += "#"
            for x in range(self.width):
                stringsWorld[y + 1] += self.world[x][y].toPitString()
            stringsWorld[y + 1] += "# #"
            for x in range(self.width):
                stringsWorld[y + 1] += self.world[x][y].toWumpusString()
            stringsWorld[y + 1] += "# #"
            for x in range(self.width):
                stringsWorld[y + 1] += self.world[x][y].toGoldString()
            stringsWorld[y + 1] += "# #"
            for x in range(self.width):
                stringsWorld[y + 1] += self.world[x][y].toAgentString()
            stringsWorld[y + 1] += "#"

        for i in range(4):
            for y in range(self.width + 2):
                stringsWorld[len(stringsWorld) - 1] += "#"
            stringsWorld[len(stringsWorld) - 1] += " "

        stringsWorld = [" Pits  Wumpus  Gold   Agent"] + stringsWorld
        return "\n".join(stringsWorld)
