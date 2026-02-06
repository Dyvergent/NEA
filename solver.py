import pygame
from pygame.locals import *
import main_game
from puzzle.classes import *
import config
pygame.font.init()
board = None
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
    n_slider = Slider(WIDTH//2-400,500,2,10,start_val=3)
    back_button = Button(70,70,150,50,"Back",BROWN,border_radius=4)
    next_button = Button(WIDTH//2+250,560,60,50,"Next",GREY,border_radius=4)
    prev_button = Button(WIDTH//2-300,560,60,50,"Previous",GREY,border_radius=4)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Solver")
    clock = pygame.time.Clock()
    running = True
    #solve the puzzle
    moves,nodes = board.solve_puzzle()
    #skip the first move since it's just the starting position twice (lazy fix)
    moves,nodes = moves[1:],nodes[1:]
    rect = pygame.rect.Rect(60,60,1160,600)
    border = pygame.rect.Rect(59,59,1162,602)
    font = pygame.font.Font("CrimsonPro-VariableFont_wght.ttf",36)
    smalltext = pygame.font.Font("CrimsonPro-VariableFont_wght.ttf",20)
    temp_board = Board(board.n,400)
    temp_board.generate_board(board.board)
    ind = -1
    check = False
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
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.handle_click(pygame.mouse.get_pos()):
                    running = False
                if next_button.handle_click(pygame.mouse.get_pos()):
                    ind += 1
                    if ind > len(moves)-1: ind = len(moves)-1
                if prev_button.handle_click(pygame.mouse.get_pos()):
                    ind -= 1
                    if ind < -1: ind = -1
        screen.fill(background)
        pygame.draw.rect(screen, WHITE, border)
        pygame.draw.rect(screen, box_colour, rect)
        back_button.create_button(screen,20,WHITE)
        prev_button.create_button(screen,15,WHITE)
        next_button.create_button(screen,15,WHITE)
        draw_text(f"Move {ind+1}/{len(moves)}",font,WHITE,screen,WIDTH//2,580)
        if ind != -1:
            temp_board = nodes[ind]
            temp_board.width = 400
            temp_board.generate_board(nodes[ind].board)
        temp_board.draw_board(screen,WIDTH//2-200,110)
        
if __name__ == "__main__":
    main()
    pygame.quit()

