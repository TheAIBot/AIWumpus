# -*- coding: utf-8 -*-

from aiLogic import *


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
    Rule("!!a", "a")
]

kRules = [
    KnowlegdeRule(["a -> b", "a"], ["a", "b"]),
    KnowlegdeRule(["a && b"], ["a", "b"]),
    KnowlegdeRule(["a -> b", "!b"], ["!a", "!b"]),
    KnowlegdeRule(["!(a || b)"], ["!a && !b"])
]



knowledge = KnowledgeBase("""
!b1,1
b1,1 <-> p1,2 || p2,1
""")

print(knowledge.tostring())
knowledge.tryRules(rules, kRules)
print()
print()
print(knowledge.tostring())

"""
    print()
    print()
    print()

    file = open("InitialKnowledgeBase.txt", "r")
    initialKnowledgeString = file.read()
    knowledge = KnowledgeBase(initialKnowledgeString)
    print(knowledge.tostring())

    print()
    print()
    print()

    knowledge.tryRule(rule1)
    #knowledge.tryRule(rule2)
    #knowledge.tryKnowledgeRule(kRule)
    print(knowledge.tostring())
"""



#kb = KnowdgeBase(....)
#kRule= KnowledgeRule([parse("a -> b"), parse("a")], [parse("b")])
#kb.inference(kRule)




























