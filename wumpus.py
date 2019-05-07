# -*- coding: utf-8 -*-


class Node:
    def __init__(self, left, right, operator):
        self.Left = left
        self.Right = right
        self.Operator = operator
        
class Conjunction(Node):
    def calculate(self):
        leftC = self.Left.Calculate()
        rightC = self.Right.Calculate()
        return leftC and rightC
    
class Disjunction(Node):
    def calculate(self):
        leftC = self.Left.Calculate()
        rightC = self.Right.Calculate()
        return leftC or rightC
    
class Implication(Node):
    def calculate(self):
        leftC = self.Left.Calculate()
        rightC = self.Right.Calculate()
        return not (leftC and not rightC)
    
class BiImplication(Node):
    def calculate(self):
        leftC = self.Left.Calculate()
        rightC = self.Right.Calculate()
        return leftC == rightC
    
class Negation(Node):
    def calculate(self):
        leftC = self.Left.Calculate()
        return not leftC
    
½½