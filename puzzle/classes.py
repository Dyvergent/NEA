import random
import pygame
import sqlite3
from pathlib import Path
import itertools

class Node:
    def __init__(self, board, blank, parent):
        self.board = board
        self.blank = blank
        self.parent = parent
        
class Board:
    def __init__(self, n, width=600):
        self.n = n
        self.width = width
        self.board = []
        self.start = tuple(cell for row in self.board for cell in row)
        self.goal = tuple(range(1, n*n)) + (0,)
        self.goal_positions = {val: (i // n, i % n) for i, val in enumerate(self.goal)}
        self.tiles = []  #store Tile objects separately
        self.tile_width = self.width // self.n

    def is_solvable(self):
        arr = []
        total = 0
        index = 0
        for x in self.board:
            for k in x:
                if k != 0:
                    arr.append(k)
                else:
                    index = len(self.board) - self.board.index(x)
        for i in range(len(arr)):
            for j in range(i+1, len(arr)):
                if arr[i] > arr[j]:
                    total += 1
        if self.n % 2 == 0:
            return (total + index) % 2 == 1
        else:
            return total % 2 == 0

    def generate_heuristics(self):
        dist = 0
        board_flat = []
        for x in self.board:
            board_flat += x
        #standard Manhattan distance
        for idx, val in enumerate(board_flat):
            if val == 0:
                continue
            x, y = divmod(idx, self.n)
            goal_x = self.goal_positions[val][0]
            goal_y = self.goal_positions[val][1]
            dist += abs(x - goal_x) + abs(y - goal_y)

        linear_conflict = 0
        #linear conflict (rows)
        for i in range(self.n):
            row = [
                self.board[i][j] for j in range(self.n)
                if self.board[i][j] != 0 and self.goal_positions[self.board[i][j]][0] == i
            ]
            for a in range(len(row)):
                for b in range(a + 1, len(row)):
                    if self.goal_positions[row[a]][1] > self.goal_positions[row[b]][1]:
                        linear_conflict += 1

        #linear conflict (columns)
        for j in range(self.n):
            col = [
                self.board[i][j] for i in range(self.n)
                if self.board[i][j] != 0 and self.goal_positions[self.board[i][j]][1] == j
            ]
            for a in range(len(col)):
                for b in range(a + 1, len(col)):
                    if self.goal_positions[col[a]][0] > self.goal_positions[col[b]][0]:
                        linear_conflict += 1

        return dist + 2 * linear_conflict

    def generate_solvable(self):
        #generate random board configurations until we get a solvable one
        while True:
            temp_board = list(range(0, self.n**2))
            random.shuffle(temp_board)
            chunks_size = self.n
            temp2_board = [temp_board[i:i + chunks_size] for i in range(0, len(temp_board), chunks_size)]
            self.board = temp2_board
            if not self.is_solvable():
                self.board = []
            else:
                break
        self.split_image()   #split image into tile_images
        self.create_tiles()  #create Tile objects using those images

    def generate_solved(self):
        temp_board = list(range(1,self.n**2))+[0]
        chunks_size = self.n
        solved_board = [temp_board[i:i + chunks_size] for i in range(0, len(temp_board), chunks_size)]
        self.board = solved_board
        self.split_image()
        self.create_tiles()

    def generate_board(self,board):
        self.board = board
        self.split_image()
        self.create_tiles()
        
    def choose_image(self):
        base_path = Path(__file__).parent.parent / "all_tiles"
        with open("ind.txt","r") as file:
            data = file.readlines()
        index = int(data[0])
        match index:
            case 1:
                image = pygame.image.load(base_path/"tiles1.png")
            case 2:
                image = pygame.image.load(base_path/"tiles2.png")
            case 3:
                image = pygame.image.load(base_path/"tiles3.png")
            case 4:
                image = pygame.image.load(base_path/"tiles4.png")
            case _:
                image = pygame.image.load(base_path/"tiles.png")
        image = pygame.transform.smoothscale(image,(self.width,self.width))
        return image
    
    def split_image(self):
        image = self.choose_image()
        img_width, img_height = image.get_size()
        tile_width = img_width // self.n
        tile_height = img_height // self.n
        self.tile_width = tile_width
        self.tile_images = []

        for row in range(self.n):
            for col in range(self.n):
                if row == self.n - 1 and col == self.n - 1:  #blank tile
                    self.tile_images.append(None)
                    continue
                rect = pygame.Rect(col * tile_width, row * tile_height, tile_width, tile_height)
                tile = image.subsurface(rect).copy()
                self.tile_images.append(tile)


    #create Tile objects for the current board values, assigning the corresponding tile image (None for blank).
    def create_tiles(self):
        self.tiles = []
        for i in range(self.n):
            row_tiles = []
            for j in range(self.n):
                value = self.board[i][j]
                #map numeric tile value to its image (0 means blank -> None)
                image = None if value == 0 else self.tile_images[value - 1]
                tile = Tile(value, i, j, self.tile_width, image)
                row_tiles.append(tile)
            self.tiles.append(row_tiles)

    def find_blank_position(self):
        for i in range(self.n):
            for j in range(self.n): #iterate through the board
                if self.board[i][j] == 0: #if that location is the blank tile, return its location as a tuple
                    return (i, j)
        return None

    def find_tile(self,tile):
        for i in range(self.n):
            for j in range(self.n):
                if self.board[i][j] == tile:
                    return (i, j)
        return None
    def is_adjacent_to_blank(self, row, col):
        blank_row, blank_col = self.find_blank_position()
        #check if positions are adjacent (horizontally or vertically)
        row_diff = abs(row - blank_row)
        col_diff = abs(col - blank_col)
        #if either of row_diff or col_diff equal 1, then the blank is adjacent and the tile at (row,col) can be swapped with the blank tile legally
        return (row_diff == 1 and col_diff == 0) or (row_diff == 0 and col_diff == 1)

    def swap_with_blank(self, row, col):
        #swap the tile at (row, col) with the blank tile if they're adjacent
        if not self.is_adjacent_to_blank(row, col):
            return False

        blank_row, blank_col = self.find_blank_position()

        #swap values in the board
        self.board[row][col], self.board[blank_row][blank_col] = self.board[blank_row][blank_col], self.board[row][col]

        #swap values AND images in self.tiles
        self.tiles[row][col].val, self.tiles[blank_row][blank_col].val = (
            self.tiles[blank_row][blank_col].val,
            self.tiles[row][col].val,
        )
        self.tiles[row][col].image, self.tiles[blank_row][blank_col].image = (
            self.tiles[blank_row][blank_col].image,
            self.tiles[row][col].image,
        )

        return True


    def handle_click(self, mouse_pos,has_game_ended):
        if has_game_ended:
            return "No"
        #handle mouse click on the board
        x, y = mouse_pos
        #take into account the offset of the board, the top leftmost corner is not (0,0) rather (40,60)
        board_left = 40
        board_top = 60
        board_width = self.n * self.tile_width
        board_height = self.n * self.tile_width
        #check if the click is within the bounds of the board
        if (board_left <= x <= board_left + board_width and board_top <= y <= board_top + board_height):
            #calculate which tile was clicked
            col = (x - board_left) // self.tile_width
            row = (y - board_top) // self.tile_width

            #ensure we're within bounds
            if 0 <= row < self.n and 0 <= col < self.n:
                #try to swap with blank tile
                return self.swap_with_blank(row, col)

        return False

    def handle_keypress(self, key, has_game_ended):
        #check if game ended
        if has_game_ended:
            return "No"
        #find blank tile
        blank_row,blank_col = self.find_blank_position()
        #check for the WASD keys or arrow keys (since they should perform the same thing)
        if key == pygame.K_w or key == pygame.K_UP:
            #check if the move to be made is within the bounds of the board (this prevents the blank tile wrapping around the board)
            if 0 <= blank_row-1 < self.n and 0 <= blank_col < self.n:
                return self.swap_with_blank(blank_row-1,blank_col)
        if key == pygame.K_s or key == pygame.K_DOWN:
            if 0 <= blank_row+1 < self.n and 0 <= blank_col < self.n:
                return self.swap_with_blank(blank_row+1,blank_col)
        if key == pygame.K_a or key == pygame.K_LEFT:
            if 0 <= blank_row < self.n and 0 <= blank_col-1 < self.n:
                return self.swap_with_blank(blank_row,blank_col-1)
        if key == pygame.K_d or key == pygame.K_RIGHT:
            if 0 <= blank_row < self.n and 0 <= blank_col+1 < self.n:
                return self.swap_with_blank(blank_row,blank_col+1)
        return False

    def is_solved(self):
        #check if the puzzle is solved
        current_state = tuple(cell for row in self.board for cell in row)
        return current_state == self.goal

    def board_to_tuple(self):
        return tuple(tuple(row) for row in self.board)

    def reconstruct_moves(self,node):
        #reconstruct the sequence of moves from the solved node back to the initial state by following parent pointers.
        moves = []
        nodes = []
        while node.parent is not None:
            px, py = node.parent.blank
            cx, cy = node.blank
            nodes.append(node.parent.board)
            moved_tile = node.parent.board.board[cx][cy]
            moves.append(moved_tile)
            node = node.parent
        return moves[::-1],nodes[::-1]

    def pop_best(self,pq):
        best_cost = float("inf")
        best_index = -1
        for i, (cost, _, _) in enumerate(pq):
            if cost < best_cost:
                best_cost = cost
                best_index = i
        return pq.pop(best_index)
    
    def solve_puzzle(self):
        #initialize counter for tie-breaking in priority queue (ensures FIFO for equal-cost nodes)
        counter = itertools.count()
        #create a copy of the starting board state (for reference)
        start_board = [row[:] for row in self.board]
        #find the initial position of the blank tile
        start_blank = self.find_blank_position()
        #priority queue to store (cost, counter, node) tuples for A* search
        pq = []
        #set to track visited board states and avoid redundant exploration
        visited = set()
        #create a Board object for the starting state
        temp = Board(self.n, self.width)
        temp.board = self.board
        #create the root node of the search tree
        start_node = Node(temp, start_blank, None)
        #add the starting node to the priority queue with its heuristic cost
        pq.append((self.generate_heuristics(), next(counter), start_node))        
        #A* search algorithm: continue until priority queue is empty
        while pq:
            #pop the node with the lowest heuristic cost
            _, _, curr = self.pop_best(pq)
            #check if the current board is the solved state (heuristic==0)
            if curr.board.generate_heuristics() == 0:
                #create a solved node and reconstruct the sequence of moves
                solved = Node(Board(self.n, self.width).generate_solved(), self.goal_positions[0], curr)
                return self.reconstruct_moves(solved)
            #convert the current board to a tuple for O(1) lookup in visited set
            state = curr.board.board_to_tuple()
            #skip this state if we've already explored it
            if state in visited:
                continue
            #mark this state as visited
            visited.add(state)
            #generate all valid neighboring board states
            for child in curr.board.get_neighbours(curr):
                #calculate the heuristic cost (Manhattan distance + linear conflicts) for the child node
                cost = child.board.generate_heuristics()
                #add the child node to the priority queue
                pq.append((cost, next(counter), child))    
        #return None if no solution exists (unsolvable puzzle -should not happen since we only generate solvable boards)
        return None

    def get_neighbours(self,node):
        #generate neighbouring board states by sliding tiles into the blank space. Returns a list of Node objects representing valid moves from the current node.
        neighbours = []
        x, y = node.blank
        size = node.board.n
        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < size and 0 <= ny < size:
                new_board = [row[:] for row in node.board.board]
                new_board[x][y], new_board[nx][ny] = new_board[nx][ny], new_board[x][y]
                temp = Board(size,self.width)
                temp.board = new_board
                neighbours.append(Node(temp, (nx, ny), node))
        return neighbours

    def draw_board(self, screen,x,y):
        #(x,y) is the coordinates of the top leftmost tile
        font = pygame.font.Font("CrimsonPro-VariableFont_wght.ttf", self.tile_width // 2)
        for i in range(self.n):
            for j in range(self.n):
                tile = self.tiles[i][j]
                tile.draw(screen, font, x + (j * self.tile_width), y + (i * self.tile_width))
        
class Tile:
    def __init__(self, value, row, col, size, image=None):
        self.val = value
        self.row = row
        self.col = col
        self.coord = (row, col)
        self.size = size
        self.image = image

    def draw(self, screen, font, x, y):
        rect = pygame.Rect(x, y, self.size, self.size)
        if self.val == 0:  #blank tile
            pygame.draw.rect(screen, (50, 50, 50), rect)
        else:
            if self.image:
                screen.blit(pygame.transform.scale(self.image, (self.size, self.size)), rect)
            else:
                pygame.draw.rect(screen, (255, 255, 255), rect)

        pygame.draw.rect(screen, (5, 21, 36), rect, 2)  #tile border
        if self.val != 0:
            text = font.render(str(self.val), True, (5, 21, 36))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)


class Button:
    def __init__(self, x, y, width, height, text, colour, opacity=255,border_radius=0):
        self.coord = (x, y)
        self.width = width
        self.height = height
        self.text = text
        self.colour = colour
        self.opacity = opacity
        self.border_radius = border_radius
    def create_button(self, screen, font_size, font_colour, code=0):
        if code == 1:
            font = pygame.font.Font("PlayfairDisplay-VariableFont_wght.ttf", font_size)
        else:
            font = pygame.font.Font("CrimsonPro-VariableFont_wght.ttf", font_size)
        #temporary surface with alpha channel
        button_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        #fill with transparent rect (with opacity)
        color_with_alpha = (*self.colour, self.opacity)
        pygame.draw.rect(
            button_surface, 
            color_with_alpha, 
            pygame.Rect(0, 0, self.width, self.height), 
            border_radius=self.border_radius
        )
        #render text
        temp_text = font.render(self.text, True, font_colour)
        temp_text.set_alpha(self.opacity)
        text_rect = temp_text.get_rect(center=(self.width // 2, self.height // 2))
        button_surface.blit(temp_text, text_rect)
        #then just blit the button surface onto the main screen
        screen.blit(button_surface, self.coord)

        
    def handle_click(self,mouse_pos):
        mx,my = mouse_pos
        if (self.coord[0] <= mx <= self.coord[0]+self.width) and (self.coord[1] <= my <= self.coord[1]+self.height):
            return True
        return False

class Slider:
    def __init__(self, x, y, min_val, max_val, width=800, height=5, start_val=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min_val = min_val
        self.max_val = max_val
        self.steps = max_val - min_val
        self.handle_radius = 15
        self.dragging = False
        self.keypressed = False

        #initial value
        if start_val is None:
            self.value = min_val
        else:
            self.value = max(min_val, min(start_val, max_val))

        self.handle_x = self.value_to_position(self.value)

    def value_to_position(self, value):
        #convert a slider value to handle x-position.
        ratio = (value - self.min_val) / self.steps
        return int(self.x + ratio * self.width)

    def position_to_value(self, pos_x):
        #convert x-position to nearest slider value.
        ratio = (pos_x - self.x) / self.width
        value = self.min_val + round(ratio * self.steps)
        return max(self.min_val, min(value, self.max_val))

    def handle_event(self, event):
        #process mouse and keyboard events
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if (mouse_x - self.handle_x) ** 2 + (mouse_y - self.y) ** 2 <= self.handle_radius**2:
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_a, pygame.K_LEFT):
                #move one step left
                if self.value > self.min_val:
                    self.value -= 1
                    self.handle_x = self.value_to_position(self.value)

            elif event.key in (pygame.K_d, pygame.K_RIGHT):
                #move one step right
                if self.value < self.max_val:
                    self.value += 1
                    self.handle_x = self.value_to_position(self.value)
        else:
            return False
        return True

    def update(self):
        #update handle position if dragging
        if self.dragging:
            mouse_x, _ = pygame.mouse.get_pos()
            self.handle_x = max(self.x, min(mouse_x, self.x + self.width))
            self.value = self.position_to_value(self.handle_x)
            self.handle_x = self.value_to_position(self.value)  # snap to step

    def draw(self, surface):
        #draw the bar
        pygame.draw.rect(surface, (200, 200, 200), (self.x, self.y - self.height//2, self.width, self.height))

        #step marks
        for v in range(self.min_val, self.max_val + 1):
            pos_x = self.value_to_position(v)
            pygame.draw.line(surface, (150, 150, 150), (pos_x, self.y - 8), (pos_x, self.y + 8), 2)

        #handle
        pygame.draw.circle(surface, (100, 200, 250), (self.handle_x, self.y), self.handle_radius)

    def get_value(self):
        return self.value

class Database:
    def __init__(self, name, db_name):
        self.name = name
        self.db_name = db_name
        self.lastrowid = None #important later
        self.create_db() #immediately create the database so I don't have to in the main code
            
    def create_db(self):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            if self.db_name == "history.db":
                table_creation = """
                CREATE TABLE IF NOT EXISTS History (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Board_Scramble VARCHAR(255) NOT NULL,
                    Board_Size INTEGER NOT NULL,
                    Time VARCHAR(255) NOT NULL,
                    Moves INTEGER NOT NULL,
                    Solved BIT NOT NULL,
                    Date_Modified VARCHAR(255) NOT NULL
                    );
                    """ #the actual SQL code, creates the table IF AND ONLY IF it does not exist already
                #adding a primary key that auto increments ensures that duplication is not an issue and I will not need to use INSERT OR IGNORE 

            elif self.db_name == "leaderboard.db":
                table_creation = f"""
                CREATE TABLE IF NOT EXISTS Leaderboard (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Time VARCHAR(255) NOT NULL,
                    Board_Size INTEGER NOT NULL
                    );
                    """
            else: pass
            cursor.execute(table_creation)
            connection.commit()
        if self.db_name == "leaderboard.db" and len(self.fetch_data()) < 8: 
            #populate leaderboard with placeholder entries to cover board sizes 3..10
            self.update_db(None,3,"00.000",None)
            self.update_db(None,4,"00.000",None)
            self.update_db(None,5,"00.000",None)
            self.update_db(None,6,"00.000",None)
            self.update_db(None,7,"00.000",None)
            self.update_db(None,8,"00.000",None)
            self.update_db(None,9,"00.000",None)
            self.update_db(None,10,"00.000",None)

    def update_db(self, board_scramble, board_size, time, moves, solved=False,date=None):
        solved = 1 if solved else 0
        board_scramble = str(board_scramble)
        if self.name == "History":
            with sqlite3.connect("history.db") as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO History (Board_Scramble, Board_Size, Time, Moves, Solved, Date_Modified) VALUES (?, ?,?, ?, ?, ?)",(board_scramble, board_size, time, moves, solved, date)
                )
                #using (?,?,?,?) ensures that SQL injection is not possible. The question marks are placeholders which ensure the format is correct, or else it will not insert anything at all
            self.lastrowid = cursor.lastrowid
        else:
            with sqlite3.connect("leaderboard.db") as connection:
                cursor = connection.cursor()
                if time == "00.000": time = "None"
                cursor.execute(
                    "INSERT INTO Leaderboard (Time,Board_Size) VALUES (?,?)",(time,board_size)
                )
            self.lastrowid = cursor.lastrowid
            
    def reduce_to_5(self):
        if self.name == "History":
            with sqlite3.connect(f"history.db") as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT COUNT(*) FROM History")
                row_count = cursor.fetchone()[0]
                #keep only the most recent 5 history records by deleting oldest entries
                while row_count > 5:
                    cursor.execute(
                    "DELETE FROM History WHERE ID IN (SELECT ID FROM History ORDER BY ID ASC LIMIT ?)",(row_count - 5,)
                    )
                    row_count -= 1
                connection.commit()

    def update_record(self, record_id, board_scramble, board_size, time, moves, solved=False,date=None):
        solved = 1 if solved else 0
        board_scramble = str(board_scramble)
        if self.name == "History":
            with sqlite3.connect("history.db") as connection:
                cursor = connection.cursor()
                try:
                    data = self.fetch_data()
                    row_id = data[record_id-1][0]
                except:
                    row_id = record_id
                cursor.execute(
                    """
                    UPDATE History
                    SET Board_Scramble = ?, 
                        Board_Size = ?, 
                        Time = ?, 
                        Moves = ?, 
                        Solved = ?,
                        Date_Modified = ?
                    WHERE ID = ?
                    """,
                    (board_scramble, board_size, round(time,3), moves, solved, date, row_id)
                )
                connection.commit()
        elif self.db_name == "leaderboard.db":
            with sqlite3.connect("leaderboard.db") as connection:
                cursor = connection.cursor()
                if time == "00.000": time = "None"
                cursor.execute(
                    """
                    UPDATE Leaderboard
                    SET Time = ?
                    WHERE Board_Size = ?
                    """,
                    (time,int(board_size))
                    )
                connection.commit()
                
                
    def drop_record(self,record_num):
        #we will only need to drop records from the history database
        with sqlite3.connect("history.db") as connection:
            cursor = connection.cursor()
            data = self.fetch_data()
            row_id = data[record_num-1][0]
            cursor.execute(
                "DELETE FROM History WHERE ID = ?",(row_id,)
                )
            connection.commit()

    def fetch_data(self):
        if self.name == "History":
            #for history, order by ID
            with sqlite3.connect(self.db_name) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM History ORDER BY ID ASC")
                return cursor.fetchall()
        else:
            #for leaderboard, order by board size
            with sqlite3.connect("leaderboard.db") as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM Leaderboard ORDER BY Board_Size ASC")
                return cursor.fetchall()

    def clear_db(self):
        if self.name == "History":
            #for history, just drop the table
            with sqlite3.connect("history.db") as connection:
                cursor = connection.cursor()
                cursor.execute("DROP TABLE History")
                connection.commit()
        elif self.name == "Leaderboard":
            #for leaderboard, just reset all times to "00.000"
            self.update_record(None,None,3,"00.000",None)
            self.update_record(None,None,4,"00.000",None)
            self.update_record(None,None,5,"00.000",None)
            self.update_record(None,None,6,"00.000",None)
            self.update_record(None,None,7,"00.000",None)
            self.update_record(None,None,8,"00.000",None)
            self.update_record(None,None,9,"00.000",None)
            self.update_record(None,None,10,"00.000",None)
            

if __name__ == "__main__":
    a = Board(5)
    a.generate_solvable()
    for row in a.board:
        print(row)
    print(a.goal_positions)
    print(a.generate_heuristics())

