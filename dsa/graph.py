class Graph:
    def __init__(self):
        self.graph = {}

    def add_vertex(self, vertex):
        if vertex not in self.graph:
            self.graph[vertex] = []

    def add_edge(self, src, dest):
        self.add_vertex(src)
        self.add_vertex(dest)
        self.graph[src].append(dest)

    def get_neighbors(self, vertex):
        return self.graph.get(vertex, [])

    def remove_vertex(self, vertex):
        if vertex in self.graph:
            del self.graph[vertex]
        for key in self.graph:
            self.graph[key] = [neighbor for neighbor in self.graph[key] if neighbor != vertex]

    def vertices(self):
        return list(self.graph.keys())
