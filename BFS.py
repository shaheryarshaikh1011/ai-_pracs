from collections import deque
infinity = float('inf')
class Node:
    def __init__(self,state,parent=None,action=None,path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1
    def __repr__(self):
        return "<Node {}>".format(self.state)
    def expand(self,problem):
        return [self.child_node(problem,action)
                for action in problem.actions(self.state)]
    def child_node(self,problem,action):
        next_state = problem.result(self.state,action)
        next_node = Node(next_state,self,action,
                         problem.path_cost(self.path_cost,self.state,action,next_state) )
        return next_node
    def solution(self) :
        return [node.action for node in self.path()[1:]]
    def path(self):
        node, path_back = self,[]
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))
class Graph:
    def __init__(self,graph_dict=None,directed=True):
        self.graph_dict = graph_dict or {}
        self.directed = directed
        if not directed:
            self.make_undirected()
    def make_undirected(self):
        for a in list(self.graph_dict.keys()):
            print("Processing Node",a)
            for (b,dist) in self.graph_dict[a].items():
                print(" Node --> ",a," Conects ",b," By distance= ",dist)
    def get(self,a,b=None):
        links = self.graph_dict.get(a)
        if b is None:
            return links
        else:
            cost = links.get(b)
        return cost
    def nodes(self):
        nodelist = list()
        for key in self.graph_dict.key():
            nodelist.append(key)
        return nodelist            
def UndirectedGraph(graph_dict=None):
        return Graph(graph_dict = graph_dict , directed=False)
class problem(object):
    def __init__(self,initial,goal=None):
        self.initial = initial
        self.goal = goal
    def actions(self,state):
        raise NotImplementedError
    def result(self,state,action):
        raise NotImplementedError
    def goal_test(self,state):
        return state == self.goal
    def path_cost(self,c,state1,action,state2):
        return c+1
    def value(self,state):
        raise NotImplementedError
class GraphProblem(problem):
    def __init__(self,initial,goal,graph):
        problem.__init__(self,initial,goal)
        self.graph = graph
    def actions(self,A):
        return list(self.graph.get(A).keys())
    def result(self,state,action):
        return action
    def path_cost(self,cost_so_far,A,action,B):
        return cost_so_far + (self.graph.get(A,B) or infinity)
def breadth_first_tree_search(problem):
    frontier = deque([Node(problem.initial)])
    print("Searching Begins from : ",frontier)
    while frontier:
        node = frontier.popleft()
        print("Now Expansion :",node)
        if problem.goal_test(node.state):
            return node
        x=node.expand(problem)
        frontier.extend(x)
    return None
romania_map =UndirectedGraph( {
        'Arad':{ 'Zerind':75,'Sibiu':140,'Timisoara':118 },
        'Bucharest':{ 'Urziceni':85,'Pitesti':101,'Giurgiu':90,'Fagaras':211 },
        'Craiova':{ 'Drobeta':120,'Rimnicu':146,'Pitesti':138 },
        'Drobeta':{ 'Mehadia':75,'Craiovo':120 },
        'Eforie':{ 'Hirsova':86 },
        'Fagaras':{ 'Sibiu':99,'Bucharest':211 },
        'Hirsova':{ 'Urziceni':98,'Eforie':86 },
        'Iasi':{ 'Vaslui':92,'Neamt':87 },
        'Lugoj':{ 'Timisoara':111,'Mehadia':70 },
        'Oradea':{ 'Zerind':71,'Sibiu':151 },
        'Pitesti':{ 'Rimnicu':97,'Bucharest':101  },
        'Rimnicu':{ 'Sibiu':80,'Pitesti':97,'Craiova':146 },
        'Urziceni':{ 'Vaslui':142,'Bucharest':85,'Hirsova':98 },
        'Timisoara': {'Arad':118,'Lugoj':111 },
        'Sibiu':{ 'Arad':140,'Rimnicu':80,'Fagaras':99,'Oradea':151 },
        'Zerind':{'Arad':75,'Oradea':71} } )
print("After Constructing Graph")
print(romania_map.graph_dict)
print(" --------- ")
print("Children of Arad =",romania_map.get("Arad") )
print("Distance from Arad to Sibiu =",romania_map.get("Arad","Sibiu"))
print(" --------- ")
print("BFS Algoritm")
romania_problem = GraphProblem('Arad','Bucharest',romania_map)
print("Key of Arad",romania_problem.actions("Arad"))
finalnode=breadth_first_tree_search(romania_problem)
print("Solution Of ",romania_problem.initial," to ",romania_problem.goal,finalnode.solution())
print("Path Cost = ",finalnode.path_cost)
