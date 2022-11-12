import pandas as pd
import numpy as np
import random


def getDeck(num):
    faces = ['a', 'j', 'k', 'q']
    for i in range(2, 11):
        faces.append(str(i))
    suits = ['spades', 'diamonds', 'clubs', 'hearts']

    deck = []
    for i in range(num):
        for suit in suits:
            for face in faces:
                card = [face, suit]
                deck.append(card)
    return random.shuffle(deck)


def getValue(hand):
    value = 0
    hasAce = 0
    handType = 'hard'
    for i in hand:
        face = i[0]
        # print(value)
        if face == 'j' or face == 'k' or face == 'q':
            value += 10
        elif face == 'a':
            value += 11
            hasAce += 1
            handType = 'soft'
        else:
            value += int(face)
    if hasAce > 0 and value > 21:
        for i in range(hasAce):
            value -= 10
        handType = 'hard'
    if (hand[0][0] == hand[1][0]):
        handType = 'pair'
    # print(value)
    # print(handType)
    return value, handType


def decision(dealerCard, value, type):
    dealerFace = dealerCard[0]
    if (type is True):
        if (value >= 17):
            return 's'
        elif (12 < value < 17 and dealerFace in ['2', '3', '4', '5', '6']):
            return 's'
        elif (value == 12 and dealerFace in ['4', '5', '6']):
            return 's'
        elif (value == 11):
            return 'd'
        elif (value == 10 and dealerFace in ['10', 'j', 'q', 'k', 'a']):
            return 'd'
        elif (value == 9 and dealerFace in ['3', '4', '5', '6']):
            return 'd'
        else:
            return 'h'
    else:
        if (value > 20):
            return 's'
        elif (value == 19):
            return 's'
        elif (value == 18 and dealerFace in ['2', '3', '4', '5', '6', '7', '8']):
            return 's'
        elif (value == 17 and dealerFace in ['3', '4', '5', '6']):
            return 'd'
        elif (value == 16 and dealerFace in ['3', '4', '5']):
            return 'd'
        elif (value == 15 and dealerFace in ['3', '4', '5']):
            return 'd'
        elif ((value == 14 or value == 13) and dealerFace in ['5', '6']):
            return 'd'
        else:
            return 'h'


def count():
    
    return

def bet():
    betSpread = [10,20,40,100]
    return
