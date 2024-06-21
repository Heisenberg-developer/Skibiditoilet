import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Настройка экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Камерамен против Скибиди Туалетов')

# Загрузка изображений и изменение их размеров
cameraman_img = pygame.transform.scale(pygame.image.load('assets/cameraman.png').convert_alpha(), (50, 50))
skibidi_toilet_img = pygame.transform.scale(pygame.image.load('assets/skibidi_toilet.png').convert_alpha(), (50, 50))
house_img = pygame.transform.scale(pygame.image.load('assets/house.png').convert_alpha(), (100, 100))
bullet_img = pygame.transform.scale(pygame.image.load('assets/bullet.png').convert_alpha(), (10, 10))
poop_img = pygame.transform.scale(pygame.image.load('assets/poop.png').convert_alpha(), (20, 20))

# Класс для Камерамена
class Cameraman(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = cameraman_img
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

# Класс для пуль
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > SCREEN_WIDTH:
            self.kill()

# Класс для какашек
class Poop(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = poop_img
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -7

    def update(self):
        self.rect.x += self.speed
        if self.rect.right < 0:
            self.kill()

# Класс для врагов
class SkibidiToilet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = skibidi_toilet_img
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = random.randint(2, 5)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()
            # Увеличиваем очки за пропущенного врага
            global score
            score += 1

# Группы спрайтов
bullets = pygame.sprite.Group()
poops = pygame.sprite.Group()
skibidi_toilets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

# Создание Камерамена
cameraman = Cameraman(100, 100)
all_sprites.add(cameraman)

# Спавн врагов
def spawn_skibidi():
    x = SCREEN_WIDTH
    y = random.randint(0, SCREEN_HEIGHT - skibidi_toilet_img.get_height())
    skibidi_toilet = SkibidiToilet(x, y)
    skibidi_toilets.add(skibidi_toilet)
    all_sprites.add(skibidi_toilet)
    if random.random() < 0.5:  # 50% шанс, что враг будет стрелять
        poop = Poop(x, y + skibidi_toilet_img.get_height() // 2)
        poops.add(poop)
        all_sprites.add(poop)

# Координаты домов (препятствия)
houses = [
    pygame.Rect(500, 400, house_img.get_width(), house_img.get_height()),
    pygame.Rect(200, 200, house_img.get_width(), house_img.get_height())
]

# Основной игровой цикл
clock = pygame.time.Clock()
running = True
score = 0
font = pygame.font.SysFont(None, 55)
game_active = False

def show_start_screen():
    screen.fill(WHITE)
    start_text = font.render("Нажмите любую клавишу для начала", True, BLACK)
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 - start_text.get_height() // 2))
    pygame.display.flip()
    wait_for_key()

def show_end_screen():
    screen.fill(WHITE)
    end_text = font.render(f"Игра окончена. Ваш счет: {score}", True, BLACK)
    screen.blit(end_text, (SCREEN_WIDTH // 2 - end_text.get_width() // 2, SCREEN_HEIGHT // 2 - end_text.get_height() // 2))
    pygame.display.flip()
    wait_for_key()

def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False

show_start_screen()
game_active = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bullet = Bullet(cameraman.rect.right, cameraman.rect.centery)
                bullets.add(bullet)
                all_sprites.add(bullet)

    if game_active:
        keys = pygame.key.get_pressed()
        cameraman.update(keys)

        # Обновление пуль и какашек
        bullets.update()
        poops.update()
        skibidi_toilets.update()

        # Спавн скибиди туалетов
        if random.randint(1, 100) < 2:
            spawn_skibidi()

        # Проверка на столкновения пуль и врагов
        for bullet in bullets:
            hit_list = pygame.sprite.spritecollide(bullet, skibidi_toilets, True)
            for hit in hit_list:
                bullet.kill()
                score += 10  # Увеличиваем счет за каждого уничтоженного врага

        # Проверка на столкновения какашек и Камерамена
        if pygame.sprite.spritecollideany(cameraman, poops):
            game_active = False
            show_end_screen()
            cameraman.rect.topleft = (100, 100)
            score = 0
            bullets.empty()
            poops.empty()
            skibidi_toilets.empty()
            all_sprites.empty()
            all_sprites.add(cameraman)
            show_start_screen()
            game_active = True

        # Обновление счета
        score += 1

        # Очистка экрана
        screen.fill(WHITE)

        # Отображение персонажей и объектов
        all_sprites.draw(screen)
        for house in houses:
            screen.blit(house_img, (house.x, house.y))

        # Отображение счета
        score_text = font.render(f"Счет: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Обновление экрана
        pygame.display.flip()

        # Ограничение FPS
        clock.tick(FPS)

pygame.quit()
sys.exit()


