import cv2
import numpy as np
import chess
import chess.pgn
from datetime import datetime


BOARDROWS = 8
BOARDCOLS = 8
GAMENR = 0

def testChess():
    #Request a new chessboard:
    board = chess.Board() 
    #Printing the chessboard in ascii:
    print(board, end="\n\n")
    #Printing the chessboard in the notebook
    #chess.svg.board(board) #with this you can get the full svg
    print(board)

def testNotations():
    board = chess.Board() #new board

    #UCI notation (from position , to position)
    movesUCI = ["e2e4","e7e5","d1h5","b8c6","f1c4","g8f6","h5f7"]
    #making some moves
    for i,move in enumerate(movesUCI):
        #display both notations of the move
        moveObject=chess.Move.from_uci(move)
        print(f"move {i} in UCI notation : {board.uci(moveObject)}")
        print(f"move {i} in SAN notation : {board.san(moveObject)}")
        #You can push any of the two notations directly with board.push_uci() or board.push_san()
        board.push_uci(move)
        #board.push(chess.Move.from_uci(move)) #chess.Move.from_uci parses a uci string to a Move object that you can push to a board
        #you can undo a move with board.pop()

    # the for loop above does the same as pushing SAN moves individualy:
    # board.push_san("e4")
    # board.push_san("e5")
    # board.push_san("Qh5")
    # board.push_san("Nc6")
    # board.push_san("Bc4")
    # board.push_san("Nf6")
    # board.push_san("Qxf7")
    print(board.is_checkmate())
    #Generate fen
    print(f"This is the fen notation of the current board:\n {board.fen()}", end="\n\n") #fen notation gives you the status of the current board
    print(board)

# converts a game to a pgn notation (in terminal and in a file)
# input is a list of UCI string's that represent the moves in the game
# e.g. movesUCI = ["e2e4","e7e5","d1h5","b8c6","f1c4","g8f6","h5f7"]
# output is the pgn of this game (printed in the terminal and saved to data/chessgame.pgn)
# RETURNS: the final board so that you can display it in the notebook
def game2pgn(movesUCI, event="Chess battle J vs O", location="On the chessboard", date="2023.01.01", white="Jorn", black="Olivier"):
  #Recording a game and writing it to a PGN
  game = chess.pgn.Game()
  game.headers["Event"] = event
  game.headers["Site"] = location
  game.headers["Date"] = date
  game.headers["White"] = white
  game.headers["Black"] = black
  node = game
  for m in movesUCI:
    b= node.board() #get the board of the current GameNode
    move = chess.Move.from_uci(m) #convert UCI notation string to Move object
    #check if move is legal
    if(move not in b.legal_moves):
      print("Illegal move " + b.uci(move))
    #make the move
    node = node.add_main_variation(move)
    
  #saving the result of the main variation in the game headers for the pgn
  finalNode = game.end() #Follows the main variation to the end and returns the last node.
  game.headers["Result"] = finalNode.board().result()

  #genreating the pgn in terminal and file
  print(50*"-")
  print("The pgn genrated of this game:")
  #print pgn to terminal
  print(game)
  print(50*"-")
  #Saving the pgn to a file
  print(game, file=open(f"data/game{GAMENR}.pgn", "w"), end="\n\n")
  return finalNode.board() 

def detectBoard(img):
  template = cv2.imread('data/games/template.jpg')
  h,w,_ = template.shape
  methods = [cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR_NORMED, cv2.TM_SQDIFF_NORMED]
  meth = methods[0] #we chose to use cv2.TM_CCOEFF_NORMED, but other methods work as well

  imgCopy = img.copy()
  res = cv2.matchTemplate(img,template,meth)
  min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
  if meth == cv2.TM_SQDIFF_NORMED:
    top_left = min_loc
  else:
    top_left = max_loc
  print(w)
  print(h) 
  bottom_right = (top_left[0] + w, top_left[1] + h)
  cv2.rectangle(imgCopy,top_left, bottom_right, (0,0,255),4)
  bottom_left = (bottom_right[0]-w, bottom_right[1])
  top_right = (top_left[0] + w, top_left[1])
  print(top_right)
  #draw vertical lines
  for x in range(9):
    startPt = (top_left[0]+x*w//8, top_left[1])
    endPt = (bottom_left[0] +x*w//8, bottom_left[1])
    cv2.line(imgCopy,startPt, endPt, (255,0,2),2)
  #draw horizontal lines
  for y in range(9):
    startPt = (top_left[0], top_left[1]+y*h//8)
    endPt = (top_right[0], top_right[1]+y*h//8)
    cv2.line(imgCopy,startPt, endPt, (0,255,0),2)
  cv2.imshow('input',img)  
  cv2.imshow('image with lines',imgCopy)
  # Waits for a keystroke
  cv2.waitKey(0) 
  #windows dichtdoen na detectie te hebben getoont
  cv2.destroyAllWindows()
  return top_left, w, h

def calcDiff(img, img2, offset, width, height):
  diff = cv2.absdiff(img, img2)
  diffGrid = np.zeros((BOARDROWS,BOARDCOLS),dtype=int)
  first = (0,0,0) #intensity of the change, x, y
  second = (0,0,0)
  for row in range(BOARDROWS):
    y1 = offset[1] + row*height//BOARDROWS
    y2 = y1 + height//BOARDROWS
    for col in range(BOARDCOLS):
      x1 = offset[0] + col*width//BOARDCOLS
      x2 = x1 + width//BOARDCOLS
      intensity = cv2.mean(diff[y1:y2, x1:x2])[0]
      diffGrid[row][col] = intensity
      if intensity > first[0]:
        second = first
        first = (intensity, row, col)
      elif intensity > second[0]:
        second = (intensity, row, col)

  print("diffgrid = \n" + str(diffGrid)) 
  print("first: " + str(first))  
  print("second: " + str(second))    

  cv2.imshow("img",img)
  cv2.imshow("img2",img2)
  cv2.imshow("diff",diff)  
  cv2.waitKey(0) 

  return diffGrid, first, second

def tupleToChessposition(tup):
  col_labels = "abcdefgh"
  col = col_labels[tup[1]]
  row = str(BOARDROWS - tup[0])  
  return col + row

def tupleToChesspiece(tup, board):
  position = tupleToChessposition(tup)
  print("pos: "+ position)
  piece = board.piece_at(chess.parse_square(position))
  print(piece)
  return piece

def main():
  
  # testChess()
  # testNotations()
  # movesUCI = ["e2e4","e7e5","d1h5","b8c6","f1c4","g8f6","h5f7"]
  # board = game2pgn(movesUCI)
  # print(board)

  #gathering game information:
  #select the game you want to process
  gameno = input("Which game do you want to process? [0-2]\n") 
  if gameno not in ["0","1","2"]:
    print("Thats not a legal game number")
    exit()
  GAMENR=int(gameno)
  #player names
  whitePlayer = input("Who is playing white?\n")
  blackPlayer = input("Who is playing black?\n")
  eventName = "Chess battle " + whitePlayer + " vs " + blackPlayer
  #use current date as date of the event
  gameDate=datetime.today().strftime('%Y.%m.%d') #format YYYY.MM.DD

  moveTurn = 0
  movesUCI = []
  board = chess.Board()

  img = cv2.imread(f"data/games/G{GAMENR}_{moveTurn:02d}_small.jpg")
  img2 = cv2.imread(f"data/games/G{GAMENR}_{moveTurn+1:02d}_small.jpg")
  #detect board
  offset, width, height = detectBoard(img)
  while img2 is not None:

    #calc the 2 squares on the board that changed the most from the previous move
    diffGrid, first, second = calcDiff(img, img2, offset, width, height)    

    #intensity of change is no longer needed in the first and second var
    first = first[1:3]
    second = second[1:3]
    #calc which is the FROM position and which is the TO position
    #   check whos turn it is and check what position contains a piece with the same color, this will be the FROM position 
    pieceOnFirst = tupleToChesspiece(first, board)
    
    print("piece: " + str(pieceOnFirst))
    if pieceOnFirst is None:
      print("FROM SECOND TO FIRST")
      move = tupleToChessposition(second) + tupleToChessposition(first)
    elif board.turn == pieceOnFirst.color :
      print("FROM FIRST TO SECOND")
      move = tupleToChessposition(first) + tupleToChessposition(second)
    else:
      print("FROM SECOND TO FIRST")
      move = tupleToChessposition(second) + tupleToChessposition(first)

    #push the move to the board
    if(not(board.is_legal(chess.Move.from_uci(move)))):
      print("last move was not legal " + move)
      break
    board.push_uci(move)
    print(board)
    movesUCI.append(move)
    print("move: " + move)
    if board.is_checkmate():
      print("CHECKMATE")
      cv2.waitKey(0) 
      break
    
    #load next move/image
    moveTurn += 1
    img = img2
    img2 = cv2.imread(f"data/games/G{GAMENR}_{moveTurn+1:02d}_small.jpg")

  game2pgn(movesUCI,event=eventName,white=whitePlayer,black=blackPlayer,date=gameDate)



if __name__=="__main__":
    main()