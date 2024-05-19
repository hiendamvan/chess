"""
Main driver file.
Handling user input.
Displaying current GameStatus object.
"""
from time import sleep
import pygame as p
import ChessEngine, ChessAI
import sys
from multiprocessing import Process, Queue
#! Đây là đối với board, đối với màn hình thì sẽ là 700, 512 gì đó. 
BOARD_WIDTH = BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQUARE_SIZE = BOARD_HEIGHT // DIMENSION #! 64
MAX_FPS = 15
IMAGES = {}


def loadImages():
    """
    Initialize a global directory of images.
    This will be called exactly once in the main.
    """
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("c:\\Users\\ASUS\\OneDrive\\ML_Scientist\\co_so_tri_tue_nhan_tao\\chess-engine\\chess\\images\\" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)

def main():
    """
    The main driver for our code.
    This will handle user input and updating the graphics.
    """
    p.init()
    #! biến screen khởi tạo màn hình
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    #! clock để thể hiện thời gian chạy (cái này có thể display lên màn hình cho người dùng)
    clock = p.time.Clock()
    #! fill với nền trắng
    screen.fill(p.Color("white"))
    
    game_state = ChessEngine.GameState() #! class gamestate này để làm gì? 
    
    
    valid_moves = game_state.getValidMoves() #! check toàn bộ move để xem cái nào valid
    #print("This is my valid_moves in beginning: "+str(valid_moves)) #! class
    move_made = False  #! biến flag, dùng để xác nhận nước đi được đi
    animate = False  # flag variable for when we should animate a move. #! animate a move là gì?
    loadImages()  # khởi tạo toàn bộ hình ảnh của Quân cờ
    running = True
    beginScreen = True
    square_selected = ()  # no square is selected initially, this will keep track of the last click of the user (tuple(row,col))
    #print("This is my square_selected = (keep track of the last click of the user)"+str(square_selected)) #! nothing
    player_clicks = []  # this will keep track of player clicks (two tuples)
    
    game_over = False
    ai_thinking = False
    move_undone = False
    move_finder_process = None
    move_log_font = p.font.SysFont("Arial", 14, False, False)
    #! 2 biến quyết định chế độ chơi. True là người false là AI
    player_one = True  # if a human is playing white, then this will be True, else False
    player_two = True  # if a hyman is playing white, then this will be True, else False
    
    
    font = p.font.Font('freesansbold.ttf', 32)
 
    # create a text surface object,
    # on which text is drawn on it.
    text = font.render('Welcome to chess game', True, green, blue)
    
    # create a rectangular object for the
    # text surface object
    textRect = text.get_rect()
    
    # set the center of the rectangular object.
    textRect.center = (BOARD_WIDTH // 2, BOARD_HEIGHT // 2)
    #! --------------------------------- phần khởi động 2 màn hình trước khi vào  -------------------------------------------
    while beginScreen:
        for e in p.event.get():
            if e.type == p.QUIT:
                beginScreen = False
            if e.type == p.KEYDOWN:
                if e.key == p.K_SPACE:
                    beginScreen = False
            
        screen.fill(white)
        screen.blit(text, textRect)
        p.display.flip()
    my_second_screen = True
    text = font.render('Instruction to play chess', True, green, blue)
    imp = p.image.load("C:/Users/ASUS/OneDrive/ML_Scientist/co_so_tri_tue_nhan_tao/chess-engine/chess/images/bK.png").convert()
    imp = p.transform.scale(imp,(BOARD_WIDTH,BOARD_HEIGHT))
    while my_second_screen:
        for e in p.event.get():
            if e.type == p.QUIT:
                my_second_screen = False
            if e.type == p.KEYDOWN:
                if e.key == p.K_SPACE:
                    my_second_screen = False
            
        
        screen.blit(imp,(0,0))
        screen.blit(text,textRect)
        p.display.flip()
    #! ----------------------------------------------------------------------------------------------------------------------------
    while running:
        #! biến human_turn để biết có phải là người chơi hay không (chế độ người chơi hay máy chơi)
        if (game_state.trangDiChuyen and player_one == True) or (not game_state.trangDiChuyen and player_two == True):
            human_turn = True
        else:
            human_turn = False
        
        #! display man hinh khoi dong chuong trinh
        
        for e in p.event.get():
            if e.type == p.KEYDOWN:
                #! -------------------------- quyết định chế độ chơi --------------------------------------
                if e.key == p.K_1:
                    #! neu an 1 thi reset game lai
                    game_state = ChessEngine.GameState()
                    valid_moves = game_state.getValidMoves()
                    square_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False
                    game_over = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True
                    #! this will be human vs human
                    player_one = True
                    player_two = True
                elif e.key == p.K_2:
                    #! reset game lai
                    game_state = ChessEngine.GameState()
                    valid_moves = game_state.getValidMoves()
                    square_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False
                    game_over = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True
                    
                    #! human vs machine
                    player_one = True
                    player_two = False
                    
                elif e.key == p.K_3:
                     #! reset game lai
                    game_state = ChessEngine.GameState()
                    valid_moves = game_state.getValidMoves()
                    square_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False
                    game_over = False
                    
                    # move_undone = True
                    player_one = False
                    player_two = False
            #! xong quyết định chế độ chơi ---------------------------------------------------------------
            
            
            
            if e.type == p.QUIT:
                p.quit()
                sys.exit()
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not game_over:
                    #! location lấy vị trí thực của mouse ở trên màn ảnh. Nó không lấy theo ô vuông 
                    #! mà lấy theo tọa độ đã định sẵn
                    location = p.mouse.get_pos()  # (x, y) location of the mouse
                    #print("This is my mouse location: "+str(location)) 
                    
                    #! nhận biết vị trí con trỏ chuột trên board
                    col = location[0] // SQUARE_SIZE #! location / 64 (512 / 64 = 8!)
                    row = location[1] // SQUARE_SIZE
                    #print("This is my row and col: ",(row,col))
                    if square_selected == (row, col) or col >= 8:  # user clicked the same square twice
                        square_selected = ()  # deselect
                        player_clicks = []  # clear clicks
                    else:
                        square_selected = (row, col)
                        #! biến player click này chỉ tồn tại tới len = 2.
                        #! trong quá trình bấm, nếu như tới lượt đen, mà tiếp tục bấm ô trắng, thì sẽ pop
                        #! tọa độ đầu tiên của click ra ngoài
                        player_clicks.append(square_selected)  # append for both 1st and 2nd click
                        #print("This is my current player_clicks: "+str(player_clicks))
                    if len(player_clicks) == 2 and human_turn:  # after 2nd click
                        move = ChessEngine.Move(player_clicks[0], player_clicks[1], game_state.board)
                        #print("This is my piece moved: ",(move.piece_moved))
                        #print("This is my startrow, startcol: ",(move.start_row, move.start_col))
                        #print("This is my endrow, endcol: ",(move.end_row, move.end_col))
                        #print("this is my piece captured: ",move.piece_captured)
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                game_state.makeMove(valid_moves[i])
                                move_made = True
                                animate = True
                                square_selected = ()  # reset user clicks
                                player_clicks = []
                        if not move_made:
                            player_clicks = [square_selected]

            # key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # undo when 'z' is pressed
                    game_state.undoMove()
                    move_made = True
                    animate = False
                    game_over = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True
                if e.key == p.K_r:  # reset the game when 'r' is pressed
                    game_state = ChessEngine.GameState()
                    valid_moves = game_state.getValidMoves()
                    square_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False
                    game_over = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True



        #! AI tìm nước đi
        if not game_over and not human_turn and not move_undone:
            if not ai_thinking:
                ai_thinking = True
                return_queue = Queue()  # used to pass data between threads
                move_finder_process = Process(target=ChessAI.findBestMove, args=(game_state, valid_moves,return_queue))
                
                
                move_finder_process.start()

            if not move_finder_process.is_alive():
                ai_move = return_queue.get()
                if ai_move is None:
                    #! it should never call this!
                    print("RANDOM IS CALLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
                    ai_move = ChessAI.findRandomMove(valid_moves)
                # ai_move = ChessAI.greedySearch(game_state,valid_moves)
                game_state.makeMove(ai_move)
                move_made = True
                animate = True
                ai_thinking = False

        if move_made:
            if animate:
                animateMove(game_state.move_log[-1], screen, game_state.board, clock)
            valid_moves = game_state.getValidMoves()
            move_made = False
            animate = False
            move_undone = False

        drawGameState(screen, game_state, valid_moves, square_selected)

        if not game_over:
            drawMoveLog(screen, game_state, move_log_font)

        if game_state.checkmate:
            game_over = True
            if game_state.trangDiChuyen:
                drawEndGameText(screen, "Black wins by checkmate")
            else:
                drawEndGameText(screen, "White wins by checkmate")

        elif game_state.stalemate:
            game_over = True
            drawEndGameText(screen, "Stalemate")

        clock.tick(MAX_FPS)
        p.display.flip()

    

def drawGameState(screen, game_state, valid_moves, square_selected):
    """
    Responsible for all the graphics within current game state.
    """
    drawBoard(screen)  # draw squares on the board
    highlightSquares(screen, game_state, valid_moves, square_selected)
    drawPieces(screen, game_state.board)  # draw pieces on top of those squares


def drawBoard(screen):
    """
    Draw the squares on the board.
    The top left square is always light.
    """
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[((row + column) % 2)]
            p.draw.rect(screen, color, p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def highlightSquares(screen, game_state, valid_moves, square_selected):
    """
    Highlight square selected and moves for piece selected.
    """
    if (len(game_state.move_log)) > 0:
        last_move = game_state.move_log[-1]
        s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
        s.set_alpha(100)
        s.fill(p.Color('green'))
        screen.blit(s, (last_move.end_col * SQUARE_SIZE, last_move.end_row * SQUARE_SIZE))
    if square_selected != ():
        row, col = square_selected
        if game_state.board[row][col][0] == (
                'w' if game_state.trangDiChuyen else 'b'):  # square_selected is a piece that can be moved
            # highlight selected square
            s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(100)  # transparency value 0 -> transparent, 255 -> opaque
            s.fill(p.Color('blue'))
            screen.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            # highlight moves from that square
            s.fill(p.Color('yellow'))
            for move in valid_moves:
                if move.start_row == row and move.start_col == col:
                    screen.blit(s, (move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE))


def drawPieces(screen, board):
    """
    Draw the pieces on the board using the current game_state.board
    """
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def drawMoveLog(screen, game_state, font):
    """
    Draws the move log.

    """
    move_log_rect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color('black'), move_log_rect)
    move_log = game_state.move_log
    move_texts = []
    for i in range(0, len(move_log), 2):
        move_string = str(i // 2 + 1) + '. ' + str(move_log[i]) + " "
        if i + 1 < len(move_log):
            move_string += str(move_log[i + 1]) + "  "
        move_texts.append(move_string)

    moves_per_row = 3
    padding = 5
    line_spacing = 2
    text_y = padding
    for i in range(0, len(move_texts), moves_per_row):
        text = ""
        for j in range(moves_per_row):
            if i + j < len(move_texts):
                text += move_texts[i + j]

        text_object = font.render(text, True, p.Color('white'))
        text_location = move_log_rect.move(padding, text_y)
        screen.blit(text_object, text_location)
        text_y += text_object.get_height() + line_spacing


def drawEndGameText(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    text_object = font.render(text, False, p.Color("gray"))
    text_location = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - text_object.get_width() / 2,
                                                                 BOARD_HEIGHT / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, False, p.Color('black'))
    screen.blit(text_object, text_location.move(2, 2))


def animateMove(move, screen, board, clock):
    """
    Animating a move
    """
    global colors
    d_row = move.end_row - move.start_row
    d_col = move.end_col - move.start_col
    frames_per_square = 10  # frames to move one square
    frame_count = (abs(d_row) + abs(d_col)) * frames_per_square
    for frame in range(frame_count + 1):
        row, col = (move.start_row + d_row * frame / frame_count, move.start_col + d_col * frame / frame_count)
        drawBoard(screen)
        drawPieces(screen, board)
        # erase the piece moved from its ending square
        color = colors[(move.end_row + move.end_col) % 2]
        end_square = p.Rect(move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        p.draw.rect(screen, color, end_square)
        # draw captured piece onto rectangle
        if move.piece_captured != '--':
            if move.is_totQuaDuong_move:
                totQuaDuong_row = move.end_row + 1 if move.piece_captured[0] == 'b' else move.end_row - 1
                end_square = p.Rect(move.end_col * SQUARE_SIZE, totQuaDuong_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            screen.blit(IMAGES[move.piece_captured], end_square)
        # draw moving piece
        screen.blit(IMAGES[move.piece_moved], p.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        p.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
