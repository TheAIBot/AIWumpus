# -*- coding: utf-8 -*-

from aiLogicNodes import *
from aiParser import *
from os import linesep
import re

class Formula:
    def __init__(self, formula, makeValueNamesIllegal = False):
        if isinstance(formula, Node):
            self.formula = formula
        else:
            self.formula = parse(formula)

        if makeValueNamesIllegal:
            values = []
            self.formula.getValues(values)
            for valueNode in values:
                valueNode.name = "###" + valueNode.name
        
    def tostring(self):
        return self.formula.tostring()
    
    def findPatternMatch(self, pattern, onlyMatchRoot):
        return self.formula.matchesRule(pattern, False, onlyMatchRoot)

    def isSame(self, formula):
        return self.findPatternMatch(formula.formula, True)
    
    def copy(self):
        return Formula(self.formula.copy())
    
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

    @staticmethod
    def replaceValuesWithFormulas(formula, replacer: dict):
        for valueName in replacer:
            node = formula.getValueNode(valueName)
            while node != None:
                Formula.replaceSubFormula(formula, node, replacer[valueName].copy())
                node = formula.getValueNode(valueName)


class Rule:
    def __init__(self, before: str, after: str):
        self.before = Formula(before, True)
        self.after = Formula(after, True)

    def tryRule(self, formula):
        match = formula.findPatternMatch(self.before.formula, False)
        if match == None:
            return False
        
        replacer = {}
        match.createReplaceTable(self.before.formula, replacer)
        
        Formula.replaceSubFormula(formula, match, self.after.formula.copy())
            
        Formula.replaceValuesWithFormulas(formula, replacer)

        return True

class KnowlegdeRule:
    def __init__(self, befores, afters):
        self.befores = []
        self.afters = []

        for before in befores:
            self.befores.append(Formula(before, True))
        for after in afters:
            self.afters.append(Formula(after, True))

    def tryRule(self, knowledgeBase):
        replacer = {}
        formulasToRemove = []
        for before in self.befores:
            actualBefore = before.copy()
            Formula.replaceValuesWithFormulas(actualBefore, replacer)

            foundMatch = False
            for formula in knowledgeBase.knowledge:
                match = formula.findPatternMatch(actualBefore.formula, True)
                if match == None:
                    continue
            
                foundMatch = True
                match.createReplaceTable(actualBefore.formula, replacer)
                formulasToRemove.append(formula)
                break;

            #Failed to find on the the formulas in the knowledge base
            if not foundMatch:
                return False

        for toRemove in formulasToRemove:
            knowledgeBase.knowledge.remove(toRemove)

        for after in self.afters:
            afterFormula = after.copy()
            Formula.replaceValuesWithFormulas(afterFormula, replacer)
            knowledgeBase.knowledge.append(afterFormula)

        return True




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

    def copy(self):
        return KnowledgeBase(self.tostring())

    def tryRule(self, rule):
        didRule = False
        for formula in self.knowledge:
            while rule.tryRule(formula):
                didRule = True
        return didRule

    def tryKnowledgeRule(self, rule):
        didRule = False
        while rule.tryRule(self):
            didRule = True
        return didRule




















