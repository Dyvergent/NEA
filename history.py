import pygame
from pygame.locals import *
from puzzle.classes import *
import main_game
import ast
import json
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
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("History")
    font = pygame.font.Font("CrimsonPro-VariableFont_wght.ttf",15)
    med_font = pygame.font.Font("CrimsonPro-VariableFont_wght.ttf",20)
    big_font = pygame.font.Font("CrimsonPro-VariableFont_wght.ttf",45)
    main_menu_button = Button(80,80,150,50,"Main Menu",BROWN,border_radius=8)
    rect = pygame.rect.Rect(60,60,1160,600)
    border = pygame.rect.Rect(59,59,1162,602)
    clock = pygame.time.Clock()
    #helper for drawing rects
    left,top = 700,71
    spacing = 120
    dates = []
    #helper for deciding which Continue buttons are loaded
    button_drawn = [False,False,False,False,False]
    history_db = Database("History","history.db")
    data = history_db.fetch_data()
    arrow_surface = pygame.Surface((200, 200), pygame.SRCALPHA)
    pygame.draw.line(arrow_surface, WHITE, (20, 100), (120, 100), 10)
    head_points = [(140, 100), (110, 80), (110, 120)]
    pygame.draw.polygon(arrow_surface, WHITE, head_points)
    #helper variables
    count = 0
    avg_time = 0
    total_time = 0
    solved_count = 0
    total_moves = 0
    fastest_time = float("inf")
    game_to_load = None
    for i in range(len(data)):
        x = list(data[i])
        x = x[1:] #skip the id field, we only care about the game data fields
        x[0] = ast.literal_eval(x[0])
        data[i] = tuple(x)  #store back as a tuple for easier indexing

    running = True
    def time_to_seconds(time_str):
        #convert a time string in H:MM:SS.sss format to seconds 
        parts = time_str.split(":")
        if len(parts) == 2:
            minutes, seconds = parts
            return int(minutes) * 60 + float(seconds)
        elif len(parts) == 3:
            hours, minutes, seconds = parts
            return int(hours) * 3600 + int(minutes) * 60 + float(seconds)
        else:
            return float(parts[0])

        
    def format_time(seconds):
        #convert seconds to H:MM:SS.sss format
        if seconds == "None": return "None"
        if seconds is None: return None
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60

        if hours > 0:
            #hours minutes and seconds
            return f"{hours:d}:{minutes:02d}:{secs:06.3f}"
        elif minutes > 0:
            #minutes and seconds
            return f"{minutes:02d}:{secs:06.3f}"
        else:
            #only seconds
            return f"{secs:06.3f}"


    def format_date(date):
        #convert ISO datetime string to separate date and time components DD-MM-YYYY and HH:MM:SS
        date = str(date).split("T")
        date[0] = "-".join(date[0].split("-")[::-1])
        return date[0],date[1].split(".")[0]

    def last_modified(dates):
        #return the index of the most recently modified game based on the list of ISO datetime strings; returns 0 if no valid dates are found
        if dates == []: return int(0)
        most_recent = max(dates)
        return dates.index(most_recent)
    #load stats for displaying
    with open("stats.json","r") as file:
        json_data = json.load(file)
    
    for i in range(5):
        #only consider solved games for stats calculations; ignore unsolved games since their times and move counts may not reflect actual solve performance
        try:
            check = True if data[i][4] == 1 else False
            if check:
                curr_time_seconds = time_to_seconds(data[i][2])
                if curr_time_seconds < fastest_time: fastest_time = curr_time_seconds
                total_time += curr_time_seconds
                solved_count += 1
                total_moves += int(data[i][3])
        except:
            pass  #ignore bad or incomplete entries in history
    #the five buttons to be drawn ONLY if necessary
    buttons_list = [Button(left+290,(top+(120*0)+5)+5,200,80,"Continue game",GREEN, border_radius=12),
                    Button(left+290,(top+(120*1)+5)+5,200,80,"Continue game",GREEN, border_radius=12),
                    Button(left+290,(top+(120*2)+5)+5,200,80,"Continue game",GREEN, border_radius=12),
                    Button(left+290,(top+(120*3)+5)+5,200,80,"Continue game",GREEN, border_radius=12),
                    Button(left+290,(top+(120*4)+5)+5,200,80,"Continue game",GREEN, border_radius=12)]
    if solved_count > 0:
        avg_time = round(total_time / solved_count, 3)
        avg_moves = int(total_moves / solved_count)
    else:
        avg_time = "0.000"
        avg_moves = 0
    #update stats.json with computed values if they exceed existing records
    json_data["total_solves"] = max(json_data["total_solves"], solved_count)
    json_data["average_moves"] = avg_moves
    json_data["average_time"] = avg_time
    json_data["fastest_solve"] = fastest_time
    avg_time_text = big_font.render(f'Average Time: {format_time(float(json_data["average_time"]))}',True, WHITE)
    amount_solved_text = big_font.render(f'Total Solves: {json_data["total_solves"]}',True,WHITE)
    avg_moves_text = big_font.render(f'Average Moves: {json_data["average_moves"]}',True,WHITE)
    fastest_time = None if fastest_time == float("inf") else json_data["fastest_solve"]
    fastest_text = big_font.render(f"Fastest Solve: {format_time(fastest_time)}",True,WHITE)
    json_data["average_time"],json_data["fastest_solve"] = str(json_data["average_time"]),str(json_data["fastest_solve"])
    while running:
        clock.tick(FPS)
        pygame.display.flip()
        for event in pygame.event.get():
            #main event handling
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #handle ONLY left click
                if event.button==1:
                    if main_menu_button.handle_click(pygame.mouse.get_pos()):
                        running = False
                    for i in range(5):
                        #decide on which game to load based on which button was pressed
                        if buttons_list[i].handle_click(pygame.mouse.get_pos()) and button_drawn[i]:
                            game_to_load = i
        screen.fill(background)
        pygame.display.set_caption("History")
        pygame.draw.rect(screen,WHITE,border)
        pygame.draw.rect(screen,box_colour,rect)
        main_menu_button.create_button(screen,20,WHITE)
        history_db = Database("History","history.db")
        data = history_db.fetch_data()
        for i in range(len(data)):
            x = list(data[i])
            x = x[1:]
            x[0] = ast.literal_eval(x[0])
            data[i] = tuple(x)
        #draw each saved game row: board preview, basic stats and last modified time
        for i in range(5):
            try:
                int(data[i][1])
            except:
                continue #ignore invalid or missing rows
            #create and draw rects and board visualisations alongside relevant data
            new_rect = pygame.rect.Rect(left,top+(120*i),500,100)
            new_border = pygame.rect.Rect(left-2,top+(120*i)-2,504,104)
            pygame.draw.rect(screen,WHITE,new_border)
            pygame.draw.rect(screen,box_colour,new_rect)
            new_board = Board(int(data[i][1]),width=90)
            new_board.generate_board(data[i][0])
            new_board.draw_board(screen,left+5,top+(120*i)+5)
            size_text = font.render(f"Board size: {data[i][1]}",True,WHITE)
            time_text = font.render(f"Time: {format_time(round(time_to_seconds(data[i][2]),3))}",True,WHITE)
            moves_text = font.render(f"Moves: {data[i][3]}",True,WHITE)
            check = True if data[i][4] == 1 else False
            solved_text = font.render(f"Solved: {check}",True,WHITE)
            modified_text = font.render(f"Last Modified:",True,WHITE)
            dates.append(data[i][5])
            #display date and time separately
            date_text = font.render(f"{format_date(data[i][5])[0]}",True,WHITE)
            current_time_text = font.render(f"{format_date(data[i][5])[1]}",True,WHITE)
            screen.blit(size_text,(left+105,(top+(120*i)+5)+2))
            screen.blit(time_text,(left+105,(top+(120*i)+5)+24))
            screen.blit(moves_text,(left+105,(top+(120*i)+5+46)))
            screen.blit(solved_text,(left+105,(top+(120*i)+5)+68))
            screen.blit(modified_text,(left+195,(top+(120*i)+5)+2))
            screen.blit(date_text,(left+215,(top+(120*i)+5)+24))
            screen.blit(current_time_text,(left+215,(top+(120*i)+5)+46))
            #if the game isn't marked as solved, show a Continue button to resume it
            if not check:
                continue_button = buttons_list[i]
                continue_button.create_button(screen,20,WHITE)
                button_drawn[i] = True
        #drawing text and most recent save arrow
        screen.blit(amount_solved_text,(150,150))
        screen.blit(avg_moves_text,(150,200))
        screen.blit(avg_time_text,(150,250))
        screen.blit(fastest_text, (150,300))
        most_recent_index = last_modified(dates)
        recent_text = med_font.render("Most Recent Save",True,WHITE)
        screen.blit(recent_text,(left-150,top+(120*most_recent_index)+25))
        screen.blit(arrow_surface,(left-150,top+(120*most_recent_index)-25))
        dates = []
        #load the selected game if Continue button was clicked
        if game_to_load is not None:
            main_game.n = data[game_to_load][1]
            main_game.main(data[game_to_load][0],round(time_to_seconds(data[game_to_load][2]),3),data[game_to_load][3],game_to_load+1)
            game_to_load = None
            
if __name__ == "__main__":
    main()
    pygame.quit()
