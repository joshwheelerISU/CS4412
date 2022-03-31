# Reference : Modified from https://www.geeksforgeeks.org/dijkstras-algorithm-for-adjacency-list-representation-greedy-algo-8/?ref=lbp
class better_heap:

    def __init__(self):
        self.array = []
        self.size = 0
        self.pos = []

    def node(self, n, key):  # Total Complexity: O(1)
        newnode = [n, key]  # O(1)
        return newnode  # O(1)

    def swap(self, first, second):  # Total Complexity: O(1)
        temp = self.array[first]   # O(1)
        self.array[first] = self.array[second]  # O(1)
        self.array[second] = temp  # O(1)

    def shuffle(self, index):  # Total complexity: O(11) + O(log(n)
        small = index  # O(1)
        left = 2 * index + 1    # O(1)
        right = 2 * index + 2    # O(1)
        if left < self.size and self.array[left][1] < self.array[small][1]:    # O(1)
            small = left    # O(1)
        if right < self.size and self.array[right][1] < self.array[small][1]:    # O(1)
            small = right    # O(1)
        if small != index:    # O(1)
            # proceed with swap
            self.pos[self.array[small][0]] = index  #O(1)
            self.pos[self.array[index][0]] = small  #O(1)
            self.swap(small, index)    # O(1)
            self.shuffle(small)   # This is where the log component comes in, O(log(v))

    def delete_min(self):  # Total Complexity: O(Log(n))
        if self.is_empty():  # O(1)
            return

        root = self.array[0] # O(1)
        lastnode = self.array[self.size - 1] # O(1)
        self.array[0] = lastnode # O(1)

        self.pos[lastnode[0]] = 0 # O(1)
        self.pos[root[0]] = self.size - 1 # O(1)

        self.size -= 1 # O(1)
        self.shuffle(0) # O(Log(N))
        return root # O(1)

    def is_empty(self):
        if self.size == 0:
            return True
        else:
            return False

    def decreaseKey(self, node, newkey):  # Total complexity: O(Log(n))
        index = self.pos[node]  # O(1)
        self.array[index][1] = newkey  # O(1)

        while index > 0 and self.array[index][1] < self.array[(index - 1) // 2][1]: # O(1) for the checks, see below for
            # the loop complexity
            self.pos[self.array[index][0]] = (index - 1) // 2  # O(1)
            self.pos[self.array[(index - 1) // 2][0]] = index  # O(1)
            self.swap(index, (index - 1) // 2)  # O(1)
            index = (index - 1) // 2   # -- > Since this cuts the size in half every time, the while loop should execute
            # Log(index) times.

    def exists(self, v):
        if self.pos[v] < self.size:
            return True
        return False

