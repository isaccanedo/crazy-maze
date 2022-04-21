import pygame


class Character(pygame.sprite.Sprite):

    def __init__(self, mediator):
        self.mediator = mediator
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.frame = 0
        self.rect = None

    def getCharacterRectNode(self):

        matrix_shape = self.mediator.maze.matrix.shape

        matrix_x = int((self.rect.x+self.mediator.game_screen.pxl_x/2)*matrix_shape[1]/self.mediator.game_screen.size[0])
        matrix_y = int((self.rect.y+self.mediator.game_screen.pxl_y/2)*matrix_shape[0]/self.mediator.game_screen.size[1])

        node = (matrix_y, matrix_x)

        return node

    def getNode(self, position_x, position_y):

        matrix_shape = self.mediator.maze.matrix.shape

        character_matrix_x = int(position_x*matrix_shape[1]/self.mediator.game_screen.size[0])
        character_matrix_y = int(position_y*matrix_shape[0]/self.mediator.game_screen.size[1])

        character_node = (character_matrix_y, character_matrix_x)

        return character_node
