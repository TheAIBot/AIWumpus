
from enum import Enum
import random
import re
import queue

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

class AgentState:
    def __init__(self, x, y, direction, hasGold, hasArrow):
        self.x = x
        self.y = y
        self.dir = direction
        self.hasArrow = hasGold
        self.hasGold = hasArrow

    def getAgentPos(self):
        return (self.x, self.y)

    def getNextState(self, action):
        if action == Action.Forward:
            if self.dir == 0: #East
                return AgentState(self.x + 1, self.y + 0, self.dir, self.hasGold, self.hasArrow)
            elif self.dir == 1: #South
                return AgentState(self.x + 0, self.y + 1, self.dir, self.hasGold, self.hasArrow)
            elif self.dir == 2: #West
                return AgentState(self.x - 1, self.y + 0, self.dir, self.hasGold, self.hasArrow)
            elif self.dir == 3: #North
                return AgentState(self.x + 0, self.y - 1, self.dir, self.hasGold, self.hasArrow)
            else:
                raise Exception("Invalid direction: " + self.dir)
        elif action == Action.Turn_Left:
            return AgentState(self.x, self.y, (self.dir - 1 + 4) % 4, self.hasGold, self.hasArrow)
        elif action == Action.Turn_Right:
            return AgentState(self.x, self.y, (self.dir + 1 - 4) % 4, self.hasGold, self.hasArrow)
        elif action == Action.Grab_Gold:
            return AgentState(self.x, self.y, self.dir, True, self.hasArrow)
        elif action == Action.Shoot:
            return AgentState(self.x, self.y, self.dir, self.hasGold, False)
        else:
            raise Exception("Invalid action.")

    def __eq__(self, value):
        return value and type(value) is AgentState and self.x == value.x and self.y == value.y and self.dir == value.dir

    def __ne__(self, value):
        return not self.__eq__(value)

    def __hash__(self):
        tt = (self.x, self.y, self.dir)
        return hash(tt)


class WunpusGame:
    def __init__(self):
        self.width = 4
        self.height = 4
        self.agent = AgentState(1, 1, 1, True, False)
        self.isAgentAlive = True
        self.performance = 0
        self.agentBumpedIntoWall = False
        self.wumpusJustDied = False
        self.isRunning = True
        self.visitedPositions = {self.agent.getAgentPos()}
        self.safePositions = {self.agent.getAgentPos()}
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
        self.world[0][0].agent = True

    def addEntityWithEffectToWorld(self, entity, effect):
        entityX = random.randint(1, self.width)
        entityY = random.randint(1, self.height)
        setattr(self.world[entityX - 1][entityY - 1], entity, True)
        self.addSurroundingEffects(entityX, entityY, effect)

    def getSurroundingPositions(self, x, y):
        if self.isWithinWorld(x + 1, y + 0):
            yield (x + 1, y + 0)
        if self.isWithinWorld(x - 1, y + 0):
            yield (x - 1, y + 0)
        if self.isWithinWorld(x + 0, y + 1):
            yield (x + 0, y + 1)
        if self.isWithinWorld(x + 0, y - 1):
            yield (x + 0, y - 1)

    def addSurroundingEffects(self, x, y, effect):
        for pos in self.getSurroundingPositions(x, y):
            self.addEffectIfInWorld(pos[0], pos[1], effect)

    def isWithinWorld(self, x, y):
        return x >= 1 and x <= self.width and y >= 1 and y <= self.height

    def addEffectIfInWorld(self, x, y, effect):
        if self.isWithinWorld(x, y):
            setattr(self.world[x - 1][y - 1], effect, True)

    def action(act):
        pass

    def getSensorValues(self):
        sensorValues = self.world[self.agent.x - 1][self.agent.y - 1].getSensorValues()
        if self.agentBumpedIntoWall:
            sensorValues.append("Bump")
        else:
            sensorValues.append("!Bump")
        if self.wumpusJustDied:
            sensorValues.append("Scream")
        else:
            sensorValues.append("!Scream")
        return sensorValues

    def didAgentJustDie(self):
        tile = self.world[self.agent.x - 1][self.agent.y - 1]
        return tile.wumpus or tile.pit

    def getNextAction(self, knowledge):
        glitterLiteral = "g{0},{1}".format(self.agent.x, self.agent.y)
        if not self.agent.hasGold and knowledge.resolution(glitterLiteral):
            return Action.Grab_Gold
        else:
            #If there are no safe spaces that hasn't been visited then all other spaces
            #must be certain death. The best course of action in that case is to go
            #back to spawn and exit the cave
            goBackToSpawn = self.safePositions.intersection(self.visitedPositions)


            frontier = queue.Queue()
            frontierSet = set()
            expandedSet = set()

            frontier.put((None, self.agent))
            actionBackToSpawn = None

            while not frontier.empty():
                leaf = frontier.get()

                if leaf[1] == (1, 1) and goBackToSpawn:
                    actionBackToSpan = leaf[0]
                    break

                #If the agent is in a new unknown position then stop searching
                #as the agent has found a new safe and unknown position to go to.
                if not leaf[1].getAgentPos() in self.visitedPositions:
                    return leaf[0]

                #Add children
                #Does not handle shooting
                for action in [Action.Forward, Action.Turn_Left, Action.Turn_Right]:
                    childState = self.getStateFromAction(frontierSet, expandedSet, leaf, action)
                    if childState != None:
                        statePos = childState[1].getAgentPos()
                        if statePos not in frontierSet and statePos not in expandedSet:
                            frontier.put(childState)
                            frontierSet.add(childState)
                expandedSet.add(leaf)

            if not goBackToSpawn:
                raise Exception("Searching for action to do yielded no action.")

            #If already at spawn then climb back up.
            #Otherwise take the action to go back.
            if actionBackToSpawn == None:
                return Action.Climb
            else:
                return actionBackToSpawn

    def getStateFromAction(self, frontierSet, expandedSet, parentState, Action):
        stateChild = parentState[1].getNextState(Action.Forward)
        statePos = stateChild.getAgentPos()
        if self.isWithinWorld(stateChild.x, stateChild.y) and statePos in self.safePositions:
            if parentState[0] == None:
                return (Action.Forward, stateChild)
            else:
                return (parentState[0], stateChild)
        return None

    #Does not handle shooting
    def executeAction(self, action):
        if action == Action.Climb:
            if self.agent.getAgentPos() != (1, 1):
                raise Exception("Can only climb in position (1,1).")
            self.performance += 1000
            self.isRunning = False
        elif action == Action.Grab_Gold:
            if not self.world[self.agent.x - 1][self.agent.y - 1].hasGold:
                raise Exception("Tried to grab the gold in a position that doesn't have the gold.")
            self.world[self.agent.x - 1][self.agent.y - 1].hasGold = False

        self.world[self.agent.x - 1][self.agent.y - 1].agent = False
        self.agent = self.agent.getNextState(action)
        self.world[self.agent.x - 1][self.agent.y - 1].agent = True
        self.visitedPositions.add(self.agent.getAgentPos())

        if self.didAgentJustDie():
            self.performance -= 1000

        self.performance -= 1

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
