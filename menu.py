from PPlay.window import *
from PPlay.gameimage import *
from ranking import recover_file
from game import Game


class Menu:
    def __init__(self):
        # Criação da janela, do controle e do mouse
        self.display = Window(600, 600)
        self.display.set_title('Space Invaders')
        self.control = Window.get_keyboard()
        self.mouse = Window.get_mouse()

        # Criação dos Game Images da imagem de fundo e do logo do space invaders
        self.background = GameImage('sprites/background.png')
        self.logo = GameImage('sprites/buttons/space_invaders_logo.png')
        self.logo.set_position((self.display.width - self.logo.width) / 2, 55)

    # Menu de dificuldades
    def difficulty(self):
        block = True

        buttons = {
            'easy': GameImage('sprites/buttons/easy_button.png'),
            'normal': GameImage('sprites/buttons/normal_button.png'),
            'hard': GameImage('sprites/buttons/hard_button.png'),
        }

        i = 5
        for b in buttons:
            buttons[b].set_position((self.display.width - buttons[b].width) / 2, self.display.height / 2 + i)
            i += 70

        while True:
            if self.control.key_pressed('esc'):
                return
            if block and not self.mouse.is_button_pressed(1):
                block = False

            # Verifica se o usuário clicou em alguma dficuldade

            if self.mouse.is_over_object(buttons['easy']):  # dificuldade fácil
                if self.mouse.is_button_pressed(1) and not block:
                    Game().run(1)
                    return

            elif self.mouse.is_over_object(buttons['normal']):  # dificuldade média
                if self.mouse.is_button_pressed(1) and not block:
                    Game().run(2)
                    return

            elif self.mouse.is_over_object(buttons['hard']):  # dificuldade difícil
                if self.mouse.is_button_pressed(1) and not block:
                    Game().run(3)
                    return

            # Atualiza a tela
            self.background.draw()
            self.logo.draw()
            for b in buttons:
                buttons[b].draw()
            self.display.update()

    # Exibe o Top 5 do ranking
    def ranking(self):
        rank = recover_file('ranking.txt')

        title = GameImage('sprites/buttons/scores_title.png')
        title.set_position((self.display.width - title.width) / 2, self.display.height / 2 - 30)

        positions = [
            {'position': '1ST', 'color': (65, 105, 225)},
            {'position': '2ND', 'color': (153, 51, 153)},
            {'position': '3RD', 'color': (236, 59, 131)},
            {'position': '4TH', 'color': (238, 173, 45)},
            {'position': '5TH', 'color': (50, 205, 50)}
        ]

        while True:
            if self.control.key_pressed('esc'):
                return

            self.background.draw()
            self.logo.draw()
            title.draw()

            p = 0
            h = self.display.height / 2 + 50
            for i in rank:
                player, score, date = i.split()
                self.display.draw_text(f'{(positions[p]['position']):<6}{player:<13}{score:>8}{date:>15}', 50, h,
                                       20, positions[p]['color'], 'retrogaming')
                h += 40
                p += 1
                if p == 5:
                    break

            self.display.update()

    # Menu Principal
    def main(self):

        buttons = {
            'play': GameImage('sprites/buttons/play_button.png'),
            'difficulty': GameImage('sprites/buttons/difficulty_button.png'),
            'ranking': GameImage('sprites/buttons/ranking_button.png'),
            'exit': GameImage('sprites/buttons/exit_button.png')
        }

        i = 5
        for b in buttons:
            buttons[b].set_position((self.display.width - buttons[b].width) / 2, self.display.height / 2 + i)
            i += 70

        while True:

            # Verifica se o usuário clicou em algum botão

            if self.mouse.is_over_object(buttons['play']):  # botão jogar
                if self.mouse.is_button_pressed(1):
                    Game().run()

            elif self.mouse.is_over_object(buttons['difficulty']):  # botão dificuldade
                if self.mouse.is_button_pressed(1):
                    self.difficulty()

            elif self.mouse.is_over_object(buttons['ranking']):  # botão ranking
                if self.mouse.is_button_pressed(1):
                    self.ranking()

            elif self.mouse.is_over_object(buttons['exit']):  # botão sair
                if self.mouse.is_button_pressed(1):
                    self.display.close()

            # Atualiza a tela
            self.background.draw()
            self.logo.draw()
            for b in buttons:
                buttons[b].draw()
            self.display.update()


Menu().main()
