import parse_deck
import random
import sys
print "Usage: mulligans.py deckfile outfile n"
filename = sys.argv[1]
outfile = sys.argv[2]
n = int(sys.argv[3])
deck = parse_deck.parse_file(filename)
lines = []
for _ in range(n):
    random.shuffle(deck)
    hand = sorted(deck[:5])
    lines.append(",".join(hand))

# Sort here, just under the assumption that similar hands being together
# will save some work.
lines.sort()

with open(outfile, "w") as f:
    for line in lines:
        f.write(line + "\n")
