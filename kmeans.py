from pandas import *
import sklearn as sk

def findClusters(csv_file):
    df = pandas.read_csv(csv_file, low_memory=False, header=0)


if __name__ == '__main__':
    df = findClusters("data/map_reduced_subject.csv")