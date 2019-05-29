# -*- coding: utf-8 -*-

from aiLogic import *
from wumpusGame import *

rules = [
    #imp, not and bicond elimination
    Rule("a <-> b", "((a -> b) && (b -> a))"),
    Rule("!!a", "a"),
    Rule("a -> b", "!a || b"),

    #Note that these two rules are duplicates of each other.
    #This is neede because the formula tree differentiates between left and right
    #and a formula does not. Essentially the tree will only match one of the rules
    #depending on which side the or is on.
    Rule("a || (b && c)", "((a || b) && (a || c))"),
    Rule("(b && c) || a", "((a || b) && (a || c))"),

    #De Morgan
    Rule("!(a || b)", "(!a && !b)")
]

#Rule to split a cnf up into clauses
kRules = [
    KnowlegdeRule(["a && b"], ["a", "b"]),
]



#Load knowledge base from file
file = open("InitialKnowledgeBase.txt", "r")
initialKnowledgeString = file.read()
knowledge = KnowledgeBase(initialKnowledgeString)

#Convert knowledge base into cnf and then into clauses
#print(knowledge.tostring())
knowledge.tryRules(rules, kRules)
#print(knowledge.tostring())


#Make random game and show it
game = WunpusGame()
print(game.tostring())

#Add sense knowledge to kb
while(game.isRunning):

    #if agent is at same position as wumpus or pit
    if game.didAgentJustDie():
        break
    
    for sensed in game.getSensorValues():
        knowledge.revision(sensed)
    
    #Do resolution on each adjacant position. Check whether the adjacant
    #position doesn't have a pit and not a wumpus. If that's the case then
    #it must be a safe position. After a resolution is true the knowledge
    #is added to the knowledge base so it's faster to do resolution
    #in the future.
    for pos in game.getSurroundingPositions(game.agent.x, game.agent.y):
        if not pos in game.visitedPositions:
            notPitLiteral = "!p{0},{1}".format(pos[0], pos[1])
            notWumpusLiteral = "!w{0},{1}".format(pos[0], pos[1])
            if knowledge.resolution(notPitLiteral):
                knowledge.addKnowledge(Formula(notPitLiteral))
                if knowledge.resolution(notWumpusLiteral):
                    knowledge.addKnowledge(Formula(notWumpusLiteral))
                    game.safePositions.add(pos)

    #Choose an action
    action = game.getNextAction(knowledge)

    #Do action
    game.executeAction(action)
    print(game.tostring())

print("Game ended")
if game.didAgentJustDie():
    print("The agent died")
print("Performance: " + game.performance)


#So resolve works but it's incredible slow the result is False.
#This is caused by the fact that all possible combination of
#formulas has to be created and that is in this case
#millions of formulas.
#print(knowledge.resolution("!p2,2"))

#Do revision
knowledge.revision("w1,1")

#print knowledge base
#print(knowledge.tostring())
