# -*- coding: utf-8 -*-

from enum import Enum
from aiLogicNodes import *
        
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
    def __init__(self, type: TokenType, text: str):
        self.tokenType = type
        self.text = text
    
        
class Scanner:
    def __init__(self, text: str):
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
            while self.char.isalpha() or self.char.isdigit() or self.char == ',':
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
        
    def have(self, lookingForType: TokenType):
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
        
    

def parse(text: str):
    scanner = Scanner(text)
    return biImpExpression(scanner)
    
def biImpExpression(scanner: Scanner):
    left = impExpression(scanner)
    while scanner.have(TokenType.BI_IMP):
        left = BiImplication(left, biImpExpression(scanner), "<->")
        
    return left
    
def impExpression(scanner: Scanner):
    left = orExpression(scanner)
    while scanner.have(TokenType.IMP):
        left = Implication(left, impExpression(scanner), "->")
        
    return left
    
def orExpression(scanner: Scanner):
    left = andExpression(scanner)
    while scanner.have(TokenType.OR):
        left = Disjunction(left, orExpression(scanner), "||")
        
    return left

def andExpression(scanner: Scanner):
    left = notExpression(scanner)
    while scanner.have(TokenType.AND):
        left = Conjunction(left, andExpression(scanner), "&&")
        
    return left
    

def notExpression(scanner: Scanner):
    left = None
    while scanner.have(TokenType.NEG):
        left = Negation(notExpression(scanner), None, "!")
    if left == None:
        left = parExpression(scanner)
        
    return left

def parExpression(scanner: Scanner):
    left = valExpression(scanner)
    if scanner.have(TokenType.PAR_START):
        left = biImpExpression(scanner)
        if not scanner.have(TokenType.PAR_END):
            raise Exception("No closing parenthesis")
    if left == None:
        raise Exception("Invalid expression")
        
    return left
    
def valExpression(scanner: Scanner):
    token = scanner.see()
    if token.tokenType == TokenType.VAL:
        scanner.have(TokenType.VAL)
        return Value(token.text)
    else:
        return None