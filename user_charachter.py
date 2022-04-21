from character import Character
import pygame
from open_window import Action
from algorithm import AuxFunc
import numpy as np


class UserCharacter(Character):

    def __init__(self, lives, mediator):
        Character.__init__(self, mediator)
        self.size = (int(mediator.game_screen.pxl_x-1), int(mediator.game_screen.pxl_y))

        for i in range(1, 4):
            image_aux = pygame.image.load('images/Walk(' + str(i) + ').png')
            image_aux = pygame.transform.scale(image_aux, self.size)
            self.images.append(image_aux)
            self.image = self.images[0]
            self.rect = self.image.get_rect()

        self.rect.x = int(self.mediator.game_screen.pxl_x) + 1
        self.rect.y = int(self.mediator.game_screen.pxl_y) + 1
        self.lives = lives


    def control(self, y, x):

        # character's current position:
        max_pos_x = self.rect.x + self.size[0] - 7  # o -7 eh para dar uma folga no seu cabelo da frente
        min_pos_x = self.rect.x + 7  # o +7 eh para dar uma folga nas suas costas
        max_pos_y = self.rect.y + self.size[1]
        min_pos_y = self.rect.y + 15  ## o +15 eh para dar uma folga no seu cabelo

        can_move = False
        blocked = True

        if x > 0:
            desired_pos1 = (max_pos_x + 4 * x, min_pos_y)
            desired_pos2 = (max_pos_x + 4 * x, max_pos_y)
            desired_node1 = self.getNode(desired_pos1[0], desired_pos1[1])
            desired_node2 = self.getNode(desired_pos2[0], desired_pos2[1])
            if self.mediator.maze.matrix[desired_node1[0]][desired_node1[1]] == 0 and \
                    self.mediator.maze.matrix[desired_node2[0]][desired_node2[1]] == 0:  # if is grass (path)
                can_move = True
                blocked = False

        elif x < 0:
            desired_pos1 = (min_pos_x + 4 * x, min_pos_y)
            desired_pos2 = (min_pos_x + 4 * x, max_pos_y)
            desired_node1 = self.getNode(desired_pos1[0], desired_pos1[1])
            desired_node2 = self.getNode(desired_pos2[0], desired_pos2[1])
            if self.mediator.maze.matrix[desired_node1[0]][desired_node1[1]] == 0 and \
                    self.mediator.maze.matrix[desired_node2[0]][desired_node2[1]] == 0:  # if is grass (path)
                can_move = True
                blocked = False

        elif y > 0:
            desired_pos1 = (min_pos_x, max_pos_y + 4 * y)
            desired_pos2 = (max_pos_x, max_pos_y + 4 * y)
            desired_node1 = self.getNode(desired_pos1[0], desired_pos1[1])
            desired_node2 = self.getNode(desired_pos2[0], desired_pos2[1])
            if self.mediator.maze.matrix[desired_node1[0]][desired_node1[1]] == 0 and \
                    self.mediator.maze.matrix[desired_node2[0]][desired_node2[1]] == 0:  # if is grass (path)
                can_move = True
                blocked = False

        elif y < 0:
            desired_pos1 = (min_pos_x, min_pos_y + 4 * y)
            desired_pos2 = (max_pos_x, min_pos_y + 4 * y)
            desired_node1 = self.getNode(desired_pos1[0], desired_pos1[1])
            desired_node2 = self.getNode(desired_pos2[0], desired_pos2[1])
            if self.mediator.maze.matrix[desired_node1[0]][desired_node1[1]] == 0 and \
                    self.mediator.maze.matrix[desired_node2[0]][desired_node2[1]] == 0:  # if is grass (path)
                can_move = True
                blocked = False

        if blocked:
            desired_pos1 = (max_pos_x + 4 * x, min_pos_y)
            desired_pos2 = (max_pos_x + 4 * x, max_pos_y)
            desired_node1 = self.getNode(desired_pos1[0], desired_pos1[1])
            desired_node2 = self.getNode(desired_pos2[0], desired_pos2[1])
            if self.mediator.maze.matrix[desired_node1[0]][desired_node1[1]] == 0 and \
                    self.mediator.maze.matrix[desired_node2[0]][desired_node2[1]] == 0:  # if is grass (path)
                blocked = False
            else:
                desired_pos1 = (min_pos_x + 4 * x, min_pos_y)
                desired_pos2 = (min_pos_x + 4 * x, max_pos_y)
                desired_node1 = self.getNode(desired_pos1[0], desired_pos1[1])
                desired_node2 = self.getNode(desired_pos2[0], desired_pos2[1])
                if self.mediator.maze.matrix[desired_node1[0]][desired_node1[1]] == 0 and \
                        self.mediator.maze.matrix[desired_node2[0]][desired_node2[1]] == 0:  # if is grass (path)
                    blocked = False

                else:
                    desired_pos1 = (min_pos_x, max_pos_y + 4 * y)
                    desired_pos2 = (max_pos_x, max_pos_y + 4 * y)
                    desired_node1 = self.getNode(desired_pos1[0], desired_pos1[1])
                    desired_node2 = self.getNode(desired_pos2[0], desired_pos2[1])
                    if self.mediator.maze.matrix[desired_node1[0]][desired_node1[1]] == 0 and \
                            self.mediator.maze.matrix[desired_node2[0]][desired_node2[1]] == 0:  # if is grass (path)
                        blocked = False

                    else:
                        desired_pos1 = (min_pos_x, min_pos_y + 4 * y)
                        desired_pos2 = (max_pos_x, min_pos_y + 4 * y)
                        desired_node1 = self.getNode(desired_pos1[0], desired_pos1[1])
                        desired_node2 = self.getNode(desired_pos2[0], desired_pos2[1])
                        if self.mediator.maze.matrix[desired_node1[0]][desired_node1[1]] == 0 and \
                                self.mediator.maze.matrix[desired_node2[0]][desired_node2[1]] == 0:  # if is grass (path)
                            blocked = False

        if can_move or blocked:
            self.rect.x += 4 * x
            self.rect.y += 4 * y
            if x > 0 or y > 0:
                self.frame += 1
                self.frame = self.frame % 3
                self.image = self.images[self.frame]
            elif x < 0 or y < 0:
                self.frame -= 1
                if self.frame < 0:
                    self.frame = 2
                self.image = self.images[self.frame]



    def updateLives(self, number):
        self.lives += number

        if self.lives == 0:
            return Action.player_dead
        else:
            return Action.stand_by

    def detectMonsterCollision(self, monster_1, monster_2, monster_3):

        monster_1_distance = np.sqrt((monster_1.rect.x - self.rect.x)**2 + (monster_1.rect.y - self.rect.y)**2)
        monster_2_distance = np.sqrt((monster_2.rect.x - self.rect.x)**2 + (monster_2.rect.y - self.rect.y)**2)
        monster_3_distance = np.sqrt((monster_3.rect.x - self.rect.x)**2 + (monster_3.rect.y - self.rect.y)**2)

        if monster_1_distance < 32:
            self.rect.x += 1
            self.rect.y += 1

            monster_1.resetPosition()
            monster_1.findNewPath(self)

            return self.updateLives(-1)

        elif monster_2_distance < 32:
            self.rect.x += 1
            self.rect.y += 1

            monster_2.resetPosition()
            monster_2.findNewPath(self)

            return self.updateLives(-1)

        elif monster_3_distance < 32:
            self.rect.x += 1
            self.rect.y += 1

            monster_3.resetPosition()
            monster_3.findNewPath(self)

            return self.updateLives(-1)

        else:
            return Action.stand_by

    def detectWin(self, action_local):
        position = self.getCharacterRectNode()

        # winning has preference
        if position[1] == self.mediator.maze.width - 2 and position[0] == self.mediator.maze.height - 2:
            return Action.player_win

        return action_local
