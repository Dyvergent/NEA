import pygame
from pygame.locals import *
import choose_screen
import tutorial
import history
import leaderboard
import settings
import config
from puzzle.classes import *
pygame.font.init()
def main():
    WIDTH = 1280
    HEIGHT = 720
    FPS = 60
    centerx,centery = WIDTH//2, HEIGHT//2
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Main Menu")
    clock = pygame.time.Clock()
    #main font
    big_font = pygame.font.Font("PlayfairDisplay-VariableFont_wght.ttf",150)
    #theme colours
    all_colours = config.get_all_colours()
    button_width = 150
    button_height = 150
    running = True
    show_confirm = False
    text_BLACK = (0,0,0)
    text_WHITE = (255,255,255)
    def refresh_all_colours():
        global buttons, BLACK, WHITE, BROWN, GREEN, GREY, YELLOW, CYAN, background, box_colour, NAVY, RED
        #reset the theme colours
        all_colours = config.get_all_colours()
        BLACK = all_colours[1]
        WHITE = all_colours[0]
        BROWN = all_colours[2]
        GREEN = all_colours[5]
        GREY = all_colours[4]
        YELLOW = all_colours[8]
        CYAN = all_colours[9]
        background = all_colours[6]
        box_colour = all_colours[7]
        NAVY = all_colours[10]
        RED = all_colours[11]
        buttons = {
            "Leaderboard":Button(centerx-155,centery-280,button_width,button_height,"Leaderboard",CYAN,border_radius=12),
            "History":Button(centerx+5,centery-280,button_width,button_height,"History",GREEN,border_radius=12),
            "Tutorial":Button(centerx-155,centery-120,button_width,button_height,"Tutorial",NAVY,border_radius=12),
            "Settings":Button(centerx-155,centery+40,button_width,button_height,"Settings",CYAN,border_radius=12),
            "Quit Game":Button(centerx+5,centery+40,button_width,button_height,"Quit Game",RED,border_radius=12)
            }
    refresh_all_colours()
    def confirmation_screen():
        #draw translucent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(175)  # 0 = transparent, 255 = opaque
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        #draw box
        box_width, box_height = 640, 360
        box_rect = pygame.Rect((WIDTH - box_width) // 2, (HEIGHT - box_height) // 2, box_width, box_height)
        #draw text
        text_font = pygame.font.Font("CrimsonPro-VariableFont_wght.ttf", 50)
        smalltext = pygame.font.Font("CrimsonPRo-VariableFont_wght.ttf",20)
        draw_text("Are you sure you wish to quit?", text_font, WHITE, screen, WIDTH // 2, HEIGHT // 2 - 200)
        #buttons
        save_button = Button(WIDTH // 2-100, 435, 240, 75, "Save & Quit", GREEN, 255,8)
        quit_button = Button(save_button.coord[0] - 130, 435, 180, 75, "Quit", BROWN, 255,8)
        cancel_button = Button(save_button.coord[0] + 150, 435, 180, 75, "Cancel", GREY, 255,8)
        text_x = quit_button.coord[0] + 175
        quit_button.create_button(screen,30,WHITE)
        cancel_button.create_button(screen,30,WHITE)

        return quit_button, save_button, cancel_button

    def draw_text(text, font, colour, surface, x, y):
        #draw text centered at (x,y)
        text_obj = font.render(text, True, colour)
        rect = text_obj.get_rect(center=(x, y))
        surface.blit(text_obj, rect)

    def draw_arrow(surface, x, y, width, height, color, text="", font=None, text_color=(0,0,0)):
        global triangle,yellow_button
        #rectangle body (about 70% of width)
        body_width = int(width * 0.7)
        yellow_button = Button(x,y,body_width,height,"",YELLOW,border_radius=12)
        yellow_button.create_button(screen,30,BLACK)
        #triangle head
        tip_x = x + width
        mid_y = y + height // 2
        triangle = [
            (x-50 + body_width, y-height//2),       #top of triangle base
            (tip_x+50, mid_y),            #arrow tip
            (x -50+ body_width, y + height*1.5) #bottom of triangle base
        ]
        pygame.draw.polygon(surface, color, triangle)

        #draw text centered in the rectangle body if provided
        if text and font:
            text_obj = font.render(text, True, text_color)
            rect = text_obj.get_rect(center=(x + body_width // 2 +50, y + height // 2))
            surface.blit(text_obj, rect)

    def point_in_triangle(point, tri):
        #uses the 2D cross product to check if the point is within the bounding box of the triangle
        def cross(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
        #check if the 2d cross product of each component is less than 0, if so for all 3 of them then the point is within the triangle
        bool1 = cross(point, tri[0], tri[1]) < 0.0
        bool2 = cross(point, tri[1], tri[2]) < 0.0
        bool3 = cross(point, tri[2], tri[0]) < 0.0

        return ((bool1 == bool2) and (bool2 == bool3))


    while running:
        clock.tick(FPS)
        pygame.display.set_caption("Main Menu")
        if show_confirm:
            #call the confirmation screen
            quit_button, save_button, cancel_button = confirmation_screen()
        pygame.display.flip()
        for event in pygame.event.get():
            #full event handling
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #handle ONLY left click
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if show_confirm:
                        #confirmation screen button handling
                        if quit_button.handle_click(mouse_pos):
                            pygame.quit()
                        elif cancel_button.handle_click(mouse_pos):
                            show_confirm = False
                    else:
                        #main menu button handling
                        if yellow_button.handle_click(mouse_pos) or point_in_triangle(mouse_pos,triangle):
                            choose_screen.main()
                        for btn in buttons.values():
                            if btn.text == "Leaderboard" and btn.handle_click(mouse_pos):
                                leaderboard.main()
                            elif btn.text == "History" and btn.handle_click(mouse_pos):
                                history.main()
                            elif btn.text == "Tutorial" and btn.handle_click(mouse_pos):
                                tutorial.main()
                            elif btn.text == "Settings" and btn.handle_click(mouse_pos):
                                settings.main()
                                refresh_all_colours()
                            elif btn.text == "Quit Game" and btn.handle_click(mouse_pos):
                                show_confirm = True
        screen.fill(background)
        #draw the buttons & text
        for btn in buttons.values():
            btn.create_button(screen,25,text_BLACK,code=1)
        draw_arrow(screen, centerx+5, centery-120, 320, 150, YELLOW, "Play New Game", pygame.font.Font("PlayfairDisplay-VariableFont_wght.ttf", 30), text_BLACK)
        draw_text("fragmentum",big_font,WHITE,screen,WIDTH//2,HEIGHT//2+250)
            
if __name__ == "__main__":
    main()
    pygame.quit()
