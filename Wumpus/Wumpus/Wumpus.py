# -*- coding: utf-8 -*-

from aiLogic import *
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

#Add sense knowledge to kb
for sensed in game.getSensorValues():
    knowledge.addKnowledge(Formula(sensed))

#Do resolution
print(knowledge.resolution("!p2,1"))
print(knowledge.resolution("!p1,2"))

#So resolve works but it's incredible slow the result is False.
#This is caused by the fact that all possible combination of
#formulas has to be created and that is in this case
#millions of formulas.
#print(knowledge.resolution("!p2,2"))

#Do revision
knowledge.revision("w1,1")

#print knowledge base
print(knowledge.tostring())




























