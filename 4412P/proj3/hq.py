class heapQueue:

    def __init__(self):
        self.nodes = []
        self.keys = []

    def insert(self, edgetoadd, keyval):  # Accidentally made this O(n^2)
        if self.isempty():  # O(1)
            self.nodes.append(edgetoadd)  # O(1)
            self.keys.append(keyval)  # O(1)
        else:
            for no,ke in zip(self.nodes, self.keys):  # (O(no = ke) = O(n)
                if keyval < ke:  # O(1)
                    self.keys.insert(self.keys.index(ke), keyval)  # put the new node at this index in the list  # O(n)
                    self.nodes.insert(self.nodes.index(no), edgetoadd)  # keep the nodes structure parallel tothekeys  # O(n)
                    break
                elif keyval == float('inf') and ke == float('inf'):  # O(1)+ O(1)
                    self.keys.insert(self.keys.index(ke), keyval)  # put the new node at this index in the list # O(n)
                    self.nodes.insert(self.nodes.index(no), edgetoadd) # O(n)
                    break
            self.keys.append(keyval) # O(1)
            self.nodes.append(edgetoadd) # O(1) # at this point we've iterated through the loop and this is roughly the
            # greatest element in the pq

    def makequeue(self, nodelist, keylist):  #O(n)
        for n, x in zip(nodelist, keylist):
            self.insert(n, x)

    def decrease_key(self, node, keyval):
        curindex = self.nodes.index(node)  # O(n)
        no = self.nodes.pop(curindex)  #O(n)
        ke = self.keys.pop(curindex)  # O(n)
        self.insert(no, keyval)  # O(n^2)

    def isempty(self):
        if len(self.nodes) == 0:
            return True
        else:
            return False

    def delete_min(self):  #O(1)
        no = self.nodes.pop(0)  # O(1) because pop will not have to iterate beyond the first element
        ke = self.keys.pop(0)   # O(1)
        return no

