class GameBoard:
    def __init__(self, size):
        self.size = size
        self.num_entries = [0] * size
        self.items = [[0] * size for x in range(size)]
        self.points = [0] * 2
     
    def num_free_positions_in_column(self, column):
        return self.items[column].count(0)
        
    def game_over(self):    
        for i in range(self.size):
            for j in range(self.size):
                if self.items[i][j] != 0:
                    # Check for horizontal win
                    if i + 3 < self.size:
                        if self.items[i][j] == self.items[i+1][j] == self.items[i+2][j] == self.items[i+3][j]:
                            return True
                    # Check for vertical win
                    if j + 3 < self.size:
                        if self.items[i][j] == self.items[i][j+1] == self.items[i][j+2] == self.items[i][j+3]:
                            return True
                    # Check for diagonal win (top-left to bottom-right)
                    if i + 3 < self.size and j + 3 < self.size:
                        if self.items[i][j] == self.items[i+1][j+1] == self.items[i+2][j+2] == self.items[i+3][j+3]:
                            return True
                    # Check for diagonal win (top-right to bottom-left)
                    if i - 3 >= 0 and j + 3 < self.size:
                        if self.items[i][j] == self.items[i-1][j+1] == self.items[i-2][j+2] == self.items[i-3][j+3]:
                            return True
        return False
        
    def display(self):
        for i in range(self.size -1, -1,-1):
            for k in range(self.size):
                if self.items[k][i] == 0:
                    print("_", end=" ")
                elif self.items[k][i] == 1:
                    print("o", end =" ")
                elif self.items[k][i] == 2:
                    print("x", end =" ")
            print("")
        print("-" * (self.size * 2 -1 ))
        
        for number_column in range(self.size):
            print(number_column, end = " ")
        print("")
        
        print(f'Points player 1: {self.points[0]}')
        print(f'Points player 2: {self.points[1]}')
         
    def add(self, column, player):
        if column >= self.size or column < 0:
            print("Invalid column! Please choose a column within the range.")
            return False
        elif self.num_free_positions_in_column(column) == 0:
            return False
        else:
            row = self.num_entries[column]
            if player == 1:
                self.items[column][row] = 1
            elif player == 2:
                self.items[column][row] = 2
            self.num_entries[column] += 1
            self.points[player - 1] += self.num_new_points(column, row, player)
            return True
        
    def num_new_points(self, column, row, player):
        # Checking for a vertical connect-4
        for i in range(row - 3, row + 1):
            if i >= 0:
                try:
                    if self.items[column][i + 1] == player and self.items[column][i] == player and self.items[column][i + 2] == player and self.items[column][i + 3] == player:
                        return 1
                except:
                    pass
        # Checking for a horizontal connect-4
        for i in range(column - 3, column + 1):
            if i >= 0:
                try:
                    if self.items[i][row] == player and  self.items[i + 1][row] == player and self.items[i + 2][row] == player and self.items[i + 3][row] == player:
                        return 1
                except:
                    pass
        # Checking for diagonals
        for i in range(-3, 1):
            if column + i >= 0 and row - i - 3 >= 0:
                try:
                    if  self.items[column + i][row - i] == player and self.items[column + i + 1][row - i - 1] == player and self.items[column + i + 2][row - i - 2] == player and self.items[column + i + 3][row - i - 3] == player:
                        return 1
                except:
                    pass
        for i in range(-3, 1):
            if column + i >= 0 and row + i >= 0:
                try:
                    if self.items[column + i][row + i] == player and self.items[column + i + 1][row + i + 1] == player and self.items[column + i + 2][row + i + 2] == player and self.items[column + i + 3][row + i + 3] == player:
                        return 1
                except:
                    pass
        return 0
        
    def free_slots_as_close_to_middle_as_possible(self):
        mylist = [] 
        size = self.size
        if size % 2 == 0:
            middle = size//2
            for i in range(middle):
                val1 = (size-1)//2 - i 
                val2 = (size-1)//2 + i + 1 
                mylist.append(val1) 
                mylist.append(val2)
        else:
            middle = (size-1)//2
            mylist.append(middle)
            for i in range(1,middle+1):
                val1 = (size-1)//2 - i 
                val2 = (size-1)//2 + i 
                mylist.append(val1) 
                mylist.append(val2)
        for x in range(len(mylist)-1,-1,-1):
            if self.num_free_positions_in_column(mylist[x])==0:
                mylist.pop(x)
        return mylist

    def column_resulting_in_max_points(self, player):
        mylist = []
        for i in range(self.size):
            point1 = self.points[player-1]
            if self.num_free_positions_in_column(i) != 0:
                row = self.items[i].index(0)
                self.add(i, player)
                point2 = self.points[player-1] - point1
                mylist.append([i, point2])
                self.points[player-1] = point1
                self.num_entries[i] -= 1
                self.items[i][row] = 0
                
        maximum  = 0
        maxlist = []
        for index,x in enumerate(mylist):
            item = mylist[index][1]
            if item > maximum:
                maximum = item
        for index,x in enumerate(mylist):
            item = mylist[index][1]
            if item == maximum:
                maxlist.append(mylist[index])
                
        middle_list = self.free_slots_as_close_to_middle_as_possible()
        if len(middle_list) > 0:
            for index in range(len(middle_list)):
                for x in range(len(maxlist)):
                    if middle_list[index] == maxlist[x][0]:
                        return tuple(maxlist[x])
        else:
            return [],

class FourInARow:
    def __init__(self, size):
        self.board=GameBoard(size)
    def play(self):
        while True:  # Keep playing until exited
            print("==========================================")
            print("               | CONNECT 4 |")
            print("==========================================")
            print("")
            print("*****************NEW GAME*****************")
            self.board.display()
            player_number=0
            print()
            while not self.board.game_over():
                print("Player ", player_number+1, ": ")
                if player_number==0:
                    valid_input = False
                    while not valid_input:
                        try:
                            column = int(input("Please input slot: "))       
                        except ValueError:
                            print("Input must be an integer in the range 0 to ", self.board.size)
                        else:
                            if column<0 or column>=self.board.size:
                                print("Input must be an integer in the range 0 to ", self.board.size)
                            else:
                                if self.board.add(column, player_number+1):
                                    valid_input = True
                                else:
                                    print("________________________________________________________________")
                                    print("Column ", column, "is already full. Please choose another one.")
                else:
                    # Choose move which maximizes new points for computer player
                    (best_column, max_points) = self.board.column_resulting_in_max_points(2)
                    if max_points>0:
                        column=best_column
                    else:
                        # If no move adds new points, choose move which minimizes points opponent player gets
                        (best_column, max_points) = self.board.column_resulting_in_max_points(1)
                        if max_points>0:
                            column=best_column
                        else:
                            # If no opponent move creates new points, then choose column as close to middle as possible
                            column = self.board.free_slots_as_close_to_middle_as_possible()[0]
                    self.board.add(column, player_number+1)
                    print("The AI chooses column ", column)
                self.board.display()   
                player_number=(player_number+1)%2

            if (self.board.points[0] > self.board.points[1]):
                print("Player 1 (circles) wins!")
            elif (self.board.points[0] < self.board.points[1]):    
                print("Player 2 (crosses) wins!")
            else:  
                print("It's a draw!")
                
            # Ask if players want to play again
            play_again = input("Do you want to play again? (yes/no): ").strip().lower()
            if play_again != "yes":
                print("Thanks for playing!")
                break  # Exit the loop if players don't want to play again
            else:
                # Reset the game board
                self.board = GameBoard(self.board.size)
            
game = FourInARow(6)
game.play()        
