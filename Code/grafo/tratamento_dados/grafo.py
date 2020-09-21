
class Graph:
    def __init__(self, vertices):
        self.__nodes = vertices
        self.__edges = {}
    def add_edges(self, node1,node2):
        if (min(node1,node2),max(node1,node2)) in self.__edges:
            self.__edges[(min(node1,node2),max(node1,node2))] += 1 
        else:
            self.__edges[(min(node1,node2),max(node1,node2))] = 0
    
    def add_edges_from_list(self, lista):
        aux = 0
        pares_criados = [(min(val1,val2), max(val1,val2)) 
            for val1 in lista[:len(lista)//2] 
            for val2 in lista[aux+1:] if val1 != val2 ]
        for par in pares_criados: 
            if par in self.__edges:
                self.__edges[par] += 1 
            else:
                self.__edges[par] = 0
        
    def get_edges(self):
        return self.__edges  
    
