import pygame
import random
from abc import ABC, abstractmethod

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Catcher")
clock = pygame.time.Clock()

# Sound
pygame.mixer.music.load('bg_music.mp3')
pygame.mixer.music.set_volume(0.5)
catch_sound = pygame.mixer.Sound('catch.mp3')
bomb_sound = pygame.mixer.Sound('bomb.mp3')
gameover_sound = pygame.mixer.Sound('gameover.mp3')
lifelost_sound = pygame.mixer.Sound('lifelost.mp3')

# === Abstract Class ===
class FallingObject(ABC):
    def __init__(self, image_path, speed_range):
        self._image = pygame.image.load(image_path)
        self._image = pygame.transform.scale(self._image, (50, 50))
        self._rect = self._image.get_rect()
        self._rect.x = random.randint(0, WIDTH - self._rect.width)
        self._rect.y = -self._rect.height
        self._speed = random.randint(*speed_range)

    def fall(self):
        self._rect.y += self._speed

    def draw(self, screen):
        screen.blit(self._image, self._rect)

    def is_caught_by(self, basket_rect):
        return self._rect.colliderect(basket_rect)

    def is_off_screen(self):
        return self._rect.top > HEIGHT

    @property
    def rect(self):
        return self._rect

    @abstractmethod
    def on_catch(self, game):
        pass

# === Subclasses ===
class Fruit(FallingObject):
    def __init__(self):
        self.kind = random.choice(['apple', 'orange', 'watermelon'])
        super().__init__(f'{self.kind}.png', (2, 4))

    def on_catch(self, game):
        catch_sound.play()

class Bomb(FallingObject):
    def __init__(self):
        super().__init__('bom.png', (5, 7))

    def on_catch(self, game):
        bomb_sound.play()

class Magnet(FallingObject):
    def __init__(self):
        super().__init__('magnet.png', (3, 5))

    def on_catch(self, game):
        pass

# === Basket ===
class Basket:
    def __init__(self, x, y):
        self._image = pygame.image.load('basket.png')
        self._image = pygame.transform.scale(self._image, (120, 70))
        self._rect = self._image.get_rect()
        self._rect.centerx = x
        self._rect.bottom = y
        self._speed = 10

    def move(self, keys):
        if keys[pygame.K_LEFT] and self._rect.left > 0:
            self._rect.x -= self._speed
        if keys[pygame.K_RIGHT] and self._rect.right < WIDTH:
            self._rect.x += self._speed

    def move2(self, keys): # Kontrol kedua untuk Co-op dan PvP
        if keys[pygame.K_a] and self._rect.left > 0:
            self._rect.x -= self._speed
        if keys[pygame.K_d] and self._rect.right < WIDTH:
            self._rect.x += self._speed

    def draw(self, screen):
        screen.blit(self._image, self._rect)

    @property
    def rect(self):
        return self._rect

# === Game Class ===
class Game:
    def __init__(self):
        self.menu_bg = pygame.transform.scale(pygame.image.load('background_menu.jpg'), (WIDTH, HEIGHT))
        self.game_bg = pygame.transform.scale(pygame.image.load('background_game.jpg'), (WIDTH, HEIGHT))
        self.mode = None
        self.reset_game()

    def reset_game(self):
        self.baskets = []
        self.objects = []
        self.score = 0
        self.lives = 3
        self.spawn_delay = 50
        self.counter = 0
        self.magnet_active = False
        self.magnet_timer = 0
        self.MAGNET_DURATION = 5000
        self.player1_score = 0
        self.player1_lives = 3
        self.player2_score = 0
        self.player2_lives = 3

        if self.mode == "singleplayer":
            self.baskets.append(Basket(WIDTH // 2, HEIGHT - 20))
        elif self.mode == "coop":
            self.baskets.append(Basket(WIDTH // 3, HEIGHT - 20))
            self.baskets.append(Basket(2 * WIDTH // 3, HEIGHT - 20))
            self.lives = 5 # Nyawa bersama
        elif self.mode == "pvp":
            self.baskets.append(Basket(WIDTH // 3, HEIGHT - 20))
            self.baskets.append(Basket(2 * WIDTH // 3, HEIGHT - 20))
            self.player1_lives = 3
            self.player2_lives = 3
            self.player1_score = 0
            self.player2_score = 0

    def show_start_screen(self):
        pygame.mixer.music.play(-1)
        screen.blit(self.menu_bg, (0, 0))
        font = pygame.font.SysFont(None, 96)
        title = font.render("Fruit Catcher", True, (0, 0, 0))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4 - 50))

        font_mode = pygame.font.SysFont(None, 48)
        single_player_text = font_mode.render("1. Singleplayer (SPACE)", True, (0, 0, 0))
        coop_text = font_mode.render("2. Co-op (C)", True, (0, 0, 0))
        pvp_text = font_mode.render("3. PvP (P)", True, (0, 0, 0))

        y_offset = HEIGHT // 2 - 50
        screen.blit(single_player_text, (WIDTH // 2 - single_player_text.get_width() // 2, y_offset))
        screen.blit(coop_text, (WIDTH // 2 - coop_text.get_width() // 2, y_offset + 50))
        screen.blit(pvp_text, (WIDTH // 2 - pvp_text.get_width() // 2, y_offset + 100))

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.mode = "singleplayer"
                        self.reset_game()
                        waiting = False
                    elif event.key == pygame.K_c:
                        self.mode = "coop"
                        self.reset_game()
                        waiting = False
                    elif event.key == pygame.K_p:
                        self.mode = "pvp"
                        self.reset_game()
                        waiting = False
    def game_over_screen(self):
        gameover_sound.play()
        screen.blit(self.menu_bg, (0, 0))
        font = pygame.font.SysFont(None, 96)
        text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 4 - 50))

        font_small = pygame.font.SysFont(None, 48)
        y_offset = HEIGHT // 2 - 75
        if self.mode == "singleplayer" or self.mode == "coop":
            score_text = font_small.render(f"Score: {self.score}", True, (0, 0, 0))
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, y_offset))
            y_offset += 50
        elif self.mode == "pvp":
            p1_score_text = font_small.render(f"Player 1 Score: {self.player1_score}", True, (0, 0, 0))
            p2_score_text = font_small.render(f"Player 2 Score: {self.player2_score}", True, (0, 0, 0))
            screen.blit(p1_score_text, (WIDTH // 2 - p1_score_text.get_width() // 2, y_offset))
            screen.blit(p2_score_text, (WIDTH // 2 - p2_score_text.get_width() // 2, y_offset + 30))
            y_offset += 80

        restart_text = font_small.render("Press R to Restart", True, (0, 0, 0))
        quit_text = font_small.render("Press Q to Quit", True, (0, 0, 0))
        menu_text = font_small.render("Press M for Main Menu", True, (0, 0, 0))

        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, y_offset))
        screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, y_offset + 50))
        screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, y_offset + 100))

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
                    elif event.key == pygame.K_m:
                        self.mode = None
                        self.reset_game()
                        self.show_start_screen()
                        return


    def run(self):
        running = True
        while running:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Gerakkan keranjang sesuai mode
            if self.mode == "singleplayer":
                self.baskets[0].move(keys)
            elif self.mode == "coop":
                self.baskets[0].move(keys) # Player 1 (panah)
                self.baskets[1].move2(keys) # Player 2 (A/D)
            elif self.mode == "pvp":
                # Gerakkan Player 1 jika masih hidup
                if self.player1_lives > 0:
                    self.baskets[0].move(keys)
                # Gerakkan Player 2 jika masih hidup
                if self.player2_lives > 0:
                    self.baskets[1].move2(keys)

            self.counter += 1
            score_for_spawn = 0
            if self.mode == "singleplayer" or self.mode == "coop":
                score_for_spawn = self.score
            elif self.mode == "pvp":
                score_for_spawn = max(self.player1_score, self.player2_score)
            self.spawn_delay = max(15, 50 - score_for_spawn // 5)

            if self.counter % self.spawn_delay == 0:
                self.objects.append(Fruit())
            if self.counter % 90 == 0:
                self.objects.append(Bomb())
            if self.counter % 200 == 0:
                self.objects.append(Magnet())

            # Matikan magnet setelah durasi
            if self.magnet_active and pygame.time.get_ticks() - self.magnet_timer > self.MAGNET_DURATION:
                self.magnet_active = False

            # Update dan tarik objek
            for obj in self.objects[:]:
                # Efek magnet (untuk semua keranjang yang masih hidup jika aktif)
                if self.magnet_active and isinstance(obj, Fruit):
                    for i, basket in enumerate(self.baskets):
                        if self.mode != "pvp" or (self.mode == "pvp" and ((i == 0 and self.player1_lives > 0) or (i == 1 and self.player2_lives > 0))):
                            dx = basket.rect.centerx - obj.rect.centerx
                            dy = basket.rect.centery - obj.rect.centery
                            dist = (dx**2 + dy**2) ** 0.5
                            if dist < 200:
                                speed = 3
                                obj._rect.x += int(speed * dx / dist)
                                obj._rect.y += int(speed * dy / dist)

                obj.fall()
                if obj.is_off_screen():
                    self.objects.remove(obj)
                    if isinstance(obj, Fruit):
                        if self.mode == "singleplayer":
                            self.lives -= 1
                            lifelost_sound.play()
                        elif self.mode == "coop":
                            self.lives -= 1
                            lifelost_sound.play()
                        # Di PvP, membiarkan jatuh tidak mengurangi nyawa
                else:
                    for i, basket in enumerate(self.baskets):
                        if obj.is_caught_by(basket.rect):
                            # Hanya proses catch jika pemain masih hidup
                            if self.mode != "pvp" or (self.mode == "pvp" and ((i == 0 and self.player1_lives > 0) or (i == 1 and self.player2_lives > 0))):
                                obj.on_catch(self)
                                self.objects.remove(obj)
                                if isinstance(obj, Fruit):
                                    if self.mode == "singleplayer":
                                        self.score += 1
                                    elif self.mode == "coop":
                                        self.score += 1
                                    elif self.mode == "pvp":
                                        if i == 0:
                                            self.player1_score += 1
                                        elif i == 1:
                                            self.player2_score += 1
                                elif isinstance(obj, Bomb):
                                    if self.mode == "singleplayer":
                                        self.lives -= 1
                                        bomb_sound.play()
                                    elif self.mode == "coop":
                                        self.lives -= 1
                                        bomb_sound.play()
                                    elif self.mode == "pvp":
                                        if i == 0:
                                            self.player1_lives -= 1
                                            bomb_sound.play()
                                        elif i == 1:
                                            self.player2_lives -= 1
                                            bomb_sound.play()
                                elif isinstance(obj, Magnet):
                                    self.magnet_active = True
                                    self.magnet_timer = pygame.time.get_ticks()
                                break # Hanya satu keranjang yang bisa menangkap satu objek

            # Kondisi Game Over
            game_over = False
            if self.mode == "singleplayer":
                if self.lives <= 0:
                    game_over = True
            elif self.mode == "coop":
                if self.lives <= 0:
                    game_over = True
            elif self.mode == "pvp":
                if self.player1_lives <= 0 and self.player2_lives <= 0:
                    game_over = True

            if game_over:
                self.game_over_screen()
                return

            screen.blit(self.game_bg, (0, 0))
            for i, basket in enumerate(self.baskets):
                # Gambar keranjang hanya jika pemain masih hidup di PvP
                if self.mode != "pvp" or (self.mode == "pvp" and ((i == 0 and self.player1_lives > 0) or (i == 1 and self.player2_lives > 0))):
                    basket.draw(screen)

            for obj in self.objects:
                obj.draw(screen)

            font = pygame.font.SysFont(None, 36)
            info_text = ""
            if self.mode == "singleplayer":
                info_text = f"Score: {self.score}   Lives: {self.lives}   Magnet: {'ON' if self.magnet_active else 'OFF'}"
            elif self.mode == "coop":
                info_text = f"Score: {self.score}   Lives: {self.lives}   Magnet: {'ON' if self.magnet_active else 'OFF'}"
            elif self.mode == "pvp":
                p1_alive = self.player1_lives > 0
                p2_alive = self.player2_lives > 0
                p1_status = f"P1 Score: {self.player1_score}  Lives: {self.player1_lives}" if p1_alive else f"P1 Score: {self.player1_score}  DEAD"
                p2_status = f"P2 Score: {self.player2_score}  Lives: {self.player2_lives}" if p2_alive else f"P2 Score: {self.player2_score}  DEAD"
                info_text = f"{p1_status}   {p2_status}   Magnet: {'ON' if self.magnet_active else 'OFF'}"
            info = font.render(info_text, True, (0, 0, 0))
            screen.blit(info, (20, 20))

            pygame.display.flip()
            clock.tick(60)

# === Main ===
if __name__ == "__main__":
    game = Game()
    while True:
        game.show_start_screen()
        if game.mode is not None:
            game.run()