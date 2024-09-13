from random import randint
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.window import *

from ranking import save_file
from monsters import Monsters


class Game:
    def __init__(self):
        self.display = Window(600, 600)
        self.display.set_title('Space Invaders')
        self.control = Window.get_keyboard()

        self.background = GameImage('sprites/background.png')

        # Criação da nave
        self.spaceship = Sprite('sprites/spaceship.png', 2)
        self.spaceship.set_position((self.display.width - self.spaceship.width) / 2, self.display.height - 70)
        self.spaceship.set_sequence_time(0, 2, 180, True)
        self.spaceship.stop()
        self.movement_spaceship = 500

        # Criação da lista de projéteis do player
        self.projetiles = []
        self.movement_projetile = -500
        self.countdown_projectile = 0
        self.shoot = False

        # Criação da matriz de monstros
        self.rows, self.columns = 4, 5
        self.monsters = Monsters(self, self.rows, self.columns)

        # Criação da lista de projéteis dos monstros
        self.projetiles_monsters = []
        self.movement_projetile_monster = 200
        self.countdown_projectile_monster = 0

        # Criação dos escudos
        self.shields = [
            {'index': 0, 'img': Sprite('sprites/shield/0.png'), 'hits': 0, 'position': (90, self.display.height - 130)},
            {'index': 1, 'img': Sprite('sprites/shield/0.png'), 'hits': 0,
             'position': ((self.display.width - Sprite('sprites/shield/0.png').width) / 2, self.display.height - 130)},
            {'index': 2, 'img': Sprite('sprites/shield/0.png'), 'hits': 0,
             'position': ((self.display.width - Sprite('sprites/shield/0.png').width - 90), self.display.height - 130)}
        ]

        for s in self.shields:
            s['img'].set_position(s['position'][0], s['position'][1])

        # Pontuação, vidas e status do jogo
        self.score = 0
        self.lives = 3
        self.difficulty = 2
        self.restart = False

        self.invulnerability = False
        self.countdown_invulnerability = 0
        self.countdown_red = 0

        # Variavéis relacionadas a taxa de quadros
        self.fr_fps = 0
        self.fr_timer = 0
        self.fr_frames = 0

    # Método que carrega uma nova fase
    def load_next_level(self):
        self.spaceship.set_position((self.display.width - self.spaceship.width) / 2, self.display.height - 70)

        self.projetiles = []
        self.countdown_projectile = 0
        self.shoot = False

        self.rows += 1
        self.columns += 1
        self.monsters = Monsters(self, self.rows, self.columns)
        self.countdown_projectile_monster = 0
        self.projetiles_monsters = []

        self.shields = [
            {'index': 0, 'img': Sprite('sprites/shield/0.png'), 'hits': 0, 'position': (90, self.display.height - 130)},
            {'index': 1, 'img': Sprite('sprites/shield/0.png'), 'hits': 0,
             'position': ((self.display.width - Sprite('sprites/shield/0.png').width) / 2, self.display.height - 130)},
            {'index': 2, 'img': Sprite('sprites/shield/0.png'), 'hits': 0,
             'position': ((self.display.width - Sprite('sprites/shield/0.png').width - 90), self.display.height - 130)}
        ]

        for s in self.shields:
            s['img'].set_position(s['position'][0], s['position'][1])

        self.restart = False
        self.countdown_red = 0

    # Método que reseta o game após o player morrer
    def game_over(self):
        self.spaceship.set_position((self.display.width - self.spaceship.width) / 2, self.display.height - 70)
        self.spaceship.play()

        self.projetiles = []
        self.countdown_projectile = 0
        self.shoot = False

        self.monsters = Monsters(self, self.rows, self.columns)
        self.countdown_projectile_monster = 0
        self.projetiles_monsters = []

        self.shields = [
            {'index': 0, 'img': Sprite('sprites/shield/0.png'), 'hits': 0, 'position': (90, self.display.height - 130)},
            {'index': 1, 'img': Sprite('sprites/shield/0.png'), 'hits': 0,
             'position': ((self.display.width - Sprite('sprites/shield/0.png').width) / 2, self.display.height - 130)},
            {'index': 2, 'img': Sprite('sprites/shield/0.png'), 'hits': 0,
             'position': ((self.display.width - Sprite('sprites/shield/0.png').width - 90), self.display.height - 130)}
        ]

        for s in self.shields:
            s['img'].set_position(s['position'][0], s['position'][1])

        self.restart = False
        self.invulnerability = True
        self.countdown_invulnerability = 240
        self.countdown_red = 0

        self.lives -= 1
        if self.lives == 0:
            save_file('ranking.txt', self.score)

    def run(self, difficulty=2):
        self.difficulty = difficulty

        # GameLoop
        while True:
            self.background.draw()

            # Verifica se o player quer sair do jogo
            if self.control.key_pressed('esc'):
                return

            # Controle da nave
            if self.control.key_pressed('left') and self.spaceship.x > 0:
                self.spaceship.move_x(-self.movement_spaceship * self.display.delta_time() / difficulty)

            if self.control.key_pressed('right') and self.spaceship.x < (self.display.width - self.spaceship.width):
                self.spaceship.move_x(self.movement_spaceship * self.display.delta_time() / difficulty)

            # Ataque do player e criação dos projetéis
            if self.control.key_pressed('space') and not self.shoot:
                projectile = Sprite('sprites/projectile.png')
                projectile.set_position(self.spaceship.x + (self.spaceship.width - projectile.width) / 2, self.spaceship.y)
                self.projetiles.append(projectile)
                self.countdown_projectile = 35 * difficulty
                self.shoot = True

                self.countdown_red += 1

                if self.countdown_red == 5:
                    pos = (self.spaceship.x, self.spaceship.y)
                    self.spaceship = Sprite('sprites/red.png')
                    self.spaceship.set_position(pos[0], pos[1])

                elif self.countdown_red == 10:
                    self.spaceship = Sprite('sprites/spaceship.png', 2)
                    self.spaceship.set_sequence_time(0, 2, 180, True)
                    self.game_over()

            if not self.control.key_pressed('space') and self.countdown_red >= 5:
                pos = (self.spaceship.x, self.spaceship.y)
                self.spaceship = Sprite('sprites/spaceship.png', 2)
                self.spaceship.set_position(pos[0], pos[1])
                self.spaceship.set_sequence_time(0, 2, 180, True)
                self.spaceship.stop()
                self.countdown_red = 0

            if not self.control.key_pressed('space'):
                self.countdown_red = 0

            if self.countdown_projectile > 0:
                self.countdown_projectile -= 1
                if self.countdown_projectile == 0:
                    self.shoot = False

            # Movimentação e desenho dos monstros
            self.monsters.update()
            if self.restart:
                self.game_over()

            for r in self.monsters.matrix:
                for m in r:
                    m.draw()

            # Criação dos projéteis dos monstros
            if self.countdown_projectile_monster == 0 and len(self.monsters.matrix) > 0:
                while True:
                    x, y = randint(0, self.rows - 1), randint(0, self.columns - 1)
                    if len(self.monsters.matrix) > x:
                        if len(self.monsters.matrix[x]) > y:
                            break
                proj_m = Sprite('sprites/projectile_monster.png')
                proj_m.set_position(self.monsters.matrix[x][y].x + (self.monsters.matrix[x][y].width - proj_m.width) / 2, self.monsters.matrix[x][y].y + 15)
                self.projetiles_monsters.append(proj_m)
                self.countdown_projectile_monster = 360 // difficulty

            elif self.countdown_projectile_monster > 0:
                self.countdown_projectile_monster -= 1

            # Movimentação, colisão e remoção dos projéteis dos monstros
            for pm in self.projetiles_monsters:
                if pm.y > self.display.height:
                    self.projetiles_monsters.remove(pm)

                for s in self.shields:
                    if pm.collided(s['img']):
                        self.projetiles_monsters.remove(pm)
                        s['hits'] += 1
                        if s['hits'] < 3:
                            s['img'] = Sprite(f'sprites/shield/{s['hits']}.png')
                            s['img'].set_position(s['position'][0], s['position'][1])
                        else:
                            self.shields.remove(s)

                if pm.collided(self.spaceship) and not self.invulnerability:
                    self.projetiles_monsters.remove(pm)
                    self.game_over()
                pm.move_y(self.movement_projetile_monster * self.display.delta_time() * difficulty)
                pm.draw()

            if self.invulnerability:
                self.countdown_invulnerability -= 1
                if self.countdown_invulnerability == 0:
                    self.spaceship.stop()
                    self.invulnerability = False

            # Movimentação, colisão e remoção dos projéteis do player otimizados
            limits = self.monsters.get_limits_matrix()
            for p in self.projetiles:
                if p.y < 0:
                    self.projetiles.remove(p)
                p.move_y(self.movement_projetile * self.display.delta_time() / difficulty)

                for s in self.shields:
                    if p.collided(s['img']):
                        self.projetiles.remove(p)

                if limits[0] <= p.x <= limits[1] and limits[2] <= p.y <= limits[3]:
                    for i in range(len(self.monsters.matrix) - 1, -1, -1):
                        if self.monsters.matrix[i]:
                            limits = self.monsters.get_limits_matrix()
                            for m in self.monsters.matrix[i]:
                                if p.collided(m) and p in self.projetiles:
                                    self.projetiles.remove(p)
                                    self.monsters.matrix[i].remove(m)
                                    self.score += 1000 // (i + 2) if (i % 2 == 0 and i != 0) else 1000 // (i + 1)
                        else:
                            self.monsters.matrix.pop(i)
                    if self.monsters.matrix == [[]]:
                        self.monsters.matrix = []
                p.draw()

            # Verifica se o player passou de fase
            if len(self.monsters.matrix) == 0:
                self.load_next_level()

            # Verifica se o player perdeu todas as vidas
            if self.lives == 0:
                return

            # Impressão do FPS
            self.fr_frames += 1
            self.fr_timer += self.display.delta_time()
            self.display.draw_text(f'FPS: {self.fr_fps:.1f}', 5, self.display.height - 10, 10, (255, 255, 255), "Arial")

            if self.fr_timer >= 1:
                self.fr_fps = self.fr_frames
                self.fr_timer = 0
                self.fr_frames = 0

            # Atualiza a tela
            self.display.draw_text(f'Score: {self.score}', 20, 20, 25, (255, 255, 255), 'retrogaming')
            self.display.draw_text(f'Lives: {self.lives}', 20, 50, 25, (255, 255, 255), 'retrogaming')

            for s in self.shields:
                s['img'].draw()

            if self.spaceship.total_frames > 1:
                self.spaceship.update()
            self.spaceship.draw()
            self.display.update()
