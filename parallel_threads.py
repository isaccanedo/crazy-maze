from threading import Thread

class ParallelThreads:

    @staticmethod
    def findMonstersNewPosition(monster_1, monster_2, monster_3, player, player_list, mediator):
        thread_1 = Thread(target=monster_1.findNewPath, args=[player])
        thread_2 = Thread(target=monster_2.findNewPath, args=[player])
        thread_3 = Thread(target=monster_3.findNewPath, args=[player])
        thread_4 = Thread(target=mediator.game_screen.showMazeScreen, args=(player_list, mediator.maze, player.lives))

        thread_1.start()
        thread_2.start()
        thread_3.start()
        thread_4.start()

        thread_1.join()
        thread_2.join()
        thread_3.join()
        thread_4.join()
