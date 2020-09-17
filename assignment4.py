# Author: Xinyu Ma

class Graph(object):
    """We use adjacent matrix to represent a Graph"""
    def __init__(self, gfile):
        '''
        gfile: the input file containing the Graph
        time complexity: O(V^2) where V is the sum of vertices
        space complexity: O(V^2) where V is the sum of vertices
        '''
        with open(gfile) as file:
            self.V = int(file.readline())
            self.adjaTable = [[(i,0)] for i in range(3 * self.V)]
            for line in file.readlines():
                u, v, w = [int(num) for num in line.split(' ')]
                self.adjaTable[u].append((v, w))
                self.adjaTable[v].append((u, w))
                self.adjaTable[u + self.V].append((v + self.V, w))
                self.adjaTable[v + self.V].append((u + self.V, w))
                self.adjaTable[u + 2 * self.V].append((v + 2 * self.V, w))
                self.adjaTable[v + 2 * self.V].append((u + 2 * self.V, w))
            
    def shallowest_spanning_tree(self):
        '''
        BFS on each node
        time complexity: O(V*(V + E)) < O(V^3)
        '''
        mindis = -1
        minnod = -1
        for node in range(self.V):
            dis = [-1 for _ in range(self.V)]
            dis[node] = 0
            searchlist = [node]
            nowpos = 0
            while nowpos < len(searchlist):
                nodeToSearch = searchlist[nowpos]
                for nextnode, _ in self.adjaTable[nodeToSearch]:
                    if dis[nextnode] == -1:
                        searchlist.append(nextnode)
                        dis[nextnode] = dis[nodeToSearch] + 1
                nowpos+=1
            maxdis = max(dis)
            if mindis == -1 or maxdis < mindis:
                mindis = maxdis
                minnod = node
        return minnod, mindis


    def shortest_errand(self, home, destination, ice_locs, ice_cream_locs):
        '''
        imaging the original graph becomes three layers, each layer is the same as the original graph
        in 1st layer, only ice_locs nodes can lead to 2nd layer
        in 2nd layer, only ice_cream_locs can lead to 3rd layer
        the number of the node on the upper layer is the number of the node on the next layer + V,
        so the problem becomes the shortest path from home to destination + 2V
        we can find the shortest path by using dijkstra directly
        time complexity: O((3E+2V)log(3V)) = O(Elog(V))
        '''
        # create path between two layers
        for node in ice_locs:
            self.adjaTable[node].append((node + self.V, 0))
            self.adjaTable[node + self.V].append((node, 0))
        for node in ice_cream_locs:
            self.adjaTable[node + 2 * self.V].append((node + self.V, 0))
            self.adjaTable[node + self.V].append((node + 2 * self.V, 0))

        dist = [float('inf') for _ in range(self.V * 3)]
        pred = [-1 for _ in range(self.V * 3)]
        dist[home] = 0

        heap = []
        vertices = [-1 for _ in range(self.V * 3)]

        def push(heap, vertices, num, v):
            '''
            add node v and the distance between home and node v into min heap
            time complexity: O(log(V))
            '''
            heap.append([v, num])
            pos = len(heap)-1
            vertices[v] = pos
            while heap[pos][1] < heap[pos//2][1]:
                temp = vertices[heap[pos][0]]
                vertices[heap[pos][0]] = vertices[heap[pos//2][0]]
                vertices[heap[pos//2][0]] = temp

                temp = heap[pos]
                heap[pos] = heap[pos//2]
                heap[pos//2] = temp

                pos = pos//2


        def pop(heap, vertices):
            '''
            pop the root node from min heap
            time complexity: O(log(V))
            '''
            u, dis = heap[0]
            heap[0] = heap[len(heap)-1]
            del heap[len(heap)-1]
            vertices[u] = -1
            if len(heap) > 0:
                vertices[heap[0][0]] = 0
            nowpos = 0
            smaller = nowpos * 2 + 1
            if nowpos*2+2 < len(heap) and heap[nowpos*2+2][1] < heap[smaller][1]:
                smaller = nowpos*2+2
            while smaller < len(heap) and heap[smaller][1] < heap[nowpos][1]:
                temp = vertices[heap[nowpos][0]]
                vertices[heap[nowpos][0]] = vertices[heap[smaller][0]]
                vertices[heap[smaller][0]] = temp

                temp = heap[smaller]
                heap[smaller] = heap[nowpos]
                heap[nowpos] = temp
                nowpos = smaller
                smaller = nowpos * 2 + 1
                if nowpos*2+2 < len(heap) and heap[nowpos*2+2][1] < heap[smaller][1]:
                    smaller = nowpos*2+2
            return u, dis


        def reduceTo(heap, vertices, num, v):
            '''
            reduce the value of root v to num
            time complexity: O(log(V))
            '''
            pos = vertices[v]
            if pos == -1:
                return 
            heap[pos][1] = num
            while heap[pos][1] < heap[pos//2][1]:
                temp = vertices[heap[pos][0]]
                vertices[heap[pos][0]] = vertices[heap[pos//2][0]]
                vertices[heap[pos//2][0]] = temp

                temp = heap[pos]
                heap[pos] = heap[pos//2]
                heap[pos//2] = temp

                pos = pos//2

        tlis = [float('inf') for v in range(self.V * 3)]
        # for u, w in self.adjaTable[home]:
        #     tlis[u] = w
        tlis[home] = 0
        for u in range(self.V * 3):
            push(heap, vertices, tlis[u], u)
            #dist[u] = tlis[u]
        while len(heap) > 0:
            v, dis = pop(heap, vertices)
            if v == destination+2 * self.V:
                break
            for u, w in self.adjaTable[v]:
                if vertices[u] != -1 and dis + w < heap[vertices[u]][1]:
                    pred[u] = v
                    dist[u] = dis + w
                    reduceTo(heap, vertices, dis + w, u)
        # organize the path according to pred
        # print(pred)
        path = [destination]
        nowpos = destination+2 * self.V
        while nowpos != home:
            prepos = pred[nowpos]
            if path[-1] != prepos % self.V:
                path.append(prepos % self.V)
            nowpos = prepos
        return dist[destination+2 * self.V], path[::-1]


def main():
    g = Graph("gfile3.txt")
    root, depth = g.shallowest_spanning_tree() #this runs task 2
    print(root, depth)
    #run task 3, with 3 as the start, 7 as the desination, 
    #2, 5 & 11 as ice locations, and 4 & 1 as drink locations 
    length, path = g.shortest_errand(0,8,[1,5,8],[4,6])
    print(length, path)

if __name__ == '__main__':
    main()
