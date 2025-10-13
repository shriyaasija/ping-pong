import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def move(self, wall_sound):
        self.prev_x = self.x
        self.prev_y = self.y

        self.x += self.velocity_x
        self.y += self.velocity_y

        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            wall_sound.play()

    def check_collision(self, player, ai, paddle_sound):
        travel_rect = pygame.Rect(
            min(self.prev_x, self.x),
            self.y,
            abs(self.velocity_x) + self.width,
            self.height,
        )

        player_rect = player.rect()
        ai_rect = ai.rect()

        if travel_rect.colliderect(player_rect):
            self.x = player_rect.right
            self.velocity_x = abs(self.velocity_x)
            paddle_sound.play()

        elif travel_rect.colliderect(ai_rect):
            self.x = ai_rect.left - self.width
            self.velocity_x = -abs(self.velocity_x)
            paddle_sound.play()

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)