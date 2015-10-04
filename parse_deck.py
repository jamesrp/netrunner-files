def parse_file(filename):
    with open(filename) as f:
        out = []
        for line in f.readlines():
            out.extend(parse_line(line))
        return out

def parse_line(line):
    seg = line.split(" (")[0]
    num = int(seg[0])
    name = seg[3:]
    return [name]*num
