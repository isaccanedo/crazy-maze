from open_window import Window
from maze import Maze


class Mediator:

    maze = None

    def __init__(self, maze_shape):
        self.game_screen = Window('images/initial_background.jpg', maze_shape)

    def createMaze(self, maze_shape):
        self.maze = Maze(maze_shape[0], maze_shape[1])
