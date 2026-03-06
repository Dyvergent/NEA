import pygame
from pygame.locals import *
import json
import config
from puzzle.classes import *
pygame.font.init()
def main():
    WIDTH = 1280
    HEIGHT = 720
    FPS = 60
    font = pygame.font.Font("CrimsonPro-VariableFont_wght.ttf",36)
    text_BLACK = (0,0,0)
    text_WHITE = (255,255,255)
    #theme colours
    def refresh_all_colours():
        global buttons_dict, theme_text, back_button, danger_text, reset_button, BLACK, WHITE, BROWN, GREEN, GREY, YELLOW, CYAN, background, box_colour, NAVY, RED
        #reset the theme colours
        all_colours = config.get_all_colours()
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
        buttons_dict = {
            "Default":Button(250,200,120,50,"Default",NAVY,border_radius=12),
            "Light":Button(250,260,120,50,"Light",WHITE,border_radius=12),
            "Sunset":Button(250,320,120,50,"Sunset",RED,border_radius=12),
            "Nordic":Button(250,380,120,50,"Nordic",CYAN,border_radius=12),
            "Forest":Button(250,440,120,50,"Forest",GREEN,border_radius=12),
            }
        back_button = Button(70,70,150,50,"Back",BROWN,border_radius=4)
        reset_button = Button(820,250,150,50,"Reset Stats",RED,border_radius=4)
        theme_text = font.render("Select your theme:",True,WHITE)
        danger_font = pygame.font.SysFont("Segoe UI Symbol",36)
        danger_text = danger_font.render("⚠︎ DANGER ZONE ⚠︎",True,RED)
    refresh_all_colours()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Settings")
    clock = pygame.time.Clock()
    stats_resetted = {
        "total_solves": 0,
        "average_moves": 0,
        "average_time": "00.000",
        "fastest_solve": "00.000"
    }
    #background rects
    rect = pygame.rect.Rect(60,60,1160,600)
    border = pygame.rect.Rect(59,59,1162,602)
    running = True
    show_confirm = False
    def draw_text(text, font, colour, surface, x, y):
        #draw text centered at (x,y)
        text_obj = font.render(text, True, colour)
        rect = text_obj.get_rect(center=(x, y))
        surface.blit(text_obj, rect)
        
    def confirmation_screen():
        #draw translucent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(175)  #0 = transparent, 255 = opaque
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        #draw text
        text_font = pygame.font.Font("CrimsonPro-VariableFont_wght.ttf", 50)
        smalltext = pygame.font.Font("CrimsonPro-VariableFont_wght.ttf", 20)
        draw_text("Are you sure you wish to reset ALL of your stats?", text_font, WHITE, screen, WIDTH // 2, HEIGHT // 2 - 200)
        #buttons
        reset_stats_button = Button(WIDTH // 2-230, 435, 180, 75, "Reset Stats", BROWN, 255,8)
        cancel_button = Button(WIDTH // 2+50, 435, 180, 75, "Cancel", GREY, 255,8)
        draw_text("This WILL clear ALL all of your statistics, including your leaderboard and history. Proceed with caution.",smalltext,WHITE,screen,500,600)
        reset_stats_button.create_button(screen,30,WHITE)
        cancel_button.create_button(screen,30,WHITE)
        return reset_stats_button, cancel_button
    while running:
        clock.tick(FPS)
        if show_confirm:
            #call the confirmation screen
            reset_stats_button, cancel_button = confirmation_screen()
        pygame.display.flip()
        for event in pygame.event.get():
            #main event handling
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #handle ONLY left click
                if event.button==1:
                    if back_button.handle_click(pygame.mouse.get_pos()):
                        running = False
                    for btn in buttons_dict.values():
                        #handle event if one of the themes was pressed
                        if btn.handle_click(pygame.mouse.get_pos()):
                            #overwrite ind.txt
                            with open("ind.txt","w") as file:
                                for i,key in enumerate(buttons_dict.values()):
                                    if key == btn:
                                        file.write(str(i))
                            refresh_all_colours()
                    if show_confirm:
                        #confirmation screen event handling
                        if reset_stats_button.handle_click(pygame.mouse.get_pos()):
                            history_db = Database("History","history.db")
                            history_db.clear_db()
                            with open("stats.json","w") as file:
                                json.dump(stats_resetted,file)
                            leaderboard_db = Database("Leaderboard","leaderboard.db")
                            leaderboard_db.clear_db()
                            show_confirm = False
                        if cancel_button.handle_click(pygame.mouse.get_pos()):
                            show_confirm = False
                    if reset_button.handle_click(pygame.mouse.get_pos()):
                        #show confirm if reset stats button is clicked
                        show_confirm = True
        screen.fill(background)
        #draw everything
        pygame.draw.rect(screen,WHITE,border)
        pygame.draw.rect(screen,box_colour,rect)
        screen.blit(theme_text,(180,130))
        screen.blit(danger_text,(740,130))
        for btn in buttons_dict.values():
            btn.create_button(screen,20,WHITE) if btn.colour != WHITE else btn.create_button(screen,20,BLACK)
        back_button.create_button(screen,20,WHITE)
        reset_button.create_button(screen,20,WHITE)

if __name__ == "__main__":
    main()
    pygame.quit()
