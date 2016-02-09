import random

def get_pairings(players, points, forbidden):
    players2 = list(players)
    players2.sort(key = lambda i: points[i])
    out = []
    while players2 != []:
        a = players2[0]
        players2.delete(a)

print get_players(range(8), [1,1,1,1,0,0,0,0], set())

# Method 1 - pair people by record, and then try to equalize their number
# of plays.

corp_win_percent = 0.5
forbidden = {}
n = 32
players = range(n)
corps = [0]*n
points = [0]*n
rounds = 2
for i in range(rounds):
    pairings = get_pairings(players, points, forbidden)
    for corp, runner in pairings:
        forbidden.add((corp,runner))
        forbidden.add((runner,corp))
        if (corps[corp] > corps[runner]) or (corps[corp] == corps[runner] and random.randrange(2) == 1):
            corp, runner = runner, corp
        corps[corp] += 1
        if random.random() < corp_win_percent:
            points[corp] += 1
        else:
            points[runner] += 1
players.sort(key = lambda i: points[i])
for i in range(players):
    print "Player {i}: corped {c}, points {p}".format(i=i,c=corps[i],p=points[i])
