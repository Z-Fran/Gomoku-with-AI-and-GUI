#评估函数类
class evaluation(object):
    def __init__(self,e):
         #位置权值，棋盘最中心点权值是7，权值向外围递减，最外圈是0
         self.POS = tuple([tuple([(7 - max(abs(i - 7), abs(j - 7))) for i in range(15)]) for j in range(15)])
         self.evaluation_type=e
         #必胜得分
         self.must_win=0
         #得分表，第一个元素是分数，元组的1代表落子，0代表空子
         self.score_line=[]
         #第一种评估方式
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
         #第二种评估方式  
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
         #对方分数与己方分数权重之比，大于1AI采取防御性策略，小于1AI采取进攻性策略
         self.rate = 0.99
         
    #评估函数，参数意义：棋盘、是否以AI的角度计算分数     
    def evaluate(self,board,is_ai):
        #黑棋（玩家）在棋盘列表中用1表示，白棋（AI）用2表示
        BLACK, WHITE = 1, 2
        #list1中存放所有黑子list2中存放所有白子
        list1=[]
        list2=[]
        for i in range(15):
            for j in range(15):
                if board[i][j]==BLACK:
                    list2.append((i,j))
                elif board[i][j]==WHITE:
                    list1.append((i,j))
        #总分=己方分数-对方分数*权总           
        sum_score = 0 
        #初始化己方和对方的棋子表
        if is_ai:
            my_list = list1
            enemy_list = list2
        else:
            my_list = list2
            enemy_list = list1
    
        #己方得分棋形记录表，记录己方所有得分形状的位置
        my_score_all = []
        #己方分数
        my_score = 0
        #遍历己方棋子，计算该棋子四个方向（正北方向、正东方向、东北方向、西北方向）的得分，并将得分求和
        for pt in my_list:
            my_score += self.cal_score(pt[0], pt[1], 0, 1, enemy_list, my_list, my_score_all)
            my_score += self.cal_score(pt[0], pt[1], 1, 0, enemy_list, my_list, my_score_all)
            my_score += self.cal_score(pt[0], pt[1], 1, 1, enemy_list, my_list, my_score_all)
            my_score += self.cal_score(pt[0], pt[1], -1, 1, enemy_list, my_list, my_score_all)
        #如果当前已经胜利，直接返回己方分数
            if my_score>self.must_win:
                return my_score
        #对方得分棋形记录表，记录己方所有得分形状的位置
        my_enemy_score_all = []
        #对方分数
        enemy_score = 0
        #以相同的方式计算对方分数
        for pt in enemy_list:
            enemy_score += self.cal_score(pt[0], pt[1], 0, 1, my_list, enemy_list, my_enemy_score_all)
            enemy_score += self.cal_score(pt[0], pt[1], 1, 0, my_list, enemy_list, my_enemy_score_all)
            enemy_score += self. cal_score(pt[0], pt[1], 1, 1, my_list, enemy_list, my_enemy_score_all)
            enemy_score += self.cal_score(pt[0], pt[1], -1, 1, my_list, enemy_list, my_enemy_score_all)
        #计算总分
        sum_score = my_score - enemy_score*self.rate
        return sum_score
    
    #对于棋子（m,n）沿着向量（x_direct, y_direct）的方向计算最好棋形的分数
    def cal_score(self,m, n, x_direct, y_direct, enemy_list, my_list, my_score_all): 
        #复制得分表
        score_line=self.score_line  
        #同时多个棋形共用子的加分
        add_score = 0  
        #最好棋形
        max_score_line = (0, None)
        #如果已经计算该点该方向的得分直接跳过
        for item in my_score_all:
            for pt in item[1]:
                if m == pt[0] and n == pt[1] and x_direct == item[2][0] and y_direct == item[2][1]:
                    return 0  
        # 遍历该店可能的得分情况，沿方向向量偏移量从-5到0
        for offset in range(-5, 1):
            #pos记录当前棋形
            pos = []
            #从offset开始沿着方向向量考察6个位置
            for i in range(0, 6):
                #判断棋子是否出界
                if m + (i + offset) * x_direct>=0 and m + (i + offset) * x_direct<15 and n + (i + offset) * y_direct>=0 and n + (i + offset) * y_direct<15:
                    #用2表示对方棋子
                    if (m + (i + offset) * x_direct, n + (i + offset) * y_direct) in enemy_list:
                        pos.append(2)
                    #用1表示己方棋子
                    elif (m + (i + offset) * x_direct, n + (i + offset) * y_direct) in my_list:
                        pos.append(1)
                    #用0表示空白
                    else:
                        pos.append(0)
                #用2表示出界位置
                else:
                    pos.append(2)
            #格局得分表，需要判断的棋形的长度可能是5可能是6，分别记录这两种情况
            tmp_line5 = (pos[0], pos[1], pos[2], pos[3], pos[4])
            tmp_line6 = (pos[0], pos[1], pos[2], pos[3], pos[4], pos[5])
            #从得分表中寻找最好棋形，并记录
            for (score, line) in score_line:
                if tmp_line5 == line or tmp_line6 == line:
                    if score > max_score_line[0]:
                        max_score_line = (score, ((m + (0+offset) * x_direct, n + (0+offset) * y_direct),
                                                    (m + (1+offset) * x_direct, n + (1+offset) * y_direct),
                                                    (m + (2+offset) * x_direct, n + (2+offset) * y_direct),
                                                    (m + (3+offset) * x_direct, n + (3+offset) * y_direct),
                                                    (m + (4+offset) * x_direct, n + (4+offset) * y_direct)), (x_direct, y_direct))
        #从得分棋形记录表中寻找是否存在两个棋形共用子的情况，如果有则加分
        if max_score_line[1] is not None:
            for item in my_score_all:
                for pt1 in item[1]:
                    for pt2 in max_score_line[1]:
                        if pt1 == pt2 and max_score_line[0] >= 50 and item[0] >= 50:
                            add_score += item[0] + max_score_line[0]
            my_score_all.append(max_score_line)
        return add_score + max_score_line[0]

# 极大极小搜索类
class searcher(object):
    # 初始化
    def __init__(self,e):
        self.evaluator = evaluation(e)
        self.board = [[0 for i in range(15)] for j in range(15)]
        self.gameover = 0
        self.overvalue = 0
        self.maxdepth = 4 
    #判断一个位置周围有没有其他棋子    
    def has_neightbor(self,i,j):
        for m in range(-1,2):
            for n in range(-1,2):
                if i+m>=0 and i+m<15 and j+n>=0 and j+n<15 and self.board[i+m][j+n]!=0:
                    return True
        return False
    # 产生当前棋局可能的下一步走法
    def genmove(self, turn):
        moves = []
        board = self.board
        POSES = self.evaluator.POS
        for i in range(15):
            for j in range(15):
                #如果当前位置未落子且该位置位置周围有其他棋子    
                if board[i][j] == 0 and self.has_neightbor(i,j):
                    score = POSES[i][j]
                    moves.append((score, i, j))
        moves.sort()
        moves.reverse()
        return moves
    
    #极大极小搜索
    def __search(self, is_ai, depth, alpha, beta):
        #黑棋（玩家）在棋盘列表中用1表示，白棋（AI）用2表示
        BLACK, WHITE = 1, 2
        if is_ai:
            turn=WHITE
        else:
            turn=BLACK
        #初始化得分
        score = 0     
        # 深度为零则评估棋盘并返回
        if depth <= 0:
            score = self.evaluator.evaluate(self.board, is_ai)
            return score       
        #生成下一步走法集
        moves = self.genmove(turn)
        bestmove = None
        #遍历当前所有下一步走法
        for score, row, col in moves:
            #标记当前走法到棋盘
            #在棋盘上落子
            self.board[row][col] = turn
            #深度优先搜索，进行下一轮的评估，alpha，beta调换取相反数，返回评分
            score = - self.__search(not is_ai, depth - 1, -beta, -alpha)
            #在棋盘上清除落子
            self.board[row][col] = 0
            # 计算最好分值的走法
            # alpha/beta 剪枝
            if score > alpha:
                alpha = score
                bestmove = (row, col)
                if alpha >= beta:
                    break

        #如果是第一层则记录最好的走法
        if depth == self.maxdepth and bestmove:
            self.bestmove = bestmove
        #返回当前最好的分数
        return alpha

    #开始搜索下一步的解，第一个参数代表当前该谁走（1是黑子玩家，2是白子AI），第二个参数是搜索深度(depth)
    def search(self, turn, depth=3):
        #判断棋盘是否为空，如果是直接在棋盘中心落子
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
        print("当前棋势：",-score,"分")
        return score, row, col