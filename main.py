import pygame

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((618, 359))
pygame.display.set_caption('My test game')
icon = pygame.image.load('images/game_icon.png').convert_alpha()
pygame.display.set_icon(icon)

#Player
bg = pygame.image.load('images/bg_image.png').convert_alpha()
walk_left = [
    pygame.image.load('images/player_left/player_left1.png').convert_alpha(),
    pygame.image.load('images/player_left/player_left2.png').convert_alpha(),
    pygame.image.load('images/player_left/player_left3.png').convert_alpha(),
    pygame.image.load('images/player_left/player_left4.png').convert_alpha(),
]
walk_right = [
    pygame.image.load('images/player_right/player_right1.png').convert_alpha(),
    pygame.image.load('images/player_right/player_right2.png').convert_alpha(),
    pygame.image.load('images/player_right/player_right3.png').convert_alpha(),
    pygame.image.load('images/player_right/player_right4.png').convert_alpha(),
]
player_speed = 5
player_x = 150
player_y = 250
player_anim_count = 0
bg_x = 0


#Enemy
ghost = pygame.image.load('images/ghost1.png').convert_alpha()
ghost_list_in_game = []
ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 2500)


is_jump = False
jump_count = 8

#Sound
bg_sound = pygame.mixer.Sound('sounds/bg_music.mp3')
bg_sound.play(loops=60)


label = pygame.font.Font('fonts/Roboto-Regular.ttf', 40)
lose_label = label.render('Game over!', False, ('Red'))
restart_label = label.render('Restart!', False, ('Green'))
restart_label_rect = restart_label.get_rect(topleft=(180, 200))


gameplay = True


running = True
while running:

    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 618, 0))

    if gameplay:
        player_rect = walk_right[0].get_rect(topleft=(player_x, player_y))

        if ghost_list_in_game:
            for (i, elem) in enumerate(ghost_list_in_game):
                screen.blit(ghost, elem)
                elem.x -= 10

                if elem.x < -10:
                    ghost_list_in_game.pop(i)

                if player_rect.colliderect(elem):
                    gameplay = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        if keys[pygame.K_LEFT] and player_x > 50:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 200:
            player_x += player_speed

        if not is_jump:
            if keys[pygame.K_UP]:
                is_jump = True
        else:
            if jump_count >= -8:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8


        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1

        bg_x -= 2
        if bg_x == -618:
            bg_x = 0

    else:
        screen.fill(('Black'))
        screen.blit(lose_label, (180, 100))
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and \
                pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
            ghost_list_in_game.clear()



    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == ghost_timer:
            ghost_list_in_game.append(ghost.get_rect(topleft=(620, 250)))

    clock.tick(15)


