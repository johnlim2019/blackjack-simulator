import blackjack

handDouble = [
    ['a','spades'],
    ['a','hearts']
]

handSoft = [
    ['a','spades'],
    ['3','hearts']
]

handHard = [
    ['5','spades'],
    ['8','hearts']
]


# print(blackjack.getValue(handHard))
assert blackjack.getValue(handHard) == (13,'hard')
assert blackjack.getValue(handSoft) == (14,'soft')
assert blackjack.getValue(handDouble) == (2,'pair')


dealerFace = ['2','3','4','5','6','7','8','9','10','j','q','k','a']
value = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
type = ['hard','soft','pair']

print(blackjack.decision('a',2,'hard'))


blackjack.decision('2',)