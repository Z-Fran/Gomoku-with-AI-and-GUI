# Evaluation function class
class evaluation(object):
    def __init__(self,e):
         # Position weights, the center point of the board has a weight of 7, the weight decreases towards the periphery, and the outermost ring is 0
         self.POS = tuple([tuple([(7 - max(abs(i - 7), abs(j - 7))) for i in range(15)]) for j in range(15)])
         self.evaluation_type=e
         # Must-win score
         self.must_win=0
         # Score table, the first element is the score, tuple's 1 represents a move, 0 represents an empty spot
         self.score_line=[]
         # First evaluation method
         if self.evaluation_type==1:
           self.score_line =[(5, (0, 1, 1, 0, 0)),
                      (5, (0, 0, 1, 1, 0)),
                      (20, (0, 1, 0, 1, 1)),
                      (20, (1, 1, 0, 1, 0)),
                      (50, (0, 0, 1, 1, 1)),
                      (50, (1, 1, 1, 0, 0)),
                      (500, (0, 1, 1, 1, 0)),
                      (500, (0, 1, 0, 1, 1, 0)),
                      (500, (0, 1, 1, 0, 1, 0)),
                      (500, (1, 1, 1, 0, 1)),
                      (500, (1, 1, 0, 1, 1)),
                      (500, (1, 0, 1, 1, 1)),
                      (500, (1, 1, 1, 1, 0)),
                      (500, (0, 1, 1, 1, 1)),
                      (5000, (0, 1, 1, 1, 1, 0)),
                      (9999999, (1, 1, 1, 1, 1))]
           self.must_win=9999999
         # Second evaluation method  
         elif self.evaluation_type==2:
             self.score_line =[(1, (0, 0, 0, 1, 1)),
                         (1, (1, 1, 0, 0, 0)),
                         (1, (0, 0, 1, 0, 1)),
                         (1, (1, 0, 1, 0, 0)),
                         (1, (0, 1, 0, 0, 1)),
                         (1, (1, 0, 0, 1, 0)),
                         (1, (1, 0, 0, 0, 1)),
                         (4, (1, 0, 0, 1, 0)),
                         (4, (0, 1, 0, 0, 1)),
                         (4, (0, 1, 0, 1, 0)),
                         (4, (0, 1, 1, 0, 0)),
                         (4, (0, 0, 1, 1, 0)),
                         (10, (0, 1, 0, 1, 1)),
                         (10, (1, 1, 0, 1, 0)),
                         (10, (0, 0, 1, 1, 1)),
                         (10, (1, 1, 1, 0, 0)),
                         (2000, (0, 1, 1, 1, 0)),
                         (2000, (0, 1, 0, 1, 1, 0)),
                         (2000, (0, 1, 1, 0, 1, 0)),
                         (9980, (1, 1, 1, 0, 1)),
                         (9980, (1, 1, 0, 1, 1)),
                         (9980, (1, 0, 1, 1, 1)),
                         (9980, (1, 1, 1, 1, 0)),
                         (9980, (0, 1, 1, 1, 1)),
                         (9990, (0, 1, 1, 1, 1, 0)),
                         (9999, (1, 1, 1, 1, 1))]
             self.must_win=9900
         # The weight ratio of the opponent's score to one's own score. If greater than 1, AI adopts a defensive strategy; if less than 1, AI adopts an offensive strategy
         self.rate = 0.99
         
    # Evaluation function, parameters: board, whether to calculate the score from the AI's perspective     
    def evaluate(self,board,is_ai):
        # Black pieces (player) are represented by 1 in the board list, white pieces (AI) by 2
        BLACK, WHITE = 1, 2
        # list1 stores all white pieces, list2 stores all black pieces
        list1=[]
        list2=[]
        for i in range(15):
            for j in range(15):
                if board[i][j]==BLACK:
                    list2.append((i,j))
                elif board[i][j]==WHITE:
                    list1.append((i,j))
        # Total score = own score - opponent's score * weight           
        sum_score = 0 
        # Initialize own and opponent's piece lists
        if is_ai:
            my_list = list1
            enemy_list = list2
        else:
            my_list = list2
            enemy_list = list1
    
        # Own scoring pattern record table, records the positions of all own scoring patterns
        my_score_all = []
        # Own score
        my_score = 0
        # Traverse own pieces, calculate the score in four directions (north, east, northeast, northwest), and sum the scores
        for pt in my_list:
            my_score += self.cal_score(pt[0], pt[1], 0, 1, enemy_list, my_list, my_score_all)
            my_score += self.cal_score(pt[0], pt[1], 1, 0, enemy_list, my_list, my_score_all)
            my_score += self.cal_score(pt[0], pt[1], 1, 1, enemy_list, my_list, my_score_all)
            my_score += self.cal_score(pt[0], pt[1], -1, 1, enemy_list, my_list, my_score_all)
        # If already won, return own score directly
            if my_score>self.must_win:
                return my_score
        # Opponent's scoring pattern record table, records the positions of all opponent's scoring patterns
        my_enemy_score_all = []
        # Opponent's score
        enemy_score = 0
        # Calculate opponent's score in the same way
        for pt in enemy_list:
            enemy_score += self.cal_score(pt[0], pt[1], 0, 1, my_list, enemy_list, my_enemy_score_all)
            enemy_score += self.cal_score(pt[0], pt[1], 1, 0, my_list, enemy_list, my_enemy_score_all)
            enemy_score += self. cal_score(pt[0], pt[1], 1, 1, my_list, enemy_list, my_enemy_score_all)
            enemy_score += self.cal_score(pt[0], pt[1], -1, 1, my_list, enemy_list, my_enemy_score_all)
        # Calculate total score
        sum_score = my_score - enemy_score*self.rate
        return sum_score
    
    # For the piece (m,n), calculate the best pattern score along the direction vector (x_direct, y_direct)
    def cal_score(self,m, n, x_direct, y_direct, enemy_list, my_list, my_score_all): 
        # Copy score table
        score_line=self.score_line  
        # Bonus for multiple patterns sharing a piece simultaneously
        add_score = 0  
        # Best pattern
        max_score_line = (0, None)
        # If the score for this point and direction has already been calculated, skip
        for item in my_score_all:
            for pt in item[1]:
                if m == pt[0] and n == pt[1] and x_direct == item[2][0] and y_direct == item[2][1]:
                    return 0  
        # Traverse possible scoring situations for this point, offset from -5 to 0 along the direction vector
        for offset in range(-5, 1):
            # pos records the current pattern
            pos = []
            # Examine 6 positions from offset along the direction vector
            for i in range(0, 6):
                # Check if the piece is out of bounds
                if m + (i + offset) * x_direct>=0 and m + (i + offset) * x_direct<15 and n + (i + offset) * y_direct>=0 and n + (i + offset) * y_direct<15:
                    # Use 2 to represent opponent's piece
                    if (m + (i + offset) * x_direct, n + (i + offset) * y_direct) in enemy_list:
                        pos.append(2)
                    # Use 1 to represent own piece
                    elif (m + (i + offset) * x_direct, n + (i + offset) * y_direct) in my_list:
                        pos.append(1)
                    # Use 0 to represent empty
                    else:
                        pos.append(0)
                # Use 2 to represent out-of-bounds position
                else:
                    pos.append(2)
            # Pattern score table, the length of the pattern to be judged may be 5 or 6, record both cases
            tmp_line5 = (pos[0], pos[1], pos[2], pos[3], pos[4])
            tmp_line6 = (pos[0], pos[1], pos[2], pos[3], pos[4], pos[5])
            # Find the best pattern from the score table and record it
            for (score, line) in score_line:
                if tmp_line5 == line or tmp_line6 == line:
                    if score > max_score_line[0]:
                        max_score_line = (score, ((m + (0+offset) * x_direct, n + (0+offset) * y_direct),
                                                    (m + (1+offset) * x_direct, n + (1+offset) * y_direct),
                                                    (m + (2+offset) * x_direct, n + (2+offset) * y_direct),
                                                    (m + (3+offset) * x_direct, n + (3+offset) * y_direct),
                                                    (m + (4+offset) * x_direct, n + (4+offset) * y_direct)), (x_direct, y_direct))
        # Check in the scoring pattern record table if there are cases where two patterns share a piece, if so, add score
        if max_score_line[1] is not None:
            for item in my_score_all:
                for pt1 in item[1]:
                    for pt2 in max_score_line[1]:
                        if pt1 == pt2 and max_score_line[0] >= 50 and item[0] >= 50:
                            add_score += item[0] + max_score_line[0]
            my_score_all.append(max_score_line)
        return add_score + max_score_line[0]

# Minimax search class
class searcher(object):
    # Initialization
    def __init__(self,e):
        self.evaluator = evaluation(e)
        self.board = [[0 for i in range(15)] for j in range(15)]
        self.gameover = 0
        self.overvalue = 0
        self.maxdepth = 4 
    # Determine if there are other pieces around a position    
    def has_neightbor(self,i,j):
        for m in range(-1,2):
            for n in range(-1,2):
                if i+m>=0 and i+m<15 and j+n>=0 and j+n<15 and self.board[i+m][j+n]!=0:
                    return True
        return False
    # Generate possible next moves for the current board situation
    def genmove(self, turn):
        moves = []
        board = self.board
        POSES = self.evaluator.POS
        for i in range(15):
            for j in range(15):
                # If the current position is empty and there are other pieces around    
                if board[i][j] == 0 and self.has_neightbor(i,j):
                    score = POSES[i][j]
                    moves.append((score, i, j))
        moves.sort()
        moves.reverse()
        return moves
    
    # Minimax search
    def __search(self, is_ai, depth, alpha, beta):
        # Black pieces (player) are represented by 1 in the board list, white pieces (AI) by 2
        BLACK, WHITE = 1, 2
        if is_ai:
            turn=WHITE
        else:
            turn=BLACK
        # Initialize score
        score = 0     
        # If depth is zero, evaluate the board and return
        if depth <= 0:
            score = self.evaluator.evaluate(self.board, is_ai)
            return score       
        # Generate next move set
        moves = self.genmove(turn)
        bestmove = None
        # Traverse all current next moves
        for score, row, col in moves:
            # Mark the current move on the board
            # Place a piece on the board
            self.board[row][col] = turn
            # Depth-first search, evaluate the next round, swap alpha and beta and take the negative, return the score
            score = - self.__search(not is_ai, depth - 1, -beta, -alpha)
            # Remove the piece from the board
            self.board[row][col] = 0
            # Calculate the best move score
            # alpha/beta pruning
            if score > alpha:
                alpha = score
                bestmove = (row, col)
                if alpha >= beta:
                    break

        # If it is the first layer, record the best move
        if depth == self.maxdepth and bestmove:
            self.bestmove = bestmove
        # Return the current best score
        return alpha

    # Start searching for the next solution, the first parameter represents whose turn it is (1 is black player, 2 is white AI), the second parameter is the search depth
    def search(self, turn, depth=3):
        # Determine if the board is empty, if so, place a piece in the center
        empty_flag=True
        for i in range(15):
            for j in range(15):
                if self.board[i][j]!=0:
                    empty_flag=False
        if empty_flag:
            row,col=7,7
            score=0
            self.is_first=False
        else:
            self.maxdepth = depth
            self.bestmove = None
            score = self.__search(turn, depth, -0x7fffffff, 0x7fffffff)
            row, col = self.bestmove
        print("Current board situation:", -score, "points")
        return score, row, col