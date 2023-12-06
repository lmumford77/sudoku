import pygame
import random
from gameBoards import boards

class Board:
    '''Board class handles the majority of the game's logic. It represents the game board and contains all the functions necessary to draw 
    and pre-fill the grid, pencil in temporary guesses, check a guess and insert it into the board if it is correct, redraw a the board when
    a change is made, and more. '''

    def __init__(self, screen):
        '''Initialize the Board.'''
        self.gameBoard = random.choice(boards)
        self.model = self.gameBoard
        self.selected = None
        self.screen = screen
        self.squares = [[Square(screen, self, j*50 + 100, i*50 + 100, self.gameBoard[i][j], i, j) for j in range(9)] for i in range(9)]

    def update_model(self):
        '''Update the model variable based on each of the Squares' values.'''
        self.model = [[self.squares[i][j].value for j in range(9)] for i in range(9)]

    def reset_values(self, model):
        '''Use the model to reset the values for each Square.'''
        for i in range(9):
            for j in range(9):
                self.squares[i][j].set_value(model[i][j])


    def timer(self, seconds):
        '''Given the number of seconds, return a string in the format x:y:z where x is hours, y is minutes and z is seconds elapsed since
        the start of the game.'''
        sec = seconds%60
        min = seconds//60
        hr = min//60
        return str(int(hr)) + ":" + str(int(min)) + ":" + str(int(sec))
        
    def draw_window(self, secondsElapsed, mistakes):
        '''Given secondsElapsed since the start of the game and the number of mistakes made, draw the current game window.'''
        # Make the screen white
        self.screen.fill((255, 255, 255))

        # Header
        font = pygame.font.SysFont(None, 50)
        header = font.render("Lakeyia's Sudoku", True, (255, 192, 203))
        self.screen.blit(header, (175, 50))

        # Solve button
        pygame.draw.ellipse(self.screen, (255, 192, 203), [265, 575, 120, 60])
        pygame.draw.ellipse(self.screen, (0, 0, 0), [265, 575, 120, 60], width=3)
        buttonText = font.render("Solve", True, (0, 0, 0))
        self.screen.blit(buttonText, (280, 590))

        # Timer
        time = self.timer(secondsElapsed)
        font = pygame.font.SysFont(None, 30)
        time_elapsed = font.render(time, True, (0, 0, 0))
        self.screen.blit(time_elapsed, (50, 600))

        # Mistakes count
        incorrectText = font.render(("Incorrect guesses: " + str(mistakes)), True, (0, 0, 0))
        self.screen.blit(incorrectText, (410, 600))

        # Game grid
        pygame.draw.rect(self.screen, (0,0,0), [100, 100, 450, 450], 3)

        # Horizontal lines in the grid
        for i in range(9):
            line_width = 3 if (i+1)%3 == 0 else 1
            pygame.draw.line(self.screen, (0,0,0), [100, (i*50) + 150], [550, (i*50) + 150], line_width)

        # Vertical lines in the grid
        for i in range(9):
            line_width = 3 if (i+1)%3 == 0 else 1
            pygame.draw.line(self.screen, (0,0,0), [(i*50) + 150, 100], [(i*50) + 150, 550], line_width)

        # Fill in known squares and temporary values
        for squareSublist in self.squares: 
            for square in squareSublist:
                if square.value != 0:
                    square.display_value(square.value) 

                if square.temp != 0:
                    square.display_temp() 
                
        # Format the selected square and ensure all others are marked not selected
        if self.selected:
            self.select((self.selected.x, self.selected.y))
                    
        # Display the updated board
        pygame.display.update()
      

    def select(self, square):
        '''Distinguish the selected Square with a pink boarder.'''
        # Reset the black boarder for the previously selected Square
        if self.selected:
            pygame.draw.rect(self.screen, (0, 0, 0), [self.selected.x, self.selected.y, 50, 50], 1)
        
        # x and y coordinates for the selected Square
        x = ((square[0] - 100) // 50) * 50 + 100 
        y = ((square[1] - 100) // 50) * 50 + 100 

        # Do nothing if user selects a location outside of the bounds of the Board
        if x < 100 or x > 500 or y < 100 or y > 500:
            return

        # Ensure only the selected Square has its selected flag set to True. Note this Square as selected in Board as well. 
        for sq in self.squares: 
            for s in sq:
                if s.x == x and s.y == y:
                    Square.selected = True
                    self.selected = s
                    s.selected = True
                else:
                    Square.selected = False

        # Format the selected Square with a pink boarder
        pygame.draw.rect(self.screen, (255, 192, 203), [x, y, 50, 50], 1)

    def find_empty(self):
        '''Return an empty Square on the Board'''
        for section in self.squares:
            for square in section:
                if (square.value == 0):
                    return square
        return None
    
    def is_valid(self, num, pos):
        '''Check if the Board is valid based on the guess. The board is valid if the guess does not have a duplicate in the same
        row, column, or 3x3 grid'''
        row, col = pos

        # Check row
        for i in range(9):
            if (num == self.model[row][i] and i != col):
                return False

        # Check column
        for i in range(9):
            if (num == self.model[i][col] and i != row):
                return False

        # Check 3x3 grid
        # rowSection and columnSection section will help get the first element in the 3x3 grid
        rowSection = row // 3
        columnSection = col // 3
        for i in range(rowSection * 3, rowSection * 3 + 3):
            for j in range(columnSection * 3, columnSection * 3 + 3):
                if (num == self.model[i][j] and (i, j) != pos):
                    return False
        return True
    
    def solve(self):
        ''' Solve the Board using the backtracking recursive method'''
        # Find the first empty Square. If there are none, the Board is solved
        empty = self.find_empty()
        if not empty:
            return True
        
        # Go through each number option and if it is valid, continue on to the next Square. If it reaches a point where the board is not
        # solvable, go back a step and try again.
        for i in range(1, 10): 
            if (self.is_valid(i, (empty.row, empty.col))):
                empty.set_value(i)
                self.update_model()

                if self.solve():
                    return True
            
        empty.set_value(0)
        self.update_model()

        return False
    
    def check_guess(self, square, guess):
        '''Return a boolean that signals whether or not the guess is correct.'''
        # Store the current model so it can be restored later
        tempModel = self.model
     
        # If the guess is valid, set the guess and try to solve the rest of the Board
        if self.is_valid(guess, (square.row, square.col)):
            square.set_value(guess)
            self.update_model()
            
            # If the Board is solveable, return True and reset the model from solved to its original state
            if self.solve():
                self.reset_values(tempModel)
                self.update_model()
                return True
        
        # Otherwise, still reset the model to its original state and return False
        self.reset_values(tempModel)
        self.update_model()
        return False
    
    def solve_and_display(self):
        '''Solve the Board and display all of the Squares' values'''
        self.solve()
        for squareSublist in self.squares: 
            for square in squareSublist:
                square.set_temp(0)
                square.display_value(square.value) 

    def display_game_over(self, userWon):
        '''Display the appropriate message depending on whether the user wins or loses'''
        font = pygame.font.SysFont(None, 150)
        if userWon:
            gameOverText = font.render("Winner!", True, (255, 192, 203))
            self.screen.blit(gameOverText, (130, 270))
        else:
            self.solve_and_display()
            gameOverText = font.render("Game Over", True, (255, 192, 203))
            self.screen.blit(gameOverText, (40, 270))
        pygame.display.update()


class Square:
    '''Square class handles functionality pertaining to a single Square in the game.'''

    def __init__(self, screen, board, x, y, value, row, col):
        '''Initialize the Square.'''
        self.screen = screen
        self.board = board
        self.x = x
        self.y = y
        self.temp = 0
        self.value = value
        self.row = row
        self.col = col
        self.selected = False

    def set_temp(self, num):
        '''Save the Square's temporary value (guess).'''
        self.temp = num

    def set_value(self, num):
        '''Save the Square's value.'''
        self.value = num

    def display_temp(self):
        '''Display the Square's temporary value penciled in grey.'''
        font = pygame.font.SysFont(None, 20)
        num_text = font.render(str(self.temp), True, (128, 128, 128))
        self.screen.blit(num_text, pygame.Vector2(self.x + 40, self.y + 5))

    def display_value(self, num):
        '''Display the Square's value'''
        self.set_value(num)
        self.board.update_model()
        font = pygame.font.SysFont(None, 50)
        num_text = font.render(str(num), True, (0,0,0))
        self.screen.blit(num_text, pygame.Vector2(115 + 50 * self.col, 115 + 50 * self.row))
       
def main():
    '''Game rendering'''
    # Setup
    pygame.init()
    window = pygame.display.set_mode((650, 650))
    board = Board(window)
    board.draw_window(0, 0)
    clock = pygame.time.Clock()
    start_ticks = pygame.time.get_ticks()
    running = True # Is the game window active
    gameOver = False # Is the game over and the user is unable to perform any subsequent actions
    win = False # Has the user successfully completed the game
    key = None # What key has the user clicked
    mistakes = 0 # Number of incorrect guesses made
    
    # Game loop
    while running:
        # Display the appropriate message when the user wins or forfeits (clicks the solve button)
        if gameOver:
            if win:
                board.display_game_over(True)
            else:
                board.display_game_over(False)

        # Run the clock as long as the game is still active
        else:  
            clock.tick(60)  # Limits FPS to 60
            seconds = (pygame.time.get_ticks()-start_ticks)/1000
            board.draw_window(seconds, mistakes) # Make the time update by redrawing the window

        for event in pygame.event.get():
            # Reset the key
            key = None

            # Quit when the user clicks X to close the window. Save the key value when a number on the keyboard is pressed.
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9 
                if event.key == pygame.K_0:
                    key = 0               

                # Set the Square's temporary value if it doesn't have a value and the key pressed is between 1 and 9
                if key != 0 and key != None and board.selected.value == 0:
                    board.selected.set_temp(key)

                # Remove the temporary value if the delete button is pressed
                if event.key == pygame.K_DELETE:
                    board.selected.set_temp(0)

                # Check the guess when the return button is pressed. If it's correct, remove the temporary value and add it instead as
                # its permanent value. If it's not correct, add to the mistakes count.
                if event.key == pygame.K_RETURN and board.selected.temp and board.selected.value == 0:
                    guessStatus = board.check_guess(board.selected, board.selected.temp)
                    if guessStatus:
                        board.selected.display_value(board.selected.temp)
                        board.selected.set_temp(0)
                    else:
                        mistakes = mistakes + 1
                        
            # Save the position of the mouse when clicked. If it's the location of a Square, select that Square.
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                board.select(pos)

                # Solve button is clicked
                if (pos[0] > 265 and pos[0] < 385 and pos[1] > 575 and pos[1] < 635):
                    gameOver = True

            # User wins when the game hasn't already been marked finished (gameOver) and there are no more empty Squares to fill
            if not gameOver and not board.find_empty():
                gameOver = True
                win = True

main()