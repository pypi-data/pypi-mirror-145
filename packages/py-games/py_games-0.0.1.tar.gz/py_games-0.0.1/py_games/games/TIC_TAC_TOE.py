import random

def start_game():
    # Tic Tac Toe

    # 打印方法
    def drawBoard(board):
        # This function prints out the board that it was passed.
        # "board" is a list of 10 strings representing the board (ignore index 0)
        print('   |   |')
        print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
        print('   |   |')
        print('-----------')
        print('   |   |')
        print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
        print('   |   |')
        print('-----------')
        print('   |   |')
        print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
        print('   |   |')

    def inputPlayerLetter():
        # Lets the player type which letter they want to be.
        # Returns a list with the player’s letter as the first item, and the computer's letter as the second.
        letter = ''
        while not (letter == 'X' or letter == 'O'):
            print('Do you want to be X or O?')
            letter = input().upper()

        # the first element in the list is the player’s letter, the second is the computer's letter.
        if letter == 'X':
            return ['X', 'O']
        else:
            return ['O', 'X']

    def whoGoesFirst():
        # Randomly choose the player who goes first.
        if random.randint(0, 1) == 0:
            return 'computer'
        else:
            return 'player'

    def playAgain():
        # This function returns True if the player wants to play again, otherwise it returns False.
        print('Do you want to play again? (yes or no)')
        return input().lower().startswith('y')

    # 下子
    def makeMove(board, letter, move):
        board[move] = letter

    # 判断游戏是否结束
    def isWinner(bo, le):
        # Given a board and a player’s letter, this function returns True if that player has won.
        # We use bo instead of board and le instead of letter so we don’t have to type as much.
        return ((bo[7] == le and bo[8] == le and bo[9] == le) or  # across the top
                (bo[4] == le and bo[5] == le and bo[6] == le) or  # across the middle
                (bo[1] == le and bo[2] == le and bo[3] == le) or  # across the bottom
                (bo[7] == le and bo[4] == le and bo[1] == le) or  # down the left side
                (bo[8] == le and bo[5] == le and bo[2] == le) or  # down the middle
                (bo[9] == le and bo[6] == le and bo[3] == le) or  # down the right side
                (bo[7] == le and bo[5] == le and bo[3] == le) or  # diagonal
                (bo[9] == le and bo[5] == le and bo[1] == le))  # diagonal

    def getBoardCopy(board):
        # Make a duplicate of the board list and return it the duplicate.
        dupeBoard = []

        for i in board:
            dupeBoard.append(i)

        return dupeBoard

    # 验证输入的list值是否为空
    def isSpaceFree(board, move):
        # Return true if the passed move is free on the passed board.
        return board[move] == ' '

    # 返回下子位置
    def getPlayerMove(board):
        # Let the player type in their move.
        move = ' '
        while move not in '1 2 3 4 5 6 7 8 9'.split() or not isSpaceFree(board, int(move)):
            print('What is your next move? (1-9)')
            move = input()
        return int(move)

    # 从这些列表里面随机下
    def chooseRandomMoveFromList(board, movesList):
        # Returns a valid move from the passed list on the passed board.
        # Returns None if there is no valid move.
        possibleMoves = []
        # 获取空子位置list
        for i in movesList:
            if isSpaceFree(board, i):
                possibleMoves.append(i)
                # list不为空，随机选一个
        if len(possibleMoves) != 0:
            return random.choice(possibleMoves)
        else:
            return None

    # 电脑获取下子位置
    def getComputerMove(board, computerLetter):
        # Given a board and the computer's letter, determine where to move and return that move.
        if computerLetter == 'X':
            playerLetter = 'O'
        else:
            playerLetter = 'X'
        # 这个是机器下子的算法
        # Here is our algorithm for our Tic Tac Toe AI:
        # 首先检测我们下一步是否能赢
        # First, check if we can win in the next move
        for i in range(1, 10):
            # copy一份目前的下子画板
            copy = getBoardCopy(board)
            # 如果备份的画板中内容不为空
            if isSpaceFree(copy, i):
                # 下子
                makeMove(copy, computerLetter, i)
                # 如果下这个位置赢就将这个位置返回
                if isWinner(copy, computerLetter):
                    return i
                    # 检测对手下一步是否会赢，会赢的话就堵它
        # Check if the player could win on their next move, and block them.
        for i in range(1, 10):
            copy = getBoardCopy(board)
            if isSpaceFree(copy, i):
                makeMove(copy, playerLetter, i)
                if isWinner(copy, playerLetter):
                    return i

                    # 优先下这些位置（优先占据角落）
        # Try to take one of the corners, if they are free.
        move = chooseRandomMoveFromList(board, [1, 3, 7, 9])
        if move != None:
            return move

        # 夺取中心点
        # Try to take the center, if it is free.
        if isSpaceFree(board, 5):
            return 5

        # 在最后的列表中下子
        # Move on one of the sides.
        return chooseRandomMoveFromList(board, [2, 4, 6, 8])

    def isBoardFull(board):
        # Return True if every space on the board has been taken. Otherwise return False.
        for i in range(1, 10):
            if isSpaceFree(board, i):
                return False
        return True

    print('Welcome to Tic Tac Toe!')

    # 死循环，没有
    while True:
        # Reset the board
        # 重置输出板
        theBoard = [' '] * 10
        # 选棋子
        playerLetter, computerLetter = inputPlayerLetter()
        # 随机产生谁先下
        turn = whoGoesFirst()
        # 打印是谁先下
        print('The ' + turn + ' will go first.')
        # 游戏开始
        gameIsPlaying = True
        while gameIsPlaying:
            # 人先下
            if turn == 'player':
                # Player’s turn.
                # 打印画板
                drawBoard(theBoard)
                # 获取下子位置
                move = getPlayerMove(theBoard)
                # 下子
                makeMove(theBoard, playerLetter, move)
                # 判断游戏是否结束
                if isWinner(theBoard, playerLetter):
                    drawBoard(theBoard)
                    print('Hooray! You have won the game!')
                    # 结束游戏
                    gameIsPlaying = False
                else:
                    # 验证画板是否画满
                    if isBoardFull(theBoard):
                        drawBoard(theBoard)
                        print('The game is a tie!')
                        break
                    else:
                        turn = 'computer'

            else:
                # Computer’s turn.
                # 机器获取下子位置
                move = getComputerMove(theBoard, computerLetter)
                makeMove(theBoard, computerLetter, move)

                if isWinner(theBoard, computerLetter):
                    drawBoard(theBoard)
                    print('The computer has beaten you! You lose.')
                    gameIsPlaying = False
                else:
                    if isBoardFull(theBoard):
                        drawBoard(theBoard)
                        print('The game is a tie!')
                        break
                    else:
                        turn = 'player'
        # 如果不想玩了就跳出循环
        if not playAgain():
            break