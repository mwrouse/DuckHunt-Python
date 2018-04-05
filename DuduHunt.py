import os
from time import sleep

import pygame


class Image(pygame.sprite.Sprite):
    def __init__(self, image_file, left=0, top=0):
        super().__init__()
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top


class Cursor(Image):
    def __init__(self):
        super().__init__('Sprites/cursor.png', left=500, top=350)  # TODO
        # Load gunshot sound
        self.gunShotSound = pygame.mixer.Sound(os.path.join(os.getcwd(), 'Sounds', 'shot.wav'))
        # Hide mouse
        pygame.mouse.set_visible(False)
        self.clicked = False

    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.rect.left = mouse_x - self.rect.size[0] / 2
        self.rect.top = mouse_y - self.rect.size[1] / 2

    def tick(self):
        # Play Gunshot Sound and add Total Sounds
        Cursor.clicked = True
        self.gunShotSound.play()
        Game.total_shots += 1

        self.update()


class Dog(Image):
    def __init__(self):
        # TODO: różne pieski
        super().__init__('Sprites/dog.PNG', left=500, top=350)
        self.image.set_colorkey(self.image.get_at((0, 0)), pygame.constants.RLEACCEL)
        self.dogWinSound = pygame.mixer.Sound(os.path.join(os.getcwd(), 'Sounds', 'howlovely.wav'))
        self.dogLoseSound = pygame.mixer.Sound(os.path.join(os.getcwd(), 'Sounds', 'eve.oga'))

    def celebration(self, cel_type):
        if cel_type == 'win':
            self.dogWinSound.play()
        elif cel_type == 'loss':
            self.dogLoseSound.play()


class Duck(Image):
    def __init__(self, duck_type):
        ducks = {'ola': 'blue',
                 'korwin': 'blue',
                 'lysy': 'red',
                 'janek': 'black'
                 }
        # Point Values Based On Duck Color
        point_values = {"blue": 25, "red": 50, "black": 75}
        super().__init__('Sprites/{}/duck1.png'.format(ducks[duck_type]), left=200, top=300)
        corner = self.image.get_at((0, 0))
        self.image.set_colorkey(corner, pygame.constants.RLEACCEL)
        self.image = pygame.transform.scale(self.image, (72, 76))


class Game:
    paused = False
    over = False
    total_shots = 0

    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 1016, 711
        self._static = True
        self.background = None
        self.crosshair = None
        self.duck_count = 2
        self.countdown = 10
        self.dog = None

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption('Dudu Hunt')
        self.background = Image('Sprites/background.png')
        self.crosshair = Cursor()
        self.duck = Duck('janek')
        self.dog = Dog()
        return True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.MOUSEBUTTONUP:
            self.crosshair.tick()
        if event.type == pygame.MOUSEMOTION:
            self.crosshair.update()

    def on_loop(self):
        pass

    def on_render(self):
        self._display_surf.blit(self.background.image, (0, 0))
        self._display_surf.blit(self.crosshair.image, self.crosshair.rect)
        self._display_surf.blit(self.duck.image, self.duck.rect)
        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if not self.on_init():
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

    def subround_end(self, type):
        self.crosshair.remove()
        # TODO: to będą 3 warunki, gdzieś je wrzucić
        # if self.duck_count == 0:
        # elif self.countdown == 0:
        # elif self.duck_count == 0:
        self.dog.add(type)


if __name__ == "__main__":
    theApp = Game()
    theApp.on_execute()
