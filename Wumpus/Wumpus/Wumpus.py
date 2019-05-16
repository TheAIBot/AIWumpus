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



#kb = KnowdgeBase(....)
#kRule= KnowledgeRule([parse("a -> b"), parse("a")], [parse("b")])
#kb.inference(kRule)




























