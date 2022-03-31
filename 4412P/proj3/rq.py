class arrayQueue:
    def __init__(self):
        self.nodes = []
        self.keys = []
        self.size = 0

    def insert(self, edgetoadd, keyval):  #total complexity: O(1) + O(1) = O(1)
        self.nodes.append(edgetoadd)  # O(1)
        self.keys.append(keyval)  # O(1)
        self.size += 1

    def makequeue(self, nodelist, keylist):  # total complexity: O(n)
        self.nodes = list(nodelist)
        self.keys = list(keylist)
        self.size = len(keylist)

    def decrease_key(self, node, keyval): # total complexity: O(n)  -> I tried fixing this to be o(1) broke program
        # nindex = self.nodes.index(node)  # lookup, worst case is O(n)
        self.keys[node.node_id] = keyval       # O(1)

    def isempty(self):
        if self.size == 0:
            return True
        else:
            return False

    def delete_min(self):  #total complexity O(n) * O(5) + 2n) = O(n)
        ret = min(self.keys)
        ind = self.keys.index(ret)
        self.keys[ind] = float('inf')
        self.size -= 1
        return self.nodes[ind]