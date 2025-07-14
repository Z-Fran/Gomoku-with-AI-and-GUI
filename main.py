import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication,QStyleFactory,QWidget,QLabel,QComboBox,QPushButton
from PyQt5.QtCore import Qt,QRect
from PyQt5.QtGui import QPixmap, QIcon,QPainter, QPen
from AI import searcher

"""
AI Thread
"""
class AI(QtCore.QThread):
    finishSignal = QtCore.pyqtSignal(float, int, int)
    def __init__(self, board, parent=None):
        super(AI, self).__init__(parent)
        self.board = board
    def run(self):
        self.ai = searcher(1)
        self.ai.board = self.board
        score, x, y = self.ai.search(2, 2) # Call minimax search algorithm
        self.finishSignal.emit(score, x, y)

"""
Class for marking the last move
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
            # Draw a circle at the position of the last piece
            qp.begin(self)
            pen = QPen(Qt.yellow, 8, Qt.SolidLine)
            qp.setPen(pen)
            rect = QRect(int(self.x-30),int(self.y-10),36,36)
            qp.drawArc(rect,0,360*16)
            qp.end()
        self.update()
       
"""
Main window class
"""
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Set window properties
        QApplication.setStyle(QStyleFactory.create("Fusion"))
        self.setWindowTitle("Gobang") 
        self.setWindowIcon(QIcon('img/black.png'))
        self.resize(600, 900)
        self.setMinimumSize(QtCore.QSize(600, 900))
        self.setMaximumSize(QtCore.QSize(600, 900))
        # Background and board images
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
        # Set prompt information
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(16)
        self.label_1 = QLabel(self)
        self.label_1.setFont(font)
        self.label_1.setAlignment(Qt.AlignCenter)
        self.label_1.setGeometry(QRect(0,670,150,50))
        self.label_1.setText("Player (Black)")
        self.label_2 = QLabel(self)
        self.label_2.setFont(font)
        self.label_2.setGeometry(QRect(490,700,150,50))
        self.label_2.setText("AI (White)")
        self.label_3 = QLabel(self)
        self.label_3.setFont(font)
        self.label_3.setGeometry(QRect(150,570,150,50))
        self.label_3.setText("Black's turn...")
        self.label_4 = QLabel(self)
        self.label_4.setFont(font)
        self.label_4.setGeometry(QRect(300,570,300,50))
        self.label_4.setText("Board Evaluation:")
        self.opt = QComboBox(self)
        self.opt.setGeometry(QtCore.QRect(270, 840, 60, 40))
        self.opt.addItem("Black First")
        self.opt.addItem("White First")
        # Buttons
        self.reset = QPushButton(self)
        self.reset.setGeometry(QtCore.QRect(50, 840, 200, 40))
        self.reset.setText("Restart")
        self.retract = QPushButton(self)
        self.retract.setGeometry(QRect(350, 840, 200, 40))
        self.retract.setText("Undo")
        QtCore.QMetaObject.connectSlotsByName(self)
        self.reset.clicked.connect(self.Reset) 
        self.retract.clicked.connect(self.Retract)
        # Show the piece to be placed at the mouse position
        self.MouseFocus = QLabel(self)  # Change mouse image to piece      
        self.MouseFocus.setPixmap(self.Black)  # Load black piece
        self.MouseFocus.setGeometry(0, 0, 36, 36)
        self.MouseFocus.setScaledContents(True)
        self.MouseFocus.raise_()  # Mouse always on top
        # Top layer for tracking mouse    
        self.Trace = QLabel(self)
        self.Trace.setGeometry(QRect(30, 10, 540, 540))
        self.Trace.setMouseTracking(True)
        self.Back.setMouseTracking(True)
        self.Board.setMouseTracking(True)
        self.setMouseTracking(True)
       
        # Initialize board and pieces
        self.board = []
        self.chess = []
        self.direction = [[(-1, 0), (1, 0)], [(0, -1), (0, 1)], [(-1, 1), (1, -1)], [(-1, -1), (1, 1)]]
        self.InitBoard()
        self.AI_finish = True # AI must finish before player can move
        self.isRun = True # Game is ongoing
        self.steps = [] # Store each move for undo
        self.show()
    
    
    """
    Args: None
    Function: Initialize the board
    """ 
    def InitBoard(self):  # Reset
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
                self.chess[i][j].setGeometry(int(x), int(y), 36, 36)
                self.chess[i][j].setPixmap(QPixmap('img/none.jpg'))
    
    """
    Args: None
    Function: Undo move
    """
    def Retract(self):
        if self.AI_finish and len(self.steps)>1:
            # Remove the last two moves recorded in steps
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
    Args: None
    Function: Restart game
    """
    def Reset(self):
        self.label_4.setText("Board Evaluation:")
        self.label_3.setText("Black's turn...")
        self.InitBoard()
        self.AI_finish = True
        self.isRun = True
        self.Board.isShow = False
        self.steps = []
        if self.opt.currentText()=="White First":
            self.AI_finish = False  
            self.label_3.setText("White's turn...")
            # Call AI thread
            self.AI = AI(self.board)
            self.AI.finishSignal.connect(self.AI_turn)
            self.AI.start()
                
    """
    Args: None
    Function: Override mouse move event
    """    
    def mouseMoveEvent(self, e):  # Black piece follows mouse movement
        if e.x()>30 and e.x()<570 and e.y()>10 and e.y()<550:
            self.MouseFocus.move(e.x() - 18, e.y() - 18) 
            self.MouseFocus.setPixmap(self.Black)  # Load black piece
        else:
            self.MouseFocus.setPixmap(QPixmap('img/none.jpg'))           
    """
    Args: None
    Function: Override mouse press event
    """  
    def mousePressEvent(self, e):  # Player move
        """
        AI vs AI
        """ 
        """
        if e.button() == Qt.LeftButton and self.AI_finish and self.isRun:
            self.AI2 = searcher(2)
            self.AI2.board = self.board
            score,i,j = self.AI2.search(2,2)
            self.chess[i][j].setPixmap(self.Black) # Set chess position to black
            self.chess[i][j].setVisible(True)
            self.board[i][j] = 1# Set chess position to 1
            self.steps.append((i,j))# Record this move
            self.Board.isShow = True
            self.Board.x,self.Board.y = self.ChessToMouse(self.steps[-1][0],self.steps[-1][1])
            if self.CheckWin(i,j):
                self.isRun = False
                return                 
            self.AI_finish = False  
            self.label_3.setText("White's turn...")
            # Call AI thread
            self.AI = AI(self.board)
            self.AI.finishSignal.connect(self.AI_turn)
            self.AI.start()
        """
        
        if e.button() == Qt.LeftButton and self.AI_finish and self.isRun:
            i, j = self.MouseToChess(e.x(), e.y()) # Convert mouse coordinates to board coordinates          
            if i >= 0 and i < 15 and j >= 0 and j < 15:
                if self.board[i][j] == 0:# Only place on empty positions
                    self.chess[i][j].setPixmap(self.Black) # Set chess position to black
                    self.chess[i][j].setVisible(True)
                    self.board[i][j] = 1# Set chess position to 1
                    self.steps.append((i,j))# Record this move
                    self.Board.isShow = True
                    self.Board.x,self.Board.y = self.ChessToMouse(self.steps[-1][0],self.steps[-1][1])
                    # Check for win
                    if self.CheckWin(i,j):
                        self.isRun = False
                        return                 
                    self.AI_finish = False  
                    self.label_3.setText("White's turn...")
                    # Call AI thread
                    self.AI = AI(self.board)
                    self.AI.finishSignal.connect(self.AI_turn)
                    self.AI.start()

    """
    Args: i, j board coordinates
    Function: Convert board coordinates to window coordinates
    """  
    def ChessToMouse(self, i, j):
        scale = 500 / 14 # Size of each grid
        return 50 + j * scale- 18, 30 + i * scale - 18
    """
    Args: x, y window coordinates
    Function: Convert window coordinates to board coordinates
    """  
    def MouseToChess(self, x, y):
        scale = 500 / 14
        i,j = int(round((y - 30) / scale)) , int(round((x - 50) / scale))
        return i,j
    
    """
    Args: score board evaluation, i, j AI move coordinates
    Function: Operations when it's AI's turn
    """  
    def AI_turn(self, score, i, j):
        self.label_4.setText("Board Evaluation:"+str(int(score)))
        self.chess[i][j].setPixmap(self.White)# Set chess position to white
        self.chess[i][j].setVisible(True)
        self.board[i][j] = 2 # Set board position to 2
        self.steps.append((i,j)) # Record this move
        self.Board.isShow = True
        self.Board.x,self.Board.y = self.ChessToMouse(self.steps[-1][0],self.steps[-1][1])
        # Check for win
        if self.CheckWin(i,j):
            self.isRun = False
            return
        self.label_3.setText("Black's turn...")
        self.AI_finish = True
        self.update()
        
    """
    Args: i, j move coordinates
    Function: Check if there are five in a row
    """
    def CheckWin(self, i, j):
        direction = [[(-1, 0), (1, 0)], [(0, -1), (0, 1)], [(-1, 1), (1, -1)], [(-1, -1), (1, 1)]]
        for a in direction: # Traverse four directions
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
                    self.label_3.setText("Black wins!")
                else:
                    self.label_3.setText("White wins!")
                return True
        return False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())
