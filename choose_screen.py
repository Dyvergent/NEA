import pygame
from pygame.locals import *
import main_game
from puzzle.classes import *
import config
pygame.font.init()
def main():
    WIDTH = 1280
    HEIGHT = 720
    FPS = 60
    #theme colours
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
    #instances of Slider & buttons created
    n_slider = Slider(WIDTH//2-400,500,2,10,start_val=3)
    confirm_button = Button(1060,600,150,50,"Confirm",GREEN,border_radius=4)
    back_button = Button(70,70,150,50,"Back",BROWN,border_radius=4)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Puzzle Selection")
    clock = pygame.time.Clock()
    running = True
    #background rects & fonts
    rect = pygame.rect.Rect(60,60,1160,600)
    border = pygame.rect.Rect(59,59,1162,602)
    font = pygame.font.Font("CrimsonPro-VariableFont_wght.ttf",36)
    smalltext = pygame.font.Font("CrimsonPro-VariableFont_wght.ttf",20)
    def draw_text(text, font, color, surface, x, y):
        #draw text centered at (x,y)
        text_obj = font.render(text, True, color)
        rect = text_obj.get_rect(center=(x, y))
        surface.blit(text_obj, rect)

    while running:
        clock.tick(FPS)
        pygame.display.set_caption("Puzzle Selection")
        pygame.display.update()
        events = pygame.event.get()
        for event in events:
            #main event handling
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if confirm_button.handle_click(pygame.mouse.get_pos()):
                        #if confirm button clicked, start the game
                        main_game.n = n_slider.get_value()
                        main_game.main()
                    elif back_button.handle_click(pygame.mouse.get_pos()):
                        running = False
            keys = pygame.key.get_pressed()
            if keys[K_RETURN]:
                #same for if enter key pressed
                main_game.n = n_slider.get_value()
                main_game.main()
            else: pass
            #handles event if the slider was clicked on or moved
            n_slider.handle_event(event)
        #update slider if anything changed
        n_slider.update()
        screen.fill(background)
        pygame.draw.rect(screen, WHITE, border)
        pygame.draw.rect(screen, box_colour, rect)
        draw_text("Select the size of the board you wish to solve:",font,WHITE,screen,WIDTH//2,100)
        #board visualisation & slider & button& text drawing
        solved_board = Board(n_slider.get_value(),300)
        solved_board.generate_solved()
        solved_board.draw_board(screen,WIDTH//2-(solved_board.width//2),150)
        n_slider.draw(screen)
        confirm_button.create_button(screen,20,WHITE)
        back_button.create_button(screen,20,WHITE)
        draw_text(f"Board size = {n_slider.get_value()}",font,WHITE,screen,WIDTH//2, 550)
if __name__ == "__main__":
    main()
    pygame.quit()
