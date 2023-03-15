import pygame
pygame.init()

from random import random

from debug import Debug
from bet import Bet
from wheel import Wheel


SCREEN_SIZE = 1280, 720
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE
SCREEN_CENTER = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

TARGET_FPS = 60


class Application:

    def __init__(self):
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Fortune Wheel')
        self.display_surface = pygame.display.set_mode(SCREEN_SIZE)
        self.debug = Debug()
        self.is_running = False

        self.bets = [
            Bet('Project Zomboid', 21000),
            Bet('Dota 2', 100000),
            Bet('Monster', 13000),
            Bet('Counter-Strike', 92000),
            Bet('Tokio Ghoul', 15000)
        ]
        self.wheel = Wheel(SCREEN_CENTER, 300, self.bets)
        self.wheel.set_rotation_time(5)

    def run(self):
        self.is_running = True
        while self.is_running:

            frame_time_ms = self.clock.tick(TARGET_FPS)
            frame_time_s = frame_time_ms / 1000.

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.stop()

            if self.wheel.target_rotation_time == 0:
                self.wheel.set_rotation_time(random() * 6 + 1)
            self.wheel.update(frame_time_s)

            self.display_surface.fill((255, 255, 255))
            self.wheel.draw(self.display_surface)
            # self._draw_debug()
            pygame.display.update()

    def _draw_debug(self):
        total_bet_sum = sum([bet.bet for bet in self.bets])
        sorted_bets = sorted(self.bets, key=lambda x: x.bet, reverse=True)
        bets_string = ''.join([f'{bet.title} ({bet.bet}): {bet.bet/total_bet_sum * 100:.2f}%\n' for bet in sorted_bets])

        debug_string = \
            f'{self.wheel.rotation_time:.2f}/{self.wheel.target_rotation_time:.2f} s\n' \
            f'{bets_string}'

        debug_text_surf = self.font.render(
            debug_string,
            True, (0, 0, 0))
        debug_text_rect = debug_text_surf.get_rect(topleft=(0, 0))
        self.display_surface.blit(debug_text_surf, debug_text_rect)

    def stop(self):
        self.is_running = False


if __name__ == '__main__':
    Application().run()
