import random
import pickle
from datetime import datetime
from typing import List
from simple_colors import *


class Deck:
    def __init__(self, num, bankRoll):
        self.decksNum = num
        self.deckCards = self.newShoe()
        self.roundCards = []
        self.bankRoll = bankRoll
        self.rawCount = 0
        self.cardsDealt = 0
        self.decksLeft = num

    def newShoe(self):
        faces = ["a", "j", "k", "q"]
        for i in range(2, 11):
            faces.append(str(i))
        suits = ["spades", "diamonds", "clubs", "hearts"]

        deck = []
        for i in range(self.decksNum):
            for suit in suits:
                for face in faces:
                    card = [face, suit]
                    deck.append(card)
        random.shuffle(deck)
        return deck

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

    def getTrueCount(self):
        if self.cardsDealt == 0:
            return 0
        else:
            return round(self.rawCount / self.decksLeft)

    def endRound(self):
        self.roundCards = []

    def reshuffle(self):
        self.deckCards = self.newShoe()
        self.rawCount = 0
        self.cardsDealt = 0
        self.decksLeft = self.decksNum


class PlayerRound:
    def __init__(self, isDealer: bool):
        self.isDealer = isDealer
        self.hand = []
        self.handType = "hard"
        self.value = 0
        self.betAmt = 0
        self.isComplete = False
        self.choices = []

    def toString(self):
        string = "is dealer: " + str(self.isDealer) + "\n"
        string += "is complete: " + str(self.isComplete) + "\n"
        string += "hand type: " + self.handType + "\n"
        string += "value: " + str(self.value) + "\n"
        string += "hand: " + str(self.hand) + "\n"
        string += "bet: " + str(self.betAmt) + "\n"
        string += "choices: " + str(self.choices) + "\n"
        return string

    def recordChoice(self, choice):
        self.choices.append(choice)

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
        if value > 21:
            self.isComplete = True
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
                    return "h"
            elif self.hand[0][0] == "6":
                if dealerCard[0] in ["2", "3", "4", "5", "6"]:
                    return "split"
                else:
                    return "h"
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
            if self.handType == "hard":
                return "s"
            else:
                return "h"

    def clearHand(self):
        self.hand = []
        self.handType = "hard"
        self.value = 0
        self.betAmt = 0
        self.choices = []
        self.isComplete = False


class Round:
    def __init__(self, deck: Deck, numPlayers: int, betSpread):
        self.dealer: PlayerRound = PlayerRound(True)
        self.players: List[PlayerRound] = []
        self.dealerCard = None
        self.deck = deck
        self.betSpread = betSpread
        self.deck
        for i in range(numPlayers):
            self.players.append(PlayerRound(False))

    def toString(self):
        string = "\nstart action"
        print(blue(string, ["bold", "underlined"]))
        for i in range(len(self.players)):
            string = "dealer card: " + str(self.dealerCard) + "\n"
            string += "Player " + str(i) + ":\n"
            string += self.players[i].toString() + "\n"
            if i == 0:
                print(green(string))
            elif i == 1:
                print(yellow(string))
            elif i == 2:
                print(blue(string))
            elif i == 3:
                print(red(string))
        print(blue("dealer: "))
        print(blue(self.dealer.toString()))
        return

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
        self.deck.count(self.deck.roundCards[:-1])

    def playIndex(self, num):
        try:
            assert self.dealerCard != None
        except Exception as e:
            print(red("dealer card is empty!"))
            raise (e)

        playerHand = self.players[num]
        if playerHand.isComplete == True:
            return playerHand

        else:
            decision = playerHand.decision(self.dealerCard)
            if decision == "h":
                playerHand.recordChoice("hit")
                card = self.deck.drawCard()
                playerHand.addCardHand(card)
                playerHand.getValue()
                return playerHand
            elif decision == "d":
                playerHand.recordChoice("double")
                playerHand.bet(playerHand.betAmt)
                card = self.deck.drawCard()
                playerHand.addCardHand(card)
                playerHand.getValue()
                playerHand.isComplete = True
                return playerHand
            elif decision == "s":
                playerHand.recordChoice("stand")
                playerHand.isComplete = True
                return playerHand
            elif decision == "split":
                playerHand.recordChoice("split")
                betValue = playerHand.betAmt
                firstCard = playerHand.hand[0]
                secondCard = playerHand.hand[1]
                playerHand.betAmt = 0
                playerHand.isComplete = True

                hand1 = PlayerRound(False)
                hand1.addCardHand(firstCard)
                card = self.deck.drawCard()
                hand1.addCardHand(card)
                hand1.bet(betValue)
                hand1.getValue()
                hand1.recordChoice("was split to")
                self.players.append(hand1)

                hand2 = PlayerRound(False)
                hand2.addCardHand(secondCard)
                card = self.deck.drawCard()
                hand2.addCardHand(card)
                hand2.bet(betValue)
                hand2.getValue()
                hand2.recordChoice("was split to")
                self.players.append(hand2)

                self.players.pop(num)
                return playerHand

            return playerHand

    def play(self):
        startingLength = len(self.players)
        for i in range(startingLength):
            self.playIndex(i)

    def dealerPlay(self):
        self.dealer.getValue()
        if self.dealer.isComplete == True:
            return
        decision = self.dealer.dealerDecision()
        if decision == "s":
            self.dealer.recordChoice("stand")
            self.dealer.isComplete = True
        elif decision == "h":
            self.dealer.recordChoice("hit")
            card = self.deck.drawCard()
            self.dealer.addCardHand(card)
            self.dealerPlay()

    def roundPlay(self):
        # print(self.deck.roundCards)
        while True:
            endRound = True
            for player in self.players:
                if player.isComplete == False:
                    endRound = False
            if endRound == True:
                break
            self.play()
        self.dealerPlay()
        self.toString()
        # print(self.deck.roundCards)
        return "end round"

    def payout(self):
        if self.dealer.value == 21 and len(self.dealer.hand) == 2:
            for player in self.players:
                self.deck.bankRoll -= player.betAmt
        else:
            counter = 0
            for player in self.players:
                counter += 1
                if player.value > self.dealer.value or self.dealer.value > 21:
                    print(
                        "Player " + str(counter) + ": Won Amount " + str(player.betAmt)
                    )
                    self.deck.bankRoll += player.betAmt * 2
                else:
                    print(
                        "Player " + str(counter) + ": Lost Amount " + str(player.betAmt)
                    )
            print("Balance:" + str(self.deck.bankRoll))

        # count the dealer's second card
        print("Cards Dealt: " + str(self.deck.roundCards))
        self.deck.count(self.deck.roundCards[-1:])
        print("Running Count: " + str(self.deck.rawCount))
        print("Decks left: " + str(self.deck.decksLeft))
        print("True Count: " + str(self.deck.getTrueCount()))
        # clear the deck roundCards
        self.deck.endRound()
        return


class Table:
    def __init__(
        self,
        playerNum: int,
        deckSize: int,
        bankRoll: int,
        betSpread: dict,
        shuffleFraction: float,
    ):
        self.deck = Deck(deckSize, bankRoll)
        self.initial_size = len(self.deck.deckCards)
        self.shuffle_fraction = shuffleFraction
        self.playerNum = playerNum
        self.betSpread = betSpread
        self.log: list[dict] = []
        # dict keys are round #, Shoe Progression, Running Count, True Count, Decks Left, Balance, Bets, Hands

    def createLog(self, round: int):
        bets = []
        hands = []
        for player in self.cards.players:
            bets.append(player.betAmt)
            hands.append(player.hand)
        log_dict = {
            "Round Num": round,
            "Shoe Progression": self.progression_fraction,
            "Decks Left": self.cards.deck.decksLeft,
            "Running Count": self.cards.deck.rawCount,
            "True Count": self.cards.deck.getTrueCount(),
            "Balance": self.cards.deck.bankRoll,
            "Bets": bets,
            "Hands": hands,
        }
        return log_dict

    def checkDeck(self):
        self.progression_fraction = len(self.deck.deckCards) / self.initial_size
        # update the deck with the len(self.deck.deckCards) /52
        self.cards.deck.decksLeft = round(
            self.progression_fraction * self.initial_size / 52
        )
        print("Shoe progression " + str(self.progression_fraction))
        if self.progression_fraction <= self.shuffle_fraction:
            print(red("\nSHUFFLE DECK", ["bold"]))
            self.deck.reshuffle()

    def playRounds(self, numberRounds: int):
        for i in range(numberRounds):
            print(blue("\nRound " + str(i + 1), ["bold", "underlined"]))
            self.cards = Round(self.deck, self.playerNum, self.betSpread)
            self.cards.deal()
            self.cards.bet()
            self.cards.roundPlay()
            self.cards.payout()
            self.checkDeck()
            self.log.append(self.createLog(i))

    def outputLog(self):
        file = open(
            "blackjack_num_players_"
            + str(self.playerNum)
            + "_num_decks_"
            + str(int(self.initial_size / 52))
            + "_shuffle_fraction_"
            + str(self.shuffle_fraction)
            + "_"
            + str(int(datetime.timestamp(datetime.now())*10**6))
            + ".pkl",
            "wb",
        )
        pickle.dump(self.log, file)
        file.close()
