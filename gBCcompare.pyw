# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 23:15:20 2017

@author: gongliang2
"""

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from gBCcompareUI import Ui_MainWindow
from gBCviewer import gBCviewer
from gBCviewer import viewTableModel
import sys

class compareTableModel(viewTableModel):
    def __init__(self, parent=None):
        super(compareTableModel, self).__init__()
        self.dataAnother = None
        
    def updateData2compare(self, data):
        self.dataAnother = data
        
    def data(self, index, role):
        x = index.row()
        y = index.column()
        if x < len(self.dataIn) and y < len(self.dataIn[x]):
            if role == QtCore.Qt.DisplayRole:           
                return str(self.dataIn[x][y])
            elif self.showDiff and role == QtCore.Qt.BackgroundColorRole:
                if self.dataAnother and ((x < len(self.dataAnother) and y < len(self.dataAnother[x]) \
                    and self.dataIn[x][y] != self.dataAnother[x][y]) or \
                    x >= len(self.dataAnother) or y >= len(self.dataAnother[x])):
                        return QtGui.QBrush(QtCore.Qt.red)
                elif x > 0:
                    if (y < len(self.dataIn[x-1]) and (self.dataIn[x][y] != self.dataIn[x-1][y])) \
                    or (y >= len(self.dataIn[x-1]) and self.dataIn[x][y]):
                        return QtGui.QBrush(QtCore.Qt.yellow)


class gBCcompare(QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self, parent=None):
        super(gBCcompare, self).__init__()
        self.setupUi(self)
        
        self.__idx4Diffs = -1   # store the current index in self.__diffs
        self.__diffs = []   # store indexes(x, y) of all discovered differences
        self.__searchFinished = False
        
        self.viewer1 = gBCviewer()
        self.viewer2 = gBCviewer()
        self.hLayout2.addWidget(self.viewer1)
        self.hLayout2.addWidget(self.viewer2)

        self.pb_compare.clicked.connect(self.tryCompare)
        self.pb_next.clicked.connect(self.getNextDiff)
        self.pb_last.clicked.connect(self.getLastDiff)
        
        
        self.viewer1.syncScrollbar4Compare = self.synchScrollbar
        self.viewer2.syncScrollbar4Compare = self.synchScrollbar
        
        
    def tryCompare(self):
        if self.viewer1.myModel.dataIn and self.viewer2.myModel.dataIn:
            model1 = compareTableModel(self)
            model1.update(self.viewer1.myModel.dataIn, self.viewer1.cb_diff.isChecked())
            model1.dataAnother = self.viewer2.myModel.dataIn
            model2 = compareTableModel(self)
            model2.update(self.viewer2.myModel.dataIn, self.viewer2.cb_diff.isChecked())
            model2.dataAnother = self.viewer1.myModel.dataIn
            self.viewer1.myModel = model1
            self.viewer2.myModel = model2
            self.viewer1.table.setModel(self.viewer1.myModel)
            self.viewer2.table.setModel(self.viewer2.myModel)
            
    def synchScrollbar(self):
        if self.viewer1.table and self.viewer2.table:
            self.viewer1.table.verticalScrollBar().valueChanged.connect(self.viewer2.table.verticalScrollBar().setValue)
            self.viewer2.table.verticalScrollBar().valueChanged.connect(self.viewer1.table.verticalScrollBar().setValue)
            self.viewer1.table.horizontalScrollBar().valueChanged.connect(self.viewer2.table.horizontalScrollBar().setValue)
            self.viewer2.table.horizontalScrollBar().valueChanged.connect(self.viewer1.table.horizontalScrollBar().setValue)
            
#    def getDiffs(self):
##        for x, row in enumerate(zip(self.viewer1.myModel.dataIn, self.viewer2.myModel.dataIn)):
##            for y, column in enumerate(zip(self.viewer1.myModel.dataIn[x], self.viewer2.myModel.dataIn[x])):
##                if column[0] != column[1]:
##                    self.__diffs.append((x, y))
##                    self.__idx4Diffs = (x, y)
##                    break
#                
#        for x in range(self.__idx4Diffs[0], min(len(self.viewer1.myModel.dataIn, self.viewer2.myModel.dataIn))):
#            for y in range(self.__idx4Diffs[1], min(len(self.viewer1.myModel.dataIn[x]), len(self.viewer2.myModel.dataIn[x]))):
#                if x != self.__idx4Diffs[0] or y != self.__idx4Diffs[1]:
#                    if self.viewer1.myModel.dataIn[x][y] != self.viewer2.myModel.dataIn[x][y]:
#                        self.__diffs.append((x, y))
#                        return (x, y)
                    
        
    def getNewDiff(self):
        if self.viewer1.myModel.dataIn and self.viewer2.myModel.dataIn:
            row, column = (0, 0)
            if self.__diffs and self.__idx4Diffs > -1:
                row, column = self.__diffs[self.__idx4Diffs]
            rowMax = max(len(self.viewer1.myModel.dataIn), len(self.viewer2.myModel.dataIn))
            for x in range(row, rowMax):
                columnMax = max(len(self.viewer1.myModel.dataIn[x]), len(self.viewer2.myModel.dataIn[x]))
                for y in range(column, columnMax):
                    if x != row or y != column: # we start just with the x, y position we found in the data, it is always safe. Then we go through the data, only when we move already to the next position in the data, we begin to find the next difference
                        if not (x in range(len(self.viewer1.myModel.dataIn))) \
                        or not (y in range(len(self.viewer1.myModel.dataIn[x]))) \
                        or not (x in range(len(self.viewer2.myModel.dataIn))) \
                        or not (y in range(len(self.viewer2.myModel.dataIn[x]))): # check if the index x, y is already out of range of any of the data in comparasion. It must be different between the 2 data
                            self.__diffs.append((x, y))
                            return True
                        elif self.viewer1.myModel.dataIn[x][y] != self.viewer2.myModel.dataIn[x][y]:
                            self.__diffs.append((x, y))
                            return True
                        else:
                            continue
                    if row == rowMax and column == columnMax:
                        self.__searchFinished = True
                column = 0  # one line is finished, so we shall begin with the first column again with the next line
                        
        return False
                        
    def getNextDiff(self):
        if self.__idx4Diffs + 1 < len(self.__diffs):
            self.__idx4Diffs += 1
            self.setScrollBar(self.__diffs[self.__idx4Diffs])
        elif (not self.__searchFinished) and self.getNewDiff():
            self.__idx4Diffs += 1
            self.setScrollBar(self.__diffs[self.__idx4Diffs])
            
            
    def getLastDiff(self):
        if self.__idx4Diffs > 0:
            self.__idx4Diffs -= 1
            self.setScrollBar(self.__diffs[self.__idx4Diffs])

    def setScrollBar(self, index):
        if index and len(index) > 1:
            x, y = index
            print(index)
            modelIdx = QtCore.QModelIndex()
            modelIdx.row, modelIdx.column = x, y
            if x < len(self.viewer1.myModel.dataIn) and y < len(self.viewer1.myModel.dataIn[x]):
                self.viewer1.table.horizontalScrollBar().setValue(y)
                self.viewer1.table.verticalScrollBar().setValue(x)
                self.viewer1.table.selectionModel().select(modelIdx, QtCore.QItemSelectionModel.SelectCurrent)
            else:
                self.viewer2.table.horizontalScrollBar().setValue(y)
                self.viewer2.table.verticalScrollBar().setValue(x)
                self.viewer2.table.selectionModel().select(modelIdx, QtCore.QItemSelectionModel.SelectCurrent)
            
            
            
#    def getSameShape2Compare(self):
#        if self.viewer1.cb_csv.isChecked() or self.viewer2.cb_csv.isChecked():
#            xMax = max(self.viewer1.myModel.rowCount(), self.viewer2.myModel.rowCount())
#            yMax = max(self.viewer1.myModel.columnCount(), self.viewer2.myModel.columnCount())
#            for oneRow in self.viewer1.myModel.dataIn:
                    
            

def main():
    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    compare = gBCcompare()  # We set the form to be the viewer
    compare.show()  # Show the form
    sys.exit(app.exec_())  # and execute the app
    

if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function