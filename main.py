"""
Bryce Rothschadl
Dr. Mukherjee
COMPSCI 332-01
2023/04/25
"""

import csv
import math
import random


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
    # Repeat N times
    for i in range(n):
        # centroids = Randomly Create K Centroids from data
        centroids = []
        clusters = []
        for j in range(k):
            centroids.append(random.choice(data))
            clusters.append([])

        # while centroids not converged (still changing) or have a stop after P iterations:
        p = 200
        is_converged = False
        while p > 0 and not is_converged:
            # for each data point:
            for x in data:
                # assign data point to the closest centroid(use Euclidean distance again)
                min_dist = float("inf")
                closest = -1  # index of closest centroid variable
                for j in range(len(centroids)):
                    d = calc_dist(x.points, centroids[j].points)
                    if d < min_dist:
                        min_dist = d
                        x.distanceToCluster = d
                        x.cluster = j
                        closest = j
                clusters[closest].append(x)

            # for each centroid:
            new_centroids = []
            new_center = Instance([0] * 8)
            for c in clusters:
                # set new centroid location to be the mean of all points in this cluster
                for x in c:
                    # add up all points respective to index
                    for j in range(len(x.points)):
                        new_center.points[j] += x.points[j]

                    # divide by total number of instances to calculate mean position of cluster
                    for j in range(len(x.points)):
                        new_center.points[j] /= n
                new_centroids.append(new_center)

            # test tolerance to see how much the centroids moved
            tol = 0.0001
            for nc in range(len(new_centroids)):
                for j in range(8):
                    if abs(new_centroids[nc].points[j] - centroids[nc].points[j]) < tol:
                        # the distance that the centroids moved is less than the
                        # tolerance value, so the clustering has converged
                        is_converged = True
                    else:
                        centroids = new_centroids
                        p -= 1

    # Calculate objective(sum of distances of each point to the cluster centroid they are assigned to)
    obj_sum = 0
    clusters = []
    for j in range(n):
        # objective sum
        obj_sum += data[j].distanceToCluster

        # clusters
        clusters.append(data[j].cluster)

    # Save in arrays the objective and the clustering found after the completion of the 2nd for loop
    return [obj_sum, clusters]


def main():
    # create data
    data_path = "Wholesalecustomersdata_processed.csv"
    data = create_data(data_path)

    k = 5
    n = len(data)

    # call the k means algorithm
    k_means_output = k_means(data, k, n)
    objective_sum = k_means_output[0]
    clustering = k_means_output[1]

    # print output
    print("K value: ", k, '\n')
    print("+---------------+--------------+")
    print("|  Point Index  |  Cluster No  |")
    print("+---------------+--------------+")
    for i in range(len(clustering)):
        # format the output to make it look nice
        print("|{:13d}".format(i), end="  ")            # index
        print("|{:12d}".format(clustering[i]), end="")  # cluster
        print("  |")
    print("+---------------+--------------+\n")
    # round the objective value to two decimal places
    print("Objective value of the final solution: {0:.2f}".format(objective_sum))


if __name__ == '__main__':
    main()
