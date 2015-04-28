import csv
import collections
import sys

#csvfilename = "SHL2.csv"
csvfilename = "OCTGN_stats_anonymized-2015-02-20.csv"

csvfile = open(csvfilename, "rb")
csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
csvrows = list(csvreader)
csvfile.close()


# To handle both SHL2 and main data set, first determine which indices map to
# which fields.
corp_player_index = csvrows[0].index('Corp_Player')
runner_player_index = csvrows[0].index('Runner_Player')
corp_faction_index = csvrows[0].index('Corp_Faction')
runner_faction_index = csvrows[0].index('Runner_Faction')
result_index = csvrows[0].index('Result')
version_index = csvrows[0].index('Version')

corp_win_conditions = frozenset(['Flatlined', 'ConcedeVictory', 'AgendaVictory', 'FlatlineVictory'])
runner_win_conditions = frozenset(['AgendaDefeat', 'DeckDefeat', 'Conceded'])

csvrows = csvrows[1:]

# Elo calculation.
elo_ratings = collections.defaultdict(lambda: 1600)
K = 16.0
for row in csvrows:
    result = row[result_index]
    if result in corp_win_conditions:
        actual0 = 1
        actual2 = 0
    elif result in runner_win_conditions:
        actual0 = 0
        actual2 = 1
    else:
        print "Error - unexpected result: " + result
        continue
    corp_player = row[corp_player_index]
    runner_player = row[runner_player_index]
    rating0 = elo_ratings[corp_player]
    rating2 = elo_ratings[runner_player]
    Q0 = 10.0**(rating0/400.0)
    Q2 = 10.0**(rating2/400.0)
    Q_sum = Q0 + Q2
    E0 = Q0 / Q_sum
    E2 = Q2 / Q_sum
    elo_ratings[corp_player] = rating0 + K*(actual0 - E0)
    elo_ratings[runner_player] = rating2 + K*(actual2 - E2)



# top players by elo
#top_elo = [(player, elo_ratings[player]) for player in wins]
top_elo = elo_ratings.items()
cutoff_elos = int(len(top_elo)*.90)
best_players = [x[0] for x in sorted(top_elo, key = lambda b: b[1])[cutoff_elos:]]
best_players = frozenset(best_players)


# Further filter identities to matches played where both players are in this set, and OCGN version == 3.16
csvrows = [row for row in csvrows if row[runner_player_index] in best_players and row[corp_player_index] in best_players and row[version_index].find("3.16") != -1]

# Redo elo calculation with deck identities.
# TODO - this seems over fancy in retrospect. Why not just treat the identities
# themselves as players and compute elo for them over all time.
# Either with or without restricting to good players.

# Elo calculation.
elo_ratings2 = collections.defaultdict(lambda: 1600)
K = 16.0
for row in csvrows:
    result = row[result_index]
    if result in corp_win_conditions:
        actual0 = 1
        actual2 = 0
    elif result in runner_win_conditions:
        actual0 = 0
        actual2 = 1
    else:
        print "Error - unexpected result: " + result
        continue
    corp_faction = row[corp_faction_index]
    runner_faction = row[runner_faction_index]
    rating0 = elo_ratings2[corp_faction]
    rating2 = elo_ratings2[runner_faction]
    Q0 = 10.0**(rating0/400.0)
    Q2 = 10.0**(rating2/400.0)
    Q_sum = Q0 + Q2
    E0 = Q0 / Q_sum
    E2 = Q2 / Q_sum
    elo_ratings2[corp_faction] = rating0 + K*(actual0 - E0)
    elo_ratings2[runner_faction] = rating2 + K*(actual2 - E2)

factions = [(faction, elo_ratings2[faction]) for faction in elo_ratings2]
factions.sort(key = lambda b: b[1])
for i in factions:
    print i
