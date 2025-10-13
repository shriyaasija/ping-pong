import pygame
import random
from .paddle import Paddle
from .ball import Ball

pygame.mixer.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.game_over_font = pygame.font.SysFont("Arial", 60)
        self.menu_font = pygame.font.SysFont("Arial", 25)

        self.game_over = False
        self.winning_score = 5

        self.paddle_hit_sound = pygame.mixer.Sound("paddle_hit.wav")
        self.wall_bounce_sound = pygame.mixer.Sound("wall_bounce.wav")
        self.score_sound = pygame.mixer.Sound("score.wav")


    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self, screen, events):
        if self.game_over:
            self.handle_replay_input(events)
            return

        self.ball.move(self.wall_bounce_sound)
        self.ball.check_collision(self.player, self.ai, self.paddle_hit_sound)

        if self.ball.x <= 0:
            self.ai_score += 1
            self.score_sound.play()
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.score_sound.play()
            self.ball.reset()

        self.ai.auto_track(self.ball, self.height)
        self.check_game_over(screen)

    def render(self, screen):
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4, 20))

        if self.game_over:
            self.render_game_over_menu(screen)

    def check_game_over(self, screen):
        if self.player_score >= self.winning_score or self.ai_score >= self.winning_score:
            self.game_over = True

    def render_game_over_menu(self, screen):
        winner = "Player Wins!" if self.player_score >= self.winning_score else "AI Wins!"
        title_surface = self.game_over_font.render(winner, True, WHITE)

        option_texts = [
            "Press 3 for Best of 3 (first to 2)",
            "Press 5 for Best of 5 (first to 3)",
            "Press 7 for Best of 7 (first to 4)",
            "Press ESC to Exit"
        ]
        option_surfaces = [self.menu_font.render(t, True, WHITE) for t in option_texts]

        padding_x, padding_y, gap = 30, 20, 15
        content_width = max(title_surface.get_width(), max(s.get_width() for s in option_surfaces))
        content_height = (
            title_surface.get_height()
            + gap
            + sum(s.get_height() for s in option_surfaces)
            + (len(option_surfaces) - 1) * 10
        )
        box_width = content_width + padding_x * 2
        box_height = content_height + padding_y * 2
        box_x = (self.width - box_width) // 2
        box_y = (self.height - box_height) // 2

        pygame.draw.rect(screen, BLACK, (box_x, box_y, box_width, box_height))
        pygame.draw.rect(screen, WHITE, (box_x, box_y, box_width, box_height), 2)

        current_y = box_y + padding_y
        title_rect = title_surface.get_rect(center=(self.width // 2, current_y + title_surface.get_height() // 2))
        screen.blit(title_surface, title_rect)
        current_y += title_surface.get_height() + gap

        for s in option_surfaces:
            rect = s.get_rect(center=(self.width // 2, current_y + s.get_height() // 2))
            screen.blit(s, rect)
            current_y += s.get_height() + 10

    def handle_replay_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_3:
                    self.start_new_game(3)
                elif event.key == pygame.K_5:
                    self.start_new_game(5)
                elif event.key == pygame.K_7:
                    self.start_new_game(7)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

    def start_new_game(self, best_of):
        self.winning_score = (best_of // 2) + 1
        self.player_score = 0
        self.ai_score = 0

        self.player.y = self.height // 2 - self.paddle_height // 2
        self.ai.y = self.height // 2 - self.paddle_height // 2
        self.ball.x = self.ball.original_x
        self.ball.y = self.ball.original_y
        self.ball.velocity_x = random.choice([-5, 5])
        self.ball.velocity_y = random.choice([-3, 3])

        self.game_over = False