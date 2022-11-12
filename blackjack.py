import pandas as pd
import numpy as np
import random
from typing import List, Dict


class Deck:
    def __init__(self, num, bankRoll):
        faces = ["a", "j", "k", "q"]
        for i in range(2, 11):
            faces.append(str(i))
        suits = ["spades", "diamonds", "clubs", "hearts"]

        deck = []
        for i in range(num):
            for suit in suits:
                for face in faces:
                    card = [face, suit]
                    deck.append(card)
        random.shuffle(deck)
        self.deckCards = deck
        self.roundCards = []
        self.bankRoll = bankRoll
        self.rawCount = 0
        self.cardsDealt = 0

    def drawCard(self):
        card = self.deckCards.pop()
        self.roundCards.append(card)
        return card

    def count(self, cards):
        currentCount = 0
        for card in cards:
            if card[0] in ["10", "j", "k", "q", "a"]:
                currentCount -= 1
            elif card[0] in ["2", "3", "4", "5", "6"]:
                currentCount += 1
            else:
                currentCount += 0
        self.rawCount += currentCount
        self.cardsDealt += len(cards)
        self.roundCards = []

    def getTrueCount(self):
        if self.cardsDealt == 0:
            return 0
        else:
            return round(self.rawCount / self.cardsDealt)

    def endRound(self):
        self.roundCards = []


class PlayerRound:
    def __init__(self, isDealer: bool):
        self.isDealer = isDealer
        self.hand = []
        self.handType = "hard"
        self.value = 0
        self.betAmt = 0

    def toString(self):
        string = "is dealer: " + str(self.isDealer) + "\n"
        string += "hand type: " + self.handType + "\n"
        string += "value: " + str(self.value) + "\n"
        string += "hand: " + str(self.hand) + "\n"
        string += "bet: " + str(self.betAmt) + "\n"
        print(string)
        return string

    def bet(self, value: int):
        self.betAmt = self.betAmt + value

    def addCardHand(self, card):
        self.hand.append(card)

    def getValue(self):
        value = 0
        hasAce = 0
        handType = "hard"
        for i in self.hand:
            face = i[0]
            if face == "j" or face == "k" or face == "q":
                value += 10
            elif face == "a":
                value += 11
                hasAce += 1
                handType = "soft"
            else:
                value += int(face)
        if hasAce > 0 and value > 21:
            for i in range(hasAce):
                value -= 10
            handType = "hard"
        if self.hand[0][0] == self.hand[1][0] and len(self.hand) == 2:
            handType = "pair"
        # print(value)
        # print(handType)
        self.value = value
        self.handType = handType
        return value, handType

    def decision(self, dealerCard):
        dealerFace = dealerCard[0]
        if self.handType == "hard":
            if self.value >= 17:
                return "s"
            elif 12 < self.value < 17 and dealerFace in ["2", "3", "4", "5", "6"]:
                return "s"
            elif self.value == 12 and dealerFace in ["4", "5", "6"]:
                return "s"
            elif self.value == 11:
                return "d"
            elif self.value == 10 and dealerFace in ["10", "j", "q", "k", "a"]:
                return "d"
            elif self.value == 9 and dealerFace in ["3", "4", "5", "6"]:
                return "d"
            else:
                return "h"
        elif self.handType == "soft":
            if self.value > 20:
                return "s"
            elif self.value == 19:
                return "s"
            elif self.value == 18 and dealerFace in ["2", "3", "4", "5", "6", "7", "8"]:
                return "s"
            elif self.value == 17 and dealerFace in ["3", "4", "5", "6"]:
                return "d"
            elif self.value == 16 and dealerFace in ["3", "4", "5"]:
                return "d"
            elif self.value == 15 and dealerFace in ["3", "4", "5"]:
                return "d"
            elif (self.value == 14 or self.value == 13) and dealerFace in ["5", "6"]:
                return "d"
            else:
                return "h"
        else:
            if self.hand[0][0] == "a":
                return "split"
            elif self.hand[0][0] in ["10", "k", "q", "j"]:
                print("s")
                return "s"
            elif self.hand[0][0] == "9":
                if dealerCard[0] in ["2", "3", "4", "5", "6", "8", "9"]:
                    return "split"
                else:
                    return "s"
            elif self.hand[0][0] == "8":
                return "split"
            elif self.hand[0][0] == "7":
                if dealerCard[0] in ["2", "3", "4", "5", "6", "7"]:
                    return "split"
                else:
                    "h"
            elif self.hand[0][0] == "6":
                if dealerCard[0] in ["2", "3", "4", "5", "6"]:
                    return "split"
                else:
                    "h"
            elif self.hand[0][0] == "5":
                if dealerCard[0] in ["10", "a", "j", "q", "k"]:
                    return "h"
                else:
                    return "d"
            elif self.hand[0][0] == "4":
                if dealerCard[0] in ["5", "6"]:
                    return "split"
                else:
                    return "h"
            elif self.hand[0][0] == "3" or self.hand[0][0] == "2":
                if dealerCard[0] in ["2", "3", "4", "5", "6", "7"]:
                    return "split"
                else:
                    return "h"

    def dealerDecision(self):
        value, type = self.getValue()
        if value < 17:
            return "h"
        else:
            return "s"

    def clearHand(self):
        self.hand = []
        self.handType = "hard"
        self.value = 0
        self.betAmt = 0


class Round:
    def __init__(self, deck: Deck, numPlayers: int, betSpread):
        self.dealer = PlayerRound(True)
        self.players: List[PlayerRound] = []
        self.dealerCard = None
        self.deck = deck
        self.betSpread = betSpread
        for i in range(numPlayers):
            self.players.append(PlayerRound(False))

    def bet(self):
        if self.deck.getTrueCount() <= 2:
            betValue = self.betSpread[2]
        elif self.deck.getTrueCount() == 3:
            betValue = self.betSpread[3]
        elif self.deck.getTrueCount() == 4:
            betValue = self.betSpread[4]
        elif self.deck.getTrueCount() >= 5:
            betValue = self.betSpread[5]
        for player in self.players:
            self.deck.bankRoll -= betValue
            player.bet(betValue)

    def deal(self):
        for i in range(2):
            card = self.deck.drawCard()
            self.dealer.addCardHand(card)
        for i in range(len(self.players)):
            for j in range(2):
                card = self.deck.drawCard()
                self.players[i].addCardHand(card)
        self.dealerCard = self.dealer.hand[0]
        self.dealer.getValue()
        for i in range(len(self.players)):
            self.players[i].getValue()

    def playIndex(self, num):
        try:
            assert self.dealerCard != None
        except Exception as e:
            print('dealer card is empty!')
            raise(e)
        playerHand = self.players[num]
        decision = playerHand.decision(self.dealerCard)
        if decision == 'h':
            card = self.deck.drawCard()
            playerHand.addCardHand(card)
    
        elif decision == 'd':
            playerHand.bet(playerHand.betAmt)

        elif decision == 's':
            return playerHand
        elif decision == 'split':
            self.players.pop(num)
            split1 = pop
        return playerHand
    
    def play(self):
