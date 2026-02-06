import pygame
import time
import ast
from datetime import datetime
from pygame.locals import *
from puzzle.classes import *
import sqlite3
import json
import config
import solver
n = 5
pygame.font.init()
def main(new_board=None,begin_time=None,begin_moves=0,record_id=None):
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
    board = Board(n)
    if new_board is None:
        board.generate_solvable()
    else:
        board.generate_board(new_board)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sliding Puzzle Game")
    clock = pygame.time.Clock()
    history_db = Database("History","history.db")
    leaderboard_db = Database("Leaderboard","leaderboard.db")
    leaderboard_data = leaderboard_db.fetch_data()
    running = True
    solved = False
    game_end = False
    moves = begin_moves
    paused = False
    quit_key = pygame.K_q
    key_down_time = None #how long the key was held for
    hold_duration = 3000 #milliseconds
    show_confirm = False
    game_started = False
    save_board = not any([new_board!=None,begin_time!=None,begin_moves!=0,record_id!=None])
    save_record = False
    check = False
    record_to_append = []
    start_time = None
    end_time = None
    current_datetime = None
    elapsed_time = 0 if begin_time is None else begin_time
    offset_time = 0.0
    pause_start = 0.0
    record_num = record_id
    cool_timer_variable = 0.0
    allowed_keys = [pygame.K_w,pygame.K_a,pygame.K_s,pygame.K_d,pygame.K_UP,pygame.K_LEFT,pygame.K_DOWN,pygame.K_RIGHT]
    font = pygame.font.Font("puzzle/CrimsonPro-VariableFont_wght.ttf", 36)
    solved_text = font.render("PUZZLE SOLVED!", True, GREEN)
    with open("stats.json","r") as file:
        json_data = json.load(file)
    save_json = False
    #create buttons
    button_spacing = 150
    buttons = {
        "pause": Button(700, 600, 80, 50, "Pause", box_colour, 255),
        "solve": Button(700+button_spacing, 600, 80, 50, "Solve", box_colour, 255),
        "save": Button(700+2*button_spacing, 600, 80, 50, "Save", box_colour, 255),
        "quit": Button(700+3*button_spacing, 600, 80, 50, "Quit", box_colour, 255)
    }
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

    def draw_text(text, font, color, surface, x, y):
        #draw text centered at (x,y)
        text_obj = font.render(text, True, color)
        rect = text_obj.get_rect(center=(x, y))
        surface.blit(text_obj, rect)
    
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

    def confirmation_screen():
        #draw translucent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(175)  #0 = transparent, 255 = opaque
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        #draw box
        box_width, box_height = 640, 360
        box_rect = pygame.Rect((WIDTH - box_width) // 2, (HEIGHT - box_height) // 2, box_width, box_height)
        #draw text
        text_font = pygame.font.Font("CrimsonPro-VariableFont_wght.ttf", 50)
        smalltext = pygame.font.Font("CrimsonPro-VariableFont_wght.ttf",20)
        draw_text("Are you sure you wish to quit?", text_font, WHITE, screen, WIDTH // 2, HEIGHT // 2 - 200)
        #buttons
        save_button = Button(WIDTH // 2 - 120, 435, 240, 75, "Save & Quit", GREEN, 255,8)
        quit_button = Button(save_button.coord[0]- 225, 435, 180, 75, "Quit", BROWN, 255,8)
        cancel_button = Button(save_button.coord[0] + 290, 435, 180, 75, "Cancel", GREY, 255,8)
        text_x = quit_button.coord[0] + 175
        draw_text("Quit - Quits the game without saving (NOT recommended as you WILL lose your progress!)", smalltext, WHITE, screen, text_x - 62,quit_button.coord[1]+100)
        draw_text("Save & Quit - Saves your current board state before quitting (Recommended as progress is not lost, great for if you wish to return to the same scramble.)", smalltext, WHITE, screen, text_x + 180,quit_button.coord[1]+125)
        draw_text("Cancel - Cancels and returns to your game (Your timer is automatically paused, so your time is preserved.)", smalltext, WHITE, screen, text_x - 4,quit_button.coord[1]+150)
        #Draw buttons
        quit_button.create_button(screen,30,WHITE)
        save_button.create_button(screen,30,WHITE)
        cancel_button.create_button(screen,30,WHITE)

        return quit_button, save_button, cancel_button

    while running:
        clock.tick(FPS)
        pygame.display.set_caption("Sliding Puzzle Game")
        if show_confirm:
            try:
                if not game_end: buttons["pause"].text = "Resume"
                elif time_elapsed != 0: buttons["pause"].text = "Resume"
            except:
                pass
            quit_button, save_button, cancel_button = confirmation_screen()

        pygame.display.flip()

        for event in pygame.event.get():
            swapped = False
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not show_confirm:
                if event.button == 1 and not game_end:
                    #board clicks
                    if not paused and board.handle_click(pygame.mouse.get_pos(), game_end):
                        swapped = True
                    #button clicks
                    if buttons["pause"].handle_click(pygame.mouse.get_pos()):
                        paused = not paused
                        if paused:
                            buttons["pause"].text = "Resume"
                        else:
                            buttons["pause"].text = "Pause"

                    if buttons["solve"].handle_click(pygame.mouse.get_pos()):
                        if board.n <=5:
                            solver.board = board
                            solver.main()

                    if buttons["save"].handle_click(pygame.mouse.get_pos()):
                        #save current board state
                        save_json = True
                        save_record = True
                            

                    if buttons["quit"].handle_click(pygame.mouse.get_pos()):
                        paused = True
                        show_confirm = True
                elif event.button == 1 and game_end:
                    if buttons["pause"].handle_click(pygame.mouse.get_pos()):
                        print("Game already ended, nothing to pause.")

                    if buttons["solve"].handle_click(pygame.mouse.get_pos()):
                        print("Game already ended, no need to solve.")

                    if buttons["save"].handle_click(pygame.mouse.get_pos()):
                        #save current board state
                        save_json = True
                        save_record = True

                    if buttons["quit"].handle_click(pygame.mouse.get_pos()):
                        show_confirm = True

            elif event.type == pygame.MOUSEBUTTONDOWN and show_confirm:
                if event.button == 1:
                    if quit_button.handle_click(pygame.mouse.get_pos()):
                        running = False
                    elif save_button.handle_click(pygame.mouse.get_pos()):
                        save_json = True
                        save_record = True
                        running = False
                    elif cancel_button.handle_click(pygame.mouse.get_pos()):
                        show_confirm = False



            elif event.type == pygame.KEYDOWN:
                if event.key not in allowed_keys:
                    pass
                else:
                    if not paused and not game_end and board.handle_keypress(event.key,game_end):
                        swapped = True
                if event.key == quit_key:
                    key_down_time = pygame.time.get_ticks()  #record press time

            #if a legal move happened, increment move counter and start timer on first move
            if swapped:
                if moves == begin_moves:
                    game_started = True
                moves += 1
                if board.is_solved():
                    solved = True
                    end_time = time.time()
                    game_end = True
                    final_time_text = font.render(f"Final Time: {format_time(elapsed_time)}", True, GREEN)
                    final_time = elapsed_time

            # Save the current board to the History database when requested
            if save_board:
                if board.n != 2:
                    record_solved = True if game_end else False
                    if record_num is None:
                        current_datetime = datetime.now().isoformat() #returns the current time in YYYY-MM-DDTHH:MM:SS.ssssss
                        history_db.update_db(board.board,board.n,elapsed_time,moves,record_solved,current_datetime)
                        history_db.reduce_to_5()
                        record_num = history_db.lastrowid
                    else:
                        history_db.update_db(board.board,board.n,elapsed_time,moves,record_solved)
                        history_db.drop_record(record_num)
                else:
                    print("Board size too small to save!")
                save_board = False
            

            if save_record:
                if board.n != 2:
                    if game_end:
                        for i in range(len(leaderboard_data)):
                            if int(leaderboard_data[i][-1]) == int(board.n):
                                try:
                                    if elapsed_time < time_to_seconds(leaderboard_data[i][1]):
                                        leaderboard_db.update_record(None,None,board.n,final_time,None)
                                except:
                                        #if the existing record is invalid or missing, just update with the new time without comparing
                                        leaderboard_db.update_record(None,None,board.n,final_time,None)
                                break
                    current_datetime = datetime.now().isoformat()
                    record_solved = game_end
                    if game_end:
                        history_db.update_record(record_num,board.board,board.n,final_time,moves,record_solved,current_datetime)
                    else:
                        history_db.update_record(record_num,board.board,board.n,elapsed_time,moves,record_solved,current_datetime) 
                    save_record = False
                    
            #update stats.json with average moves/time and total solves when a game completes
            if save_json:
                if board.n != 2 and game_end:
                    new_solve = 1 if game_end else 0
                    json_data["average_moves"] = int((json_data["average_moves"]*(json_data["total_solves"])+moves)/(json_data["total_solves"]+new_solve))
                    json_data["average_time"] = round((time_to_seconds(json_data["average_time"])*(json_data["total_solves"])+elapsed_time)/(json_data["total_solves"]+new_solve),3)
                    json_data["total_solves"] += new_solve
                    json_data["average_time"],json_data["fastest_solve"] = str(json_data["average_time"]),str(json_data["fastest_solve"])
                    with open("stats.json","w") as file:
                        json.dump(json_data,file,indent=4)
                save_json = False
                
            if event.type == pygame.KEYUP:
                if event.key == quit_key:
                    key_down_time = None  # reset if released early
            #check if Q is held for 3 seconds to quit without confirmation
            keys = pygame.key.get_pressed()
            if keys[quit_key] and key_down_time is not None:
                elapsed = pygame.time.get_ticks() - key_down_time
                if elapsed >= hold_duration:
                    print("Q was held for 3 seconds! Quitting game...")
                    pygame.quit()
        screen.fill(background)
        # Update elapsed time
        if game_started and not paused:
            elapsed_time += clock.get_time()/1000

        box_rect = pygame.Rect(690,60,550,600)
        box_border = pygame.Rect(688,58,554,604)
        pygame.draw.rect(screen,WHITE,box_border)
        pygame.draw.rect(screen,box_colour,box_rect)

        #buttons
        for btn in buttons.values():
            rect = pygame.Rect(btn.coord[0]-1,btn.coord[1]-1,btn.width+2,btn.height+2)
            pygame.draw.rect(screen,WHITE,rect)
            btn.create_button(screen,25,WHITE)

        board.draw_board(screen,40,60)

        #display move counter
        moves_text = font.render(f"Moves: {moves}", True, WHITE)
        screen.blit(moves_text, (700, 70))
        action_text = font.render(f"Actions:",True, WHITE)
        screen.blit(action_text, (700,450))
        #display stopwatch
        if not solved:
            time_text = font.render(f"Time: {format_time(elapsed_time)}", True, WHITE)
            screen.blit(time_text, (700, 110))
        else:
            screen.blit(solved_text, (700, 110))
            screen.blit(final_time_text, (700, 150))

        #display instructions when game ended
        if game_end:
            r_text = font.render(f"Press R to start a new game.", True, WHITE)
            screen.blit(r_text, (700,190))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                board.generate_solvable()
                solved = False
                moves = 0
                game_end = False
                paused = False
                buttons["pause"].text = "Pause"
                start_time = None
                end_time = None
                begin_moves = 0
                game_started = False
                elapsed_time = 0
                offset_time = 0.0
                pause_start = 0.0


if __name__ == "__main__":
    main()
    
    pygame.quit()
