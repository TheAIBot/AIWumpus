# -*- coding: utf-8 -*-

from aiparser import *
from ailogic import *

    
formula = parse("!!!a || b && q || z")
print(formula.tostring())
print(formula.copy().tostring())

rule = Rule(parse("!!a"), parse("a"))

formula.executeRuleIfPossible(rule)
print(formula.tostring())



#kb = KnowdgeBase(....)
#kRule= KnowledgeRule([parse("a -> b"), parse("a")], [parse("b")])
#kb.inference(kRule)




























