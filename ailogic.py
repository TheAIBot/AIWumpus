# -*- coding: utf-8 -*-

class Formula:
    def __init__(self, formula):
        self.formula = formula
        
    def tostring(self):
        return self.formula.tostring()
    
    def findMatch(self, rule):
        return self.formula.matchesRule(rule.before.formula)
    
class Rule:
    def __init__(self, before, after):
        self.before = before
        self.after = after
    
    def executeRule(self, node):
        return None

class Node:
    def __init__(self, left, right, operator):
        self.Left = left
        self.Right = right
        self.Operator = operator
    def tostring(self):
        return "(" + self.Left.tostring() + " " + self.Operator + " " + self.Right.tostring() + ")"
    def matchesRule(self, node):
        if type(node) is Value:
            return self
        print(type(self))
        print(type(node))
        if type(self) != type(node):
            return None
        elif self.Left.matchesRule(node.Left) == None or self.Right.matchesRule(node.Right) == None:
            return None
        return self
        
class Conjunction(Node):
    def calculate(self, truth):
        leftC = self.Left.Calculate()
        rightC = self.Right.Calculate()
        return leftC and rightC
    
class Disjunction(Node):
    def calculate(self, truth):
        leftC = self.Left.Calculate()
        rightC = self.Right.Calculate()
        return leftC or rightC
    
class Implication(Node):
    def calculate(self, truth):
        leftC = self.Left.Calculate()
        rightC = self.Right.Calculate()
        return not (leftC and not rightC)
    
class BiImplication(Node):
    def calculate(self, truth):
        leftC = self.Left.Calculate()
        rightC = self.Right.Calculate()
        return leftC == rightC
    
class Negation(Node):
    def calculate(self, truth):
        leftC = self.Left.Calculate()
        return not leftC
    def tostring(self):
        return "(" + self.Operator + self.Left.tostring() + ")"
    def matchesRule(self, node):
        if type(node) is Value:
            return self
        if type(self) != type(node):
            return None
        elif self.Left.matchesRule(node.Left) == None:
            return None
        return self

class Value(Node):
    def __init__(self, name):
        Node.__init__(self, None, None, None)
        self.name = name
    
    def calculate(self, truth):
        return truth[self.name]
    def tostring(self):
        return self.name
    def isSame(self, node):
        raise Exception("not allowed to compare values between different equations")






















