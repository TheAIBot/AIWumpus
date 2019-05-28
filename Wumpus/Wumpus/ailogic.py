# -*- coding: utf-8 -*-

from aiLogicNodes import *
from aiParser import *
from os import linesep
import re
import itertools

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
        return self.formula.isSame(formula.formula)
    
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
        self.onlyLookAtRoot = True

        for before in befores:
            self.befores.append(Formula(before, True))
        for after in afters:
            self.afters.append(Formula(after, True))

    def findMatches(self, index, replacer, formulasToRemove, knowledgeBase, usedFormulas):
        before = self.befores[index]
        actualBefore = before.copy()
        Formula.replaceValuesWithFormulas(actualBefore, replacer)

        for formula in knowledgeBase.knowledge:
            alreadyUsed = False
            for used in usedFormulas:
                if formula.isSame(used):
                    alreadyUsed = True
                    break
            if alreadyUsed:
                continue

            match = formula.findPatternMatch(actualBefore.formula, self.onlyLookAtRoot)
            if match == None:
                continue
            
            newReplacer = {}
            match.createReplaceTable(actualBefore.formula, newReplacer)
            
            combinedReplacer = dict(replacer)
            combinedReplacer.update(newReplacer)
            if index + 1 == len(self.befores):
                replacer.update(newReplacer)
                formulasToRemove.append(formula)
                return True
            else:
                usedFormulas.append(formula)
                if self.findMatches(index + 1, combinedReplacer, formulasToRemove, knowledgeBase, usedFormulas):
                    replacer.update(newReplacer)
                    formulasToRemove.append(formula)
                    return True
                usedFormulas.pop()
        return False

    def tryRule(self, knowledgeBase):
        replacer = {}
        formulasToRemove = []
        if not self.findMatches(0, replacer, formulasToRemove, knowledgeBase, []):
            return False

        for toRemove in formulasToRemove:
            knowledgeBase.knowledge.remove(toRemove)

        for after in self.afters:
            afterFormula = after.copy()
            Formula.replaceValuesWithFormulas(afterFormula, replacer)
            knowledgeBase.addKnowledge(afterFormula)

        return True

class RevisionRule(KnowlegdeRule):
    def __init__(self, befores, afters):
        KnowlegdeRule.__init__(self, befores, afters)
        self.onlyLookAtRoot = False

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

    def addKnowledge(self, formula):
        if any(x.isSame(formula) for x in self.knowledge):
            return
        self.knowledge.append(formula)

    def tryRules(self, rules, knowledgeRules):
        anyRulesUsed = False
        while True:
            usedRule = False
            for rule in rules:
                if self.tryRule(rule):
                    usedRule = True
            for kRule in knowledgeRules:
                if self.tryKnowledgeRule(kRule):
                    usedRule = True
            anyRulesUsed = anyRulesUsed or usedRule
            if not usedRule:
                break
        return anyRulesUsed

    def resolve(self, formula1, formula2):
        resolvants = [formula1, formula2]
        for literal in formula1:
            lookFor = literal
            if literal[0] == '!':
                lookFor = literal[1:]
            else:
                lookFor = "!" + literal

            if lookFor in formula2:
                r = list(formula1) + list(formula2)
                r.remove(literal)
                r.remove(lookFor)
                if len(r) == 0:
                    return None, True
                else:
                    resolvants.append(frozenset(r))
        return resolvants, False


    def resolution(self, alpha):
        #First negate alpha
        negate = Rule("a", "!a")
        doubleNegElim = Rule("!!a", "a")
        if not negate.tryRule(alpha):
            raise Exception("Failed to execute negation rule.")
        doubleNegElim.tryRule(alpha)

        clauses = set()
        for formula in self.knowledge:
            literals = [e.strip() for e in formula.tostring().split("||")]
            clauses.add(frozenset(literals))

        clauses.add(frozenset([e.strip() for e in alpha.tostring().split("||")]))

        while True:
            clauseCount = len(clauses)
            cl = clauses.copy()
            counter = 0
            #Creates all pairs
            for pair in itertools.combinations(cl, 2):
                counter += 1
                resolvants, res = self.resolve(pair[0], pair[1])
                if res:
                    return True
                clauses.update(resolvants)
            if len(clauses) == clauseCount:
                return False
























