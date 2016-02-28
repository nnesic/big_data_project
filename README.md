# Distributed K-means 

This is a simple implementation of the distributed K-means algorithm done as the final project in Big Data course.
It follows the map-reduce pattern, where the master distributes data points to various worker nodes, which calculate the necessary
adjustments to the centroids. The data is returned to the master, which aggregates the adjustments and evaluates whether more 
itterations of the algorithm are needed. 

The goal of the clustering was to use a dump of StackExchange database to identify various user types in various topic forums. 
The implementation is quite simplistic, and not particularly robust, its primary purpose being trying my hand at writing a distributed 
algorithm and then making some pretty graphs that measure the performance of the said algorithm. 

Included is an informal project report, which goes into more detail on the implementation and results of the clustering. 
