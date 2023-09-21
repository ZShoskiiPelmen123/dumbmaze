import pygame
import sys

width = 1280
height = 710
FPS = 180
size = 20

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
white = (255, 255, 255)

up = (0, -1)
down = (0, 1)
left = (-1, 0)
right = (1, 0)

speed = 1
pygame.init()

sc = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()


def finish():
    pygame.quit()
    sys.exit(0)


def main():

    snake = pygame.Rect(55, 666, size, size)
    head = up

    block = pygame.Rect(0, 0, 100, 500)

    second_block = pygame.Rect(200, 200, 100, 500)

    third_block = pygame.Rect(400, 0, 100, 650)

    fourth_block = pygame.Rect(500, 0, 500, 400)

    fifth_block = pygame.Rect(600, 500, 700, 200)

    sixth_block = pygame.Rect(600, 400, 50, 40)

    seventh_block = pygame.Rect(750, 460, 50, 40)

    eighth_block = pygame.Rect(950, 400, 50, 60)

    ninth_block = pygame.Rect(1050, 350, 75, 75)

    tenth_block = pygame.Rect(1150, 300, 100, 100)

    eleventh_block = pygame.Rect(1025, 115, 125, 125)

    twelfth_block = pygame.Rect(1225, 75, 100, 100)

    thirteenth_block = pygame.Rect(1000, 0, 500, 50)

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                finish()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake.move_ip(-5, 0)
                    head = left

                if event.key == pygame.K_RIGHT:
                    snake.move_ip(5, 0)
                    head = right

                if event.key == pygame.K_UP:
                    snake.move_ip(0, -5)
                    head = up

                if event.key == pygame.K_DOWN:
                    snake.move_ip(0, 5)
                    head = down

        if snake.bottom > height or snake.top < 0 or snake.left < 0 or snake.right > width:
            return
        if block.colliderect(snake):
            return
        if second_block.colliderect(snake):
            return
        if third_block.colliderect(snake):
            return
        if fourth_block.colliderect(snake):
            return
        if fifth_block.colliderect(snake):
            return
        if sixth_block.colliderect(snake):
            return
        if seventh_block.colliderect(snake):
            return
        if eighth_block.colliderect(snake):
            return
        if ninth_block.colliderect(snake):
            return
        if tenth_block.colliderect(snake):
            return
        if eleventh_block.colliderect(snake):
            return
        if twelfth_block.colliderect(snake):
            return
        if thirteenth_block.colliderect(snake):
            head = down
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        return
                else:
                    return

            finalText = pygame.font.Font('scootchover-sans.ttf', 36)
            show_final = finalText.render('ВЫ ПОБЕДИЛИ!', 1, (255, 0, 255))
            sc.blit(show_final, (height / 2, width / 2))
        sc.fill(black)
        pygame.draw.rect(sc, green, block)
        pygame.draw.rect(sc, green, second_block)
        pygame.draw.rect(sc, green, third_block)
        pygame.draw.rect(sc, green, fourth_block)
        pygame.draw.rect(sc, green, fifth_block)
        pygame.draw.rect(sc, green, sixth_block)
        pygame.draw.rect(sc, green, seventh_block)
        pygame.draw.rect(sc, green, eighth_block)
        pygame.draw.rect(sc, green, ninth_block)
        pygame.draw.rect(sc, green, tenth_block)
        pygame.draw.rect(sc, green, eleventh_block)
        pygame.draw.rect(sc, green, twelfth_block)
        pygame.draw.rect(sc, red, thirteenth_block)
        snake_head = [speed * x for x in head]
        snake.move_ip(snake_head[0], snake_head[1])
        pygame.draw.rect(sc, green, snake)
        clock.tick(FPS)
        pygame.display.update()


main()