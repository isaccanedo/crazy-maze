import pygame
from enum import Enum


class Action(Enum):
    stand_by = -1
    quit_game = 0
    change_screen = 1
    player_dead = 2
    local_loop = 3
    player_win = 4


MISSING = object()


class Window:

    font_location = "fonts/conthrax-sb.ttf"
    size = (1000, 667)
    window = pygame.display.set_mode(size)
    grass_image = pygame.image.load("images/grass2.jpg")
    grass_image = pygame.transform.scale(grass_image, size)
    heart_image = pygame.image.load("images/heart.png")
    heart_image = pygame.transform.scale(heart_image, (24,24))
    pressed_start_button = pygame.image.load("images/initial_button_pressed.png")
    pressed_start_button = pygame.transform.scale(pressed_start_button, (int(720 / 2), int(231 / 2)))
    start_button = pygame.image.load("images/initial_button.png")
    start_button = pygame.transform.scale(start_button, (int(720 / 2), int(231 / 2)))
    exit_button = pygame.image.load("images/exit_button.png")
    exit_button = pygame.transform.scale(exit_button, (360, 115))
    pressed_exit_button = pygame.image.load("images/exit_button_pressed.png")
    pressed_exit_button = pygame.transform.scale(pressed_exit_button, (360, 115))
    restart_button = pygame.image.load("images/restart_button.png")
    restart_button = pygame.transform.scale(restart_button, (360, 115))
    pressed_restart_button = pygame.image.load("images/restart_button_pressed.png")
    pressed_restart_button = pygame.transform.scale(pressed_restart_button, (360, 115))
    game_over_image = pygame.image.load("images/game_over.png")
    game_over_image = pygame.transform.scale(game_over_image, size)
    you_escaped_image = pygame.image.load("images/you_escaped.png")
    you_escaped_image = pygame.transform.scale(you_escaped_image, size)

    def __init__(self, background, maze_size):
        self.background = background
        pygame.init()

        # showMazeScreen variables:
        ## Coloquei elas aqui, pois as imagens precisam ser carregadas apenas uma vez, caso contrario, o jogo fica
        ## muito lento
        self.pxl_x = self.size[0] / (maze_size[0] * 2 + 1)
        self.pxl_y = self.size[1] / (maze_size[1] * 2 + 1)

        self.wall_image = pygame.image.load("images/wall.png")
        self.wall_image = pygame.transform.scale(self.wall_image, (int(self.pxl_x + 1), int(self.pxl_y + 1)))
        self.exit_image = pygame.image.load("images/exit.png")
        self.exit_image = pygame.transform.scale(self.exit_image, (int(self.pxl_x + 1), int(self.pxl_y + 1)))

        self.background_image = pygame.image.load(self.background)
        self.background_image = pygame.transform.scale(self.background_image, self.size)

    def showText(self, text, position, font_size, color):
        title_font = pygame.font.Font(self.font_location, font_size)
        text_surface = title_font.render(text, True, color)
        text_rectangle = text_surface.get_rect()
        text_rectangle.center = position
        self.window.blit(text_surface, text_rectangle)

    def showImage(self, image_path, position, scale=MISSING):
        image = pygame.image.load(image_path)
        if scale is not MISSING:
            image = pygame.transform.scale(image, scale)
        self.window.blit(image, position)

    def initialWindow(self):
        pygame.display.set_caption("Crazy Maze")
        self.window.blit(self.start_button, (self.size[0] / 2 - 180, 450))
        self.window.blit(self.background_image, (0, 0))
        self.showImage("images/title_initial.png", (2, 40), (int(1996 / 2), int(667 / 2)))


    def showMazeScreen(self, player_list, maze, lives):
        self.window.blit(self.grass_image, (0, 0))

        # Draw the maze
        for y in range(maze.height):
            for x in range(maze.width):
                if maze.matrix[y][x] == 1:
                    self.window.blit(self.wall_image, (x*self.pxl_x, y*self.pxl_y))

        # Draw exit sign
        self.window.blit(self.exit_image, ((maze.width -2) * self.pxl_x, (maze.height - 2)* self.pxl_y))

        # Draw characters
        player_list.draw(self.window)

        # Draw player lives
        self.showText("Vidas", (50, 15), 23, (255, 255, 255))
        for i in range(0, lives):
            self.window.blit(self.heart_image, (110 + 26*i, 3))
        pygame.display.flip()

    def showEndScreen(self, time):
        self.window.blit(self.game_over_image, (0, 0))
        # self.showImage("images/text_box.png", (110, 40), (758, 234))
        # self.showText("Você morreu!", (470, 90), 50, (23, 39, 36))
        # self.showText("Você durou apenas", (470, 140), 25, (255, 255, 255))

        if time <= 60:
            time = int(time*100)
            time = time/100.0
            self.showText("Em apenas " + str(time) + " segundos no jogo!", (self.size[0] / 2, 400), 25, (255, 255, 255))
        else:
            time = time/60
            time = int(time*100)
            time = time/100.0
            self.showText("Em apenas " + str(time) + " minutos no jogo!", (self.size[0] / 2, 400), 25, (255, 255, 255))

        # self.showText("Tente sair do labirinto", (470, 210), 40, (23, 39, 36))
        # self.showText("sã e salvo!", (470, 250), 40, (23, 39, 36))
        self.window.blit(self.restart_button, (self.size[0] / 4 - 180, 500))
        self.window.blit(self.exit_button, (3*self.size[0] / 4 - 180, 500))


    def showWinningScreen(self, time):
        self.window.blit(self.you_escaped_image, (0, 0))
        self.showImage("images/text_box.png", (100, 50), (758, 200))
        self.showText("Você Escapou!!", (480, 120), 60, (23, 39, 36))

        if time <= 60:
            time = int(time * 100)
            time = time / 100.0
            self.showText("Em um total de " + str(time) + " segundos no jogo!", (self.size[0] / 2, 180), 25,
                          (23, 39, 36))
        else:
            time = time / 60
            time = int(time * 100)
            time = time / 100.0
            self.showText("Em um total de " + str(time) + " minutos no jogo!", (self.size[0] / 2, 180), 25,
                          (23, 39, 36))
