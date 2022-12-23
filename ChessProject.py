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

def main():
    testChess()
    testNotations()
    
    movesUCI = ["e2e4","e7e5","d1h5","b8c6","f1c4","g8f6","h5f7"]
    board = game2pgn(movesUCI)
    print(board)

if __name__=="__main__":
    main()
