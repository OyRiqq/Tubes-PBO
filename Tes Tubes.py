import pygame
import random

class Basket:
    def __init__(self):
        self.image = pygame.image.load('basket.png')  # gambar keranjang
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
        self.image = pygame.image.load('fruit.png')  # gambar buah
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = random.randint(3,4)

    def fall(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)
class Game:
    def __init__(self):
        self.basket = Basket()
        self.fruits = []
        self.score = 0
        self.lives = 3
        self.spawn_delay = 30  # jeda antar buah
        self.counter = 0

    def run(self):
        running = True
        while running:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.basket.move(keys)
            self.counter += 1
            if self.counter >= self.spawn_delay:
                self.fruits.append(Fruit())
                self.counter = 0

            for fruit in self.fruits[:]:
                fruit.fall()
                if fruit.rect.top > HEIGHT:
                    self.fruits.remove(fruit)
                    self.lives -= 1
                elif fruit.rect.colliderect(self.basket.rect):
                    self.fruits.remove(fruit)
                    self.score += 1

            # Game over check
            if self.lives <= 0:
                self.game_over_screen()

            screen.fill((135, 206, 235))  # biru langit
            self.basket.draw(screen)
            for fruit in self.fruits:
                fruit.draw(screen)

            # Tampilkan skor dan nyawa
            font = pygame.font.SysFont(None, 36)
            score_text = font.render(f"Score: {self.score}   Lives: {self.lives}", True, (0, 0, 0))
            screen.blit(score_text, (10, 10))

            pygame.display.flip()
            clock.tick(60)
        
if __name__ == "__main__":
    pygame.init()
    WIDTH, HEIGHT = 600, 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    game = Game()
    game.run()

    pygame.quit()
