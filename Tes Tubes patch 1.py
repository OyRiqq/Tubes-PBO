import pygame
import random

# Inisialisasi pygame dan ukuran layar
pygame.init()
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Catcher")
clock = pygame.time.Clock()

class Basket:
    def __init__(self):
        self.image = pygame.image.load('basket.jpg')
        self.image = pygame.transform.scale(self.image, (100, 60))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
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
        self.image = pygame.image.load(f'{self.kind}.jpg')
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = random.randint(3, 4)

    def fall(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Bomb:
    def __init__(self):
        self.image = pygame.image.load('bomb.png')
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = random.randint(4, 6)

    def fall(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Game:
    def __init__(self):
        self.basket = Basket()
        self.fruits = []
        self.bombs = []
        self.score = 0
        self.lives = 3
        self.spawn_delay = 30
        self.counter = 0

    def show_start_screen(self):
        screen.fill((255, 255, 255))
        font = pygame.font.SysFont(None, 72)
        title = font.render("Fruit Catcher", True, (0, 0, 0))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100))
        
        font_small = pygame.font.SysFont(None, 36)
        prompt = font_small.render("Press SPACE to Start", True, (0, 0, 0))
        screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False

    def game_over_screen(self):
        font = pygame.font.SysFont(None, 72)
        text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.delay(2000)
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

            if self.counter % self.spawn_delay == 0:
                self.fruits.append(Fruit())

            if self.counter % 90 == 0:
                self.bombs.append(Bomb())

            for fruit in self.fruits[:]:
                fruit.fall()
                if fruit.rect.top > HEIGHT:
                    self.fruits.remove(fruit)
                    self.lives -= 1
                elif fruit.rect.colliderect(self.basket.rect):
                    self.fruits.remove(fruit)
                    self.score += 1

            for bomb in self.bombs[:]:
                bomb.fall()
                if bomb.rect.top > HEIGHT:
                    self.bombs.remove(bomb)
                elif bomb.rect.colliderect(self.basket.rect):
                    self.bombs.remove(bomb)
                    self.lives -= 1

            if self.lives <= 0:
                self.game_over_screen()

            screen.fill((255, 255, 255))
            self.basket.draw(screen)
            for fruit in self.fruits:
                fruit.draw(screen)
            for bomb in self.bombs:
                bomb.draw(screen)

            font = pygame.font.SysFont(None, 36)
            score_text = font.render(f"Score: {self.score}   Lives: {self.lives}", True, (0, 0, 0))
            screen.blit(score_text, (10, 10))

            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.show_start_screen()
    game.run()
