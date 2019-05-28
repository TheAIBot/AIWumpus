# -*- coding: utf-8 -*-

from ailogic import *
from wumpusGame import *

rules = [
    #not, imp and bicond elimination
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
knowledge.tryRules(rules, kRules)


#Make random game and show it
game = WunpusGame()
print(game.tostring())
alive = True
visitedSquares = [[game.agentX, game.agentY]]
safeSquares = [[game.agentX, game.agentY]]
unsafeSquares = [[]]

#Add sense knowledge to kb
while(alive):
    #if agent is at same position as wumpus or pit
        alive = False
        print("you are dead")
        break
    
    for sensed in game.getSensorValues():
        knowledge.addKnowledge(Formula(sensed))
    
    #Do resolution
    
    #Check if next square is safe. I think we just as a first priority check 
    #the agentX+1 square. If it is not in visitedSquares, and not in unsafe
    #Squares, we do resolution on it. If it is safe, no wumpus or pit, we go
    #it. Next priority is agentY+1, then agentX-1 and at last agentY-1. 
    #We also need to check, that we don't do resolution on a wall.
    #The if below is how resolution should be done, perhaps there is a more
    #efficient way. 
    if(knowledge.resolution("!p{0},{1}".format(game.agentX, game.agentY))):
        knowledge.addKnowledge(Formula("!p2,1"))
        if (knowledge.resolution("!w2,1")):
            knowledge.addKnowledge(Formula("!w2,1"))
            #Update agent position
            #AddToSafeSquares
        else:
            knowledge.addKnowledge(Formula("w2,1"))
            #AddToUnsafeSquares
    else:
        knowledge.addKnowledge(Formula("p2,1"))
        #AddToUnsafeSquares
        if (knowledge.resolution("!w2,1")):
            knowledge.addKnowledge(Formula("!w2,1"))
        else:
            knowledge.addKnowledge("w2,1")
            
    #I have made a updateWorld function, that just updates the position of the
    #agent, when a move have been made
    game.updateWorld()


#So resolve works but it's incredible slow the result is False.
#This is caused by the fact that all possible combination of
#formulas has to be created and that is in this case
#millions of formulas.
#print(knowledge.resolution("!p2,2"))

#Do revision
knowledge.revision("w1,1")

#print knowledge base
#print(knowledge.tostring())
