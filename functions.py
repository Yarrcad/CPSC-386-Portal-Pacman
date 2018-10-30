import pygame
import sys



def check_keydown_events(event, pacman):
    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
        pacman.next_move = "right"
    elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
        pacman.next_move = "left"
    elif event.key == pygame.K_w or event.key == pygame.K_UP:
        pacman.next_move = "up"
    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
        pacman.next_move = "down"

def check_mouse_clicks(event, bportal, oportal, menu, game, score_button, play_button, pacman, screen, maze, audio):
    if score_button.rect.collidepoint(pygame.mouse.get_pos()):
        menu.show_scores = not menu.show_scores
    elif event.type == pygame.MOUSEBUTTONDOWN and play_button.rect.collidepoint(pygame.mouse.get_pos()) and not game.active:
        game.active = True
        maze.build()
        audio.a.play(audio.begin)
    elif event.button == 1 and game.active and check_space(pacman, screen) and pacman.alive:
        bportal.active = True
        bportal.location()
    elif event.button == 3 and game.active and check_space(pacman, screen) and pacman.alive:
        oportal.active = True
        oportal.location()

def check_space(pacman, screen):
    if pacman.direction == 'right' and int(pacman.centerx) + 13 * 4 < screen.get_rect().right:
        return (0, 0, 0) == screen.get_at((int(pacman.centerx) + 13 * 4 - 1, int(pacman.centery))) or (255, 255, 255) == screen.get_at((int(pacman.centerx) + 13 * 4 - 1, int(pacman.centery)))
    if pacman.direction == 'left' and int(pacman.centerx) + 13 * 4 > screen.get_rect().left:
        return (0, 0, 0) == screen.get_at((int(pacman.centerx) - 13 * 4 - 1, int(pacman.centery))) or (255, 255, 255) == screen.get_at((int(pacman.centerx) - 13 * 4 - 1, int(pacman.centery)))
    if pacman.direction == 'up' and int(pacman.centery) + 13 * 4 > screen.get_rect().top:
        return (0, 0, 0) == screen.get_at((int(pacman.centerx), int(pacman.centery) - 13 * 4 - 1)) or (255, 255, 255) == screen.get_at((int(pacman.centerx), int(pacman.centery) - 13 * 4 - 1))
    if pacman.direction == 'down' and int(pacman.centery) + 13 * 4 < screen.get_rect().bottom:
        return (0, 0, 0) == screen.get_at((int(pacman.centerx), int(pacman.centery) + 13 * 4 - 1)) or (255, 255, 255) == screen.get_at((int(pacman.centerx), int(pacman.centery) + 13 * 4 - 1))

def check_events(pacman, score_button, menu, play_button, game, bportal, oportal, screen, maze, audio):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, pacman)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            check_mouse_clicks(event, bportal, oportal, menu, game, score_button, play_button, pacman , screen, maze, audio)
        if score_button.rect.collidepoint(pygame.mouse.get_pos()):
            score_button.active = True
        else:
            score_button.active = False
        if play_button.rect.collidepoint(pygame.mouse.get_pos()):
            play_button.active = True
        else:
            play_button.active = False


def check_score_button(score_button, mouse_x, mouse_y, menu):
    """Start a new game when the player clicks Play."""
    button_clicked = score_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and menu.show_scores:
        menu.show_scores = False
    elif button_clicked and not menu.show_scores:
        menu.show_scores = True


def check_collisions(pacman, bricks, shields, powerpills, scoreboard, blinky, pinky, inky, clyde, qpills, fruit, audio):
    powerpill = pygame.sprite.spritecollideany(pacman, powerpills)
    if powerpill:
        scoreboard.score += 100
        scoreboard.eaten += 1
        powerpills.remove(powerpill)
    qpill = pygame.sprite.spritecollideany(pacman, qpills)
    if qpill:
        qpills.remove(qpill)
        pacman.boosted = True
        change_direction(blinky)
        change_direction(pinky)
        change_direction(inky)
        change_direction(clyde)
    if pygame.sprite.collide_rect(pacman, fruit) and fruit.active:
        scoreboard.score += 400
        fruit.active = False
        audio.b.play(audio.fruit)
    pac_collide(pacman, bricks, shields)
    if pacman.boosted:
        ghost_ai3(blinky, bricks, shields, scoreboard, audio)
        ghost_ai3(pinky, bricks, shields, scoreboard, audio)
        ghost_ai3(inky, bricks, shields, scoreboard, audio)
        ghost_ai3(clyde, bricks, shields, scoreboard, audio)
    else:
        if blinky.active:
            ghost_ai2(blinky, bricks, shields, audio)
        else:
            ghost_ai4(blinky, bricks)
        if inky.active:
            ghost_ai1(inky, bricks, shields, audio)
        else:
            ghost_ai4(inky, bricks)
        if pinky.active:
            ghost_ai1(pinky, bricks, shields, audio)
        else:
            ghost_ai4(pinky, bricks)
        if clyde.active:
            ghost_ai1(clyde, bricks, shields, audio)
        else:
            ghost_ai4(clyde, bricks)
        
def change_direction(ghost):
    if ghost.direction == "right":
        ghost.direction = "left"
    elif ghost.direction == "left":
        ghost.direction = "right"
    elif ghost.direction == "up":
        ghost.direction = "down"
    elif ghost.direction == "down":
        ghost.direction = "up"



def pac_collide(pacman, bricks, shields):
    if pacman.next_move == "left":
        pacman.rect.centerx -= 1
        if not pygame.sprite.spritecollideany(pacman, bricks) and not pygame.sprite.spritecollideany(pacman, shields):
            pacman.direction = "left"
            pacman.next_move = "none"
            pacman.index = 0
            pacman.move = True
        pacman.rect.centerx += 1
    if pacman.next_move == "right":
        pacman.rect.centerx += 1
        if not pygame.sprite.spritecollideany(pacman, bricks) and not pygame.sprite.spritecollideany(pacman, shields):
            pacman.direction = "right"
            pacman.next_move = "none"
            pacman.index = 0
            pacman.move = True
        pacman.rect.centerx -= 1
    if pacman.next_move == "up":
        pacman.rect.centery -= 1
        if not pygame.sprite.spritecollideany(pacman, bricks) and not pygame.sprite.spritecollideany(pacman, shields):
            pacman.direction = "up"
            pacman.next_move = "none"
            pacman.index = 0
            pacman.move = True
        pacman.rect.centery += 1
    if pacman.next_move == "down":
        pacman.rect.centery += 1
        if not pygame.sprite.spritecollideany(pacman, bricks) and not pygame.sprite.spritecollideany(pacman, shields):
            pacman.direction = "down"
            pacman.index = 0
            pacman.next_move = "none"
            pacman.move = True
        pacman.rect.centery -= 1

    if pacman.direction == "left":
        pacman.rect.centerx -= 1
        if pygame.sprite.spritecollideany(pacman, bricks) or pygame.sprite.spritecollideany(pacman, shields):
            pacman.move = False
        pacman.rect.centerx += 1
    if pacman.direction == "right":
        pacman.rect.centerx += 1
        if pygame.sprite.spritecollideany(pacman, bricks) or pygame.sprite.spritecollideany(pacman, shields):
            pacman.move = False
        pacman.rect.centerx -= 1
    if pacman.direction == "up":
        pacman.rect.centery -= 1
        if pygame.sprite.spritecollideany(pacman, bricks) or pygame.sprite.spritecollideany(pacman, shields):
            pacman.move = False
        pacman.rect.centery += 1
    if pacman.direction == "down":
        pacman.rect.centery += 1
        if pygame.sprite.spritecollideany(pacman, bricks) or pygame.sprite.spritecollideany(pacman, shields):
            pacman.move = False
        pacman.rect.centery -= 1

def ghost_ai1(ghost, bricks, shields, audio):
    if pygame.sprite.collide_rect(ghost, ghost.pacman) and ghost.pacman.alive:
        audio.a.play(audio.death)
        ghost.pacman.death()
    if ghost.direction == "left":
        ghost.rect.centerx -= ghost.move_speed
        if pygame.sprite.spritecollideany(ghost, bricks) or pygame.sprite.spritecollideany(ghost, shields):
            ghost.rect.centerx += ghost.move_speed
            if ghost.centery < ghost.pacman.centery:
                ghost.rect.centery += ghost.move_speed
                if not pygame.sprite.spritecollideany(ghost, bricks) and not pygame.sprite.spritecollideany(ghost, shields):
                    ghost.direction = "down"
                else:
                    ghost.direction = "up"
                ghost.rect.centery -= ghost.move_speed
            else:
                ghost.rect.centery -= ghost.move_speed
                if not pygame.sprite.spritecollideany(ghost, bricks) and not pygame.sprite.spritecollideany(ghost, shields):
                    ghost.direction = "up"
                else:
                    ghost.direction = "down"
                ghost.rect.centery += ghost.move_speed
        else:
            ghost.rect.centerx += ghost.move_speed

    elif ghost.direction == "right":
        ghost.rect.centerx += ghost.move_speed
        if pygame.sprite.spritecollideany(ghost, bricks) or pygame.sprite.spritecollideany(ghost, shields):
            ghost.rect.centerx -= ghost.move_speed
            if ghost.centery < ghost.pacman.centery:
                ghost.rect.centery += ghost.move_speed
                if not pygame.sprite.spritecollideany(ghost, bricks) and not pygame.sprite.spritecollideany(
                        ghost, shields):
                    ghost.direction = "down"
                else:
                    ghost.direction = "up"
                ghost.rect.centery -= ghost.move_speed
            else:
                ghost.rect.centery -= ghost.move_speed
                if not pygame.sprite.spritecollideany(ghost, bricks) and not pygame.sprite.spritecollideany(
                        ghost, shields):
                    ghost.direction = "up"
                else:
                    ghost.direction = "down"
                ghost.rect.centery += ghost.move_speed
        else:
            ghost.rect.centerx -= ghost.move_speed

    elif ghost.direction == "up":
        ghost.rect.centery -= ghost.move_speed
        if pygame.sprite.spritecollideany(ghost, bricks) or pygame.sprite.spritecollideany(ghost, shields):
            ghost.rect.centery += ghost.move_speed
            if ghost.centerx < ghost.pacman.centerx:
                ghost.rect.centerx += ghost.move_speed
                if not pygame.sprite.spritecollideany(ghost, bricks) and not pygame.sprite.spritecollideany(
                        ghost, shields):
                    ghost.direction = "right"
                else:
                    ghost.direction = "left"
                ghost.rect.centerx -= ghost.move_speed
            else:
                ghost.rect.centerx -= ghost.move_speed
                if not pygame.sprite.spritecollideany(ghost, bricks) and not pygame.sprite.spritecollideany(
                        ghost, shields):
                    ghost.direction = "left"
                else:
                    ghost.direction = "right"
                ghost.rect.centerx += ghost.move_speed
        else:
            ghost.rect.centery += ghost.move_speed

    elif ghost.direction == "down":
        ghost.rect.centery += ghost.move_speed
        if pygame.sprite.spritecollideany(ghost, bricks) or pygame.sprite.spritecollideany(ghost, shields):
            ghost.rect.centery -= ghost.move_speed
            if ghost.centerx < ghost.pacman.centerx:
                ghost.rect.centerx += ghost.move_speed
                if not pygame.sprite.spritecollideany(ghost, bricks) and not pygame.sprite.spritecollideany(
                        ghost, shields):
                    ghost.direction = "right"
                else:
                    ghost.direction = "left"
                ghost.rect.centerx -= ghost.move_speed
            else:
                ghost.rect.centerx -= ghost.move_speed
                if not pygame.sprite.spritecollideany(ghost, bricks) and not pygame.sprite.spritecollideany(
                        ghost, shields):
                    ghost.direction = "left"
                else:
                    ghost.direction = "right"
                ghost.rect.centerx += ghost.move_speed
        else:
            ghost.rect.centery -= ghost.move_speed


def ghost_ai2(ghost, bricks, shields, audio):
    if pygame.sprite.collide_rect(ghost, ghost.pacman) and ghost.pacman.alive:
        audio.a.play(audio.death)
        ghost.pacman.death()
    if (ghost.direction == "left" or ghost.direction == "right") and ghost.pacman.centery > ghost.centery:
        ghost.next_move = "down"
    elif (ghost.direction == "left" or ghost.direction == "right") and ghost.pacman.centery < ghost.centery:
        ghost.next_move = "up"
    elif (ghost.direction == "up" or ghost.direction == "down") and ghost.pacman.centerx > ghost.centerx:
        ghost.next_move = "right"
    elif (ghost.direction == "up" or ghost.direction == "down") and ghost.pacman.centerx < ghost.centerx:
        ghost.next_move = "left"
        
    if ghost.next_move == "left":
        ghost.rect.centerx -= ghost.move_speed
        if not pygame.sprite.spritecollideany(ghost, bricks) and not pygame.sprite.spritecollideany(ghost, shields):
            ghost.direction = "left"
        ghost.rect.centerx += ghost.move_speed
    if ghost.next_move == "right":
        ghost.rect.centerx += ghost.move_speed
        if not pygame.sprite.spritecollideany(ghost, bricks) and not pygame.sprite.spritecollideany(ghost, shields):
            ghost.direction = "right"
        ghost.rect.centerx -= ghost.move_speed
    if ghost.next_move == "up":
        ghost.rect.centery -= ghost.move_speed
        if not pygame.sprite.spritecollideany(ghost, bricks) and not pygame.sprite.spritecollideany(ghost, shields):
            ghost.direction = "up"
        ghost.rect.centery += ghost.move_speed
    if ghost.next_move == "down":
        ghost.rect.centery += ghost.move_speed
        if not pygame.sprite.spritecollideany(ghost, bricks) and not pygame.sprite.spritecollideany(ghost, shields):
            ghost.direction = "down"
        ghost.rect.centery -= ghost.move_speed

        
    if ghost.direction == "left":
        ghost.rect.centerx -= ghost.move_speed
        if pygame.sprite.spritecollideany(ghost, bricks) or pygame.sprite.spritecollideany(ghost, shields):
            ghost.rect.centerx += ghost.move_speed
            if ghost.centery < ghost.pacman.centery:
                ghost.rect.centery += ghost.move_speed
                if not pygame.sprite.spritecollideany(ghost, bricks) and not pygame.sprite.spritecollideany(ghost,
                                                                                                            shields):
                    ghost.direction = "down"
                else:
                    ghost.direction = "up"
                ghost.rect.centery -= ghost.move_speed
            else:
                ghost.rect.centery -= ghost.move_speed
                if not pygame.sprite.spritecollideany(ghost, bricks) and not pygame.sprite.spritecollideany(ghost,
                                                                                                            shields):
                    ghost.direction = "up"
                else:
                    ghost.direction = "down"
                ghost.rect.centery += ghost.move_speed
        else:
            ghost.rect.centerx += ghost.move_speed

    elif ghost.direction == "right":
        ghost.rect.centerx += ghost.move_speed
        if pygame.sprite.spritecollideany(ghost, bricks) or pygame.sprite.spritecollideany(ghost, shields):
            ghost.rect.centerx -= ghost.move_speed
            if ghost.centery < ghost.pacman.centery:
                ghost.rect.centery += ghost.move_speed
                if not pygame.sprite.spritecollideany(ghost, bricks) and not pygame.sprite.spritecollideany(
                        ghost, shields):
                    ghost.direction = "down"
                else:
                    ghost.direction = "up"
                ghost.rect.centery -= ghost.move_speed
            else:
                ghost.rect.centery -= ghost.move_speed
                if not pygame.sprite.spritecollideany(ghost, bricks) and not pygame.sprite.spritecollideany(
                        ghost, shields):
                    ghost.direction = "up"
                else:
                    ghost.direction = "down"
                ghost.rect.centery += ghost.move_speed
        else:
            ghost.rect.centerx -= ghost.move_speed

    elif ghost.direction == "up":
        ghost.rect.centery -= ghost.move_speed
        if pygame.sprite.spritecollideany(ghost, bricks) or pygame.sprite.spritecollideany(ghost, shields):
            ghost.rect.centery += ghost.move_speed
            if ghost.centerx < ghost.pacman.centerx:
                ghost.rect.centerx += ghost.move_speed
                if not pygame.sprite.spritecollideany(ghost, bricks) and not pygame.sprite.spritecollideany(
                        ghost, shields):
                    ghost.direction = "right"
                else:
                    ghost.direction = "left"
                ghost.rect.centerx -= ghost.move_speed
            else:
                ghost.rect.centerx -= ghost.move_speed
                if not pygame.sprite.spritecollideany(ghost, bricks) and not pygame.sprite.spritecollideany(
                        ghost, shields):
                    ghost.direction = "left"
                else:
                    ghost.direction = "right"
                ghost.rect.centerx += ghost.move_speed
        else:
            ghost.rect.centery += ghost.move_speed

    elif ghost.direction == "down":
        ghost.rect.centery += ghost.move_speed
        if pygame.sprite.spritecollideany(ghost, bricks) or pygame.sprite.spritecollideany(ghost, shields):
            ghost.rect.centery -= ghost.move_speed
            if ghost.centerx < ghost.pacman.centerx:
                ghost.rect.centerx += ghost.move_speed
                if not pygame.sprite.spritecollideany(ghost, bricks) and not pygame.sprite.spritecollideany(
                        ghost, shields):
                    ghost.direction = "right"
                else:
                    ghost.direction = "left"
                ghost.rect.centerx -= ghost.move_speed
            else:
                ghost.rect.centerx -= ghost.move_speed
                if not pygame.sprite.spritecollideany(ghost, bricks) and not pygame.sprite.spritecollideany(
                        ghost, shields):
                    ghost.direction = "left"
                else:
                    ghost.direction = "right"
                ghost.rect.centerx += ghost.move_speed
        else:
            ghost.rect.centery -= ghost.move_speed


def ghost_ai3(ghost, bricks, shields, scoreboard, audio):
    if pygame.sprite.collide_rect(ghost, ghost.pacman) and ghost.active:
        ghost.pacman.ghost_score += 1
        scoreboard.score += ghost.pacman.ghost_score * 200
        ghost.death()
        audio.b.play(audio.ghost)
    if (ghost.direction == "left" or ghost.direction == "right") and ghost.pacman.centery > ghost.centery:
        ghost.next_move = "up"
    elif (ghost.direction == "left" or ghost.direction == "right") and ghost.pacman.centery < ghost.centery:
        ghost.next_move = "down"
    elif (ghost.direction == "up" or ghost.direction == "down") and ghost.pacman.centerx > ghost.centerx:
        ghost.next_move = "left"
    elif (ghost.direction == "up" or ghost.direction == "down") and ghost.pacman.centerx < ghost.centerx:
        ghost.next_move = "right"

    if ghost.next_move == "left":
        ghost.rect.centerx -= ghost.move_speed
        if not pygame.sprite.spritecollideany(ghost, bricks) and not pygame.sprite.spritecollideany(ghost, shields):
            ghost.direction = "left"
        ghost.rect.centerx += ghost.move_speed
    if ghost.next_move == "right":
        ghost.rect.centerx += ghost.move_speed
        if not pygame.sprite.spritecollideany(ghost, bricks) and not pygame.sprite.spritecollideany(ghost, shields):
            ghost.direction = "right"
        ghost.rect.centerx -= ghost.move_speed
    if ghost.next_move == "up":
        ghost.rect.centery -= ghost.move_speed
        if not pygame.sprite.spritecollideany(ghost, bricks) and not pygame.sprite.spritecollideany(ghost, shields):
            ghost.direction = "up"
        ghost.rect.centery += ghost.move_speed
    if ghost.next_move == "down":
        ghost.rect.centery += ghost.move_speed
        if not pygame.sprite.spritecollideany(ghost, bricks) and not pygame.sprite.spritecollideany(ghost, shields):
            ghost.direction = "down"
        ghost.rect.centery -= ghost.move_speed

    if ghost.direction == "left":
        ghost.rect.centerx -= ghost.move_speed
        if pygame.sprite.spritecollideany(ghost, bricks) or pygame.sprite.spritecollideany(ghost, shields):
            ghost.rect.centerx += ghost.move_speed
            if ghost.centery < ghost.pacman.centery:
                ghost.rect.centery += ghost.move_speed
                if not pygame.sprite.spritecollideany(ghost, bricks) and not pygame.sprite.spritecollideany(ghost,
                                                                                                            shields):
                    ghost.direction = "down"
                else:
                    ghost.direction = "up"
                ghost.rect.centery -= ghost.move_speed
            else:
                ghost.rect.centery -= ghost.move_speed
                if not pygame.sprite.spritecollideany(ghost, bricks) and not pygame.sprite.spritecollideany(ghost,
                                                                                                            shields):
                    ghost.direction = "up"
                else:
                    ghost.direction = "down"
                ghost.rect.centery += ghost.move_speed
        else:
            ghost.rect.centerx += ghost.move_speed

    elif ghost.direction == "right":
        ghost.rect.centerx += ghost.move_speed
        if pygame.sprite.spritecollideany(ghost, bricks) or pygame.sprite.spritecollideany(ghost, shields):
            ghost.rect.centerx -= ghost.move_speed
            if ghost.centery < ghost.pacman.centery:
                ghost.rect.centery += ghost.move_speed
                if not pygame.sprite.spritecollideany(ghost, bricks) and not pygame.sprite.spritecollideany(
                        ghost, shields):
                    ghost.direction = "down"
                else:
                    ghost.direction = "up"
                ghost.rect.centery -= ghost.move_speed
            else:
                ghost.rect.centery -= ghost.move_speed
                if not pygame.sprite.spritecollideany(ghost, bricks) and not pygame.sprite.spritecollideany(
                        ghost, shields):
                    ghost.direction = "up"
                else:
                    ghost.direction = "down"
                ghost.rect.centery += ghost.move_speed
        else:
            ghost.rect.centerx -= ghost.move_speed

    elif ghost.direction == "up":
        ghost.rect.centery -= ghost.move_speed
        if pygame.sprite.spritecollideany(ghost, bricks) or pygame.sprite.spritecollideany(ghost, shields):
            ghost.rect.centery += ghost.move_speed
            if ghost.centerx < ghost.pacman.centerx:
                ghost.rect.centerx += ghost.move_speed
                if not pygame.sprite.spritecollideany(ghost, bricks) and not pygame.sprite.spritecollideany(
                        ghost, shields):
                    ghost.direction = "right"
                else:
                    ghost.direction = "left"
                ghost.rect.centerx -= ghost.move_speed
            else:
                ghost.rect.centerx -= ghost.move_speed
                if not pygame.sprite.spritecollideany(ghost, bricks) and not pygame.sprite.spritecollideany(
                        ghost, shields):
                    ghost.direction = "left"
                else:
                    ghost.direction = "right"
                ghost.rect.centerx += ghost.move_speed
        else:
            ghost.rect.centery += ghost.move_speed

    elif ghost.direction == "down":
        ghost.rect.centery += ghost.move_speed
        if pygame.sprite.spritecollideany(ghost, bricks) or pygame.sprite.spritecollideany(ghost, shields):
            ghost.rect.centery -= ghost.move_speed
            if ghost.centerx < ghost.pacman.centerx:
                ghost.rect.centerx += ghost.move_speed
                if not pygame.sprite.spritecollideany(ghost, bricks) and not pygame.sprite.spritecollideany(
                        ghost, shields):
                    ghost.direction = "right"
                else:
                    ghost.direction = "left"
                ghost.rect.centerx -= ghost.move_speed
            else:
                ghost.rect.centerx -= ghost.move_speed
                if not pygame.sprite.spritecollideany(ghost, bricks) and not pygame.sprite.spritecollideany(
                        ghost, shields):
                    ghost.direction = "left"
                else:
                    ghost.direction = "right"
                ghost.rect.centerx += ghost.move_speed
        else:
            ghost.rect.centery -= ghost.move_speed

def ghost_ai4(ghost, bricks):
    if (ghost.direction == "left" or ghost.direction == "right") and 28.5 * 13 < ghost.centery:
        ghost.next_move = "up"
    elif (ghost.direction == "left" or ghost.direction == "right") and 28.5 * 13 > ghost.centery:
        ghost.next_move = "down"
    elif (ghost.direction == "up" or ghost.direction == "down") and 23.5 * 13 < ghost.centerx:
        ghost.next_move = "left"
    elif (ghost.direction == "up" or ghost.direction == "down") and 23.5 * 13 > ghost.centerx:
        ghost.next_move = "right"

    if ghost.next_move == "left":
        ghost.rect.centerx -= ghost.move_speed
        if not pygame.sprite.spritecollideany(ghost, bricks):
            ghost.direction = "left"
        ghost.rect.centerx += ghost.move_speed
    if ghost.next_move == "right":
        ghost.rect.centerx += ghost.move_speed
        if not pygame.sprite.spritecollideany(ghost, bricks):
            ghost.direction = "right"
        ghost.rect.centerx -= ghost.move_speed
    if ghost.next_move == "up":
        ghost.rect.centery -= ghost.move_speed
        if not pygame.sprite.spritecollideany(ghost, bricks):
            ghost.direction = "up"
        ghost.rect.centery += ghost.move_speed
    if ghost.next_move == "down":
        ghost.rect.centery += ghost.move_speed
        if not pygame.sprite.spritecollideany(ghost, bricks):
            ghost.direction = "down"
        ghost.rect.centery -= ghost.move_speed

    if ghost.direction == "left":
        ghost.rect.centerx -= ghost.move_speed
        if pygame.sprite.spritecollideany(ghost, bricks):
            ghost.rect.centerx += ghost.move_speed
            if ghost.centery < ghost.pacman.centery:
                ghost.rect.centery += ghost.move_speed
                if not pygame.sprite.spritecollideany(ghost, bricks):
                    ghost.direction = "down"
                else:
                    ghost.direction = "up"
                ghost.rect.centery -= ghost.move_speed
            else:
                ghost.rect.centery -= ghost.move_speed
                if not pygame.sprite.spritecollideany(ghost, bricks):
                    ghost.direction = "up"
                else:
                    ghost.direction = "down"
                ghost.rect.centery += ghost.move_speed
        else:
            ghost.rect.centerx += ghost.move_speed

    elif ghost.direction == "right":
        ghost.rect.centerx += ghost.move_speed
        if pygame.sprite.spritecollideany(ghost, bricks):
            ghost.rect.centerx -= ghost.move_speed
            if ghost.centery < ghost.pacman.centery:
                ghost.rect.centery += ghost.move_speed
                if not pygame.sprite.spritecollideany(ghost, bricks):
                    ghost.direction = "down"
                else:
                    ghost.direction = "up"
                ghost.rect.centery -= ghost.move_speed
            else:
                ghost.rect.centery -= ghost.move_speed
                if not pygame.sprite.spritecollideany(ghost, bricks):
                    ghost.direction = "up"
                else:
                    ghost.direction = "down"
                ghost.rect.centery += ghost.move_speed
        else:
            ghost.rect.centerx -= ghost.move_speed

    elif ghost.direction == "up":
        ghost.rect.centery -= ghost.move_speed
        if pygame.sprite.spritecollideany(ghost, bricks):
            ghost.rect.centery += ghost.move_speed
            if ghost.centerx < ghost.pacman.centerx:
                ghost.rect.centerx += ghost.move_speed
                if not pygame.sprite.spritecollideany(ghost, bricks):
                    ghost.direction = "right"
                else:
                    ghost.direction = "left"
                ghost.rect.centerx -= ghost.move_speed
            else:
                ghost.rect.centerx -= ghost.move_speed
                if not pygame.sprite.spritecollideany(ghost, bricks):
                    ghost.direction = "left"
                else:
                    ghost.direction = "right"
                ghost.rect.centerx += ghost.move_speed
        else:
            ghost.rect.centery += ghost.move_speed

    elif ghost.direction == "down":
        ghost.rect.centery += ghost.move_speed
        if pygame.sprite.spritecollideany(ghost, bricks):
            ghost.rect.centery -= ghost.move_speed
            if ghost.centerx < ghost.pacman.centerx:
                ghost.rect.centerx += ghost.move_speed
                if not pygame.sprite.spritecollideany(ghost, bricks):
                    ghost.direction = "right"
                else:
                    ghost.direction = "left"
                ghost.rect.centerx -= ghost.move_speed
            else:
                ghost.rect.centerx -= ghost.move_speed
                if not pygame.sprite.spritecollideany(ghost, bricks):
                    ghost.direction = "left"
                else:
                    ghost.direction = "right"
                ghost.rect.centerx += ghost.move_speed
        else:
            ghost.rect.centery -= ghost.move_speed

