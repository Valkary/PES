import pygame

maze: list[list[str]] = []

with open('laberinto_1.in', 'r') as file:
    for (i, line) in enumerate(file):
        if i == 0: continue
        maze.append([]);
        for c in list(line):
            if c == '\n': continue
            maze[i-1].append(c)

print(maze)

checked_pos: set[tuple[int, int]] = set()

class Node:
    def __init__(self, dato: tuple[int, int]) -> None:
        self.dato = dato
        self.parent: "Node" | None = None
        self.children: list["Node"] = list()

    def __repr__(self) -> str:
        return f"{self.dato}"

class Tree:
    def __init__(self) -> None:
        self.root: Node | None = None
        self.size: int = 0
        self.dfs: list[tuple[int, int]] = []

    def create_root(self, dato: tuple[int, int]) -> Node:
        root = Node(dato)
        self.root = root
        self.size = 1
        return root

    def insert_child(self, parent: Node | None, dato: tuple[int, int]) -> Node | None:
        if not self.root:
            print("No se pueden agregar hijos si no hay raiz")
            return None
        elif not parent:
            print("Se tiene que dat un nodo")
            return None

        self.size += 1
        child = Node(dato)
        child.parent = parent
        parent.children.append(child)
        return child

    def ancestors(self, nodo: Node | None) -> list[tuple[int, int]]:
        if not nodo:
            return []

        curr = nodo

        ancestros: list[tuple[int, int]] = [curr.dato]

        while curr.parent != None:
            if curr.parent is curr:
                break

            ancestros.append(curr.parent.dato)
            curr = curr.parent

        return ancestros

    def descendants(self, nodo: Node | None) -> list[tuple[int, int]]:
        if not nodo:
            return []

        descendientes: list[tuple[int, int]] = [nodo.dato]

        def list_descendants(arr: list[tuple[int, int]], nodo: Node) -> list[tuple[int, int]]:
            for child in nodo.children:
                arr.append(child.dato)
                list_descendants(arr, child)

            return arr

        list_descendants(descendientes, nodo)

        return descendientes
    
    def depth_first_search(self, nodo: Node | None) -> list[tuple[int, int]]:
        desc = self.descendants(nodo)

        path: list[tuple[int, int]] = []

        for node in desc:
            path.append(node)

            if maze[node[1]][node[0]] == 'B':
                break

        return path

    def size_tree(self) -> int:
        return self.size

    def depth_tree(self, nodo: Node | None) -> int:
        if not nodo:
            return -1

        count = 0
        curr = nodo

        while curr.parent and curr is not curr.parent:
            curr = curr.parent
            count += 1

        return count

    def height_tree(self, nodo: Node | None) -> int:
        if not nodo:
            return -1
        if not nodo.children:
            return 0
        return 1 + max(map(self.height_tree, nodo.children))
    
def findStart(maze: list[list[str]]) -> tuple[int, int]:
    for (y, row) in enumerate(maze):
        for (x, val) in enumerate(row):
            if val == 'A':
                return (x,y)
            
    return (-1, -1)

pos_A = findStart(maze)

arbol = Tree()
root = arbol.create_root(pos_A)

checked_pos.add((root.dato[1], root.dato[0]))

def build_tree(parent: Node):
    if parent.dato[1] - 1 >= 0 and maze[parent.dato[1] - 1][parent.dato[0]] != '0': # ARRIBA
        if (parent.dato[1] - 1, parent.dato[0]) not in checked_pos:
            checked_pos.add((parent.dato[1] - 1, parent.dato[0]))

            new = arbol.insert_child(parent, (parent.dato[0], parent.dato[1] - 1))
            
            if new:
                # print("Arriba!", new.dato)
                build_tree(new)        
    
    if parent.dato[0] - 1 >= 0 and maze[parent.dato[1]][parent.dato[0] - 1] != '0': # IZQUIERDA
        if (parent.dato[1], parent.dato[0] - 1) not in checked_pos:
            checked_pos.add((parent.dato[1], parent.dato[0] - 1))

            new = arbol.insert_child(parent, (parent.dato[0] - 1, parent.dato[1]))
        
            if new:
                # print("Izquierda!", new.dato)
                build_tree(new)

    if parent.dato[1] + 1 < len(maze) and maze[parent.dato[1] + 1][parent.dato[0]] != '0': # ABAJO
        if (parent.dato[1] + 1, parent.dato[0]) not in checked_pos:
            checked_pos.add((parent.dato[1] + 1, parent.dato[0]))

            new = arbol.insert_child(parent, (parent.dato[0], parent.dato[1] + 1))

            if new:
                # print("Abajo!", new.dato)
                build_tree(new)
        

    if parent.dato[0] + 1 < len(maze[0]) and maze[parent.dato[1]][parent.dato[0] + 1] != '0': # DERECHA
        if (parent.dato[1], parent.dato[0] + 1) not in checked_pos:
            checked_pos.add((parent.dato[1], parent.dato[0] + 1))
            
            new = arbol.insert_child(parent, (parent.dato[0] + 1, parent.dato[1]))
        
            if new:
                # print("Derecha!", new.dato)
                build_tree(new)

build_tree(root)

# print(root.dato)
# print(root.children[0].dato)
# print(arbol.descendants(root))

print("==> DESCENDANTS")
print(len(arbol.descendants(root)))
print("==> DEPTH FIRST SEARCH")
print(arbol.depth_first_search(root))