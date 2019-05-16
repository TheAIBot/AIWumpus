# -*- coding: utf-8 -*-

from aiLogicNodes import *
from aiParser import *
from os import linesep
import re

class Formula:
    def __init__(self, formulaString: str):
        self.formula = parse(formulaString)
        
    def tostring(self):
        return self.formula.tostring()
    
    def findRuleMatch(self, rule):
        return self.formula.matchesRule(rule.before.formula, False)
    
    def copy(self):
        return Formula(self.formula.tostring())
    
    def getValueNode(self, name: str):
        return self.formula.getValueNode(name)
    
    @staticmethod
    def replaceSubFormula(formula, node: Node, replaceWith: Node):
        if node.parent != None:
            parent = node.parent
            if parent.Left == node:
                parent.Left = replaceWith
                parent.Left.parent = parent
            elif parent.Right == node:
                parent.Right = replaceWith
                parent.Right.parent = parent
            else:
                raise Exception("Failed to find correct node")
        else:
            formula.formula = replaceWith

    def executeRuleIfPossible(self, rule):
        match = self.findRuleMatch(rule)
        if match == None:
            return None
        
        replacer = {}
        match.createReplaceTable(rule.before.formula, replacer)
        
        Formula.replaceSubFormula(self, match, rule.after.formula.copy())
            
        for valueName in replacer:
            node = self.getValueNode(valueName)
            while node != None:
                Formula.replaceSubFormula(self, node, replacer[valueName].copy())
                node = self.getValueNode(valueName)

class Rule:
    def __init__(self, before: str, after: str):
        self.before = Formula(before)
        self.after = Formula(after)

class KnowlegdeRule:
    def __init__(self, befores, afters):
        self.befores = befores
        self.afters = afters

class KnowledgeBase:
    def __init__(self, knowledge: str):
        self.knowledge = []
        formulaStrings = knowledge.splitlines()
        for formulaString in formulaStrings:
            #Remove comments
            formulaString = re.sub("#.*", "", formulaString)
            #Don't add if the string is empty
            if  formulaString:
                self.knowledge.append(Formula(formulaString))

    def tostring(self):
        formulaStrings = []
        for formula in self.knowledge:
            formulaStrings.append(formula.tostring())
        return linesep.join(formulaStrings)




















