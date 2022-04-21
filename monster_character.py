import pygame
from open_window import Window
from algorithm import Algorithm
from enum import Enum
from character import Character


class Move(Enum):
    up = 1
    left = 2
    down = 3
    right = 4


class MonsterCharacter(Character):

    path_to_player = list()
    last_monster_node_x = -1
    last_monster_node_y = -1
    aStar_delay = 20
    aStar_counter = 0
    last_movement = 0

    def __init__(self, image_path, node, speed, mediator):
        Character.__init__(self, mediator)
        self.size = (25, 25)
        image_aux = pygame.image.load(image_path)
        image_aux = pygame.transform.scale(image_aux, self.size)
        self.image = image_aux
        self.rect = self.image.get_rect()
        start_position_x = node[0]*mediator.game_screen.pxl_x + 1
        start_position_y = node[1]*mediator.game_screen.pxl_y + 1
        self.start_position = (start_position_x, start_position_y)
        self.rect.x = start_position_x
        self.rect.y = start_position_y
        self.speed = speed

    def resetPosition(self):
        self.rect.x = self.start_position[0]
        self.rect.y = self.start_position[1]

    def findNewPath(self, player):

        # aStar eh muito pesado e estava causando lag no jogo, adicionei um delay para sua execucao:
        if self.aStar_counter == 0 or self.aStar_counter > self.aStar_delay:
            player_node = player.getCharacterRectNode()
            monster_node = self.getCharacterRectNode()
            if self.mediator.maze.matrix[player_node[0]][player_node[1]] == 0:
                if self.last_monster_node_x != monster_node[0] or self.last_monster_node_y != monster_node[1]:
                    self.path_to_player = Algorithm.aStar(self.mediator.maze.matrix, monster_node, player_node)

            self.aStar_counter = 0

        self.aStar_counter = self.aStar_counter + 1


    def inOnlyOneNode(self):
        up_left_corner = self.getNode(self.rect.x, self.rect.y)
        up_right_corner = self.getNode(self.rect.x+self.size[0], self.rect.y)

        if up_left_corner[0] != up_right_corner[0] or up_left_corner[1] != up_right_corner[1]:
            return False
        down_left_corner = self.getNode(self.rect.x, self.rect.y + self.size[1])
        if up_left_corner[0] != down_left_corner[0] or up_left_corner[1] != down_left_corner[1]:
            return False
        down_right_corner = self.getNode(self.rect.x + self.size[0], self.rect.y+self.size[1])
        if up_left_corner[0] != down_right_corner[0] or up_left_corner[1] != down_right_corner[1]:
            return False
        else:
            return True

    def updatePosition(self):
        if self.path_to_player is not None and len(self.path_to_player) > 0:
            next_node = self.path_to_player[-1]
            # monster's current position:
            up_left_corner = self.getNode(self.rect.x, self.rect.y)
            down_right_corner = self.getNode(self.rect.x + self.size[0], self.rect.y + self.size[1])

            if down_right_corner[0] - next_node[0] > 0:
                self.rect.y -= self.speed
            elif up_left_corner[0] - next_node[0] < 0:
                self.rect.y += self.speed
            elif down_right_corner[1] - next_node[1] > 0:
                self.rect.x -= self.speed
            elif up_left_corner[1] - next_node[1] < 0:
                self.rect.x += self.speed
            else:
                self.path_to_player.pop()
