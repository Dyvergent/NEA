import pygame
from pygame.locals import *
from tutorials import main_game_tutorial,history_tutorial,leaderboard_tutorial,history_database_tutorial,solver_tutorial,solve_it_tutorial
from puzzle.classes import *
import config
pygame.font.init()
def main():
    WIDTH = 1280
    HEIGHT = 720
    FPS = 60
    # setting the theme colours
    all_colours = config.get_all_colours()
    text_BLACK = (0,0,0)
    text_WHITE = (255,255,255)
    BLACK = all_colours[1]
    WHITE = all_colours[0]
    BROWN = all_colours[2]
    GREEN = all_colours[3]
    GREY = all_colours[4]
    YELLOW = all_colours[8]
    CYAN = all_colours[9]
    background = all_colours[6]
    box_colour = all_colours[7]
    NAVY = all_colours[10]
    RED = all_colours[11]
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tutorial Menu")
    clock = pygame.time.Clock()
    rect = pygame.rect.Rect(60,60,1160,600)
    border = pygame.rect.Rect(59,59,1162,602)
    main_game_button = Button(200,HEIGHT//2-150,200,80,"Main Game Tutorial",GREEN,border_radius=12)
    history_button = Button(200,HEIGHT//2-50,200,80,"History Tutorial",GREEN,border_radius=12)
    leaderboard_button = Button(840,HEIGHT//2-150,200,80,"Leaderboard",NAVY,border_radius=12)
    history_database_button = Button(840,HEIGHT//2-50,200,80,"History Database",NAVY,border_radius=12)
    solver_button = Button(840,HEIGHT//2+50,200,80,"Solver",NAVY,border_radius=12)
    solve_it_button = Button(200,HEIGHT//2+50,200,80,"How to Solve",GREEN,border_radius=12)
    main_menu_button = Button(80,80,150,50,"Main Menu",BROWN,border_radius=12)
    font = pygame.font.Font("CrimsonPro-VariableFont_wght.ttf", 36)
    running = True
    def draw_text(text, font, color, surface, x, y):
        #Draw text centered at (x,y)
        text_obj = font.render(text, True, color)
        rect = text_obj.get_rect(center=(x, y))
        surface.blit(text_obj, rect)
    while running:
        clock.tick(FPS)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if main_game_button.handle_click(pygame.mouse.get_pos()):
                    main_game_tutorial.main()
                elif history_button.handle_click(pygame.mouse.get_pos()):
                    history_tutorial.main()
                elif leaderboard_button.handle_click(pygame.mouse.get_pos()):
                    leaderboard_tutorial.main()
                elif history_database_button.handle_click(pygame.mouse.get_pos()):
                    history_database_tutorial.main()
                elif solver_button.handle_click(pygame.mouse.get_pos()):
                    solver_tutorial.main()
                elif solve_it_button.handle_click(pygame.mouse.get_pos()):
                    solve_it_tutorial.main()
                elif main_menu_button.handle_click(pygame.mouse.get_pos()):
                    running = False

        screen.fill(background)
        pygame.draw.rect(screen,WHITE,border)
        pygame.draw.rect(screen,box_colour,rect)
        draw_text("Select which tutorial you would like to view:",font,WHITE,screen,WIDTH//2,110)
        draw_text("Tutorials",font,WHITE,screen,300,175)
        draw_text("How It Works",font,WHITE,screen,940,175)
        main_game_button.create_button(screen,20,WHITE)
        main_menu_button.create_button(screen,20,WHITE)
        leaderboard_button.create_button(screen,20,WHITE)
        history_button.create_button(screen,20,WHITE)
        history_database_button.create_button(screen,20,WHITE)
        solver_button.create_button(screen,20,WHITE)
        solve_it_button.create_button(screen,20,WHITE)
        

if __name__ == "__main__":
    main()
    pygame.quit()
