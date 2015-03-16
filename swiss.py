def make_pairings(standings, opps):
    # To handle dropped players, just don't include them in pairings.
    # Their opponents will still get credit for sos.
    if len(standings)%2 == 0:
        return ffg_backtrack([], standings, opps)
    return ffg_backtrack([], standings + ["BYE"], opps)

def ffg_backtrack(pairings, to_pair, opps):
    if to_pair == []:
        return pairings
    p1 = to_pair[0]
    for p2 in to_pair[1:]:
        if p2 not in opps[p1]:
            new_to_pair = [x for x in to_pair if x != p1 and x != p2]
            outcome = ffg_backtrack(pairings + [(p1, p2)], new_to_pair, opps)
            if outcome == None:
                continue
            return outcome
    return None

def make_sos(players, points, opps):
    sos = {p: sum(points[q] for q in opps[p]) for p in players}
    return sos

def make_standings(players, points, sos):
    s = sorted(players, key = lambda p: (-points[p], -sos[p]))
    return s

def print_standings(standings, points, sos):
    print "STANDINGS"
    for e, p in enumerate(standings):
        print "%d. %s points %2d sos %2d"%(e+1,p+ "."*(30 - len(p)),points[p],sos[p])

def print_pairings(pairings):
    pairings2 = pairings + [(p[1], p[0]) for p in pairings]
    pairings2.sort()
    print "PAIRINGS"
    for p in pairings2:
        print "%-30s -VS- %30s"%(p[0], p[1])

def full_update(players, points, opps):
    sos = make_sos(players, points, opps)
    standings = make_standings(players, points, sos)
    print_standings(standings, points, sos)
    pairings = make_pairings(standings, opps)
    print_pairings(pairings)
    updated_opps = dict()
    for p in pairings:
        p1, p2 = p
        updated_opps[p1] = opps[p1] + [p2]
        updated_opps[p2] = opps[p2] + [p1]
    print_opps(updated_opps)

def print_opps(opps):
    print "UPDATED OPPONENTS"
    print repr(opps)

players = ["a", "b", "c", "d", "e", "f"]
points = {x:0 for x in players}
opps = {x:[] for x in players}
full_update(players, points, opps)

points = {"a": 2, "b": 2, "f": 0, "e": 4, "c": 2, "d": 1}

