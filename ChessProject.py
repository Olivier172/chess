import cv2
import numpy as np
import chess
import chess.pgn



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
def game2pgn(movesUCI, event="Chess battle J vs O", location="On the chessboard", date="17.12.2022", white="Jorn", black="Olivier"):
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
  print(game, file=open("data/chessgame.pgn", "w"), end="\n\n")
  return finalNode.board() 

def detectBoard(img):

  template = cv2.imread('data/games/template.jpg')

  h,w,_ = template.shape

  imgListOut = list()
  methods = [cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR_NORMED, cv2.TM_SQDIFF_NORMED]


  for meth in methods:
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
    imgListOut.append(imgCopy)

  cv2.imshow('input',img)  
  cv2.imshow('ccoeff',imgListOut[0])
  cv2.imshow('ccorr',imgListOut[1])
  cv2.imshow('sqdiff',imgListOut[2])
  # Waits for a keystroke
  cv2.waitKey(0)  


def processImages():
  #test input inlezen
  #test = cv2.imread("data/chessboard/test_0.png",0 )
  GAMENR = 0
  MOVE = 0
  
  print(f"data/games/G{GAMENR}_{MOVE+1:02d}.jpg")

  img = cv2.imread(f"data/games/G{GAMENR}_{MOVE:02d}.jpg",0)
  img2 = cv2.imread(f"data/games/G{GAMENR}_{MOVE+1:02d}.jpg",0)
  
  #img.resize((400,400))
  #scaled_img = cv2.resize(img, (img.shape[1] // 4, img.shape[0] // 4))
  #scaled_img2 = cv2.resize(img2, (img2.shape[1] // 4, img2.shape[0] // 4))



  diff = cv2.absdiff(img, img2)

  # Specify the size of t
  # he chessboard (8x8)
  chessboard_size = (5, 5)
  #Displays image inside a window
  cv2.imshow('img1',cv2.resize(img, (img.shape[1] // 4, img.shape[0] // 4)) )  
  cv2.imshow('img2',cv2.resize(img2, (img2.shape[1] // 4, img2.shape[0] // 4)))
  cv2.imshow('diff',cv2.resize(diff, (diff.shape[1] // 4, diff.shape[0] // 4)))
  # Waits for a keystroke
  cv2.waitKey(0)  

  #Find the chessboard corners
  thres,thresIm = cv2.threshold(diff,0,255,cv2.THRESH_OTSU)
  ret, corners = cv2.findChessboardCorners(thresIm, chessboard_size)
  print(corners)
  #If the corners were found, draw them on the image
  if ret:
    imgCor = cv2.drawChessboardCorners(diff, chessboard_size, corners, ret)
    #Displays image inside a window
    cv2.imshow('img1',cv2.resize(img, (img.shape[1] // 4, img.shape[0] // 4)) )  
    cv2.imshow('img2',cv2.resize(img2, (img2.shape[1] // 4, img2.shape[0] // 4)))
    cv2.imshow('diff',cv2.resize(diff, (diff.shape[1] // 4, diff.shape[0] // 4)))
    # Waits for a keystroke
    cv2.waitKey(0)  
  else:
    print ("no corners found")



  # # Color-segmentation to get binary mask
  # lwr = np.array([0, 0, 143])
  # upr = np.array([179, 150, 252])
  # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
  # msk = cv2.inRange(hsv, lwr, upr)

  # # Extract chess-board
  # krn = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 30))
  # dlt = cv2.dilate(msk, krn, iterations=5)
  # res = 255 - cv2.bitwise_and(dlt, msk)

  # # Displaying chess-board features
  # res = np.uint8(res)
  # ret, corners = cv2.findChessboardCorners(res, chessboard_size)
  # if ret:
  #     print(corners)
  #     fnl = cv2.drawChessboardCorners(img, chessboard_size, corners, ret)
  #     #lab.grid_imshow([scaled_img, scaled_img2, fnl],bgr2rgb=True)

  # else:
  #     print("No Checkerboard Found")
  #     #Displays image inside a window
  #     cv2.imshow('color image',cv2.resize(img, (img.shape[1] // 4, img.shape[0] // 4)) )  
  #     cv2.imshow('grayscale image',cv2.resize(img2, (img2.shape[1] // 4, img2.shape[0] // 4)))
  #     cv2.imshow('unchanged image',cv2.resize(diff, (diff.shape[1] // 4, diff.shape[0] // 4)))
  #     # Waits for a keystroke
  #     cv2.waitKey(0)  
  #     # Destroys all the windows created
  #     cv2.destroyAllwindows() 


def main():
  testChess()
  testNotations()
  
  movesUCI = ["e2e4","e7e5","d1h5","b8c6","f1c4","g8f6","h5f7"]
  board = game2pgn(movesUCI)
  print(board)
  

  GAMENR = 0
  MOVE = 0
  img = cv2.imread(f"data/games/G{GAMENR}_{MOVE:02d}_small.jpg")
  img2 = cv2.imread(f"data/games/G{GAMENR}_{MOVE+1:02d}_small.jpg")
  detectBoard(img)
  detectBoard(img2)


  # processImages()



if __name__=="__main__":
    main()
