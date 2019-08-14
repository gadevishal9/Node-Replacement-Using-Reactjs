from flask import *
from json import *
from flask import request
from flask_cors import CORS, cross_origin
import networkx as nx
import math
import random
import json
app = Flask(__name__)
CORS(app)
def euclidean_distance(x1,y1,x2,y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)
def create_random_points(n):
    X = []
    Y = []
    #adds n ramndom X and Y co-ordinates
    for i in range(n):
        #random point is a random decimal number between 0 and 2*n
        random_point = random.uniform(0,2*n)
        #add generated random X co-ordinate to X is "random_point" is not in X
        if random_point not in X:
            X.append(random_point)
        random_point = random.uniform(0,2*n)
        #add generated random X co-ordinate to X is "random_point" is not in X
        if random_point not in Y:
            Y.append(random_point)
    #X = [list of random X co-ordinates]
    #Y = [list of random Y co-ordinates]
    return X,Y
def create_json(mst_t,name):
    nodes = [{'id': str(i)}
        for i in mst_t.nodes()]
    links = [{'source': str(v), 'target': str(u), 'label' : str(round(w['weight'],2)) }
        for v,u,w in mst_t.edges(data = True)]
    path = '/Users/vishalgade95/my-algo-project/src/'+ name+'.json'
    return json.dumps({'nodes': nodes, 'links': links})
def create_new_json(mst_t,name):
    nodes = [{'id': str(i), 'label':str(i),'title' : 'title'+str(i)}
        for i in mst_t.nodes()]
    links = [{'from': str(v), 'to': str(u) }
        for v,u,w in mst_t.edges(data = True)]
    
    path = '/Users/vishalgade95/my-algo-project/src/'+ name+'.json'
    return json.dumps({'nodes': nodes, 'edges': links})
def isCyclicUtil(visited,adjacency_matrix,i,par):
        #recurse through all neighbouring nodes of i
    for j in adjacency_matrix[i]:
        #if node j is visited and j is not parent of i, ie j!=par then return True
        if visited[j] and j!= par:
            return True
        elif not visited[j]:
            #make the node j as visited
            visited[j] = True
            if isCyclicUtil(visited,adjacency_matrix,j,i):
                return True
    return False
def iscyclic(mst_t):
    nodes = list(mst_t.nodes())
    visited = {}
    #initialize all visited nodes as False.
    for i in nodes:
        visited[i] = False
    adjacency_matrix = {}
    # create adjacency matrix. This adjacency matrix is of the form :
    # adjacency_matrix = {'node' : [list of neighbouring nodes of 'node']}
    for i in mst_t.edges:
        v,d =i
        if v not in adjacency_matrix and d not in adjacency_matrix:
            vertices = []
            vertices.append(d)
            adjacency_matrix[v] = vertices
            vertices = []
            vertices.append(v)
            adjacency_matrix[d] = vertices
        elif v not in adjacency_matrix or d not in adjacency_matrix:
            if v not in adjacency_matrix:
                vertices = []
                vertices.append(d)
                adjacency_matrix[v] = vertices
                adjacency_matrix[d].append(v)
            else:
                vertices = []
                vertices.append(v)
                adjacency_matrix[d] = vertices
                adjacency_matrix[v].append(d)
        else:
            adjacency_matrix[d].append(v)
            adjacency_matrix[v].append(d)
    
    for i in nodes:
        if not visited[i]:
            visited[i] = True
            if isCyclicUtil(visited,adjacency_matrix,i,-1):
                return True
    return False
def create_mst(graph_list):
    #create empty graph
    mst_t = nx.Graph()
    #for each edge in graph, add it to graph is graph has a cycle
    for (v1,v2,w) in graph_list:
        current_edge = (v1,v2)
        mst_t.add_edge(*current_edge,weight = w['weight'])
        #check if the present mst has a cycle. If it has a cycle remove edge otherwise continue
        if iscyclic(mst_t):
            mst_t.remove_edge(*current_edge)
    return mst_t


@app.route('/', methods = ['POST'])
def hello_world():
    d =  request.get_json()
    # T is the initial empty graph
    T = nx.Graph()
    
    n = int(d['nodes'])
    B = int(d['budget'])
    # generate a list of random X and Y list of Co-Ordinates of size n
    X,Y = create_random_points(n)
    # Creates a complete graph
    for i in range(n):
        for j in range(i+1,n):
            T.add_edge(i,j,weight = euclidean_distance(X[i],Y[i],X[j],Y[j]))

    intial_graph = create_json(T,'initial_graph')       
    #graph_list is a list where each element of of the form (node1,node2,{'weight': number})
    graph_list = sorted(T.edges(data =True),key = lambda x:x[2]['weight'])

    #cretes a minimum spanning tree
    mst_t = create_mst(graph_list)
    print(mst_t)
    #create_json(mst_t,'mst_graph')
    #sum is current cost to construct the network
    mst_graph = create_json(mst_t,'fds')
    sum = 0
    for (v,d,x) in mst_t.edges(data = True):
        edge = (v,d)
        x['weight'] = x['weight'] - 1
        sum = sum + x['weight']
    # do while Present budget is greater than Total Budget
    Components = 1
    while(sum > B):
        maximum = -9999999
        #find edge with maximum weight
        for (v,d,x) in mst_t.edges(data = True):
            if x['weight'] > maximum:
                maximum = x['weight']
                edge = (v,d)
        #remove edge from the mst
        mst_t.remove_edge(*edge)
        sum -= maximum
        Components += 1
    #final number of Components
    print('Number of Components:', Components)
    
    final_graph = create_json(mst_t,'final_graph')

    
    all_graphs = {'all_graphs': [{'initial_graph' : intial_graph}, {'mst_graph' : mst_graph}, {'final_graph':final_graph}]};

    return (jsonify(all_graphs))

if __name__ == '__main__':
    app.run(debug=True)