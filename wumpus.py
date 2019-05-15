# -*- coding: utf-8 -*-

from aiparser import *
from ailogic import *

    
formula = parse("!!!a || b && q || z")
print(formula.tostring())

rule = Rule(parse("!!a"), parse("a"))
match = formula.findMatch(rule)
match.tostring()




























