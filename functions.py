#coding:utf-8

def addMessage(message):
    with open('message.txt', 'a') as fic:
        fic.write(message)

def getMessages():
    with open('message.txt', 'r') as fic:
        return fic.read()