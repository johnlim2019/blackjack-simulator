import blackjack
betSpread = {2: 5, 3: 10, 4: 20, 5: 50}

table = blackjack.Table(1,6,1500,betSpread,0.3)
table.playRounds(180)
table.outputLog()