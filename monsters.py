from PPlay.sprite import *


class Monsters:
    def __init__(self, game, rows, columns):
        self.game = game
        self.movement = [65, 800]

        self.matrix = []
        for r in range(rows):
            array = []
            for c in range(columns):
                if r < 2:
                    monster = Sprite(f'sprites/monsters/{r}.png')
                else:
                    monster = Sprite('sprites/monsters/2.png')
                monster.set_position((monster.width + monster.width / 2) * c + 20,
                                     (monster.height + monster.height / 2) * r + 20)
                array.append(monster)
            self.matrix.append(array)

        self.collision_x = False
        self.collision_y = False

    def update(self):
        for rows in self.matrix:
            for monster in rows:
                v = self.movement[0] * self.game.display.delta_time() * self.game.difficulty
                if (v+monster.x) < self.game.display.width:
                    monster.move_x(v)

                if (monster.x + monster.width + 5) >= self.game.display.width or monster.x <= 5:
                    self.collision_x = True

                if monster.y + monster.height >= self.game.spaceship.y:
                    self.collision_y = True

                else:
                    for s in self.game.shields:
                        if monster.y + monster.height >= s['img'].y:
                            self.collision_y = True

        if self.collision_x:
            self.movement[0] *= -1
            for rows in self.matrix:
                for monster in rows:
                    v = self.movement[1] * self.game.display.delta_time() * self.game.difficulty
                    if (v+monster.y) < self.game.display.height:
                        monster.move_y(v)
            self.collision_x = False

        if self.collision_y:
            self.game.restart = True
            self.collision_y = False

    def get_limits_matrix(self):
        listX = []
        listY = []

        for rows in self.matrix:
            for monster in rows:
                listX.append(monster.x)
                listY.append(monster.y)

        if listX:
            minX, maxX = min(listX), max(listX) + Sprite('sprites/monsters/0.png').width
        else:
            minX = maxX = 0

        if listY:
            minY, maxY = min(listY), max(listY) + Sprite('sprites/monsters/0.png').height
        else:
            minY = maxY = 0

        return [minX, maxX, minY, maxY]
