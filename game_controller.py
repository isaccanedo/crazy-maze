from user_charachter import *
from maze import *
from monster_character import *
from parallel_threads import ParallelThreads
from mediator import Mediator
import time
import pygame


class GameController:

    playing_time = 0

    def __init__(self, maze_shape):
        self.mediator = Mediator(maze_shape)
        pygame.mixer.init()

    def quitGame(self):
        pygame.quit()

    def showInitialWindow(self):
        self.mediator.game_screen.initialWindow()
        action = Action.stand_by

        pygame.mixer.music.load("sounds/initial_track.mp3")
        pygame.mixer.music.play()

        while action == Action.stand_by:

            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play()

            mx, my = pygame.mouse.get_pos()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    action = Action.quit_game
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if (self.mediator.game_screen.size[0] / 2 - 180) <= mx <= (self.mediator.game_screen.size[0] / 2 + 180) and \
                            450 <= my <= 555.5:
                        action = Action.change_screen

            if (self.mediator.game_screen.size[0] / 2 - 180) <= mx <= (self.mediator.game_screen.size[0] / 2 + 180) and \
                    450 <= my <= 555.5:
                self.mediator.game_screen.window.blit(self.mediator.game_screen.pressed_start_button,
                                               (self.mediator.game_screen.size[0]/2 - 180, 450))

            else:
                self.mediator.game_screen.window.blit(self.mediator.game_screen.start_button,
                                                      (self.mediator.game_screen.size[0] / 2 - 180, 450))

            pygame.display.flip()

        return action

    def playGame(self, maze_shape):
        self.mediator.createMaze(maze_shape)
        player = UserCharacter(3, self.mediator)
        player_list = pygame.sprite.Group()

        red_monster = MonsterCharacter('images/monster1.png', (1, self.mediator.maze.height - 2), 2, self.mediator)
        green_monster = MonsterCharacter('images/monster2.png', (self.mediator.maze.width - 2, 1), 1, self.mediator)
        ugly_monster = MonsterCharacter('images/monster3.png', (self.mediator.maze.width - 2, 1), 2, self.mediator)
        player_list.add(player)
        player_list.add(red_monster)
        player_list.add(green_monster)
        player_list.add(ugly_monster)

        pygame.mixer.music.load("sounds/gameplay_track.mp3")
        pygame.mixer.music.play()

        action_local = Action.stand_by

        start_time = time.time()

        while action_local == Action.stand_by:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play()
            # update maze:
            self.mediator.maze.updateMaze(player.getCharacterRectNode())
            self.mediator.game_screen.showMazeScreen(player_list, self.mediator.maze, player.lives)
            ParallelThreads.findMonstersNewPosition(red_monster, green_monster, ugly_monster, player, player_list,
                                                    self.mediator)

            # Move characters
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[ord('a')]:
                player.control(0, -1)
                red_monster.updatePosition()
                green_monster.updatePosition()
                ugly_monster.updatePosition()
                ParallelThreads.findMonstersNewPosition(red_monster, green_monster, ugly_monster, player, player_list,
                                                        self.mediator)

            elif keys[pygame.K_RIGHT] or keys[ord('d')]:
                player.control(0, 1)
                red_monster.updatePosition()
                green_monster.updatePosition()
                ugly_monster.updatePosition()
                ParallelThreads.findMonstersNewPosition(red_monster, green_monster, ugly_monster, player, player_list,
                                                        self.mediator)

            elif keys[pygame.K_UP] or keys[ord('w')]:
                player.control(-1, 0)
                red_monster.updatePosition()
                green_monster.updatePosition()
                ugly_monster.updatePosition()
                ParallelThreads.findMonstersNewPosition(red_monster, green_monster, ugly_monster, player, player_list,
                                                        self.mediator)

            elif keys[pygame.K_DOWN] or keys[ord('s')]:
                player.control(1, 0)
                red_monster.updatePosition()
                green_monster.updatePosition()
                ugly_monster.updatePosition()
                ParallelThreads.findMonstersNewPosition(red_monster, green_monster, ugly_monster, player, player_list,
                                                        self.mediator)

            red_monster.updatePosition()
            green_monster.updatePosition()
            ugly_monster.updatePosition()

            action_local = player.detectMonsterCollision(red_monster, green_monster, ugly_monster)
            action_local = player.detectWin(action_local)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    action_local = Action.quit_game

        self.playing_time = time.time() - start_time

        return action_local

    def endScreen(self):
        pygame.mixer.music.load("sounds/defeat_track.mp3")
        pygame.mixer.music.play()

        exit_position = ((3 * self.mediator.game_screen.size[0] / 4 - 180), 500)
        restart_position = (self.mediator.game_screen.size[0] / 4 - 180, 500)

        self.mediator.game_screen.showEndScreen(self.playing_time)

        action = Action.local_loop

        while action == Action.local_loop:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play()

            mx, my = pygame.mouse.get_pos()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    action = Action.quit_game
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_position[0] <= mx <= restart_position[0]+360 and \
                            500 <= my <= 605.5:
                        action = Action.stand_by
                    elif exit_position[0] <= mx <= exit_position[0] + 360 and \
                            500 <= my <= 605.5:
                        action = Action.quit_game

            if restart_position[0] <= mx <= restart_position[0]+360 and \
                    500 <= my <= 605.5:
                self.mediator.game_screen.window.blit(self.mediator.game_screen.pressed_restart_button,
                                                      (restart_position[0], 500))

            else:
                self.mediator.game_screen.window.blit(self.mediator.game_screen.restart_button,
                                                      (restart_position[0], 500))

            if exit_position[0] <= mx <= exit_position[0] + 360 and \
                    500 <= my <= 605.5:
                self.mediator.game_screen.window.blit(self.mediator.game_screen.pressed_exit_button,
                                                      (exit_position[0], 500))

            else:
                self.mediator.game_screen.window.blit(self.mediator.game_screen.exit_button, (exit_position[0], 500))

            pygame.display.flip()

        return action

    def winningScreen(self):
        pygame.mixer.music.load("sounds/victory_track.mp3")
        pygame.mixer.music.play()

        restart_position = (self.mediator.game_screen.size[0] / 4 - 235, 490)
        exit_position = ((3 * self.mediator.game_screen.size[0] / 4 - 140), 490)

        self.mediator.game_screen.showWinningScreen(self.playing_time)

        action = Action.local_loop

        while action == Action.local_loop:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play()

            mx, my = pygame.mouse.get_pos()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    action = Action.quit_game
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_position[0] <= mx <= restart_position[0]+360 and \
                            restart_position[1] <= my <= restart_position[1] + 105.5:
                        action = Action.stand_by
                    elif (3 * self.mediator.game_screen.size[0] / 4 - 180) <= mx \
                            <= (3 * self.mediator.game_screen.size[0] / 4 + 180) and \
                            exit_position[1] <= my <= exit_position[1] + 105.5:
                        action = Action.quit_game

            if restart_position[0] <= mx <= restart_position[0]+360 and \
                    restart_position[1] <= my <= restart_position[1] + 105.5:
                self.mediator.game_screen.window.blit(self.mediator.game_screen.pressed_restart_button,
                                                      (restart_position[0], restart_position[1]))

            else:
                self.mediator.game_screen.window.blit(self.mediator.game_screen.restart_button,
                                                      (restart_position[0], restart_position[1]))

            if (3 * self.mediator.game_screen.size[0] / 4 - 180) <= mx \
                    <= (3 * self.mediator.game_screen.size[0] / 4 + 180) and \
                    exit_position[1] <= my <= exit_position[1] + 105.5:
                self.mediator.game_screen.window.blit(self.mediator.game_screen.pressed_exit_button, exit_position)

            else:
                self.mediator.game_screen.window.blit(self.mediator.game_screen.exit_button, exit_position)

            pygame.display.flip()

        return action
