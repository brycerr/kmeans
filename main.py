"""
Bryce Rothschadl
Dr. Mukherjee
COMPSCI 332-01
2023/04/03
"""

import csv
import math
import random
from statistics import mean


class Instance:
    def __init__(self, points):
        self.points = points    # list of points
        self.cluster = -1       # the cluster that the instance belongs to
        self.distanceToCluster = 0

    def __repr__(self):
        return "Instance: " + str(self.cluster)


def create_data(path):  # reads file, returns list of data
    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        data_list = []
        for row in reader:
            temp = []
            for x in row:
                temp.append(float(x))
            data_list.append(Instance(temp))
    return data_list


def calc_dist(a, b):  # calculates euclidean distance
    dist = 0
    for i in range(8):
        c = abs(a[i] - b[i])
        dist += pow(c, 2)
    dist = math.sqrt(dist)
    return dist


def k_means(data, k, n):
    for i in range(n):
        converged = False
        centroids = []
        clusters = []
        for j in range(k):  # randomly create k centroids from data
            centroids.append(random.choice(data))
            clusters.append([])
        p = 200  # stop value
        while not converged and p > 0:
            # assign instances to a cluster
            for x in data:
                min_dist = float('inf')
                for j in range(k):
                    d = calc_dist(x.points, centroids[j].points)
                    if d < min_dist:
                        print("d:", d, " | md:", min_dist, " | j:", j)
                        min_dist = j    # set min_dist to the index of the current centroid
                        x.cluster = min_dist
                        x.distanceToCluster = d
                clusters[min_dist].append(x)    # assign instance to closest cluster

            # create new centroids from current clusters
            new_centroids = []  # initialize list of new centroids

            for x in clusters:
                new_center = [0]*8

                for points in x:
                    for temp in range(8):
                        new_center[temp] += points.points[temp]

                for temp in range(8):
                    new_center[temp] = new_center[temp] / n

                new_centroids.append(new_center)

            # print(clusters)
            if centroids == new_centroids:
                converged = True
                print("CONVERGED")
            p -= 1

        # calculate objective sum
        obj_sum = 0
        for x in data:
            obj_sum += x.distanceToCluster

        return obj_sum


def main():
    # create data
    data_path = "Wholesalecustomersdata_processed.csv"
    data = create_data(data_path)

    k = 5
    n = len(data)

    # call k means algorithm
    objective_sum = k_means(data, k, n)

    # print output
    print("K value: ", k, '\n')
    print("+---------------+--------------+")
    print("|  Point Index  |  Cluster No  |")
    print("+---------------+--------------+")
    #
    print("+---------------+--------------+\n")
    print("Objective value of the final solution:", objective_sum)


if __name__ == '__main__':
    main()
