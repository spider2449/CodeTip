# -*- coding: utf-8 -*-

"""
Module implementing FramelessWindow.
"""
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sip, os
#import configparser #You need pip install configparser


from Ui_framelesswindow import Ui_FramelessWindow

PADDING=4  
class FramelessWindow(QWidget, Ui_FramelessWindow):

    def __init__(self, parent=None):
        super(FramelessWindow, self).__init__(parent, Qt.FramelessWindowHint)
        self.setupUi(self)

        self.contentLayout = QHBoxLayout(self)
        
        self.restoreButton.setVisible(False)
        
        self.setAttribute(Qt.WA_TranslucentBackground);#透明
        
        self.setWindowFlags( Qt.FramelessWindowHint)
        
        #=============================== 托盘图标 ================================#
        self.icon = QIcon('./db/360ask.png')  #创建图标  

        self.tray = QSystemTrayIcon(self) #创建系统托盘对象  
        self.tray.setIcon(self.icon)  #设置系统托盘图标
        
        self.MaxAction = QAction(u'最大化 ', self, triggered=lambda:self.setWindowState(Qt.WindowMaximized)) #添加一级菜单动作选项(最大化主窗口)  
        self.RestoreAction = QAction(u'还原 ', self, triggered=self.show) #添加一级菜单动作选项(还原主窗口)  
        self.QuitAction = QAction(u'退出 ', self, triggered=self.close) #添加一级菜单动作选项(退出程序)  

        self.tray_menu = QMenu(QApplication.desktop()) #创建菜单  
        self.tray_menu.addAction(self.MaxAction) #为菜单添加动作  
        self.tray_menu.addAction(self.RestoreAction) #为菜单添加动作  
        self.tray_menu.addAction(self.QuitAction)  
        
        self.tray.setContextMenu(self.tray_menu) #设置系统托盘菜单  
        self.tray.show()
        
#=================== 无 窗 体 拉 伸 ===================↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
        self.setMouseTracking(True) # 设置widget鼠标跟踪   
        self.SHADOW_WIDTH=0   #边框距离  
        self.isLeftPressDown = False #鼠标左键是否按下  
        self.dragPosition=0     #拖动时坐标  
        self.Numbers = self.enum(UP=0, DOWN=1, LEFT=2, RIGHT=3, LEFTTOP=4, LEFTBOTTOM=5, RIGHTBOTTOM=6, RIGHTTOP=7, NONE=8) #枚举参数  

        self.dir=self.Numbers.NONE #初始鼠标状态  
        
        self._padding=10
        
#        self.setting=QSettings('D:/QGroup_432987409/CodeTip/db/setting.ini', QSettings.IniFormat) 
       
        if os.path.isfile("../db/setting.ini"):
            self.setting=QSettings('../db/setting.ini', QSettings.IniFormat)
        else:
            self.setting=QSettings('./db/setting.ini', QSettings.IniFormat) 
        
        self._getSetting()

    def enum(self,**enums):  
        return type('Enum', (), enums)  
  
    def region(self,cursorGlobalPoint):  
        #获取窗体在屏幕上的位置区域，tl为topleft点，rb为rightbottom点  
        rect = self.rect()  
        tl = self.mapToGlobal(rect.topLeft())  
        rb = self.mapToGlobal(rect.bottomRight())  
  
        x = cursorGlobalPoint.x()  
        y = cursorGlobalPoint.y()  
  
        if(tl.x() + PADDING >= x and tl.x() <= x and tl.y() + PADDING >= y and tl.y() <= y):  
            #左上角  
            self.dir = self.Numbers.LEFTTOP  
            self.setCursor(QCursor(Qt.SizeFDiagCursor))   #设置鼠标形状  
        elif(x >= rb.x() - PADDING and x <= rb.x() and y >= rb.y() - PADDING and y <= rb.y()):  
            #右下角  
            self.dir = self.Numbers.RIGHTBOTTOM  
            self.setCursor(QCursor(Qt.SizeFDiagCursor))  
        elif(x <= tl.x() + PADDING and x >= tl.x() and y >= rb.y() - PADDING and y <= rb.y()):  
            #左下角  
            self.dir = self.Numbers.LEFTBOTTOM  
            self.setCursor(QCursor(Qt.SizeBDiagCursor))  
        elif(x <= rb.x() and x >= rb.x() - PADDING and y >= tl.y() and y <= tl.y() + PADDING):  
            #右上角  
            self.dir = self.Numbers.RIGHTTOP  
            self.setCursor(QCursor(Qt.SizeBDiagCursor))  
        elif(x <= tl.x() + PADDING and x >= tl.x()):  
            #左边  
            self.dir = self.Numbers.LEFT  
            self.setCursor(QCursor(Qt.SizeHorCursor))  
        elif( x <= rb.x() and x >= rb.x() - PADDING):  
            #右边  
  
            self.dir = self.Numbers.RIGHT  
            self.setCursor(QCursor(Qt.SizeHorCursor))  
        elif(y >= tl.y() and y <= tl.y() + PADDING):  
            #上边  
            self.dir = self.Numbers.UP  
            self.setCursor(QCursor(Qt.SizeVerCursor))  
        elif(y <= rb.y() and y >= rb.y() - PADDING):  
            #下边  
            self.dir = self.Numbers.DOWN  
            self.setCursor(QCursor(Qt.SizeVerCursor))  
        else:  
            #默认  
            self.dir = self.Numbers.NONE  
            self.setCursor(QCursor(Qt.ArrowCursor))  
  
    def mouseReleaseEvent(self,event):  
        if(event.button() == Qt.LeftButton):  
            self.isLeftPressDown = False  
            if(self.dir != self.Numbers.NONE):  
                self.releaseMouse()  
                self.setCursor(QCursor(Qt.ArrowCursor))  
  
    def mousePressEvent(self,event):  
        if(event.button()==Qt.LeftButton):  
            self.isLeftPressDown=True  
            if(self.dir != self.Numbers.NONE):  
                self.mouseGrabber()  
            else:  
                self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()  
  
    def mouseMoveEvent(self,event):  
        gloPoint = event.globalPos()  
        rect = self.rect()  
        tl = self.mapToGlobal(rect.topLeft())  
        rb = self.mapToGlobal(rect.bottomRight())  
  
        if(not self.isLeftPressDown):  
            self.region(gloPoint)    
        else:  
            if(self.dir != self.Numbers.NONE):  
                rmove=QRect(tl, rb)  
                if(self.dir==self.Numbers.LEFT):  
                    if(rb.x() - gloPoint.x() <= self.minimumWidth()):  
                        rmove.setX(tl.x())  
                    else:  
                        rmove.setX(gloPoint.x())  
                elif(self.dir==self.Numbers.RIGHT):  
                     
                    rmove.setWidth(gloPoint.x() - tl.x())  
                elif(self.dir==self.Numbers.UP):  
                    if(rb.y() - gloPoint.y() <= self.minimumHeight()):  
                        rmove.setY(tl.y())  
                    else:  
                        rmove.setY(gloPoint.y())  
                elif(self.dir==self.Numbers.DOWN):  
                    rmove.setHeight(gloPoint.y() - tl.y())  
                elif(self.dir==self.Numbers.LEFTTOP):  
                    if(rb.x() - gloPoint.x() <= self.minimumWidth()):  
                        rmove.setX(tl.x())  
                    else:  
                        rmove.setX(gloPoint.x())  
                    if(rb.y() - gloPoint.y() <= self.minimumHeight()):  
                        rmove.setY(tl.y())  
                    else:  
                        rmove.setY(gloPoint.y())  
                elif(self.dir==self.Numbers.RIGHTTOP):  
                    rmove.setWidth(gloPoint.x() - tl.x())  
                    rmove.setY(gloPoint.y())  
                elif(self.dir==self.Numbers.LEFTBOTTOM):  
                    rmove.setX(gloPoint.x())  
                    rmove.setHeight(gloPoint.y() - tl.y())  
                elif(self.dir==self.Numbers.RIGHTBOTTOM):  
                    rmove.setWidth(gloPoint.x() - tl.x())  
                    rmove.setHeight(gloPoint.y() - tl.y())  
                else:  
                   pass  
                self.setGeometry(rmove)  
            else:  
                try:
                    self.move(event.globalPos() - self.dragPosition)  
                except:
                    pass
                event.accept()  
        
#=================== 无 窗 体 拉 伸 ===================↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑


#=================== 贴 边 隐 藏 ===================↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
    def enterEvent(self, event):

        self.setCursor(QCursor(Qt.ArrowCursor))  
            
        if(self.x() == self._padding-self.width()):
            self.move(-self._padding+5,self.y())
            #左边
            
        elif(self.x() == QApplication.desktop().screenGeometry().width()-self._padding):
            self.move(QApplication.desktop().screenGeometry().width()-self.width()+self._padding,self.y())
            #右边    
            
        elif(self.y() == self._padding-self.height()+self.y()-self.geometry().y()):
            self.move(self.x(),-self._padding)
            #上边
        
    def leaveEvent(self,event):    
        cx,cy = QCursor.pos().x(),QCursor.pos().y()
        
        if(cx >= self.x() and cx <= self.x()+self.width()
            and cy >= self.y() and cy <= self.geometry().y()):
            return#title bar

        elif(self.x() < 0 and QCursor.pos().x()>0):
            self.move(self._padding-self.width(),self.y())
            #左边
            
        elif(self.x() > (QApplication.desktop().screenGeometry().width()-self.width())\
            and QCursor.pos().x()>0):
            self.move(QApplication.desktop().screenGeometry().width()-self._padding,self.y())
            #右边
            
        elif(self.y() < 0 and QCursor.pos().y()>0):
            self.move(self.x(), self._padding-self.height()+self.y()-self.geometry().y())
            #上边 
#    def moveEvent(self, e): 
#        #左上角坐标
#        print('x:', self.x(),'y:',  self.y())
#        #鼠标坐标
#        print('cx:', QCursor.pos().x(),'cy:', QCursor.pos().y())
#        #距离
#        print('gx:', self.geometry().x(),'gy:', self.geometry().y())
#        #分辨率
#        print('dx:', QApplication.desktop().screenGeometry().width(),'dy:', QApplication.desktop().screenGeometry().height())
    
    
#=================== 贴 边 隐 藏 ===================↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
    
    @pyqtSlot()
    def on_applicationStateChanged(state):
        pass
    
    @pyqtSlot()
    def on_windowTitlebar_doubleClicked(self):
        if (self.windowState()==Qt.WindowNoState) :
            self.on_maximizeButton_clicked();
        
        elif (self.windowState()== Qt.WindowMaximized):
            self.on_restoreButton_clicked();
        
    @pyqtSlot()
    def on_minimizeButton_clicked(self):
        self.setWindowState(Qt.WindowMinimized);
    
    @pyqtSlot()
    def on_restoreButton_clicked(self):
        self.restoreButton.setVisible(False);
        self.maximizeButton.setVisible(True);
        self.setWindowState(Qt.WindowNoState);
#        self.styleWindow(True, True);
#    
    @pyqtSlot()
    def on_maximizeButton_clicked(self):
        self.restoreButton.setVisible(True);
        self.maximizeButton.setVisible(False);
        self.setWindowState(Qt.WindowMaximized);
#        self.styleWindow(True, False);
    
    @pyqtSlot()
    def on_closeButton_clicked(self):

        self.close()  
#        qApp.quit()
        try:
            sip.delete(self.tray)
        except:
            pass
    def setContent(self, w):
        self.contentLayout.setContentsMargins(0, 0, 0, 0)
        self.contentLayout.setSpacing(0)
        
        self.contentLayout.addWidget(w);
        self.windowContent.setLayout(self.contentLayout);

    def setTitle(self, text):
        self.titleText.setText(text)
                
    def paintEvent(self, e):        
        painter=QPainter(self);
        painter.setRenderHint(QPainter.Antialiasing); #反锯齿;
        painter.setBrush(QBrush(QColor(49,54,59)));
        painter.setPen(Qt.transparent);
        rect = self.rect();
        rect.setWidth(rect.width() );
        rect.setHeight(rect.height() );
        painter.drawRoundedRect(rect, 8, 8);
        
    def _getSetting(self):    
        desktop_x=QApplication.desktop().screenGeometry().width()        
        if(self.setting.contains("Position/x")):   #此节点是否存在该数据
            x=int(self.setting.value("Position/x"))
            y=int(self.setting.value("Position/y"))
            w=int(self.setting.value("Position/w"))
            h=int(self.setting.value("Position/h"))
            self.resize(w, h)
            
            if x<=0:  
                if y<0: #x<0 , 且y<0;
                    self.move(x, self._padding-y)
                elif y>0:
                    self.move(self._padding-w, y)                    
            elif x>=desktop_x-w :#在右上角
                    self.move(desktop_x-self._padding, y)
            elif 0<x<desktop_x-w :
                if y>0:
                    self.move(x, y)
                elif y<0:
                    self.move(x, self._padding-y)
            
            check = int(self.setting.value("SetTop/isCheck"))  
            self.setTop(check)
    def setTop(w, check):
        if check==1:
            w.setWindowFlags(Qt.WindowStaysOnTopHint|Qt.Tool|Qt.Widget|Qt.FramelessWindowHint)
#            w.setWindowFlags(Qt.WindowStaysOnTopHint|Qt.FramelessWindowHint)
        elif check==0:
            w.setWindowFlags(Qt.Widget|Qt.Tool|Qt.FramelessWindowHint)
#            w.setWindowFlags(Qt.Widget|Qt.FramelessWindowHint)
        if w.isVisible()==False:
            w.setVisible(True);
            
    def closeEvent(self, event):
        self.setWindowFlags(Qt.Widget)
        
#        config = configparser.ConfigParser()
#        try:        
#            config.readfp(open('../db/setting.ini'))
#            path = '../db/setting.ini'
#        except:
#            path = './db/setting.ini'
#            config.readfp(open(path))
#        config.set("Position", "x", str(self.x())) #设置x坐标
#        config.set("Position", "y", str(self.y())) #设置设置y坐标
#        config.set("Position", "w", str(self.width())) #设置宽度
#        config.set("Position", "h", str(self.height())) #设置高度
#        config.write(open(path, "r+"))

        self.setting.setValue("Position/x",str(self.x()));#设置x坐标
        self.setting.setValue("Position/y",str(self.y()));#设置设置y坐标
        self.setting.setValue("Position/w",str(self.width()));#设置宽度
        self.setting.setValue("Position/h",str(self.height()));#设置高度
        sip.delete(self.tray)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
  
    ui = FramelessWindow()
    ui.show()
    sys.exit(app.exec_())
        


