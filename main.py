import math
import pygame
import random
import datetime
from pygame import mixer

# initialising pygame
pygame.init()
windows = pygame.display.set_mode((1228, 720))

pygame.display.set_caption("Spazio Tiratore")
# loading icon for the game
icon = pygame.image.load('explosive.png')
# displaying the icon
pygame.display.set_icon(icon)

e = datetime.datetime.now()

# loading all the images/surfaces required for the game
ship_img = pygame.image.load('pics/battleship.png')
back_img = pygame.image.load('pics/background.jpg')
enemy_img = pygame.image.load('pics/alien.png')
bullet_img = pygame.image.load('pics/bullet.png')
laser_img = pygame.image.load('pics/laser.png')
increase_bullet_img = pygame.image.load('pics/running-shoes.png')

# initial coordinates and variables for the manipulation of ship. Used for x and y parameters for the ship function
ship_x = 584
ship_y = 600
ship_x_change = 0

no_of_Bullets = 4
no_of_enemies = 8
bullet_y_change = 2
increase_in_bullets = 6
laser_y_change = 0.38

score = 0
collide = 0
booll = 0

bullet_sound = mixer.Sound('sound/laser.wav')
explosion_sound = mixer.Sound('sound/explosion.wav')
enemy_bullet_sound = mixer.Sound('sound/enemy_shooting.wav')
mixer.music.load('sound/background.wav')

score_record = []


def laser(x, y, wh):
    global state_laser
    state_laser[wh] = 'boom'
    windows.blit(laser_pic[wh], (x + 16, y))


def bullet(x, y, z):
    global state
    state[z] = 'boom'
    windows.blit(bullet_pic[z], (x + 16, y - 24))


# function that draws the ship/player at parameters x and y
def ship(x, y):
    windows.blit(ship_img, (x, y))


# function that draws the background
def background():
    windows.blit(back_img, (0, 0))


# function that draws the enemy at parameters x and y
def enemy(x, y, p):
    windows.blit(enemy_pic[p], (x, y))


def rand_dir():
    return random.randint(-1, 1)


def collision_state(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow((enemy_x - bullet_x), 2) + math.pow((enemy_y - bullet_y), 2))
    if distance <= 35:
        return True
    else:
        return False


def hit(ship_x, ship_y, laser_x, laser_y):
    distance = math.sqrt(math.pow((ship_x - laser_x), 2) + math.pow((ship_y - laser_y), 2))
    if distance <= 30:
        return True
    else:
        return False


def probability():
    prob = random.randint(0, 10)
    if prob == 1:
        return True
    else:
        return False


def increased_bullets(x, y, z):
    windows.blit(increase_bullet_pic[z], (x, y))
    increase_bullet_state[z] = 'drop'


lim = 0
change = 0


# Main game loop where everything happens

def game():
    pygame.time.Clock().tick(60)
    mixer.music.play(-1)
    global enemy_x, enemy_x_change, enemy_y, enemy_y_change, state, score, rand_dir, lim, game_running, increase_bullet_state, increase_bullet_x, increase_bullet_y
    global ship_x, ship_x_change, bullet_y, bullet_x, no_of_Bullets, bullet_y_change, laser_y_change, change
    game_running = True
    score = 2
    while game_running:
        windows.fill((0, 0, 0))
        background()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # quits the game
                pygame.quit()
            if event.type == pygame.KEYDOWN:  # checks if any key is pressed
                if event.key == pygame.K_ESCAPE:  # checks if escape key is pressed
                    Menu.pause()

                if event.key == pygame.K_LEFT:  # controlling the movement of ship/player
                    ship_x_change = -2

                if event.key == pygame.K_RIGHT:
                    ship_x_change = 2

                if event.key == pygame.K_SPACE:
                    for b in range(no_of_Bullets):
                        if state[b] == 'wait':
                            bullet_sound.play()
                            bullet(ship_x, bullet_y[b], b)
                            bullet_x[b] = ship_x
                            break

            if event.type == pygame.KEYUP:  # stopping movement after key is released
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    ship_x_change = 0
        for fire in range(no_of_enemies):
            if state_laser[fire] == 'wait':
                enemy_bullet_sound.play()
                laser(laser_x[fire], laser_y[fire], fire)
                break

        for check in range(no_of_enemies):
            if state_laser[check] == 'boom':
                laser(laser_x[check], laser_y[check], check)
                laser_y[check] += laser_y_change
            if laser_y[check] >= 700:
                laser_y[check] = enemy_y[check]
                laser_x[check] = enemy_x[check]
                state_laser[check] = 'wait'

        for col in range(no_of_enemies):
            booll = hit(ship_x, ship_y, laser_x[col], laser_y[col])
            if booll is True:
                date = (e.day, e.month, e.year)
                time = (e.hour, e.minute, e.second)
                score_dict = {"Score": score, "Date": date + time}
                score_record.append(score_dict)
                print(score_record)
                Menu.gameover()

        # defining borders for ship
        if ship_x >= 1164:
            ship_x = 1164
        if ship_x <= 0:
            ship_x = 0
        # movement of ship
        ship_x += ship_x_change

        # defining borders for enemy and prep for movement
        for g in range(no_of_enemies):
            if enemy_x[g] >= 1164:
                enemy_x_change[g] = -0.6
            if enemy_x[g] <= 0:
                enemy_x_change[g] = 0.6
            if enemy_y[g] >= 570:
                date = (e.day, e.month, e.year)
                time = (e.hour, e.minute, e.second)
                score_dict = {"Score": score, "Date": date + time}
                score_record.append(score)
                print(score_record)
                Menu.gameover()
            # movement of enemy
            enemy_x[g] += enemy_x_change[g]
            enemy_y[g] += enemy_y_change[g]
            enemy(enemy_x[g], enemy_y[g], g)

        # movement of bullet
        for c in range(no_of_Bullets):
            if state[c] is 'boom':
                bullet(bullet_x[c], bullet_y[c], c)
                bullet_y[c] -= bullet_y_change

            if bullet_y[c] <= 0:
                bullet_y[c] = 576
                state[c] = 'wait'

        for d in range(no_of_Bullets):
            for i in range(no_of_enemies):
                bol = collision_state(enemy_x[i], enemy_y[i], bullet_x[d], bullet_y[d])
                if bol is True:
                    explosion_sound.play()
                    bullet_y[d] = 576
                    state[d] = 'wait'
                    score += 2
                    print(score)
                    if probability():
                        increase_bullet_x[i] = enemy_x[i]
                        increase_bullet_y[i] = enemy_y[i]
                        increase_bullet_state[i] = 'drop'
                    enemy_x[i] = random.randint(0, 1164)
                    enemy_y[i] = random.randint(50, 268)

        for h in range(no_of_enemies):
            # movement of boosts
            if increase_bullet_state[h] == 'drop':
                increased_bullets(increase_bullet_x[h], increase_bullet_y[h], h)
                increase_bullet_y[h] += laser_y_change

            if increase_bullet_y[h] >= 600:
                increase_bullet_state[h] = 'nhit'
                increase_bullet_y[h] = enemy_y[h]
                increase_bullet_x[h] = enemy_x[h]
            hitt = collision_state(increase_bullet_x[h], increase_bullet_y[h], ship_x, ship_y)
            if hitt is True:
                increase_bullet_state[h] = 'nhit'
                increase_bullet_y[h] = enemy_y[h]
                increase_bullet_x[h] = enemy_x[h]
                no_of_Bullets = 4 + increase_in_bullets
                bullet_y_change = 8
                for a in range(increase_in_bullets):
                    bullet_x.append(0)
                    bullet_y.append(ship_y)
                    state.append('wait')
                    bullet_pic.append(bullet_img)

        # accessing above functions to draw surfaces for animation
        ship(ship_x, ship_y)

        font_s = pygame.font.Font('freesansbold.ttf', 22)
        score_count = font_s.render("Score: " + str(score), True, (255, 255, 255))
        score_count_rect = score_count.get_rect()
        score_count_rect.center = (60, 40)
        windows.blit(score_count, score_count_rect)
        if score % 10 == 0:
            for i in range(no_of_enemies):
                laser_y_change += 0.01
            score += 2

        pygame.display.update()


# font sizes
font_m = pygame.font.Font('freesansbold.ttf', 40)
font_op = pygame.font.Font('freesansbold.ttf', 30)

# main menu
text = font_m.render('SPAZIO  TIRATORE', True, (255, 255, 255), (0, 0, 0))
option1 = font_op.render("START GAME", True, (255, 255, 255), (0, 0, 0))
option2 = font_op.render("OPTIONS", True, (255, 255, 255), (0, 0, 0))
option3 = font_op.render("SCORE", True, (255, 255, 255), (0, 0, 0))
option4 = font_op.render("EXIT", True, (255, 255, 255), (0, 0, 0))
option1_rect = option1.get_rect()
option1_rect.center = ((1280 // 2) - 40, 260)
option2_rect = option2.get_rect()
option2_rect.center = ((1280 // 2) - 40, 340)
option3_rect = option3.get_rect()
option3_rect.center = ((1280 // 2) - 40, 420)
option4_rect = option4.get_rect()
option4_rect.center = ((1280 // 2) - 40, 500)

# exit options
exit_option_1 = font_op.render("ARE YOU SURE YOU WANT TO EXIT ?", True, (255, 255, 255), (0, 0, 0))
exit_option_2 = font_op.render("Y / N ?", True, (255, 255, 255), (0, 0, 0))
exit_option_1_rect = exit_option_1.get_rect()
exit_option_1_rect.center = ((1280 // 2) - 40, 720 // 2 - 80)
exit_option_2_rect = exit_option_2.get_rect()
exit_option_2_rect.center = ((1280 // 2) - 40, 720 // 2)
text_rect = text.get_rect()
text_rect.center = ((1280 // 2) - 40, 150)
animation = font_op.render('anything', True, (0, 0, 0), (0, 0, 0))
animation_rect = animation.get_rect()

# start
game_type_1 = font_op.render("INFINITE MODE", True, (255, 255, 255), (0, 0, 0))
game_type_1_rect = game_type_1.get_rect()
game_type_1_rect.center = ((1280 // 2) - 40, 320)

# records
records_title = font_op.render("HIGH SCORE", True, (255, 255, 255), (0, 0, 0))
records_title_rect = records_title.get_rect()
records_title_rect.center = ((1280 // 2) - 40, 100)

# single record
record_score = []
record_score_rect = []

high_score = 2500
addition = 228
depth = 200

for i in range(7):
    record_time = str(random.randint(26, 30)) + "/" + str(12) + "/" + str(2021) + " " + str(
        random.randint(8, 13)) + ":" + str(random.randint(0, 60)) + ":" + str(random.randint(0, 60))
    record_score.append(font_op.render((str(i + 1) + ")") + "   " + str(
        high_score) + "                                                       " + record_time, True, (255, 255, 255),
                                       (0, 0, 0)))
    record_score_rect.append(record_score[i].get_rect())
    record_score_rect[i].center = (575, depth)
    high_score -= addition
    depth += 70

# scoring
your_score = font_op.render("Your Score is: " + str(score), True, (255, 255, 255), (0, 0, 0))
your_score_rect = your_score.get_rect()
your_score_rect.center = ((1280 // 2) - 40, 100)


def confirmation():
    running = True
    windows.fill((0, 0, 0))
    windows.blit(exit_option_1, exit_option_1_rect)
    windows.blit(exit_option_2, exit_option_2_rect)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    pygame.quit()

                if event.key == pygame.K_n:
                    running = False
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()


class Menu:
    def main(self):
        mixer.music.play(-1)
        global enemy_x, enemy_y, enemy_x_change, enemy_y_change, laser_x, laser_y, state_laser, enemy_pic, laser_y_change, laser_pic, bullet_x, bullet_y, state, bullet_pic, increase_bullet_state, increase_bullet_x, increase_bullet_y, increase_bullet_pic
        global game_running, bullet_y_change, increase_in_bullets, no_of_Bullets, option1, option2, option3, option4, score
        main_running = True

        score = 0

        no_of_Bullets = 4
        no_of_enemies = 8
        bullet_y_change = 2
        increase_in_bullets = 6
        laser_y_change = 0.38

        # increase enemies
        enemy_x = []
        enemy_y = []
        enemy_pic = []
        enemy_x_change = []
        enemy_y_change = []
        increase_bullet_pic = []
        increase_bullet_state = []
        increase_bullet_x = []
        increase_bullet_y = []
        for f in range(no_of_enemies):
            x = random.randint(0, 1280)
            y = random.randint(50, 268)
            enemy_x.append(x)
            enemy_y.append(y)
            enemy_pic.append(enemy_img)
            enemy_x_change.append(0.6)
            enemy_y_change.append(0.08)
            increase_bullet_pic.append(increase_bullet_img)
            increase_bullet_state.append('nhit')
            increase_bullet_x.append(x)
            increase_bullet_y.append(y)

        # enemy shooting
        laser_x = []
        laser_y = []
        state_laser = []
        laser_pic = []
        for num in range(no_of_enemies):
            laser_x.append(enemy_x[num])
            laser_y.append(enemy_y[num])
            state_laser.append('wait')
            laser_pic.append(laser_img)

        # increase bullets
        bullet_x = []
        bullet_y = []
        state = []
        bullet_pic = []
        for a in range(no_of_Bullets):
            bullet_x.append(0)
            bullet_y.append(ship_y)
            state.append('wait')
            bullet_pic.append(bullet_img)

        while main_running:
            x, y = pygame.mouse.get_pos()
            windows.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        confirmation()
                    if event.key == pygame.K_KP_ENTER:
                        game()
                    if event.key == pygame.K_DOWN:
                        pass
                if event.type == pygame.QUIT:
                    pygame.quit()
            windows.blit(text, text_rect)
            windows.blit(option1, option1_rect)
            windows.blit(option2, option2_rect)
            windows.blit(option3, option3_rect)
            windows.blit(option4, option4_rect)
            if collision_state(x, y, (1280 // 2) - 40, 270) is True:
                option1 = font_op.render("START GAME", True, (0, 0, 0), (255, 255, 255))
                if pygame.mouse.get_pressed(3)[0] is True:
                    Menu.choice()

            if collision_state(x, y, (1280 // 2) - 40, 270) is False:
                option1 = font_op.render("START GAME", True, (255, 255, 255), (0, 0, 0))
            if collision_state(x, y, (1280 // 2) - 40, 340) is True:
                option2 = font_op.render("OPTIONS", True, (0, 0, 0), (255, 255, 255))
            if collision_state(x, y, (1280 // 2) - 40, 340) is False:
                option2 = font_op.render("OPTIONS", True, (255, 255, 255), (0, 0, 0))
            if collision_state(x, y, (1280 // 2) - 40, 420) is True:
                option3 = font_op.render("SCORE", True, (0, 0, 0), (255, 255, 255))
                if pygame.mouse.get_pressed(3)[0] is True:
                    Menu.records()
            if collision_state(x, y, (1280 // 2) - 40, 420) is False:
                option3 = font_op.render("SCORE", True, (255, 255, 255), (0, 0, 0))
            if collision_state(x, y, (1280 // 2) - 40, 500) is True:
                option4 = font_op.render("EXIT", True, (0, 0, 0), (255, 255, 255))
            if collision_state(x, y, (1280 // 2) - 40, 500) is False:
                option4 = font_op.render("EXIT", True, (255, 255, 255), (0, 0, 0))
            pygame.display.update()

    def pause(self):
        global font_op, font_m

        pause_font = font_op.render("GAME IS CURRENTLY PAUSED!", True, (255, 255, 255))
        pause_font_rect = pause_font.get_rect()
        pause_font_rect.center = ((1280 // 2) - 40, 720 // 2)

        paused = True
        while paused:
            windows.fill((0, 0, 0))
            mixer.music.pause()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        mixer.music.unpause()
                        paused = False

            windows.blit(pause_font, pause_font_rect)
            pygame.display.update()

    def gameover(self):
        gameover = True
        global font_op, font_m

        over_font = font_op.render("GAME OVER", True, (255, 255, 255))
        over_font_rect = over_font.get_rect()
        over_font_rect.center = ((1280 // 2) - 40, 720 // 2)
        while gameover:
            windows.fill((0, 0, 0))
            mixer.music.stop()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Menu.main()

            # scoring
            your_score = font_op.render("Your Score is: " + str(score), True, (255, 255, 255), (0, 0, 0))
            your_score_rect = your_score.get_rect()
            your_score_rect.center = ((1280 // 2) - 40, 100)

            windows.blit(over_font, over_font_rect)
            windows.blit(your_score, your_score_rect)
            pygame.display.update()

    def records(self):
        records = True
        while records:
            windows.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
            windows.blit(records_title, records_title_rect)
            for i in range(7):
                windows.blit(record_score[i], record_score_rect[i])
            pygame.display.update()

    def choice(self):
        global game_type_1
        choice = True
        while choice:
            x, y = pygame.mouse.get_pos()
            windows.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

            windows.blit(game_type_1, game_type_1_rect)

            if collision_state(x, y, (1280 // 2) - 40, 320) is True:
                game_type_1 = font_op.render("INFINITE MODE", True, (0, 0, 0), (255, 255, 255))
                if pygame.mouse.get_pressed(3)[0] is True:
                    game()
            if collision_state(x, y, (1280 // 2) - 40, 320) is False:
                game_type_1 = font_op.render("INFINITE MODE", True, (255, 255, 255), (0, 0, 0))
            pygame.display.update()


Menu.main()
