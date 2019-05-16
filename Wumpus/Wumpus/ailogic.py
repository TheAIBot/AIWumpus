# -*- coding: utf-8 -*-

class Formula:
    def __init__(self, formula):
        self.formula = formula
        
    def tostring(self):
        return self.formula.tostring()
    
    def findRuleMatch(self, rule):
        return self.formula.matchesRule(rule.before.formula, False)
    
    def copy(self):
        return Formula(self.formula.copy())
    
    def getValueNode(self, name):
        return self.formula.getValueNode(name)
    
    @staticmethod
    def replaceSubFormula(formula, node, replaceWith):
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
    def __init__(self, before, after):
        self.before = before
        self.after = after

class KnowlegdeRule:
    def __init__(self, befores, afters):
        self.befores = befores
        self.afters = afters



class Node:

    def __init__(self, left, right, operator):
        self.Left = left
        self.Right = right
        self.Operator = operator
        self.parent = None
        if self.Left != None:
            self.Left.parent = self
        if self.Right != None:
            self.Right.parent = self
    def tostring(self):
        return "(" + self.Left.tostring() + " " + self.Operator + " " + self.Right.tostring() + ")"
    def matchesRule(self, node, startedMatching):
        if startedMatching and type(node) is Value:
            return self
        
        if type(self) == type(node):
            if self.Left.matchesRule(node.Left, True) != None or self.Right.matchesRule(node.Right, True) != None:
                return self
        
        leftMatch = self.Left.matchesRule(node, False)
        if leftMatch != None:
            return leftMatch
        
        rightMatch = self.Right.matchesRule(node, False)
        if rightMatch != None:
            return rightMatch
        return None
    def createReplaceTable(self, node, replacer):
        if type(node) is Value:
            replacer[node.name] = self
            return
            
        self.Left.createReplaceTable(node.Left, replacer)
        self.Right.createReplaceTable(node.Right, replacer)
    def getValueNode(self, name):
        leftValue = self.Left.getValueNode(name)
        if leftValue != None:
            return leftValue
        
        rightValue = self.Right.getValueNode(name)
        if rightValue != None:
            return rightValue
        return None
            
        
class Conjunction(Node):
    def calculate(self, truth):
        leftC = self.Left.Calculate()
        rightC = self.Right.Calculate()
        return leftC and rightC
    def copy(self):
        return Conjunction(self.Left.copy(), self.Right.copy(), self.Operator)
    
class Disjunction(Node):
    def calculate(self, truth):
        leftC = self.Left.Calculate()
        rightC = self.Right.Calculate()
        return leftC or rightC
    def copy(self):
        return Disjunction(self.Left.copy(), self.Right.copy(), self.Operator)
    
class Implication(Node):
    def calculate(self, truth):
        leftC = self.Left.Calculate()
        rightC = self.Right.Calculate()
        return not (leftC and not rightC)
    def copy(self):
        return Implication(self.Left.copy(), self.Right.copy(), self.Operator)
    
class BiImplication(Node):
    def calculate(self, truth):
        leftC = self.Left.Calculate()
        rightC = self.Right.Calculate()
        return leftC == rightC
    def copy(self):
        return BiImplication(self.Left.copy(), self.Right.copy(), self.Operator)
    
class Negation(Node):
    def calculate(self, truth):
        leftC = self.Left.Calculate()
        return not leftC
    def tostring(self):
        return "(" + self.Operator + self.Left.tostring() + ")"
    def matchesRule(self, node, startedMatching):
        if startedMatching and type(node) is Value:
            return self
        if type(self) == type(node):
            if self.Left.matchesRule(node.Left, True) != None:
                return self
            
        leftMatch = self.Left.matchesRule(node, False)
        if leftMatch != None:
            return leftMatch
        return None
    
    def createReplaceTable(self, node, replacer):
        if type(node) is Value:
            replacer[node.name] = self
            return
            
        self.Left.createReplaceTable(node.Left, replacer)
    def copy(self):
        return Negation(self.Left.copy(), None, self.Operator)
    def getValueNode(self, name):
        leftValue = self.Left.getValueNode(name)
        if leftValue != None:
            return leftValue
        return None

class Value(Node):
    def __init__(self, name):
        Node.__init__(self, None, None, None)
        self.name = name
    
    def calculate(self, truth):
        return truth[self.name]
    def tostring(self):
        return self.name
    def matchesRule(self, node, startedMatching):
        if type(node) is Value:
            return self
        return None
    def createReplaceTable(self, node, replacer):
        if type(node) is Value:
            replacer[node.name] = self
    def copy(self):
        return Value(self.name)
    def getValueNode(self, name):
        if self.name == name:
            return self
        return None






















