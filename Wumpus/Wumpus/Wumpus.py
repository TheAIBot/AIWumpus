# -*- coding: utf-8 -*-

from aiLogic import *
from wumpusGame import *


"""
    formula = Formula("!!!s1,1 <-> w1,2 || w2,1")
    print(formula.tostring())
    #print(formula.copy().tostring())

    rule1 = Rule("a <-> b", "((a -> b) && (b -> a))")
    rule2 = Rule("!!a", "a")
    #rule3 = Rule(parse("a && b"), parse("a"))

    rule1.tryRule(formula)
    rule2.tryRule(formula)
    #formula.executeRuleIfPossible(rule3)
    print(formula.tostring())
"""

rules = [
    Rule("a <-> b", "((a -> b) && (b -> a))"),
    Rule("!!a", "a"),
    Rule("a -> b", "!a || b")
]

kRules = [
    KnowlegdeRule(["a -> b", "a"], ["a", "b"]),
    KnowlegdeRule(["a && b"], ["a", "b"]),
    CNFRule(["a || b", "c || !b"], ["a || c"]),
    CNFRule(["b || a", "!b || c"], ["a || c"]),
    CNFRule(["a || b", "!b || c"], ["a || c"]),
    CNFRule(["b || a", "c || !b"], ["a || c"]),

    CNFRule(["b || a", "!b || c"], ["a"])
    #KnowlegdeRule(["a -> b", "!b"], ["!a", "!b"]),
    #KnowlegdeRule(["!(a || b)"], ["!a && !b"])
]

game = WunpusGame()
print(game.tostring())



knowledge = KnowledgeBase("""
!b1,1
b1,1 <-> p1,2 || p2,1
""")

"""
    print(knowledge.tostring())
    knowledge.tryRules(rules, kRules)
    knowledge.addKnowledge(Formula("!b1,4"))
    knowledge.tryRules(rules, kRules)
    print()
    print()
    print(knowledge.tostring())
"""


"""
    print()
    print()
    print()

    file = open("InitialKnowledgeBase.txt", "r")
    initialKnowledgeString = file.read()
    knowledge = KnowledgeBase(initialKnowledgeString)

    knowledge.addKnowledge(Formula("b1,3 && s1,3"))
    knowledge.tryRules(rules, kRules)

    print(knowledge.tostring())

    print()
    print()
    print()

    knowledge.tryRules(rules, kRules)
    print(knowledge.tostring())
"""





#kb = KnowdgeBase(....)
#kRule= KnowledgeRule([parse("a -> b"), parse("a")], [parse("b")])
#kb.inference(kRule)




























