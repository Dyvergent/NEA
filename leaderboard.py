import pygame
import config
from pygame.locals import *
from puzzle.classes import *
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
    left_1,top_1 = 80,65
    left_2 = 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Leaderboard")
    clock = pygame.time.Clock()
    rect = pygame.rect.Rect(60,60,1160,600)
    border = pygame.rect.Rect(59,59,1162,602)
    font = pygame.font.Font("CrimsonPro-VariableFont_wght.ttf",36)
    smalltext = pygame.font.Font("CrimsonPro-VariableFont_wght.ttf",25)
    leaderboard_db = Database("Leaderboard","leaderboard.db")
    data = leaderboard_db.fetch_data()
    for i in range(len(data)):
        x = list(data[i])
        x = x[1:] #skip the id field, we only care about the game data fields
        try:
            x[0] = float(x[0])  #convert time from string to float for easier formatting in the UI
        except:
            pass
        data[i] = tuple(x)  # store back as a tuple for later indexing
    def format_time(seconds):
        #convert seconds to H:MM:SS.sss format
        if seconds == "None": return "None"
        if seconds is None: return None
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        if hours > 0:
            return f"{hours:d}:{minutes:02d}:{secs:06.3f}"
        elif minutes > 0:
            return f"{minutes:02d}:{secs:06.3f}"
        else:
            return f"{secs:06.3f}"
    back_button = Button(70,70,150,50,"Back",BROWN,border_radius=4)
    fastest_text = font.render("Fastest Times (Personal):",True,WHITE)
    running = True
    while running:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.handle_click(pygame.mouse.get_pos()):
                    running = False
        screen.fill(background)
        pygame.draw.rect(screen, WHITE, border)
        pygame.draw.rect(screen, box_colour, rect)
        screen.blit(fastest_text,(WIDTH//2-200,100))
        #left column: example solved boards for odd sizes 3,5,7,9 and their times
        #data is ordered by board size, odd sizes are located at indices 0,2,4,6 -> accessed as 2*i
        for i in range(4):
            new_rect = pygame.rect.Rect(left_1,top_1+(120*(i+1)),500,100)
            new_border = pygame.rect.Rect(left_1-2,top_1+(120*(i+1))-2,504,104)
            pygame.draw.rect(screen,WHITE,new_border)
            pygame.draw.rect(screen,box_colour,new_rect)
            temp_board = Board(3+(2*i),width=90)
            temp_board.generate_solved()  #draw a solved example for clarity
            temp_board.draw_board(screen,left_1+5,top_1+(120*(i+1))+5)
            size_text = smalltext.render(f"Board size: {3+(2*i)}",True,WHITE)
            time_text = smalltext.render(f"Time: {format_time(data[2*i][0])}",True,WHITE)
            screen.blit(size_text,(left_1+105,top_1+(120*(i+1))+15))
            screen.blit(time_text,(left_1+105,top_1+(120*(i+1))+50))    
        #right column: example solved boards for even sizes 4,6,8,10 and their times
        #data is ordered by board size; even sizes are located at indices 1,3,5,7 -> accessed as 1+2*i
        for i in range(4):
            new_rect = pygame.rect.Rect(left_2,top_1+(120*(i+1)),500,100)
            new_border = pygame.rect.Rect(left_2-2,top_1+(120*(i+1))-2,504,104)
            pygame.draw.rect(screen,WHITE,new_border)
            pygame.draw.rect(screen,box_colour,new_rect)
            temp_board = Board(4+(2*i),width=90)
            temp_board.generate_solved()
            temp_board.draw_board(screen,left_2+5,top_1+(120*(i+1))+5)
            size_text = smalltext.render(f"Board size: {4+(2*i)}",True,WHITE)
            time_text = smalltext.render(f"Time: {format_time(data[1+(2*i)][0])}",True,WHITE)
            screen.blit(size_text,(left_2+105,top_1+(120*(i+1))+15))
            screen.blit(time_text,(left_2+105,top_1+(120*(i+1))+50))
        back_button.create_button(screen,20,WHITE)
        
if __name__ == "__main__":
    main()
    pygame.quit()
