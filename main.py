import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication,QStyleFactory,QWidget,QLabel,QComboBox,QPushButton
from PyQt5.QtCore import Qt,QRect
from PyQt5.QtGui import QPixmap, QIcon,QPainter, QPen
from AI import searcher

"""
AI线程
"""
class AI(QtCore.QThread):
    finishSignal = QtCore.pyqtSignal(float, int, int)
    def __init__(self, board, parent=None):
        super(AI, self).__init__(parent)
        self.board = board
    def run(self):
        self.ai = searcher(1)
        self.ai.board = self.board
        score, x, y = self.ai.search(2, 2)#调用极小极大值搜索算法
        self.finishSignal.emit(score, x, y)

"""
为实现标记最后一步棋子定义的类
"""
class BoardLabel(QLabel):
    def __init__(self, parent=None):
        super(BoardLabel,self).__init__(parent)
        self.isShow = False
        self.x = 0
        self.y = 0 
    def paintEvent(self, event):
        super().paintEvent(event)
        qp = QPainter()
        if self.isShow:
            #在最后一颗棋子位置画一个圆
            qp.begin(self)
            pen = QPen(Qt.yellow, 8, Qt.SolidLine)
            qp.setPen(pen)
            rect = QRect(self.x-30,self.y-10,36,36)
            qp.drawArc(rect,0,360*16)
            qp.end()
        self.update()
       
"""
主窗口类
"""
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        #设置窗口相关属性
        QApplication.setStyle(QStyleFactory.create("Fusion"))
        self.setWindowTitle("五子棋") 
        self.setWindowIcon(QIcon('img/black.png'))
        self.resize(600, 900)
        self.setMinimumSize(QtCore.QSize(600, 900))
        self.setMaximumSize(QtCore.QSize(600, 900))
        #背景和棋盘图片
        self.Back = QLabel(self)
        self.Back.setGeometry(QRect(0, 0, 600, 900))
        self.Back.setPixmap(QPixmap('img/back.jpg'))
        self.Back.setScaledContents(True)
        self.Board = BoardLabel(self)
        self.Board.setGeometry(QRect(30, 10, 540, 540))
        self.Board.setPixmap(QPixmap('img/board.jpg')) 
        self.Board.setScaledContents(True)
        self.Black = QPixmap('img/black.png')
        self.White = QPixmap('img/white.png')
        #设置提示信息
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(16)
        self.label_1 = QLabel(self)
        self.label_1.setFont(font)
        self.label_1.setAlignment(Qt.AlignCenter)
        self.label_1.setGeometry(QRect(0,670,150,50))
        self.label_1.setText("玩家(黑)")
        self.label_2 = QLabel(self)
        self.label_2.setFont(font)
        self.label_2.setGeometry(QRect(490,700,150,50))
        self.label_2.setText("AI(白)")
        self.label_3 = QLabel(self)
        self.label_3.setFont(font)
        self.label_3.setGeometry(QRect(150,570,150,50))
        self.label_3.setText("轮到黑棋...")
        self.label_4 = QLabel(self)
        self.label_4.setFont(font)
        self.label_4.setGeometry(QRect(300,570,300,50))
        self.label_4.setText("棋势评估:")
        self.opt = QComboBox(self)
        self.opt.setGeometry(QtCore.QRect(270, 840, 60, 40))
        self.opt.addItem("黑先")
        self.opt.addItem("白先")
        #按钮
        self.reset = QPushButton(self)
        self.reset.setGeometry(QtCore.QRect(50, 840, 200, 40))
        self.reset.setText("重新开始")
        self.retract = QPushButton(self)
        self.retract.setGeometry(QRect(350, 840, 200, 40))
        self.retract.setText("悔棋")
        QtCore.QMetaObject.connectSlotsByName(self)
        self.reset.clicked.connect(self.Reset) 
        self.retract.clicked.connect(self.Retract)
        #在鼠标位置显示将要下的棋子
        self.MouseFocus = QLabel(self)  # 将鼠标图片改为棋子      
        self.MouseFocus.setPixmap(self.Black)  # 加载黑棋
        self.MouseFocus.setGeometry(0, 0, 36, 36)
        self.MouseFocus.setScaledContents(True)
        self.MouseFocus.raise_()  # 鼠标始终在最上层
        #用于追踪鼠标的最上层图层    
        self.Trace = QLabel(self)
        self.Trace.setGeometry(QRect(30, 10, 540, 540))
        self.Trace.setMouseTracking(True)
        self.Back.setMouseTracking(True)
        self.Board.setMouseTracking(True)
        self.setMouseTracking(True)
       
        #初始化棋盘和棋子
        self.board = []
        self.chess = []
        self.direction = [[(-1, 0), (1, 0)], [(0, -1), (0, 1)], [(-1, 1), (1, -1)], [(-1, -1), (1, 1)]]
        self.InitBoard()
        self.AI_finish = True #表示AI下完玩家才可以下
        self.isRun = True #表示游戏正在进行
        self.steps = [] #存放每步下棋的位置用于悔棋
        self.show()
    
    
    """
    参数：无
    功能：初始化棋盘
    """ 
    def InitBoard(self):  # 重置
        self.board = []
        for i in range(15):
            a=[]
            for j in range(15):
                a.append(0)
            self.board.append(a)
        if not len(self.chess):
            for i in range(15):
                b=[]
                for j in range(15):
                    b.append(QLabel(self))
                self.chess.append(b)
        for i in range(15):
            for j in range(15):
                x,y = self.ChessToMouse(i,j)
                self.chess[i][j].setVisible(False)
                self.chess[i][j].setScaledContents(True)
                self.chess[i][j].setGeometry(x, y, 36, 36)
                self.chess[i][j].setPixmap(QPixmap('img/none.jpg'))
    
    """
    参数：无
    功能：悔棋
    """
    def Retract(self):
        if self.AI_finish and len(self.steps)>1:
            #删去steps记录的最后两步
            i1,j1=self.steps[-1][0],self.steps[-1][1]
            i2,j2=self.steps[-2][0],self.steps[-2][1]
            self.board[i1][j1] = 0
            self.board[i2][j2] = 0
            self.chess[i1][j1].setPixmap(QPixmap('img/none.jpg'))
            self.chess[i2][j2].setPixmap(QPixmap('img/none.jpg'))
            del self.steps[-1]
            del self.steps[-1]
            if len(self.steps)>0:
                self.Board.isShow = True
                self.Board.x,self.Board.y = self.ChessToMouse(self.steps[-1][0],self.steps[-1][1])
        if (not self.AI_finish) or len(self.steps)<1:
            self.Board.isShow = False
    
    """
    参数：无
    功能：重新开始
    """
    def Reset(self):
        self.label_4.setText("棋势评估:")
        self.label_3.setText("轮到黑棋...")
        self.InitBoard()
        self.AI_finish = True
        self.isRun = True
        self.Board.isShow = False
        self.steps = []
        if self.opt.currentText()=="白先":
            self.AI_finish = False  
            self.label_3.setText("轮到白棋...")
            #调用AI线程
            self.AI = AI(self.board)
            self.AI.finishSignal.connect(self.AI_turn)
            self.AI.start()
                
    """
    参数：无
    功能：重写鼠标移动事件
    """    
    def mouseMoveEvent(self, e):  # 黑色棋子随鼠标移动
        if e.x()>30 and e.x()<570 and e.y()>10 and e.y()<550:
            self.MouseFocus.move(e.x() - 18, e.y() - 18) 
            self.MouseFocus.setPixmap(self.Black)  # 加载黑棋
        else:
            self.MouseFocus.setPixmap(QPixmap('img/none.jpg'))           
    """
    参数：无
    功能：重写鼠标按压事件
    """  
    def mousePressEvent(self, e):  # 玩家下棋
        """
        AI对战
        """ 
        """
        if e.button() == Qt.LeftButton and self.AI_finish and self.isRun:
            self.AI2 = searcher(2)
            self.AI2.board = self.board
            score,i,j = self.AI2.search(2,2)
            self.chess[i][j].setPixmap(self.Black) #设置chess对应位置为黑棋
            self.chess[i][j].setVisible(True)
            self.board[i][j] = 1#设置chess对应位置为1
            self.steps.append((i,j))#记录此步行棋
            self.Board.isShow = True
            self.Board.x,self.Board.y = self.ChessToMouse(self.steps[-1][0],self.steps[-1][1])
            if self.CheckWin(i,j):
                self.isRun = False
                return                 
            self.AI_finish = False  
            self.label_3.setText("轮到白棋...")
            #调用AI线程
            self.AI = AI(self.board)
            self.AI.finishSignal.connect(self.AI_turn)
            self.AI.start()
        """
        
        if e.button() == Qt.LeftButton and self.AI_finish and self.isRun:
            i, j = self.MouseToChess(e.x(), e.y()) #鼠标坐标转为棋盘坐标          
            if i >= 0 and i < 15 and j >= 0 and j < 15:
                if self.board[i][j] == 0:#只能下到空白位置
                    self.chess[i][j].setPixmap(self.Black) #设置chess对应位置为黑棋
                    self.chess[i][j].setVisible(True)
                    self.board[i][j] = 1#设置chess对应位置为1
                    self.steps.append((i,j))#记录此步行棋
                    self.Board.isShow = True
                    self.Board.x,self.Board.y = self.ChessToMouse(self.steps[-1][0],self.steps[-1][1])
                    #检测是否胜利
                    if self.CheckWin(i,j):
                        self.isRun = False
                        return                 
                    self.AI_finish = False  
                    self.label_3.setText("轮到白棋...")
                    #调用AI线程
                    self.AI = AI(self.board)
                    self.AI.finishSignal.connect(self.AI_turn)
                    self.AI.start()

    """
    参数：i,j棋盘坐标
    功能：将棋盘坐标转为窗口坐标
    """  
    def ChessToMouse(self, i, j):
        scale = 500 / 14 #每格的大小
        return 50 + j * scale- 18, 30 + i * scale - 18
    """
    参数：x,y窗口坐标
    功能：将窗口坐标转为棋盘坐标
    """  
    def MouseToChess(self, x, y):
        scale = 500 / 14
        i,j = int(round((y - 30) / scale)) , int(round((x - 50) / scale))
        return i,j
    
    """
    参数：score棋势得分 i，j AI下棋坐标
    功能：轮到AI时进行的操作
    """  
    def AI_turn(self, score, i, j):
        self.label_4.setText("棋势评估:"+str(int(score)))
        self.chess[i][j].setPixmap(self.White)#将chess对应位置设为白棋
        self.chess[i][j].setVisible(True)
        self.board[i][j] = 2 #将board对应位置设为2
        self.steps.append((i,j)) #记录此步行棋
        self.Board.isShow = True
        self.Board.x,self.Board.y = self.ChessToMouse(self.steps[-1][0],self.steps[-1][1])
        #检测是否胜利
        if self.CheckWin(i,j):
            self.isRun = False
            return
        self.label_3.setText("轮到黑棋...")
        self.AI_finish = True
        self.update()
        
    """
    参数：i,j下棋坐标
    功能：检查当前是否有五子连线
    """
    def CheckWin(self, i, j):
        direction = [[(-1, 0), (1, 0)], [(0, -1), (0, 1)], [(-1, 1), (1, -1)], [(-1, -1), (1, 1)]]
        for a in direction: #遍历四个方向
            n = 1
            for b in a:
                i1 = i
                j1 = j
                while True:
                    i2 = i1+b[0]
                    j2 = j1+b[1]
                    if i2<0 or i2>14 or j2<0 or j2>14:
                        break
                    if self.board[i1][j1] == self.board[i2][j2]:
                        n += 1
                        i1 = i2
                        j1 = j2
                    else:
                        break            
            if n >= 5:
                if self.board[i][j]==1:
                    self.label_3.setText("黑棋胜利!")
                else:
                    self.label_3.setText("白棋胜利!")
                return True
        return False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())
