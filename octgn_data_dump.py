import csv
import collections

csvfilename = "SHL2.csv"

csvfile = open(csvfilename, "rb")
csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
csvrows = list(csvreader)
csvfile.close()

# For debugging
# [(0, 'Corp_Player'), (1, 'Corp_Faction'), (2, 'Runner_Player'), (3,
# 'Runner_Faction'), (4, 'GameStart'), (5, 'Duration'), (6, 'Result'), (7,
# 'Turns_Played'), (8, 'Win'), (9, 'Version'), (10, 'Corp_Inf'), (11,
# 'Runner_Inf'), (12, 'Corp_Score'), (13, 'Runner_Score'), (14, 'GameLobby'),
# (15, 'P_ANR'), (16, 'P_CNR'), (17, 'O_CNR'), (18, 'LeagueID')]
# print list(enumerate(csvrows[0]))
# print list(enumerate(csvrows[1]))
# [(0, 'explodycat'), (1, 'Haas-Bioroid | Engineering the Future'), (2,
# 'lpoulter'), (3, 'Criminal | Andromeda'), (4, '2014-11-22 02:15:50'), (5,
# '24'), (6, 'AgendaVictory'), (7, '15'), (8, 'True'), (9, '3.15.1.1'), (10,
# '15'), (11, '15'), (12, '7'), (13, '4'), (14, 'SHL2'), (15, '13'), (16, '59'),
# (17, '45'), (18, 'SHL2')]
csvrows = csvrows[1:]

# Rank players by win percentage.
wins = collections.defaultdict(int)
total = collections.defaultdict(int)

for row in csvrows:
    total[row[0]] += 1
    total[row[2]] += 1
    if row[8] == "True":
        wins[row[0]] += 1
    if row[8] == "False":
        wins[row[2]] += 1

winrates = [(player, float(wins[player]) / total[player]) for player in wins 
        if total[player] > 10]
print sorted(winrates, key = lambda b: b[1])
