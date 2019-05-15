# -*- coding: utf-8 -*-

from enum import Enum


class Node:
    def __init__(self, left, right, operator):
        self.Left = left
        self.Right = right
        self.Operator = operator
    def tostring(self):
        return "(" + self.Left.tostring() + " " + self.Operator + " " + self.Right.tostring() + ")"
        
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

class Value(Node):
    def __init__(self, name):
        Node.__init__(self, None, None, None)
        self.name = name
    
    def calculate(self, truth):
        return truth[self.name]
    def tostring(self):
        return self.name
        
class TokenType(Enum):
    AND = 1
    OR = 2
    IMP = 3
    BI_IMP = 4
    NEG = 5
    VAL = 6
    PAR_START = 7
    PAR_END = 8
    END = 9
    
class Token:
    def __init__(self, type, text):
        self.tokenType = type
        self.text = text
    
        
class Scanner:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.char = text[self.pos]
        
    def nextChar(self):
        self.pos = self.pos + 1
        if len(self.text) <= self.pos:
            self.char = '\0'
        else:
            self.char = self.text[self.pos]
     
    def getToken(self):
        while self.char == ' ':
            self.nextChar()
        
        if self.char == '|':
            self.nextChar()
            if self.char == '|':
                self.nextChar()
                return Token(TokenType.OR, None)
        elif self.char == '&':
            self.nextChar()
            if self.char == '&':
                self.nextChar()
                return Token(TokenType.AND, None)
        elif self.char == '-':
            self.nextChar()
            if self.char == '>':
                self.nextChar()
                return Token(TokenType.IMP, None)
        elif self.char == '<':
            self.nextChar()
            if self.char == '-':
                self.nextChar()
                if self.char == '>':
                    self.nextChar()
                    return Token(TokenType.BI_IMP, None)
        elif self.char == '!':
            self.nextChar()
            return Token(TokenType.NEG, None)
        elif self.char.isalpha():
            buffer = self.char
            self.nextChar()
            while self.char.isalpha():
                buffer = buffer+ self.char
                self.nextChar()
            return Token(TokenType.VAL, buffer)
        elif self.char == '(':
            self.nextChar()
            return Token(TokenType.PAR_START, None)
        elif self.char == ')':
            self.nextChar()
            return Token(TokenType.PAR_END, None)
        elif self.char == '\0':
            return Token(TokenType.END, None)
        else:
            raise Exception("character was not recognized: " + self.char)
        
    def see(self):
        if len(self.text) <= self.pos:
            return Token(TokenType.END, None)
        
        curPos = self.pos
        token = self.getToken()
        #print(token.tokenType)
        self.pos = curPos
        self.char = self.text[self.pos]
        
        return token
        
    def have(self, lookingForType):
        if len(self.text) <= self.pos:
            return False
        
        curPos = self.pos
        token = self.getToken()
        #print(token.tokenType)
        if token.tokenType == lookingForType:
            return True
        
        self.pos = curPos
        self.char = self.text[self.pos]
        return False
        
    

def parse(text):
    scanner = Scanner(text)
    return biImpExpression(scanner)
    
def biImpExpression(scanner):
    left = impExpression(scanner)
    while scanner.have(TokenType.BI_IMP):
        left = BiImplication(left, impExpression(scanner), "<->")
        
    return left
    
def impExpression(scanner):
    left = orExpression(scanner)
    while scanner.have(TokenType.IMP):
        left = Implication(left, orExpression(scanner), "->")
        
    return left
    
def orExpression(scanner):
    left = andExpression(scanner)
    while scanner.have(TokenType.OR):
        left = Disjunction(left, andExpression(scanner), "||")
        
    return left

def andExpression(scanner):
    left = notExpression(scanner)
    while scanner.have(TokenType.AND):
        left = Conjunction(left, notExpression(scanner), "&&")
        
    return left
    

def notExpression(scanner):
    left = None
    while scanner.have(TokenType.NEG):
        left = Negation(parExpression(scanner), None, "!")
    if left == None:
        left = parExpression(scanner)
        
    return left

def parExpression(scanner):
    left = valExpression(scanner)
    if scanner.have(TokenType.PAR_START):
        left = biImpExpression(scanner)
        if not scanner.have(TokenType.PAR_END):
            raise Exception("No closing parenthesis")
    if left == None:
        raise Exception("Invalid expression")
        
    return left
    
def valExpression(scanner):
    token = scanner.see()
    if token.tokenType == TokenType.VAL:
        scanner.have(TokenType.VAL)
        return Value(token.text)
    else:
        return None
    
ast = parse("!a || b && q || z")
print(ast.tostring())




























