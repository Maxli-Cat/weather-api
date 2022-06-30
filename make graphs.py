from matplotlib import pyplot as plt
from collections import defaultdict
import datetime

locations = defaultdict(lambda :[])

def make_graph(filename="1656514500-1656530100.csv"):
    data = [i for i in open(filename).read().split('\n') if len(i) > 0]

    for datum in data:
        l, t, v = (datum.split(','))
        t = int(t)
        t = datetime.datetime.fromtimestamp(t)
        v = round(float(v),2)

        locations[l].append((t,v))


    for location in locations.keys():
        spt = (zip(*locations[location]))
        plt.plot(*spt, label=location)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    make_graph()