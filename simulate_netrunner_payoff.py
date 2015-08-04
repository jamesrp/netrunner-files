# TODO(jpfeiff):
#  * byes
#  * Option to use files to process a real tournament
#  * (stretch) alternate pairing algorithm i.e. matching-based

import math, random, collections

def update_round(players, prev_points, prev_opps):
    pairings = make_pairings(players, prev_points, prev_opps)
    curr_points = {p:prev_points[p] for p in players}
    curr_opps = {p:list(prev_opps[p]) for p in players}
    for p in pairings:
        a, b = get_result(p, curr_points)
        curr_points[p[0]] += a
        curr_points[p[1]] += b
        curr_opps[p[0]].append(p[1])
        curr_opps[p[1]].append(p[0])
    standings = make_standings(players, curr_points, curr_opps)
    return standings, curr_points, curr_opps

def run_rounds(num_rounds, num_players):
    players = range(num_players)

    points = {p:0 for p in players}
    opps = {p:[] for p in players}

    for i in range(num_rounds):
        players, points, opps = update_round(players, points, opps)
    # return final standings
    return points.values()

def make_pairings(standings, points, opponents):
    # FFG algorithm.
    output = []
    to_pair = list(standings)
    # Without proof of correctness, we may fail.
    count = 0
    while to_pair != [] and count < 1000:
        count += 1
        p, q = to_pair[:2]
        if q not in opponents[p]:
            output.append((p,q))
            to_pair = to_pair[2:]
        elif len(to_pair) > 2:
            # Move one player down two places.
            if random.randrange(2):
                to_pair[0], to_pair[2] = to_pair[2], to_pair[0]
            else:
                to_pair[1], to_pair[3] = to_pair[3], to_pair[1]
        else:
            raise ValueError, "pairings stuck - last two in two_pair already played"
    if to_pair != []:
        raise ValueError, "pairings timeout"
    return output

def quantiles_hist(data, r, total = None):
    # Assumes data is list of (value, count) pairs sorted by value increasing
    if total == None:
        total = sum(x[1] for x in data)
    target = int(r * total)
    count = 0
    for x in data:
        count += x[1]
        if count >= target:
            break
    return x[0]

def make_standings(players, ri_points, ri_opps):
    sos = {p: sum(ri_points[q] for q in ri_opps[p]) for p in players}
    s = sorted(players, key = lambda p: (-ri_points[p], -sos[p], random.random()))
    #for e, p in enumerate(s):
    #    print "%d. %s: points=%d, sos=%d"%(e,p,ri_points[p],sos[p])
    return s

def get_result(p, points):
    a, b = p
    diff = points[a] - points[b]
    pa = 0.5 + diff * 0.05
    x,y = 0,0
    for i in range(2):
        if random.random() < pa:
            x += 1
        else:
            y += 1
    return x,y

def simulate(payoff, num_players, num_rounds, samples):
    results = collections.defaultdict(int)
    count = 0
    for loop in xrange(samples):
        try:
            result = run_rounds(num_rounds, num_players)
            total = sum(payoff[x] for x in result)
            results[total] += 1
            count += 1
        except ValueError:
            continue
    hist = sorted(results.iteritems(), key = lambda y: y[0])
    return hist, count

if __name__ == "__main__":
    payoff5 = {10:85, 9:65, 8:45, 7:25, 6:15, 5:5, 4:0, 3:0, 2:0, 1:0, 0:0}
    payoff4 = {8:80, 7:45, 6:30, 5:15, 4:5, 3:0, 2:0, 1:0, 0:0}
    tests = [("30 players 5 rounds", 30, 5, payoff5),
             ("20 players 5 rounds", 20, 5, payoff5)]
    tests += [("%d players 4 rounds"%i, i, 4, payoff4) for i in range(10,50,2)]
    for t in tests:
        print "\n",t[0], t[3]
        hist, count = simulate(t[3], t[1], t[2], 10000)
        float_denominator = float(count)
        avg = sum(x*y/float_denominator for y,x in hist)
        stdev = math.pow(sum(x*((y-avg)**2) for y,x in hist)/(count-1),0.5)
        lo, hi = quantiles_hist(hist, 0.025, count), quantiles_hist(hist, 0.975, count)
        print "Average:", avg
        print "Std Dev:", stdev
        print "95% interval", (lo, hi)

