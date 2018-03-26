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


# pointerImg_rect = pointerImg.get_rect()
#
# in your main loop update the position every frame
#
# pointerImg_rect.center = pygame.mouse.get_pos()
#
# in your draw, draw your image to its rect position
#
# gameDisplay.blit(cursor, cursor_rect)


class Cursor(Image):

    def __init__(self):
        super().__init__('Sprites/cursor.png', left=500, top=350)
        # Load gunshot sound
        self.gunShotSound = pygame.mixer.Sound(os.path.join(os.getcwd(), 'Sounds', 'shot.wav'))

    def update(self):
        self.rect.left, self.rect.top = pygame.mouse.get_pos()

    def tick(self):
        if not Game.paused and not Game.over:
            # Check if the mouse was clicked
            if pygame.key.get_pressed () [0] and not Cursor.clicked:
                # Play Gunshot Sound and add Total Sounds
                Cursor.clicked = True
                self.gunShotSound.play()
                Game.total_shots += 1

            # Avoid repeated mouse clicks
            while pygame.key.get_pressed () [0]:
                sleep(0.1)
            Cursor.clicked = False
            self.update()

            # Bring the tree and grass infront of all the ducks
            # foreground.elevate()


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

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption('Dudu Hunt')
        self.background = Image('Sprites/background.png')
        self.crosshair = Cursor()
        # self._display_surf.blit(self.crosshair.image, (500,350))  # TODO
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


if __name__ == "__main__":
    theApp = Game()
    theApp.on_execute()
