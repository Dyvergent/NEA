import pygame
from pygame.locals import *
from pathlib import Path
from puzzle import *
pygame.font.init()
def main():
    WIDTH = 1280
    HEIGHT = 720
    FPS = 60
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BROWN = (150, 75, 0)
    GREEN = (0, 150, 0)
    GREY = (150, 150, 150)
    background = (5, 21, 36)
    box_colour = (7, 31, 53)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tutorial")
    clock = pygame.time.Clock()
    rect = pygame.rect.Rect(60,60,1160,600)
    border = pygame.rect.Rect(59,59,1162,602)
    font = pygame.font.Font("CrimsonPro-VariableFont_wght.ttf",36)
    smalltext = pygame.font.Font("CrimsonPro-VariableFont_wght.ttf",20)
    running = True
    base_path = Path(__file__).parent / "history_database_images"
    img_arr = {
        0:pygame.image.load(base_path / "tutorial0.png"),
        1:pygame.image.load(base_path / "tutorial1.png"),
        2:pygame.image.load(base_path / "tutorial2.png")
        }
    current_screen = 0
    surf_x, surf_y = WIDTH - 150, HEIGHT // 2
    next_button = Button(surf_x, surf_y, 100, 50, "Next", GREY, opacity=150, border_radius=8)
    prev_button = Button(50, surf_y, 100, 50, "Previous", GREY, opacity=150, border_radius=8)
    main_button = Button(surf_x, 60, 100, 50, "Back to Hub", BROWN, opacity=150, border_radius=8)
    while running:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if next_button.handle_click(mouse_pos):
                        current_screen += 1
                        if current_screen >= 2: current_screen = 2
                    elif prev_button.handle_click(mouse_pos):
                        current_screen -= 1
                        if current_screen <= 0: current_screen = 0
                    elif main_button.handle_click(mouse_pos):
                        running = False
        screen.fill(background)
        screen.blit(img_arr[current_screen],(0,0))
        next_button.create_button(screen, 20, WHITE)
        prev_button.create_button(screen, 20, WHITE)
        main_button.create_button(screen, 20, WHITE)


if __name__ == "__main__":
    main()
    pygame.quit()
