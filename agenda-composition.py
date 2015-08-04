NUM_AGENDA_POINTS = 7
DECK_SIZE = 49
AGENDAS = ["TFP"]*7

import random, collections

def simulate(points, deck_size, agendas, samples):
    deck = agendas + [0]*(deck_size - len(agendas))
    counts = collections.defaultdict(int)
    for loop in range(samples):
        random.shuffle(deck)
        counts[num_accesses(deck, points)] += 1
    out = dict()
    for k, v in counts.iteritems():
        out[k] = v/float(samples)
    return out

def num_accesses(deck, points):
    if points == 0:
        return 0
    total = 0
    for e, v in enumerate(deck):
        if v == "TFP":
            if random.random() > 0.4:
                continue
            else:
                total += 3
                continue
        total += v
        if total >= points:
            return e + 1

def test_num_accesses():
    deck = [0,0,1,0,3]
    assert(num_accesses(deck, 1) == 3)        
    assert(num_accesses(deck, 4) == 5)
    assert(num_accesses(deck, 0) == 0)

test_num_accesses()

def pprint(d):
    ks = sorted(d.iterkeys())
    for k in ks:
        print k, d[k]

def ms(d):
    mean, variance = 0, 0
    for value, probability in d.iteritems():
        mean += probability * value
    for value, probability in d.iteritems():
        variance += probability * (value - mean)**2
    return mean, variance
    
def quantiles(d, qs):
    i, q, maxi = 0, qs[0], len(qs)-1
    total_probability = 0
    out = dict()
    for value, probability in d.iteritems():
        total_probability += probability
        if total_probability >= q:
            out[q] = value
            i += 1
            if i > maxi:
                break
            q = qs[i]
    return out

out = simulate(NUM_AGENDA_POINTS, DECK_SIZE, AGENDAS, 100000)
pprint(out)
mean, variance = ms(out)
q = quantiles(out, [.1,.25,.5,.75,.9])
print "Quantiles:"
pprint(q)
print "Mean, stdev:\n", mean, variance**0.5
