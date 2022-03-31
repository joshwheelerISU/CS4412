#!/usr/bin/python3


class CS4412GraphEdge:
    def __init__( self, src_node, dest_node, edge_length ):
        self.src   = src_node
        self.dest  = dest_node
        self.length= edge_length

    def __repr__( self ):
        return self.__str__()

    def __str__( self ):
        return '(src={} dest={} length={})'.format(self.src,self.dest,self.length)

class CS4412GraphNode:
    def __init__( self, node_id, node_loc ):
        self.node_id   = node_id
        self.loc       = node_loc
        self.neighbors = [] #node_neighbors

    def addEdge( self, neighborNode, weight ):
        self.neighbors.append( CS4412GraphEdge(self,neighborNode,weight) )

    def __str__( self ):
        neighbors = [edge.dest.node_id for edge in self.neighbors]
        return 'Node(id:{},neighbors:{})'.format(self.node_id,neighbors)


class CS4412Graph:
    def __init__( self, nodeList, edgeList ):
        self.nodes    = []
        for i in range(len(nodeList)):
            self.nodes.append( CS4412GraphNode( i, nodeList[i] ) )

        for i in range(len(nodeList)):
            neighbors = edgeList[i]
            for n in neighbors:
                self.nodes[i].addEdge( self.nodes[n[0]], n[1] )
        
    def __str__( self ):
        s = []
        for n in self.nodes:
            s.append(n.neighbors)
        return str(s)

    def getNodes( self ):
        return self.nodes


class dist:
    def __init__(self, node, distance):
        self.n = node;
        self.d = distance;



class heapQueue:
    def __init__(self):
        self.nodes = []
        self.keys = []

    def makequeue(self, nodelist, keylist):
        for n, x in zip(nodelist, keylist):
            self.insert(n, x)

    def insert(self, edgetoadd, keyval):
        self.nodes.insert(edgetoadd)
        self.keys.insert(keyval)

    def decrease_key(self, node, keyval):
        nindex = self.nodes.index(node)
        self.keys[nindex] = keyval

    def isempty(self):
        if len(self.nodes) == 0:
            return True
        else:
            return False

    def delete_min(self):
        ret = float('inf')
        for keyval in self.keys:
            if ret == float('inf'):
                ret = keyval
            else:
                new = keyval
                if new < ret:
                    ret = new
        self.nodes.remove(ret)
        return ret

