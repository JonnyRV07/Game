import pygame
import random


class Road(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.im = pygame.image.load('data/image/road.png').convert_alpha()
        self.rect = self.im.get_rect()


class Car(pygame.sprite.Sprite):
    def __init__(self, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(x=-5, y=0)


class Coin(pygame.sprite.Sprite):
    def __init__(self, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('data/image/coin.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self, *args):
        if self.rect.y < args[0]:
            pass
        else:
            self.rect.y = args[0] + self.image.get_rect().size[1]


class Tires(pygame.sprite.Sprite):
    def __init__(self, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('data/image/tires.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self, *args):
        if self.rect.y < args[0]:
            pass
        else:
            self.rect.y = args[0] + self.image.get_rect().size[1]


class Button:
    def __init__(self, width_, height_, active_clr=(244, 164, 96), inactive_clr=(165, 42, 42)):
        self.width = width_
        self.height = height_
        self.active_clr = active_clr
        self.inactive_clr = inactive_clr

    def draw(self, x, y, message, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(sc, self.active_clr, (x, y, self.width, self.height))
            if click[0] == 1:
                if action is not None:
                    action()
        else:
            pygame.draw.rect(sc, self.inactive_clr, (x, y, self.width, self.height))
        sc.blit(message, (x + 5, y + 10))


if __name__ == '__main__':
    pygame.init()
    size = width, height = 500, 900  # приветствуется ширина(400 <= width <= 600) и высота(500 <= height <= 1000)
    # на данном этапе разработки НЕ СЛЕДУЕТ менять размер экрана, так как этот момент продуман только на 20%
    # (не реализовано масштабирование для всех объектов и тем более не откорректировано)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Neer For Speed: the distant past')
    pygame.display.set_icon(pygame.image.load('data/image/icon.jpg'))
    pygame.display.update()

    sc = screen
    surfaces = []
    surfaces.append(screen), surfaces.append(screen)

    coeff = width / 100 if width == 500 else (height - width + 100) / 100 # коээфициент отвечающий за масштабирование
    # масштабирование объектов пока НЕ РЕАЛИЗОВАНО
    speed = 5 # рекомендуется 5 <= speed <= 15
    new_sc = screen
    CF = False
    start = False
    flag = False
    restart = False
    running = True
    coinFlag = True
    tireFlag = True
    f = pygame.font.SysFont('Bauhaus93', 45)
    f_end = pygame.font.SysFont('Bauhaus93', 30)
    X1, Y1 = random.randrange(50, width - 120), random.randrange(0, height - 600)
    X2, Y2 = random.randrange(50, width - 120), random.randrange(0, height - 600)

    coin_coords = []
    score = []
    tires_coords = []
    coin_sprites = pygame.sprite.Group()
    tire_sprites = pygame.sprite.Group()
    cars_sprites = pygame.sprite.Group()

    clock = pygame.time.Clock()

    road = Road()
    road.im = pygame.transform.scale(road.im, (width + 5, height))
    road.rect.x, road.rect.y = 0, 0

    new_road = Road()
    new_road.im = pygame.transform.scale(new_road.im, (width + 5, height))
    new_road.rect.x, new_road.rect.y = 0, -(new_road.im.get_rect().size[1])

    car2 = Car('data/image/car/car1.png')
    car2.image = pygame.transform.scale(car2.image, (car2.image.get_rect().size[0] // coeff,
                                                     car2.image.get_rect().size[1] // coeff))
    car2.rect = car2.image.get_rect(x=width // 3 + 5, y=height - car2.image.get_rect().size[1] - 5)
    cars_sprites.add(car2)

    coin = Coin(speed)
    coin.image = pygame.transform.scale(coin.image, (coin.image.get_rect().size[0] // 15,
                                                     coin.image.get_rect().size[1] // 15))

    coin_coords.append([X1, Y1])
    coin_sprites.add(coin)

    tire = Tires(speed)
    tires_coords.append([X2, Y2])
    tire_sprites.add(tire)

    coin.rect.x, coin.rect.y = X1, Y1
    tire.rect.x, tire.rect.y = X2, Y2

    manual1 = f.render('Press the SPACE bar', True, 'WHITE')
    manual2 = f.render('to start playing', True, 'WHITE')
    pause = f.render('Press ENTER to continue', True, 'WHITE')
    ending1 = f_end.render('You crashed!', True, 'Red')
    ending2 = f_end.render('The game is over.', True, 'Red')
    ending3 = f_end.render('Click SPACE to restart', True, 'Red')
    ending4 = f_end.render('Click ESC to exit and save', True, 'Red')
    ending5 = f_end.render('Click SPACE to exit and save', True, 'Red')

    H, H2 = 0, -(new_road.im.get_rect().size[1])

    def get_data():
        file = open('data_scores.txt', 'r', encoding='utf-8')
        res_score = [int(i) for i in file.read() if i.isalnum()]
        return res_score


    def show_menu():
        global running, restart, score
        menu_bg = pygame.image.load('data/image/bg.jpg')
        menu_bg = pygame.transform.scale(menu_bg, (500, 900))
        start_btn = Button(200, 70)
        show = True

        while show:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            sc.blit(menu_bg, (0, 0))
            start_btn.draw(150, 300, f.render('Start!', True, 'WHITE'), game_start)
            sc.blit(f.render('Neer For Speed:', True, 'WHITE'), (100, 160, 200, 70))
            sc.blit(f.render('the distant past', True, 'WHITE'), (100, 210, 200, 70))
            sc.blit(f.render(f'Record: {max(get_data()) if get_data() else 0}', True, 'WHITE'), (20, 10, 200, 70))
            pygame.display.update()

    def run():
        global H, H2, flag, X1, Y1, X2, Y2, coinFlag, tireFlag, score, CF
        if (H < height and H2 < 0) or (H2 < height and H < 0):
            coin_sprites.draw(sc)
            tire_sprites.draw(sc)
            cars_sprites.draw(sc)
            if ((coin.rect.x >= car2.rect.x - 20 and coin.image.get_rect().size[0] + coin.rect.x <=
                 car2.rect.x + car2.image.get_rect().size[0] + 20) and
                    (car2.rect.y >= coin.rect.y + coin.image.get_rect().size[1] - 30 >= car2.rect.y - 25)):
                CF = True
                if CF is True and coin_sprites:
                    coin.kill()
                    score.append(True)
                    CF = False
            if ((tire.rect.x + 40 >= car2.rect.x - 20 and tire.image.get_rect().size[0] + tire.rect.x - 40 <=
                 car2.rect.x + car2.image.get_rect().size[0] + 20) and
                    (car2.rect.y >= tire.rect.y + tire.image.get_rect().size[1] - 50 >= car2.rect.y - 5)):
                game_over()
            road.rect.y += speed
            H += speed
            new_road.rect.y += speed
            H2 += speed
            coin.rect.y += speed
            tire.rect.y += speed
        else:
            if flag is False:
                coin_sprites.update(height)
                tire_sprites.update(height)
                road.rect.y = -(road.im.get_rect().size[1])
                new_road.rect.y = 0
                H, H2 = -(new_road.im.get_rect().size[1]), 0
                coin.rect.y = height
                tire.rect.y = height
                flag = True
            else:
                if coinFlag is True:
                    X1 = random.randrange(100, width - 100)
                    if (X1 + coin.image.get_rect().size[0] + 25 < tires_coords[0][0]) or \
                            (X1 + 25 < tires_coords[0][0] + tire.image.get_rect().size[0]):
                        X1 = random.randrange(100, width - 100)
                    else:
                        coin_coords.clear()
                        coin_coords.append([X1, Y1])
                if tireFlag is True:
                    X2 = random.randrange(100, width - 100)
                    if (X2 + tire.image.get_rect().size[0] + 25 < coin_coords[0][0]) or \
                            (X2 + 25 < coin_coords[0][0] + coin.image.get_rect().size[0]):
                        X2 = random.randrange(100, width - 100)
                    else:
                        tires_coords.clear()
                        tires_coords.append([X2, Y2])
                Y1, Y2 = -51, -51
                if X1 + coin.image.get_rect().size[0] < X2 or X2 + tire.image.get_rect().size[0] < X1:
                    coin.rect.x, coin.rect.y = X1, Y1
                    tire.rect.x, tire.rect.y = X2, Y2
                    coin_sprites.add(coin)
                    tire_sprites.add(coin)
                    road.rect.y = 0
                    new_road.rect.y = -(road.im.get_rect().size[1])
                    H, H2 = 0, -(new_road.im.get_rect().size[1])
                    flag = False
                    pygame.display.update()

    def pause_():
        global restart
        paused = True
        while paused:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            sc.blit(pause, pause.get_rect(center=(250, 200)))
            sc.blit(ending5, ending5.get_rect(center=(250, 250)))

            k = pygame.key.get_pressed()
            if k[pygame.K_RETURN]:
                paused = False
            elif k[pygame.K_SPACE]:
                restart = True
                with open('data_scores.txt', 'a', encoding='utf-8') as file:
                    file.write(f'{len(score)};')
                    file.close()
                show_menu()
            pygame.display.update()

    def game_over():
        global start, restart, running, surfaces, new_sc
        running = False
        restart = True
        end = True
        while end:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            scr = f.render(f'Score: {len(score)}', True, 'Chocolate')
            sc.blit(ending1, ending1.get_rect(center=(250, 200)))
            sc.blit(ending2, ending2.get_rect(center=(250, 250)))
            sc.blit(scr, scr.get_rect(center=(250, 300)))
            sc.blit(ending3, ending3.get_rect(center=(250, 360)))
            sc.blit(ending4, ending4.get_rect(center=(250, 400)))

            keys_ = pygame.key.get_pressed()
            if keys_[pygame.K_SPACE]:
                new_sc = surfaces[1]
                del surfaces[0]
                surfaces.append(screen)
                game_start()
            elif keys_[pygame.K_ESCAPE]:
                with open('data_scores.txt', 'a', encoding='utf-8') as file:
                    file.write(f'{len(score)};')
                    file.close()
                show_menu()

            pygame.display.update()

    def game_start():
        global running, start, score, restart, flag, coinFlag, sc, tireFlag, coin_coords, tires_coords, coin_sprites, \
            tire_sprites, cars_sprites, H, H2, X1, Y1, X2, Y2, CF

        if restart is False:
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN and start:
                        if event.key == pygame.K_ESCAPE:
                            pause_()
                        if event.key == pygame.K_LEFT:
                            if car2.rect.x > 15:
                                car2.rect.x -= 15
                                cars_sprites.draw(sc)
                                pygame.display.update()
                            else:
                                car2.rect.x = 0
                                cars_sprites.draw(sc)
                                pygame.display.update()
                        if event.key == pygame.K_RIGHT:
                            if car2.rect.x + car2.image.get_rect().size[0] < width - 15:
                                car2.rect.x += 15
                                cars_sprites.draw(sc)
                                pygame.display.update()
                            else:
                                car2.rect.x = width - 150
                                cars_sprites.draw(sc)
                                pygame.display.update()

                clock.tick(60)

                sc.blit(road.im, road.rect)
                sc.blit(new_road.im, new_road.rect)
                cars_sprites.draw(sc)

                keys = pygame.key.get_pressed()

                if not keys[pygame.K_SPACE]:
                    sc.blit(manual1, manual1.get_rect(center=(250, 300)))
                    sc.blit(manual2, manual2.get_rect(center=(250, 350)))
                else:
                    start = True

                if start is True and restart is False:
                    sc.fill((0, 0, 0))
                    sc.blit(road.im, road.rect)
                    sc.blit(new_road.im, new_road.rect)
                    cars_sprites.draw(sc)
                    run()

                pygame.display.update()
        else:
            sc = new_sc
            CF = False
            start = False
            flag = False
            restart = False
            running = True
            coinFlag = True
            tireFlag = True
            X1, Y1 = random.randrange(50, width - 120), random.randrange(0, height - 600)
            X2, Y2 = random.randrange(50, width - 120), random.randrange(0, height - 600)
            coin_coords = []
            score = []
            tires_coords = []
            coin_sprites = pygame.sprite.Group()
            tire_sprites = pygame.sprite.Group()
            cars_sprites = pygame.sprite.Group()
            road.rect.x, road.rect.y = 0, 0
            new_road.rect.x, new_road.rect.y = 0, -(new_road.im.get_rect().size[1])
            car2.rect = car2.image.get_rect(x=width // 3 + 5, y=height - car2.image.get_rect().size[1] - 5)
            cars_sprites.add(car2)
            coin_coords.append([X1, Y1])
            coin_sprites.add(coin)
            tires_coords.append([X2, Y2])
            tire_sprites.add(tire)
            coin.rect.x, coin.rect.y = X1, Y1
            tire.rect.x, tire.rect.y = X2, Y2
            H, H2 = 0, -(new_road.im.get_rect().size[1])

            restart = False
            running = True
            game_start()

    show_menu()

    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()
