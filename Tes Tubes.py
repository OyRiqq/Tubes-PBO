import pygame
import random

# Inisialisasi pygame
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Catcher")
clock = pygame.time.Clock()

# Load background music
pygame.mixer.music.load('bg_music.mp3')
pygame.mixer.music.set_volume(0.5)

# Load sound effects
catch_sound = pygame.mixer.Sound('catch.mp3')
bomb_sound = pygame.mixer.Sound('bomb.mp3')
gameover_sound = pygame.mixer.Sound('gameover.mp3')
lifelost_sound = pygame.mixer.Sound('lifelost.mp3')

class Basket:
    def __init__(self):
        self.image = pygame.image.load('basket.png')
        self.image = pygame.transform.scale(self.image, (120, 70))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 20
        self.speed = 7

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Fruit:
    def __init__(self):
        self.kind = random.choice(['apple', 'orange', 'watermelon'])
        self.image = pygame.image.load(f'{self.kind}.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = random.randint(2, 4)  # diperlambat

    def fall(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Bomb:
    def __init__(self):
        self.image = pygame.image.load('bom.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = random.randint(5, 7)

    def fall(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Game:
    def __init__(self):
        self.menu_bg = pygame.transform.scale(pygame.image.load('background_menu.jpg'), (WIDTH, HEIGHT))
        self.game_bg = pygame.transform.scale(pygame.image.load('background_game.jpg'), (WIDTH, HEIGHT))
        self.reset_game()

    def reset_game(self):
        self.basket = Basket()
        self.fruits = []
        self.bombs = []
        self.score = 0
        self.lives = 3
        self.spawn_delay = 50  # diperlambat
        self.counter = 0

    def show_start_screen(self):
        pygame.mixer.music.play(-1)
        screen.blit(self.menu_bg, (0, 0))
        font = pygame.font.SysFont(None, 96)
        title = font.render("Fruit Catcher", True, (0, 0, 0))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 200))

        font_small = pygame.font.SysFont(None, 48)
        prompt = font_small.render("Press SPACE to Start", True, (0, 0, 0))
        screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting = False

    def game_over_screen(self):
        gameover_sound.play()
        screen.blit(self.menu_bg, (0, 0))
        font = pygame.font.SysFont(None, 96)
        text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 150))

        font_small = pygame.font.SysFont(None, 48)
        restart_text = font_small.render("Press R to Restart or Q to Quit", True, (0, 0, 0))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()
                        self.run()
                        return
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        exit()

    def run(self):
        running = True
        while running:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.basket.move(keys)
            self.counter += 1

            # Spawn rate buah berdasarkan skor (semakin kecil delay, makin cepat)
            self.spawn_delay = max(15, 50 - self.score // 5)

            if self.counter % self.spawn_delay == 0:
                self.fruits.append(Fruit())

            if self.counter % 90 == 0:
                self.bombs.append(Bomb())

            for fruit in self.fruits[:]:
                fruit.fall()
                if fruit.rect.top > HEIGHT:
                    self.fruits.remove(fruit)
                    self.lives -= 1
                    lifelost_sound.play()
                elif fruit.rect.colliderect(self.basket.rect):
                    self.fruits.remove(fruit)
                    self.score += 1
                    catch_sound.play()

            for bomb in self.bombs[:]:
                bomb.fall()
                if bomb.rect.top > HEIGHT:
                    self.bombs.remove(bomb)
                elif bomb.rect.colliderect(self.basket.rect):
                    self.bombs.remove(bomb)
                    self.lives -= 1
                    bomb_sound.play()

            if self.lives <= 0:
                self.game_over_screen()
                return

            screen.blit(self.game_bg, (0, 0))
            self.basket.draw(screen)
            for fruit in self.fruits:
                fruit.draw(screen)
            for bomb in self.bombs:
                bomb.draw(screen)

            font = pygame.font.SysFont(None, 48)
            score_text = font.render(f"Score: {self.score}   Lives: {self.lives}", True, (0, 0, 0))
            screen.blit(score_text, (20, 20))

            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.show_start_screen()
    game.run()
