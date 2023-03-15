import pygame.draw
from math import cos, sin, pi, degrees, radians
from random import randint
from time import sleep


font = pygame.font.SysFont(None, 24)


class Sector:
    def __init__(self, bet, start_angle, end_angle):
        self.bet = bet
        self.bet_title_surf = font.render(self.bet.title, True, (0, 0, 0))
        self.bet_title_rect = self.bet_title_surf.get_rect()
        self.color = ([randint(0, 255) for _ in range(3)])

        self.start_angle = start_angle
        self.end_angle = end_angle
        self.middle_angle = (start_angle + end_angle) / 2

    def rotate(self, angle):
        # angle in radians
        self.start_angle = (self.start_angle + angle) % (2 * pi)
        self.end_angle = (self.end_angle + angle) % (2 * pi)
        self.middle_angle = (self.middle_angle + angle) % (2 * pi)


class Wheel:
    def __init__(self, center, radius, bets):
        self.center = center
        self.radius = radius

        self._reset_velocity()
        self.max_rotation_speed = 1500

        total_bet_amount = sum([bet.bet for bet in bets])
        total_circumference = 2 * self.radius * pi
        self.sectors = []
        start_angle = 0
        for bet in bets:
            circumference_percent = bet.bet / total_bet_amount
            end_angle = start_angle + 2 * pi * circumference_percent
            # print(degrees(start_angle), degrees(end_angle))
            self.sectors.append(Sector(bet, start_angle, end_angle))
            start_angle = end_angle

        x0 = self.center[0]
        y0 = self.center[1] - self.radius
        self.selector_triangle_points = (
            (x0, y0 + 15),
            (x0 - 10, y0 - 3),
            (x0 + 10, y0 - 3)
        )

    def _reset_velocity(self):
        self.target_rotation_time = 0
        self.rotation_time = 0
        self.ease_time = 0
        self.const_speed_time = 0

        self.acceleration = 0
        self.rotation_speed = 0  # deg/s

    def set_rotation_time(self, seconds):
        self.target_rotation_time = seconds
        self.ease_time = seconds * 1/3
        self.const_speed_time = 1/3
        self.acceleration = self.max_rotation_speed / self.ease_time

    def get_winner(self):
        for sector in self.sectors:
            start_angle = (sector.start_angle + pi / 2) % (pi * 2)
            end_angle = (sector.end_angle + pi / 2) % (pi * 2)
            # print(sector.bet.title, start_angle, end_angle)
            if end_angle < start_angle:
                return sector.bet
            if start_angle <= 0 < end_angle:
                return sector.bet

    def update(self, frame_time_s):

        if self.target_rotation_time > 0:
            self.rotation_time += frame_time_s

            if self.rotation_time <= self.ease_time:
                self.rotation_speed += self.acceleration * frame_time_s
            elif self.rotation_time >= self.target_rotation_time - self.ease_time:
                self.rotation_speed -= self.acceleration * frame_time_s
            self.rotation_speed = min(self.rotation_speed, self.max_rotation_speed)

            delta_angle = radians(self.rotation_speed * frame_time_s)
            for sector in self.sectors:
                sector.rotate(delta_angle)

            # spin finished
            if self.rotation_time >= self.target_rotation_time:
                self._reset_velocity()
                print('Spin finished: ', self.get_winner().title)
                # for sector in self.sectors:
                #     print(degrees(sector.start_angle), degrees(sector.end_angle))

    def draw(self, surface):
        for sector in self.sectors:

            # line borders
            x0 = self.center[0] + self.radius * cos(sector.start_angle)
            y0 = self.center[1] + self.radius * sin(sector.start_angle)
            # x1 = self.center[0] + self.radius * cos(sector.end_angle)
            # y1 = self.center[1] + self.radius * sin(sector.end_angle)
            pygame.draw.line(surface, (0, 0, 0), self.center, (x0, y0), 1)
            # pygame.draw.line(surface, (0, 0, 0), self.center, (x1, y1), 1)

            # middle sector's title
            x2 = self.center[0] + (self.radius / 2) * cos(sector.middle_angle)
            y2 = self.center[1] + (self.radius / 2) * sin(sector.middle_angle)
            # sector.bet_title_surf = pygame.transform.rotate(sector.bet_title_surf, degrees(sector.middle_angle))
            # sector.bet_title_rect = sector.bet_title_surf.get_rect(center=(c2, y2))
            sector.bet_title_rect.center = (x2, y2)
            surface.blit(sector.bet_title_surf, sector.bet_title_rect)

        # circle frame
        pygame.draw.circle(surface, (0, 0, 0), self.center, self.radius, 1)

        # triangle selector on top
        pygame.draw.polygon(surface, (255, 255, 255), self.selector_triangle_points)
        pygame.draw.polygon(surface, (0, 0, 0), self.selector_triangle_points, 1)

