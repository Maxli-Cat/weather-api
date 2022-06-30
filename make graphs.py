from matplotlib import pyplot as plt
from collections import defaultdict
import datetime
import os
import sys
import platform

locations = defaultdict(lambda :[])
filenames = []

def get_all_filenames(path=None):
    if path is None:
        if platform.system() == "Windows": path="summaries\\"
        else: path = "//home//maxli//weather-api//summaries//"
    names = [f"{path}{name}" for name in os.listdir(path) if os.path.isfile(f"{path}{name}")]
    print(f"{names=}")
    return names

def get_bounded_filenames(start, end, path=None):
    if path is None:
        if platform.system() == "Windows": path="summaries\\"
        else: path = "//home//maxli//weather-api//summaries"
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

def make_graph(filename = None):
    for location in locations.keys():
        locations[location].sort(key=lambda x:x[0])
        spt = (zip(*locations[location]))
        plt.plot(*spt, label=location)
    plt.xticks(rotation=90)
    plt.grid(axis='y')
    plt.legend()

    if filename is None:
        plt.show()
    else:
        plt.savefig(fname=filename, dpi=450)


def make_bounded_graph(start, end, filename=None):
    for location in locations.keys():
        locations[location].sort(key=lambda x: x[0])
        data = locations[location]
        data = [datum for datum in data if start <= datum[0] < end]
        spt = (zip(*data))
        plt.plot(*spt, label=location)
    plt.xticks(rotation = 90)
    plt.grid(axis='y')
    plt.legend()

    if filename is None:
        plt.show()
    else:
        plt.savefig(fname=filename, dpi=450)

def load_all():
    global filenames
    filenames = get_all_filenames()
    for f in filenames:
        load_data(f)
        print(f)


if __name__ == "__main__":
    bounded = False

    try: filename = sys.argv[1]
    except: filename = "graph.png"

    if len(sys.argv) > 2:
        try: start = int(sys.argv[2])
        except: pass
        try: end = int(sys.argv[3])
        except: pass
        bounded = True
        start = datetime.datetime.fromtimestamp(start)
        end = datetime.datetime.fromtimestamp(end)

    load_all()
    if bounded:
        make_bounded_graph(start, end, filename)
    else:
        make_graph(filename)