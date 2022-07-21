import time, datetime
import platform

BLOCK_SIZE = 300

class DataPoint:
    def __init__(self, time, catagory, value):
        self.time = float(time)
        self.catagory = catagory
        self.value = float(value)

    def __str__(self):
        return (f"{self.catagory}, {self.value}, {int(self.time)}")

class DataTimes:
    def __init__(self, catagory, start, end):
        self.catagory = catagory
        self.start = start
        self.end = end
        self.values = []

    def insert(self, value):
        self.values.append(value)

    def average(self):
        try:
            return sum(self.values) / len(self.values)
        except ZeroDivisionError:
            return 0

    def in_bounds(self, time):
        return self.start <= time < self.end

    def __str__(self):
        return f"{self.catagory}, {self.start} - {self.end}, {self.average()}"

    def export_value(self):
        if self.catagory in names.keys():
            return f"{names[self.catagory]},{(self.start + self.end) // 2},{self.average()}\n"
        else:
            return f"{self.catagory},{(self.start + self.end)//2},{self.average()}\n"

datapoints = []
datatimes = []

names = {
    "/temp/03":"Loft",
    "/temp/12":"Kitchen",
    "/temp/11":"Basement",
    "/temp/04":"Barn",
    "/temp/02":"Outside",
    "/temp/22":"Living Room"
}

def readFile(filename="//home//maxli//weather-api//log.csv"):
    print(filename)
    raw = open(filename).read()
    f = open(filename, "w")
    f.close()
    #print(*[i for i in raw.split('\n')], sep='\n')
    for datum in [i for i in raw.split('\n') if len(i) > 0]:
        try:
            t, c, v = datum.split(',')
        except ValueError as ex:
            print(datum)
            raise ex
        dp = DataPoint(t,c,v)
        datapoints.append(dp)

    print(*datapoints, sep='\n')

def convert_to_datatimes():
    for dp in datapoints:
        inserted = False
        for dt in datatimes:
            if dt.in_bounds(dp.time) and dt.catagory == dp.catagory:
                dt.insert(dp.value)
                inserted = True

        if not inserted:
            dt = DataTimes(dp.catagory, int(dp.time)-(int(dp.time)%BLOCK_SIZE), (int(dp.time)-(int(dp.time)%BLOCK_SIZE)) + BLOCK_SIZE)
            dt.insert(dp.value)
            datatimes.append(dt)

    print(*datatimes, sep='\n')

def save_to_disk():
    start = min([i.start for i in datatimes])
    end = max([i.end for i in datatimes])

    if platform.system() == "Windows":
        filename = f"summaries//{start}-{end}.csv"
    else:
        filename = f"//home//maxli//weather-api//summaries//{start}-{end}.csv"

    f = open(filename, 'w')
    for dt in datatimes:
        f.write(dt.export_value())
    f.close()


if __name__ == "__main__":
    if platform.system() == "Windows":
        readFile("log.csv")
    else:
        readFile()
    convert_to_datatimes()
    save_to_disk()
