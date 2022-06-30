from matplotlib import pyplot as plt
from collections import defaultdict
import datetime
import os

locations = defaultdict(lambda :[])
filenames = []

def get_all_filenames(path="summaries\\"):
    names = [f"{path}{name}" for name in os.listdir(path) if os.path.isfile(f"{path}{name}")]
    return names

def get_bounded_filenames(start, end, path="summaries\\"):
    names = [name for name in os.listdir(path) if os.path.isfile(f"{path}{name}")]
    starts, ends = zip(*[name.split('.')[0].split('-') for name in names])
    print(starts, ends)

def load_data(filename):
    data = [i for i in open(filename).read().split('\n') if len(i) > 0]

    for datum in data:
        l, t, v = (datum.split(','))
        t = int(t)
        t = datetime.datetime.fromtimestamp(t)
        v = round(float(v), 2)
        locations[l].append((t, v))

def make_graph():
    for location in locations.keys():
        spt = (zip(*locations[location]))
        plt.plot(*spt, label=location)
    plt.legend()
    plt.show()


def make_bounded_graph(start, end):
    for location in locations.keys():
        data = locations[location]
        data = [datum for datum in data if start <= datum[0] < end]
        spt = (zip(*data))
        plt.plot(*spt, label=location)
    plt.legend()
    plt.show()

def load_all():
    global filenames
    filenames = get_all_filenames()
    for f in filenames:
        load_data(f)


if __name__ == "__main__":
    start = datetime.datetime.fromtimestamp(1656608500)
    end = datetime.datetime.fromtimestamp(1656609000)

    load_all()
    make_bounded_graph(start, end)
    make_graph()