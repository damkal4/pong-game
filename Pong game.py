import pygame
import sys
import random

pygame.init()

width, height = 1280, 960
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong game")

white = (255, 255, 255)
black = (0, 0, 0)
light_grey = (200, 200, 200)

block_width, block_height = 10, 140

ball_radius = 15

game_font = pygame.font.Font("freesansbold.ttf", 32)
menu_font = pygame.font.Font("freesansbold.ttf", 70)

inscription = "Press space to start"

clock = pygame.time.Clock()


class Block:
    color = light_grey
    speed = 0
    speeding = 7

    def __init__(self, x_pos, y_pos, width, height, score):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.score = score

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x_pos, self.y_pos, self.width, self.height))


class Ball:
    speed = 0
    color = light_grey
    max_speed = 5

    def __init__(self, x_pos, y_pos, radius):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radius = radius
        self.x_speed = self.speed
        self.y_speed = self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x_pos, self.y_pos), self.radius)

    def move(self):
        self.x_pos += self.x_speed
        self.y_pos += self.y_speed


def draw(screen, blocks, player_score, opponent_score, inscription, ball):
    screen.fill(black)
    pygame.draw.aaline(screen, light_grey, (width/2, 0), (width/2, height))

    player_text = game_font.render(f"{player_score}", False, light_grey)
    screen.blit(player_text, (660, 470))
    opponent_text = game_font.render(f"{opponent_score}", False, light_grey)
    screen.blit(opponent_text, (600, 470))
    if ball.x_speed == 0:
        inscription_text = game_font.render(f"{inscription}", False, white)
        screen.blit(inscription_text, (490, 100))

    for block in blocks:
        block.draw(screen)

    pygame.display.update()


def handle_collision(ball, player, opponent):
    if ball.y_pos + ball.radius >= height or ball.y_pos - ball.radius <= 0:
        ball.y_speed *= -1

    if ball.x_speed < 0:
        if ball.y_pos >= opponent.y_pos and ball.y_pos <= opponent.y_pos + opponent.height:
            if ball.x_pos - ball.radius <= opponent.x_pos + opponent.width:
                ball.x_speed *= -1

                middle_y_pos = opponent.y_pos + opponent.height/2
                difference_y_pos = middle_y_pos - ball.y_pos
                factor = (opponent.height/2) / ball.max_speed
                ball.y_speed = difference_y_pos / factor * -1

    if ball.x_speed > 0:
        if ball.y_pos >= player.y_pos and ball.y_pos <= player.y_pos + player.height:
            if ball.x_pos + ball.radius >= player.x_pos:
                ball.x_speed *= -1

                middle_y_pos = player.y_pos + player.height / 2
                difference_y_pos = middle_y_pos - ball.y_pos
                factor = (player.height / 2) / ball.max_speed
                ball.y_speed = difference_y_pos / factor * -1


def move(block):
    block.y_pos += block.speed
    if block.y_pos >= height - block_height:
        block.y_pos = height - block_height
    if block.y_pos <= 0:
        block.y_pos = 0


def score(player, opponent, ball):
    if ball.x_pos < 0:
        player.score += 1
        stop = True
        reset(player, opponent, ball, stop)

    elif ball.x_pos > width:
        opponent.score += 1
        stop = True
        reset(player, opponent, ball, stop)


def reset(player, opponent, ball, stop):
    if stop:
        player.y_pos, opponent.y_pos = height/2 - 70, height/2 - 70
        ball.x_pos = width/2
        ball.y_pos = height/2
        ball.y_speed, ball.x_speed = 0, 0


def two_players():
    player = Block(width - 20, height/2 - 70, block_width, block_height, 0)
    opponent = Block(10, height/2 - 70, block_width, block_height, 0)
    ball = Ball(width/2, height/2, ball_radius)

    while True:
        clock.tick(60)
        draw(screen, [player, opponent, ball], player.score, opponent.score, inscription, ball)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    player.speed += player.speeding
                if event.key == pygame.K_UP:
                    player.speed -= player.speeding
                if event.key == pygame.K_s:
                    opponent.speed += opponent.speeding
                if event.key == pygame.K_w:
                    opponent.speed -= opponent.speeding
                if event.key == pygame.K_SPACE:
                    ball.y_speed = random.randrange(-6, 6, 1)
                    ball.x_speed = random.choice([-15, 15])

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player.speed -= player.speeding
                if event.key == pygame.K_UP:
                    player.speed += player.speeding
                if event.key == pygame.K_s:
                    opponent.speed -= opponent.speeding
                if event.key == pygame.K_w:
                    opponent.speed += opponent.speeding

        move(player)
        move(opponent)
        ball.move()
        handle_collision(ball, player, opponent)
        score(player, opponent, ball)


def main():
    pygame.display.set_caption("Menu")
    while True:
        clock.tick(60)
        screen.fill(black)
        click = False

        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        name = menu_font.render("PONG GAME", True, white)
        screen.blit(name, (410, 50))
        menu = menu_font.render("MAIN MENU", True, white)
        screen.blit(menu, (420, 150))

        players = pygame.Rect(450, 570, 380, 60)
        pygame.draw.rect(screen, black, players)
        players_text = menu_font.render("2 PLAYERS", True, white)
        screen.blit(players_text, (445, 570))

        exit = pygame.Rect(560, 720, 170, 60)
        pygame.draw.rect(screen, black, exit)
        exit_text = menu_font.render("EXIT", True, white)
        screen.blit(exit_text, (555, 720))

        if players.collidepoint((mouse_x, mouse_y)):
            players_text = menu_font.render("2 PLAYERS", True, light_grey)
            screen.blit(players_text, (445, 570))
            if click:
                two_players()
        if exit.collidepoint((mouse_x, mouse_y)):
            exit_text = menu_font.render("EXIT", True, light_grey)
            screen.blit(exit_text, (555, 720))
            if click:
                pygame.quit()
                sys.exit()

        pygame.display.update()


if __name__ == '__main__':
    main()
