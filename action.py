import blackjack

betSpread = {1: 10, 2: 20, 3: 40, 4: 80, 5: 100, 6: 120}
table = blackjack.Table(1, 6, 1500, betSpread, 0.6)
table.playRounds(100)
table.outputLog()
