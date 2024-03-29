import blackjack
from simple_colors import *

hands = []
dealers = []
corrects = []

hands.append([["5", "hearts"], ["10", "hearts"]])
dealers.append(["j", "hearts"])
corrects.append("h")

hands.append([["q", "hearts"], ["a", "hearts"]])
dealers.append(["8", "hearts"])
corrects.append("s")

hands.append([["q", "hearts"], ["a", "hearts"]])
dealers.append(["8", "hearts"])
corrects.append("s")

hands.append([["j", "hearts"], ["a", "hearts"]])
dealers.append(["4", "hearts"])
corrects.append("s")

hands.append([["k", "hearts"], ["k", "hearts"]])
dealers.append(["8", "hearts"])
corrects.append("s")

hands.append([["j", "hearts"], ["a", "hearts"]])
dealers.append(["4", "hearts"])
corrects.append("s")

hands.append([["3", "hearts"], ["2", "hearts"]])
dealers.append(["a", "hearts"])
corrects.append("h")

hands.append([["7", "hearts"], ["8", "hearts"]])
dealers.append(["3", "hearts"])
corrects.append("s")

hands.append([["6", "hearts"], ["q", "hearts"]])
dealers.append(["4", "hearts"])
corrects.append("s")

hands.append([["2", "hearts"], ["5", "hearts"]])
dealers.append(["2", "hearts"])
corrects.append("h")

hands.append([["q", "hearts"], ["4", "hearts"]])
dealers.append(["9", "hearts"])
corrects.append("h")

hands.append([["2", "hearts"], ["3", "hearts"]])
dealers.append(["q", "hearts"])
corrects.append("h")

hands.append([["2", "hearts"], ["5", "hearts"]])
dealers.append(["q", "hearts"])
corrects.append("h")

hands.append([["a", "hearts"], ["k", "hearts"]])
dealers.append(["q", "hearts"])
corrects.append("s")

hands.append([["2", "hearts"], ["2", "hearts"]])
dealers.append(["6", "hearts"])
corrects.append("split")

hands.append([["6", "hearts"], ["3", "hearts"]])
dealers.append(["q", "hearts"])
corrects.append("h")

hands.append([["a", "hearts"], ["j", "hearts"]])
dealers.append(["8", "hearts"])
corrects.append("s")

hands.append([["j", "hearts"], ["3", "hearts"]])
dealers.append(["3", "hearts"])
corrects.append("s")

hands.append([["2", "hearts"], ["q", "hearts"]])
dealers.append(["q", "hearts"])
corrects.append("h")

hands.append([["7", "hearts"], ["7", "hearts"]])
dealers.append(["j", "hearts"])
corrects.append("h")
# 
player = blackjack.PlayerRound(False)

for i in range(len(hands)):
    # print(player.hand)
    for card in hands[i]:
        # print(card)
        player.addCardHand(card)
    player.getValue()
    try:
        print()
        print(i)
        assert player.decision(dealers[i]) == corrects[i]
    except Exception as e:
        print("actual: " + str(player.decision(dealers[i])))
        print("expected: " + corrects[i])
        print(player.handType)
        print(hands[i])
        print(dealers[i])
        print(player.value)
        raise (e)
    player.clearHand()


deck = blackjack.Deck(6, 5000)
betSpread = {2: 5, 3: 10, 4: 20, 5: 50}

round = blackjack.Round(deck, 2, betSpread)
round.deal()
round.bet()
round.roundPlay()
round.payout()

round.deal()
round.bet()
round.roundPlay()
round.payout()


