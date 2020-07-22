

from functools import reduce

def readPerSecond(fname):
    f = open(fname)
    lines = f.readlines()
    lines = list(filter(lambda l : not l[0].isalpha(), lines))
    def func(accum,elt):
        if len(elt) == 0:
            return accum
        if elt[0] == "{":
            accum.append(elt)
        else:
            accum[len(accum)-1] = accum[len(accum)-1] + elt
        return accum

    import json
    flat = reduce(func, lines, [])
    objs = list(map(lambda l : json.loads(l), flat))

    uptimes = list(map(lambda obj: obj["result"]["uptime"],objs))

    def to_seconds(uptime):
        split = uptime.split(",")
        trimmed = list(map(lambda l: l.strip(), split))
        def to_seconds_help(elt):
            pair = elt.split(" ")
            if "day" in pair[1]:
                return int(pair[0]) * 60 * 60 * 24
            elif "hour" in pair[1]:
                return int(pair[0]) * 60 * 60
            elif "minute" in pair[1]:
                return int(pair[0]) * 60
            elif "second" in pair[1]:
                return int(pair[0])
        return reduce(lambda acc, elt: elt + acc, list(map(lambda l: to_seconds_help(l), trimmed)), 0)

    seconds = list(map(lambda elt: to_seconds(elt), uptimes))

    reads = list(map(lambda obj: obj["result"]["node_reads_total"] - obj["result"]["node_reads_hit"], objs))

    zipped = list(zip(seconds, reads))

    readsPerSecond = list(map(lambda elt: elt[1] / elt[0], zipped))
    return (reduce(lambda acc, elt: acc + elt, readsPerSecond, 0), min(seconds), max(seconds), sum(seconds))


import sys
files = sys.argv[1:]
readsPerSecond = list(map(lambda f: readPerSecond(f), files))
minUptime = min(list(map(lambda l: l[1],readsPerSecond)))
maxUptime = max(list(map(lambda l: l[2], readsPerSecond)))
totalUptime = sum(list(map(lambda l: l[3], readsPerSecond)))
totalReadsPerSecond = reduce(lambda acc, elt: readPerSecond(elt)[0] + acc, files,0)
print("reads per second: " + str(totalReadsPerSecond))
print("max uptime : " + str(maxUptime))
print("min uptime : " + str(minUptime))
print("total uptime : " + str(totalUptime))
