import pygame
from collections import deque
import sys

sys.setrecursionlimit(100000)

maze: list[list[str]] = []

with open('laberinto_3.in', 'r') as file:
    for (i, line) in enumerate(file):
        if i == 0:
            continue
        maze.append([])
        for c in list(line):
            if c == '\n':
                continue
            maze[i-1].append(c)


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

    def ancestors(self, nodo: Node | None) -> list[Node]:
        if not nodo:
            return []

        curr = nodo
        ancestros: list[Node] = [curr]

        while curr.parent != None:
            if curr.parent is curr:
                break

            ancestros.append(curr.parent)
            curr = curr.parent

        return ancestros

    def descendants(self, nodo: Node | None) -> list[Node]:
        if not nodo:
            return []

        descendientes: list[Node] = [nodo]

        def list_descendants(arr: list[Node], nodo: Node) -> list[Node]:
            for child in nodo.children:
                arr.append(child)
                list_descendants(arr, child)

            return arr

        list_descendants(descendientes, nodo)

        return descendientes

    def bread_first_search(self, nodo) -> list[Node]:
        q: list[Node] = [nodo]

        found = False
        for parent in q:
            for child in parent.children:
                q.append(child)
                if maze[child.dato[1]][child.dato[0]] == 'B':
                    found = True
                    break
            if found:
                break

        return q

    def depth_first_search(self, nodo: Node | None) -> list[Node]:
        desc = self.descendants(nodo)

        path: list[Node] = []

        for node in desc:
            path.append(node)
            if maze[node.dato[1]][node.dato[0]] == 'B':
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
                return (x, y)

    return (-1, -1)


pos_A = findStart(maze)

arbol = Tree()
root = arbol.create_root(pos_A)

checked_pos.add((root.dato[1], root.dato[0]))


def build_big_tree(parent: Node):
    q = deque()

    def build_tree(parent: Node):
        if parent.dato[1] - 1 >= 0 and maze[parent.dato[1] - 1][parent.dato[0]] != '0':  # ARRIBA
            if (parent.dato[1] - 1, parent.dato[0]) not in checked_pos:
                checked_pos.add((parent.dato[1] - 1, parent.dato[0]))

                new = arbol.insert_child(
                    parent, (parent.dato[0], parent.dato[1] - 1))

                if new:
                    # print("Arriba!", new.dato)
                    q.append(new)

        if parent.dato[0] - 1 >= 0 and maze[parent.dato[1]][parent.dato[0] - 1] != '0':  # IZQUIERDA
            if (parent.dato[1], parent.dato[0] - 1) not in checked_pos:
                checked_pos.add((parent.dato[1], parent.dato[0] - 1))

                new = arbol.insert_child(
                    parent, (parent.dato[0] - 1, parent.dato[1]))

                if new:
                    # print("Izquierda!", new.dato)
                    q.append(new)

        # ABAJO
        if parent.dato[1] + 1 < len(maze) and maze[parent.dato[1] + 1][parent.dato[0]] != '0':
            if (parent.dato[1] + 1, parent.dato[0]) not in checked_pos:
                checked_pos.add((parent.dato[1] + 1, parent.dato[0]))

                new = arbol.insert_child(
                    parent, (parent.dato[0], parent.dato[1] + 1))

                if new:
                    # print("Abajo!", new.dato)
                    q.append(new)

        # DERECHA
        if parent.dato[0] + 1 < len(maze[0]) and maze[parent.dato[1]][parent.dato[0] + 1] != '0':
            if (parent.dato[1], parent.dato[0] + 1) not in checked_pos:
                checked_pos.add((parent.dato[1], parent.dato[0] + 1))

                new = arbol.insert_child(
                    parent, (parent.dato[0] + 1, parent.dato[1]))

                if new:
                    # print("Derecha!", new.dato)
                    q.append(new)
        # print(q)
        # print(q)
        if len(q) != 0:
            build_tree(q.popleft())
    build_tree(parent)


build_big_tree(root)
print('\n\n\n\n\n')
# camino = arbol.depth_first_search(root)
camino = arbol.bread_first_search(root)
camino_recorrido = set()


pygame.init()

ancho_pantalla, alto_pantalla = 1000, 700
tam_pantalla = (ancho_pantalla, alto_pantalla)
pantalla = pygame.display.set_mode(tam_pantalla)
pygame.display.set_caption("Prueba")
colores = dict()
colores['0'] = (134, 7, 0)
colores['1'] = (255, 255, 255)
colores['A'] = (0, 255, 0)
colores['B'] = (255, 0, 0)

tam_x = len(maze[0])
tam_y = len(maze)

tam = 25

for punto in camino:
    x = punto.dato[0]
    y = punto.dato[1]

    camino_recorrido.add((x, y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    esq_izq = tam

    for i in range(tam_y):
        for j in range(tam_x):
            esq_izq = tam*j
            esq_sup = tam*i
            ancho = tam
            alto = tam

            pos = (esq_izq, esq_sup, ancho, alto)
            color = colores[maze[i][j]]

            if (j, i) in camino_recorrido:
                color = (0, 50, 100)

            pygame.draw.rect(pantalla, color, pos)

    esq_izq = tam*x
    esq_sup = tam*y
    ancho = tam
    alto = tam
    pos = (esq_izq, esq_sup, ancho, alto)
    color = (0, 0, 0)
    pygame.draw.rect(pantalla, color, pos)

    pygame.display.update()
    pygame.time.delay(100)

ultimo = camino[-1]

camino = arbol.ancestors(ultimo)
camino_recorrido = set()

for punto in camino:
    x = punto.dato[0]
    y = punto.dato[1]

    camino_recorrido.add((x, y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    esq_izq = tam

    for i in range(tam_y):
        for j in range(tam_x):
            esq_izq = tam*j
            esq_sup = tam*i
            ancho = tam
            alto = tam

            pos = (esq_izq, esq_sup, ancho, alto)
            color = colores[maze[i][j]]

            if (j, i) in camino_recorrido:
                color = (0, 0, 255)

            pygame.draw.rect(pantalla, color, pos)

    esq_izq = tam*x
    esq_sup = tam*y
    ancho = tam
    alto = tam
    pos = (esq_izq, esq_sup, ancho, alto)
    color = (0, 0, 0)
    pygame.draw.rect(pantalla, color, pos)

    pygame.display.update()
    pygame.time.delay(50)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
