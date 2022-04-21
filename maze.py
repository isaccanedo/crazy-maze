import numpy as np
import copy
from algorithm import Algorithm


# Usa o algoritmo de Prim, logo o labirinto é um conjunto de celulas conexas
# (o jogador pode chegar em qualquer celula partindo de qualquer celula)

# IMPORTANTE: Para que o labirinto seja dinamico, o jogador nao deve
#             ocupar uma poscao que antes era de uma parede, apenas posicao de celulas

# Ao longo do codigo tem-se usado a seguinte notacao:
#   - cell = noh do grafo
#   - node = posicao na matriz que descreve o labirinto
## sim, eh uma notacao confusa e deve ser ajeitada


class Maze:

    def __init__(self, num_cells_x, num_cells_y, start_cell=(0, 0)):
        self.num_cells_x = num_cells_x
        self.num_cells_y = num_cells_y
        self.start_cell = start_cell

        self.width = num_cells_x * 2 + 1
        self.height = num_cells_y * 2 + 1

        # Transition variable:
        self.update_counter = 0
        self.delay_counter = 0
        self.max_delay_counter = 25
        self.mazes_matrices = []

        self.matrix = Algorithm.prim(self)

    def newTrasition(self, player_node):
        self.update_counter = 0
        self.mazes_matrices = [self.matrix]

        start_node = player_node
        start_cell = (int((start_node[1]-1)/2), int((start_node[0]-1)/2))
        new_maze = Maze(self.num_cells_x, self.num_cells_y, start_cell)

        x = start_node[1]
        y = start_node[0]

        M = copy.deepcopy(self.matrix)
        j = 1
        while x - j >= 0 or x + j <= self.width or y - j >= 0 or y + j <= self.height:
            x_min, y_min = max(0, x - j), max(0, y - j)
            x_max, y_max = min(self.width, x + j), min(self.height, y + j)

            M[y_min: y_max, x_min] = copy.deepcopy(new_maze.matrix[y_min: y_max, x_min])
            M[y_min: y_max, x_max - 1] = copy.deepcopy(new_maze.matrix[y_min: y_max, x_max - 1])
            M[y_min, x_min:x_max] = copy.deepcopy(new_maze.matrix[y_min, x_min:x_max])
            M[y_max - 1, x_min:x_max] = copy.deepcopy(new_maze.matrix[y_max - 1, x_min:x_max])

            self.mazes_matrices.append(copy.deepcopy(M))
            j += 1

    def updateMaze(self, player_node):

        if self.delay_counter == self.max_delay_counter:
            if self.update_counter == 0 or self.update_counter >= len(self.mazes_matrices)-1:
                self.newTrasition(player_node)

            self.update_counter = self.update_counter + 1
            self.matrix = self.mazes_matrices[self.update_counter]
            self.delay_counter = 0

        else:
            self.delay_counter = self.delay_counter+1
