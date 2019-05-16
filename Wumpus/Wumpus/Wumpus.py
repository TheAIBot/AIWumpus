# -*- coding: utf-8 -*-

from aiLogic import *

    
formula = Formula("s1,1 <-> w1,2 || w2,1")
print(formula.tostring())
#print(formula.copy().tostring())

rule1 = Rule("a <-> b", "((a -> b) && (b -> a))")
rule2 = Rule("!!a", "a")
#rule3 = Rule(parse("a && b"), parse("a"))

formula.executeRuleIfPossible(rule1)
formula.executeRuleIfPossible(rule2)
#formula.executeRuleIfPossible(rule3)
print(formula.tostring())



print()
print()
print()
knowledge = KnowledgeBase("""
g1,1 <-> gold1,1
g1,2 <-> gold1,2
g1,3 <-> gold1,3
g1,4 <-> gold1,4
g2,1 <-> gold2,1
g2,2 <-> gold2,2
g2,3 <-> gold2,3
g2,4 <-> gold2,4
g3,1 <-> gold3,1
g3,2 <-> gold3,2
g3,3 <-> gold3,3
g3,4 <-> gold3,4
g4,1 <-> gold4,1
g4,2 <-> gold4,2
g4,3 <-> gold4,3
g4,4 <-> gold4,4

b1,1 <-> p1,2 || p2,1
b1,2 <-> p1,1 || p2,2 || p1,3
b1,3 <-> p1,2 || p2,3 || p1,4
b1,4 <-> p1,3 || p2,4
b2,1 <-> p1,1 || p2,2 || p3,1
b2,2 <-> p1,2 || p2,3 || p2,1 || p3,2
b2,3 <-> p1,3 || p2,4 || p2,2 || p3,3
b2,4 <-> p1,4 || p2,3 || p3,4
b3,1 <-> p2,1 || p3,2 || p4,1
b3,2 <-> p3,1 || p2,2 || p3,3 || p4,2
b3,3 <-> p3,2 || p2,3 || p3,4 || p4,3
b3,4 <-> p3,3 || p2,4 || p4,4
b4,1 <-> p3,1 || p4,2
b4,2 <-> p4,1 || p3,2 || p4,3
b4,3 <-> p4,2 || p3,3 || p4,4
b4,4 <-> p3,4 || p4,3

s1,1 <-> w1,2 || w2,1
s1,2 <-> w1,1 || w2,2 || w1,3
s1,3 <-> w1,2 || w2,3 || w1,4
s1,4 <-> w1,3 || w2,4
s2,1 <-> w1,1 || w2,2 || w3,1
s2,2 <-> w1,2 || w2,3 || w2,1 || w3,2
s2,3 <-> w1,3 || w2,4 || w2,2 || w3,3
s2,4 <-> w1,4 || w2,3 || w3,4
s3,1 <-> w2,1 || w3,2 || w4,1
s3,2 <-> w3,1 || w2,2 || w3,3 || w4,2
s3,3 <-> w3,2 || w2,3 || w3,4 || w4,3
s3,4 <-> w3,3 || w2,4 || w4,4
s4,1 <-> w3,1 || w4,2
s4,2 <-> w4,1 || w3,2 || w4,3
s4,3 <-> w4,2 || w3,3 || w4,4
s4,4 <-> w3,4 || w4,3

w1,1 || w1,2 || w1,3 || w1,4 || w2,1 || w2,2 || w2,3 || w2,4 || w3,1 || w3,2 || w3,3 || w3,4 || w4,1 || w4,2 || w4,3 || w4,4
""")
print(knowledge.tostring())



#kb = KnowdgeBase(....)
#kRule= KnowledgeRule([parse("a -> b"), parse("a")], [parse("b")])
#kb.inference(kRule)




























