import pygame
import random
from .paddle import Paddle
from .ball import Ball

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

        # Scores for points within a game
        self.player_score = 0
        self.ai_score = 0

        # Game and match stats
        self.player_games = 0
        self.ai_games = 0
        self.games_to_win = 2  # default = best of 3 → first to 2 games
        self.points_to_win = 5  # points per game

        self.font = pygame.font.SysFont("Arial", 30)
        self.big_font = pygame.font.SysFont("Arial", 60)
        self.menu_font = pygame.font.SysFont("Arial", 25)

        self.game_over = False
        self.in_main_menu = True
        self.match_over = False

        self.wall_sound = pygame.mixer.Sound("wall_bounce.wav")
        self.paddle_sound = pygame.mixer.Sound("paddle_hit.wav")
        self.score_sound = pygame.mixer.Sound("score.wav")

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self, screen, events):
        if self.in_main_menu:
            self.render_main_menu(screen)
            self.handle_main_menu_input(events)
            return
        
        if self.match_over:
            self.handle_replay_input(events)
            return

        self.ball.move(self.wall_sound)
        self.ball.check_collision(self.player, self.ai, self.paddle_sound)

        if self.ball.x <= 0:
            self.ai_score += 1
            if self.score_sound:
                self.score_sound.play()       
            self.ball.reset()

        elif self.ball.x >= self.width:
            self.player_score += 1
            if self.score_sound:
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

        # Scoreboard: points + games
        score_text = self.font.render(
            f"{self.player_score} ({self.player_games})   -   {self.ai_score} ({self.ai_games})", True, WHITE
        )
        screen.blit(score_text, (self.width // 2 - score_text.get_width() // 2, 20))

        if self.match_over:
            self.render_match_over_menu(screen)

    def check_game_over(self, screen):
        # When a player reaches the points_to_win threshold
        if self.player_score >= self.points_to_win or self.ai_score >= self.points_to_win:
            # Record game result
            if self.player_score >= self.points_to_win:
                self.player_games += 1
                winner = "Player"
            else:
                self.ai_games += 1
                winner = "AI"

            # Check match completion
            if self.player_games >= self.games_to_win or self.ai_games >= self.games_to_win:
                self.match_over = True
                return

            # Show short “Game Over” message for current round
            self.display_game_winner(screen, winner)

            # Reset scores for next game
            self.player_score = 0
            self.ai_score = 0
            self.ball.reset()

    def display_game_winner(self, screen, winner):
        # Show temporary “Game won” banner for 2 seconds
        text_surface = self.big_font.render(f"{winner} wins this game!", True, WHITE)
        rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
        screen.fill(BLACK)
        screen.blit(text_surface, rect)
        pygame.display.flip()
        pygame.time.delay(2000)

    def render_match_over_menu(self, screen):
        winner = "Player Wins the Match!" if self.player_games > self.ai_games else "AI Wins the Match!"
        title_surface = self.big_font.render(winner, True, WHITE)

        option_texts = [
            "Press 3 for Best of 3 Games",
            "Press 5 for Best of 5 Games",
            "Press 7 for Best of 7 Games",
            "Press ESC to Exit"
        ]
        option_surfaces = [self.menu_font.render(t, True, WHITE) for t in option_texts]

        # Black panel box
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

    def render_main_menu(self, screen):
        screen.fill(BLACK)
        title_surface = self.big_font.render("PING PONG", True, WHITE)

        option_texts = [
            "Press 3 for Best of 3 Games",
            "Press 5 for Best of 5 Games",
            "Press 7 for Best of 7 Games",
            "Press ESC to Exit"
        ]
        option_surfaces = [self.menu_font.render(t, True, WHITE) for t in option_texts]

        # Draw centered black box behind menu text
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

        # Draw title and options
        current_y = box_y + padding_y
        title_rect = title_surface.get_rect(center=(self.width // 2, current_y + title_surface.get_height() // 2))
        screen.blit(title_surface, title_rect)
        current_y += title_surface.get_height() + gap

        for s in option_surfaces:
            rect = s.get_rect(center=(self.width // 2, current_y + s.get_height() // 2))
            screen.blit(s, rect)
            current_y += s.get_height() + 10


    def handle_main_menu_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_3:
                    self.start_new_match(3)
                    self.in_main_menu = False
                elif event.key == pygame.K_5:
                    self.start_new_match(5)
                    self.in_main_menu = False
                elif event.key == pygame.K_7:
                    self.start_new_match(7)
                    self.in_main_menu = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

    def handle_replay_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_3:
                    self.start_new_match(3)
                elif event.key == pygame.K_5:
                    self.start_new_match(5)
                elif event.key == pygame.K_7:
                    self.start_new_match(7)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

    def start_new_match(self, best_of_games):
        # Reset full match
        self.games_to_win = (best_of_games // 2) + 1  # majority
        self.points_to_win = 5  # each game up to 5 points
        self.player_games = 0
        self.ai_games = 0
        self.player_score = 0
        self.ai_score = 0

        # Reset paddles and ball
        self.player.y = self.height // 2 - self.paddle_height // 2
        self.ai.y = self.height // 2 - self.paddle_height // 2
        self.ball.x = self.ball.original_x
        self.ball.y = self.ball.original_y
        self.ball.velocity_x = random.choice([-5, 5])
        self.ball.velocity_y = random.choice([-3, 3])

        self.match_over = False
        self.in_main_menu = False