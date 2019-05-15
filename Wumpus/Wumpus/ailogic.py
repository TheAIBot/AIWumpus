# -*- coding: utf-8 -*-

class Formula:
    def __init__(self, formula):
        self.formula = formula
        
    def tostring(self):
        return self.formula.tostring()
    
    def findRuleMatch(self, rule):
        return self.formula.matchesRule(rule.before.formula)
    
    def copy(self):
        return Formula(self.formula.copy())
    
    def getValueNode(self, name):
        return self.formula.getValueNode(name)
    
    def executeRuleIfPossible(self, rule):
        match = self.findRuleMatch(rule)
        if match == None:
            return None
        
        replacer = {}
        match.createReplaceTable(rule.before.formula, replacer)
        
        if match.parent != None:
            parent = match.parent
            if parent.Left == match:
                parent.Left = rule.after.formula.copy()
                parent.Left.parent = parent
            elif parent.Right == match:
                parent.Right = rule.after.formula.copy()
                parent.Right.parent = parent
            else:
                raise Exception("Failed to find correct node")
        else:
            self.formula = rule.after.formula.copy()
            
        for valueName in replacer:
            node = self.getValueNode(valueName)
            while node != None:
                if node.parent == None:
                    self.formula = replacer[valueName]
                else:
                    parent = node.parent
                    if parent.Left == node:
                        parent.Left = replacer[valueName]
                        parent.Left.parent = parent
                    elif parent.Right == node:
                        parent.Right = replacer[valueName]
                        parent.Right.parent = parent
                    else:
                        raise Exception("Failed to find correct node")
                node = self.getValueNode(valueName)
            

    
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
        self.parent = None
        if self.Left != None:
            self.Left.parent = self
        if self.Right != None:
            self.Right.parent = self
    def tostring(self):
        return "(" + self.Left.tostring() + " " + self.Operator + " " + self.Right.tostring() + ")"
    def matchesRule(self, node):
        if type(node) is Value:
            return self
        
        if type(self) == type(node):
            if self.Left.matchesRule(node.Left) != None or self.Right.matchesRule(node.Right) != None:
                return self
        
        leftMatch = self.Left.matchesRule(node.Left)
        if leftMatch != None:
            return leftMatch
        
        rightMatch = self.Right.matchesRule(node.Right)
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
    def matchesRule(self, node):
        if type(node) is Value:
            return self
        if type(self) == type(node):
            if self.Left.matchesRule(node.Left) != None:
                return self
            
        leftMatch = self.Left.matchesRule(node.Left)
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
    def matchesRule(self, node):
        if type(node) is Value:
            return self
        raise Exception("not allowed to compare values between different equations")
    def createReplaceTable(self, node, replacer):
        if type(node) is Value:
            replacer[node.name] = self
    def copy(self):
        return Value(self.name)
    def getValueNode(self, name):
        if self.name == name:
            return self
        return None






















