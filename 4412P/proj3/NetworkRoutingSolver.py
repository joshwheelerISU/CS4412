#!/usr/bin/python3


from CS4412Graph import *
from rq import *
from hqbetter import *
import time
# from hq import *



class NetworkRoutingSolver:
    distoutput = []
    distnodes = []
    distdistances = []
    prevnodes = []
    prevnodes2 = []
    def __init__( self):
        pass

    def initializeNetwork( self, network ):
        assert( type(network) == CS4412Graph )
        self.network = network

    def getShortestPath( self, destIndex ):
        self.dest = destIndex
        # TODO: RETURN THE SHORTEST PATH FOR destIndex
        #       INSTEAD OF THE DUMMY SET OF EDGES BELOW
        #       IT'S JUST AN EXAMPLE OF THE FORMAT YOU'LL 
        #       NEED TO USE
        path_edges = []
        total_length = 0
        node = self.network.nodes[self.source]
        edges_left = 3
        while edges_left > 0:
            edge = node.neighbors[2]
            path_edges.append( (edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)) )
            total_length += edge.length
            node = edge.dest
            edges_left -= 1
        testcost = self.distoutput[destIndex]
        testpath = []
        destnode = self.network.nodes[destIndex]
        currentpoint = destnode
        while currentpoint.node_id != self.source:
            reversepoint = self.prevnodes2[currentpoint.node_id]
            if reversepoint is None:
                return {'cost':float('inf'), 'path':testpath}
            else:
                for ed in reversepoint.neighbors:
                    if ed.dest == currentpoint:
                        testpath.append( (ed.src.loc, ed.dest.loc, '{:.0f}'.format(ed.length)) )
                        currentpoint = reversepoint
        return {'cost':testcost, 'path':testpath}

    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.source = srcIndex
        t1 = time.time()
        if use_heap == True:
            self.distoutput = self.dijkstra_implementation_better_heap(self.network, srcIndex)
        else:
            self.distoutput = self.dijkstra_implementation_list(self.network, srcIndex)
        t2 = time.time()
        return (t2-t1)

    def dijkstra_implementation_list(self, graph, startvertex):
        # some of these ended up being unnecessary, they've been eliminated in the heap implementation
        self.distnodes = []  # O(1)
        self.distdistances = []  # O(1)
        self.prevnodes = []  # O(1)
        self.prevnodes2 = []  # O(1)
        # initializing distance to infinity and prev to none
        for node in graph.nodes:  # O(n)
            self.distnodes.append(node)  # O(1)
            self.distdistances.append(float('inf'))  # O(1)
            self.prevnodes.append(node)  # O(1)
            self.prevnodes2.append(node)  # O(1)
        self.distdistances[startvertex] = 0  # O(1)

        H = arrayQueue()
        H.makequeue(self.distnodes, self.distdistances)
        while not H.isempty():
            u = H.delete_min()  # DeleteMin in the list implementation is O(n)
            for possibleEdge in u.neighbors:  # 3(O(n)) because there are at most 3 connections per node
                possibleDest = possibleEdge.dest  # O(1)
                vindex = possibleDest.node_id
                uindex = u.node_id
                if self.distdistances[vindex] > (self.distdistances[uindex] + possibleEdge.length):  # O(1)
                    self.distdistances[vindex] = (self.distdistances[uindex] + possibleEdge.length)  # O(1)
                    previndex = possibleDest.node_id
                    # set previous and then decrease the key
                    self.prevnodes2[previndex] = u  # O(1)
                    H.decrease_key(possibleDest, self.distdistances[vindex])  #O(n)
        # return the distances list
        return self.distdistances

    def dijkstra_implementation_better_heap(self, graph, startvertex):
        self.prevnodes2 = []
        self.dist = []
        H = better_heap()
        # initializing distance to infinity and prev to none
        for node in self.network.nodes:  # O(n)
            self.dist.append(float('inf'))
            self.prevnodes2.append(node)
            # add the nodes to the heap: this is the equivalent to the makequeue function in the list impl
            H.array.append(H.node(node.node_id, self.dist[node.node_id]))
            H.pos.append(node.node_id)
        # initialize the beginning point in the heap
        H.pos[startvertex] = startvertex
        self.dist[startvertex] = 0
        H.decreaseKey(startvertex, self.dist[startvertex])

        H.size = len(self.network.nodes)
        while H.is_empty() == False:
            u = H.delete_min()
            node_id = u[0]

            for possibleEdge in self.network.nodes[node_id].neighbors:  # 3(O(n)) because there are at most 3 connections per node
                destination = possibleEdge.dest  # O(1)
                if H.exists(destination.node_id) and self.dist[node_id] != float('inf') and possibleEdge.length + \
                        self.dist[node_id] < self.dist[destination.node_id]:
                    self.dist[destination.node_id] = possibleEdge.length + self.dist[node_id]
                    # update previous node, decrease the key with the new found value
                    self.prevnodes2[destination.node_id] = self.network.nodes[node_id]
                    H.decreaseKey(destination.node_id, self.dist[destination.node_id])  # O(Log(n))
        # return the distance list
        return self.dist

