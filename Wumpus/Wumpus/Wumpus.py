# -*- coding: utf-8 -*-

from aiparser import *
from ailogic import *

    
formula = parse("s11 <-> w12 || w21")
print(formula.tostring())
#print(formula.copy().tostring())

rule1 = Rule(parse("a <-> b"), parse("((a -> b) && (b -> a))"))
rule2 = Rule(parse("!!a"), parse("a"))
#rule3 = Rule(parse("a && b"), parse("a"))



formula.executeRuleIfPossible(rule1)
formula.executeRuleIfPossible(rule2)
#formula.executeRuleIfPossible(rule3)
print(formula.tostring())



#kb = KnowdgeBase(....)
#kRule= KnowledgeRule([parse("a -> b"), parse("a")], [parse("b")])
#kb.inference(kRule)




























