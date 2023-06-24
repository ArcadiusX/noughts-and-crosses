board = ["_", "_", "_", 
         "_", "_", "_", #board, underscore means empty
         "_", "_", "_"]
tie = False
win = False
c = ""

def getLegalMoves(testBoard):    
  global legalMoves
  legalMoves = []         #makes a list of all the empty spots
  for n in range (0, 9):
    if testBoard[n] == "_":
      legalMoves.append(n)
    
def makeBoard():  #prints the board
  print ( "\n" + board[0] + " " + board[1] + " " + board[2] + "\n" + board[3] + " " + board[4] + " " + board[5] + "\n" + board[6] + " " + board[7] + " " + board[8])
  
class player:

  def __init__(self, g, s):  #g is human or ai, s is x or o
    self.g = g
    self.s = s
    

  def winning(self):
    global win, c, tie
    #all possible win condtions are: 036, 147, 258, 012, 345, 678, 048, 246 

    for n in range(0, 7, 3):  #checking if winning in columns
      if board[n] != "_" and board[n] == board[n+1] and board[n] == board[n+2]:
        win = True 
        c = board[n]
    for n in range(0, 3): #checking if winning in rows
      if board[n] != "_" and board[n] == board[n+3] and board[n] == board[n+6]:
        win = True
        c = board[n]
    if board[0] != "_" and board[0] == board[4] and board[0] == board[8]: #checking diagonals
      win = True
      c = board[0]
    elif board[2] != "_" and board[2] == board[4] and board[2] == board[6]:
      win = True
      c = board[2]

    elif "_" not in board: #tie condition
      
      tie = True
      win = True


  def xTurn(self): #human playing x
    move = int(input("\nx move: "))
    if move <= 9 and move >=0 and board[move-1] == "_":
      board[move-1] = "x"
    else:
      print ("\ninvalid move")
      self.xTurn()

		
  def oTurn(self): #human playing o
    move = int(input("\no move: "))
    if move <= 9 and move >=0 and board[move-1] == "_":
      board[move-1] = "o"
    else:
      print ("\ninvalid move")
      self.oTurn()

  def doXAi(self): #x as ai
    global board, win, tie
    getLegalMoves(board)
  
    if len(legalMoves) == 9: # always play 0 first turn
      board[0] = "x"
    
    elif len(legalMoves) == 7: #plays either bottom right or top right on the second turn. preferring bottom
      if board[8] == "_":
        board[8] = "x"
      else:
        board[2] = "x"
      
    elif len(legalMoves) == 5:  #on the third turn it checks to see if it can win, and if not it sees how it can block the other player, and if the other player doesn't have two in a row then it plays the top right or bottom left corner
      if board[8] == "x" and board[4] == "_":
        board[4] = "x"
        win = True
      elif board[1] == "_" and board[2] == "x":
        board[1] = "x"
        win = True
      for n in legalMoves:
        if win == False:
          board[n] = "o"
          self.winning()
          board[n] = "_"
          if win == True:
            board[n] = "x"
          win = False 
      getLegalMoves(board)
      if win == False and len(legalMoves) == 5:
        if board[2] == "_":
          board[2] = "x"
        elif board[6] == "_":
          board[6] = "x"
        
    elif len(legalMoves) == 3: #on the fourth turn it prioritizes combinations that can win, and then combinations that block the other player, satisfying every case based on the previous moves
      for n in legalMoves:
        if win == False:
          board[n] = "x"
          self.winning()
          if win == False:
            board[n] = "_"
          else:
            win = True

      if win == False:
        for n in legalMoves:
          if win == False:
            board[n] = "o"
            self.winning()
            board[n] = "_"
            if win == True:
              board[n] = "x"
            win = False
          
    elif len(legalMoves) == 1:
      board[legalMoves[0]] = "x"

  def doOAi(self): #o as ai
    global win, board, tie
    getLegalMoves(board)
  
    if len(legalMoves) == 8: #on the first turn goes on one of the edges
      if board[4] == "_":
        board[4] = "o"
      else:
        board[0] = "o"

    elif len(legalMoves) <= 6: #on all other turns it first sees if it can win, then if it can block, then the middle square, then the first legal move in the legalMove[] list
      global i
      i = len(legalMoves)
      for n in legalMoves:
        if win == False:
          board[n] = "o"
          self.winning()
          if win == False:
            board[n] = "_"
          else:
            win = True
      if win == False:      
        for n in legalMoves:
          if win == False:
            board[n] = "x"
            self.winning()
            board[n] = "_"
            if win == True:
              board[n] = "o"
        win = False     
      getLegalMoves(board)
      if len(legalMoves) == i:
        if board[4] == "_":
          board[4] = "o"  
        else:
          board[legalMoves[0]] = "o"
            
  def move(self): #based on the attributes of the object it does different methods
    if self.g == "h" and self.s == "x":
      self.xTurn()
      
    if self.g == "a" and self.s == "x":
      self.doXAi()
      
    if self.g == "h" and self.s == "o":
      self.oTurn()
      
    if self.g == "a" and self.s == "o":
      self.doOAi()

#gets input from the player for g and s, makes the x and o objects
g = str(input('Type "a" for ai and "h" for human control for x'))
x = player(g, "x")
g = str(input('Type "a" for ai and "h" for human control for o'))
o = player(g, "o")

#game loop, makes the board, moves x, checks if it has won, then if it hasn't won it does the same thing for o, ending when one player has won
while win == False:
  makeBoard()
  x.move()
  x.winning()
  if win == False:
    makeBoard()
    o.move()
    o.winning()

#if it is a tie, then it prints one message, and if isn't, then it says who won
if tie != True:
  makeBoard()
  print("\n" + c + " is the winner!")
else:
  makeBoard()
  print("\nTie!")
