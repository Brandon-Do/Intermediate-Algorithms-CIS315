import sys
import queue

class node():
    def __init__(self, name, link=None):
        """
        INPUT:
            number: node number or 'name',
            link: list containing name in 0 index, weight in 1 index. This indicates a link to another node
        OUTPUT: N/A

        Properties:
            self.number: the 'name' of the node.
            self.points:
                A dictionary of pointers to other nodes by 'name'.
                The key will be the 'name' of the node being pointed to and the value of self.pointers[number] will be the weight of the edge.
        """


        self.visited = False
        self.name = name
        self.pointers = []    #The edges that point from this specific node
        self.before = [] #The nodes that point to this

        if link != None:
            self.add_path(link)

    def add_path(self, edge):
        """
        INPUT:
            link: list containing name in 0 index, weight in 1 index. This indicates a link to another node
        OUTPUT: N/A

        Properties:
            Modifies self.pointers, adding a path to another node.
        """
        self.pointers.append(edge)

    def is_connected(self, node):
        for edge in self.pointers:
            if edge.end == node.name:
                return True
            return False


class edge():
    def __init__(self, node_a, node_b, distance):
        """
        INPUT:
            node_a:
                The order matters! The first node is A
            node_b:
                The node that is being pointed to, B
            distance: distance value
        OUTPUT: N/A

        Properties:
            will be used to store edges in a systematic way. A -> B
        """

        self.start = node_a
        self.end = node_b
        self.distance = distance
        self.in_between = []

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, edge):
            return self.start == other.start and self.end == other.end and self.distance == other.distance and self.in_between == self.in_between
        return False

    def merge(self, other):
        if self.start == other.end:
            new = edge(other.start, self.end, self.distance + other.distance)
            new.in_between = self.in_between + other.in_between + [self.start]
            return new

        elif self.end == other.start:
            new = edge(self.start, other.end, self.distance + other.distance)
            new.in_between = self.in_between + other.in_between + [self.end]
            return new

        return None

    def print(self):
        print(self.start, "->", self.end, ", Distance:", self.distance, ", In-Between:", self.in_between)

class graph():
    def __init__(self):
        """
        INPUT: N/A
        OUTPUT: N/A

        Properties:
            self.collection:
                A dictionary of nodes, where each key is the node.name
            self.paths:
                A dictionary of edges where each key is the path length
        """

        self.collection = {}
        self.paths = {}

    def print_nodes(self):
        for key in self.collection.keys():
            node = self.collection[key]
            print("Node:", node.name ,", Pointers:")
            for e in node.pointers:
                e.print()
            print("Nodes pointing to '{}'".format(node.name))
            for n in node.before:
                print(n.name)
            print()

    def print_paths(self):
        for key in self.paths.keys():
            for path in self.paths[key]:
                path.print()

    def add_path(self, e): #e is an edge
        if e != None:
            if e.distance in self.paths and not e in self.paths[e.distance]:
                self.paths[e.distance].append(e)
            else:
                self.paths[e.distance] = [e]


if __name__ == '__main__':

    G = graph()
    Q = queue.Queue()

    print("Enter the name of the file or enter 0 to exit.")

    if True:
    #for inpt in sys.stdin:

        #if inpt.strip() == '0':
         #   print("Exiting...")
          #  break

        #try:
        #Fix before turning in.
        if True:
            #f = open(inpt.strip())
            #FIX THIS WHEN YOU'RE DONE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            f = open('a.txt')

#            print("Running: {}".format(inpt))

            nodes, edges = f.readline().split(" ")

            start = None

            for _ in range(int(edges)):
                name, neighbor, distance = f.readline().strip().split(" ")
                name, neighbor, distance = int(name), int(neighbor), int(distance)
                new_edge = edge(name, neighbor, distance)

                if name in G.collection:
                    G.collection[name].add_path(new_edge)
                else:
                    G.collection[name] = node(name, new_edge)

                    if start == None:
                        start = G.collection[name]
                        start.visted = True
                        Q.put(start)

                if not neighbor in G.collection:
                    G.collection[neighbor] = node(neighbor)

                if distance in G.paths:
                    G.paths[distance].append(new_edge)
                else:
                    G.paths[distance] = [new_edge]

            while not Q.empty():
                current_node = Q.get()

                print("At: {}".format(current_node.name))

                for c_edge in current_node.pointers:
                    end_point = G.collection[c_edge.end]
                    if not end_point.visited:

                        if not current_node in end_point.before:
                            end_point.before.append(current_node)

                        edges = end_point.pointers #Make a copy or link it to the actual thing? The latter becomes a problem

                        for e_edge in end_point.pointers:
                            e = c_edge.merge(e_edge)
                            G.add_path(e)

                            if end_point.before:
                                for b_node in end_point.before:
                                    for b_edge in b_node.pointers:
                                        G.add_path(e_edge.merge(b_edge))

                        Q.put(end_point)



                """

                        T_Q = queue.Queue()
                        T_Q.put(current_node)

                        while not T_Q.empty():

                            t_node = T_Q.get()
                            for edge_in in t_node.pointers_in:
                                edges.append(edge_in)
                                T_Q.put(G.collection[edge_in.start])
                                
                        
                        print("Printing edges!")
                        for te in edges:
                            te.print()

                for key in G.paths:
                    for path in G.paths[key]:
                        print(path.start, path.end)
                    print()

                result = an_edge.merge(path)

                        if result:
                            new_edges.append(result)
                            #print([an_edge.start, an_edge.end], [path.start, path.end], [result.start, result.end])

                for e in new_edges:
                    if e.distance in G.paths and not e in G.paths[e.distance]:
                        G.paths[e.distance].append(e)
                    else:
                        G.paths[e.distance] = [e]
                """

    G.print_nodes()
    print()
    #G.print_paths()
    print()

    max_value = max(G.paths.keys())
    max_paths = len(G.paths[max_value])

    print("longest path: {}".format(max_value))
    if  max_paths > 1:
        print("number of longest paths: {}".format(max_paths))
        #except:
            #print("Error, file cannot be found or is formatted differently then expected.")