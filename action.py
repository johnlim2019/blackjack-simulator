import blackjack
betSpread = {2: 5, 3: 10, 4: 20, 5: 50}


for i in range(100):
    table = blackjack.Table(1,6,1500,betSpread,0.6)
    table.playRounds(100)
    table.outputLog()