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
        self.__currentDiff = ()

        
    def updateData2compare(self, data):
        self.dataAnother = data
        
    def data(self, index, role):
        x = index.row()
        y = index.column()
        if x < len(self.dataIn) and y < len(self.dataIn[x]):
            if role == QtCore.Qt.DisplayRole:           
                return str(self.dataIn[x][y])
            elif role == QtCore.Qt.BackgroundColorRole:
                if self.__currentDiff and (x, y) == self.__currentDiff:
                    return QtGui.QBrush(QtCore.Qt.cyan)
                if self.showDiff:
                    if len(self.dataAnother) and ((x < len(self.dataAnother) and y < len(self.dataAnother[x]) \
                        and self.dataIn[x][y] != self.dataAnother[x][y]) or \
                        x >= len(self.dataAnother) or y >= len(self.dataAnother[x])):
                            return QtGui.QBrush(QtCore.Qt.red)
                    elif x > 0:
                        if (y < len(self.dataIn[x-1]) and (self.dataIn[x][y] != self.dataIn[x-1][y])) \
                        or (y >= len(self.dataIn[x-1]) and self.dataIn[x][y]):
                            return QtGui.QBrush(QtCore.Qt.yellow)
        
    
    def updateCompareCell(self, index):
        self.__currentDiff = index

class gBCcompare(QtWidgets.QMainWindow, Ui_MainWindow):
    
    version = 'V0.001'
    
    def __init__(self, parent=None):
        super(gBCcompare, self).__init__()
        self.setupUi(self)
        self.setWindowTitle(self.windowTitle() + 4*' ' + '-' + 4*' ' + gBCcompare.version)
        
        self.__idx4Diffs = -1   # store the current index in self.__diffs
        self.__diffs = []   # store indexes(x, y) of all discovered differences
        self.__searchFinished = False
        
        self.viewer1 = gBCviewer()
        self.viewer2 = gBCviewer()
        self.hLayout2.addWidget(self.viewer1)
        self.hLayout2.addWidget(self.viewer2)

        self.pb_compare.clicked.connect(self.getAllDiffs)
        self.pb_next.clicked.connect(self.getNextDiff)
        self.pb_last.clicked.connect(self.getLastDiff)
        
        
        self.viewer1.syncScrollbar4Compare = self.synchScrollbar
        self.viewer2.syncScrollbar4Compare = self.synchScrollbar
        
        
    def tryCompare(self):
        if self.viewer1.myModel and len(self.viewer1.myModel.dataIn) and len(self.viewer2.myModel.dataIn):
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
            self.enableCompareButtons()   # compare is finished compare button can be disabled and enable navigation buttons of differences 
        else:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'no enough data to compare.')
            
    def synchScrollbar(self):
        if self.viewer1.table and self.viewer2.table:
            self.viewer1.table.verticalScrollBar().valueChanged.connect(self.viewer2.table.verticalScrollBar().setValue)
            self.viewer2.table.verticalScrollBar().valueChanged.connect(self.viewer1.table.verticalScrollBar().setValue)
            self.viewer1.table.horizontalScrollBar().valueChanged.connect(self.viewer2.table.horizontalScrollBar().setValue)
            self.viewer2.table.horizontalScrollBar().valueChanged.connect(self.viewer1.table.horizontalScrollBar().setValue)
            self.tryCompare()    #when both table are available, it is ready to compare

    def enableCompareButtons(self):
        compareEnabled = (type(self.viewer1.myModel) is compareTableModel) and (type(self.viewer2.myModel) is compareTableModel)
        self.pb_compare.setEnabled(compareEnabled)
        self.pb_last.setEnabled(compareEnabled)
        self.pb_next.setEnabled(compareEnabled)

    def getNewDiff(self, justOneDiff=True):
        if len(self.viewer1.myModel.dataIn) and len(self.viewer2.myModel.dataIn):
            row, column = (0, -1)   # they shall be different than (0, 0) or we will not be able to compare the (0,0) elements from 2 files with each other. Before we start to compare they are initialized with (0,-1) the closest value to the first real element.
            if self.__diffs and self.__idx4Diffs > -1:
                row, column = self.__diffs[self.__idx4Diffs]    # we start just with the x, y position we found in the data
            rowMax = max(len(self.viewer1.myModel.dataIn), len(self.viewer2.myModel.dataIn))
            
            for x in range(row, rowMax):
                columnMax = 0
                if x >= len(self.viewer1.myModel.dataIn):
                    columnMax = len(self.viewer2.myModel.dataIn[x])
                elif x >= len(self.viewer2.myModel.dataIn):
                    columnMax = len(self.viewer1.myModel.dataIn[x])
                    
                if columnMax:
                    for y in range(columnMax):
                        self.__diffs.append((x, y))
                    if justOneDiff:
                        return # difference found, we return to display the difference in program
                    else:
                        continue # one line is finished because the line is not in viewer1 or not in viewer2
                
                columnMax = max(len(self.viewer1.myModel.dataIn[x]), len(self.viewer2.myModel.dataIn[x]))
                for y in range(column, columnMax):
                    if x != row or y != column: # we start just with the x, y position in the data where we found the difference, it is always safe. Then we go through the data, only when we move away from the position of last difference, we begin to look for the next difference
                        if y >= len(self.viewer1.myModel.dataIn[x]) \
                        or y >= len(self.viewer2.myModel.dataIn[x]): # check if the index x, y is already out of range of any of the data in comparasion. If yes, it must be a difference between the 2 data
                            self.__diffs.append((x, y))                            
                            if justOneDiff:
                                return
                        elif self.viewer1.myModel.dataIn[x][y] != self.viewer2.myModel.dataIn[x][y]:
                            self.__diffs.append((x, y))
                            if justOneDiff:
                                return
                        
                    if row == rowMax and column == columnMax:
                        self.__searchFinished = True
                column = 0  # one line is finished, so we shall begin with the first column again with the next line
                        
        return
                        
    def getNextDiff(self):
        if type(self.viewer1.myModel) is compareTableModel:
            if self.__idx4Diffs + 1 < len(self.__diffs):
                self.__idx4Diffs += 1
                self.setScrollBar(self.__diffs[self.__idx4Diffs])
            elif (not self.__searchFinished):
                self.getNewDiff()
                if self.__idx4Diffs + 1 < len(self.__diffs):
                    self.__idx4Diffs += 1
                    self.setScrollBar(self.__diffs[self.__idx4Diffs])
        else:
            QtWidgets.QMessageBox.information(self, 'Info', 'press first the compare button.')
            
            
    def getLastDiff(self):
        if self.__idx4Diffs > 0:
            self.__idx4Diffs -= 1
            self.setScrollBar(self.__diffs[self.__idx4Diffs])

    def getAllDiffs(self):
        if not self.__searchFinished:
            self.getNewDiff(False)

    def setScrollBar(self, index):
        if index and len(index) > 1:
            x, y = index
            # print(index)
            modelIdx = QtCore.QModelIndex()
            
            if x < len(self.viewer1.myModel.dataIn) and y < len(self.viewer1.myModel.dataIn[x]):
                self.viewer1.table.horizontalScrollBar().setValue(y)
                self.viewer1.table.verticalScrollBar().setValue(x)
                #self.viewer1.table.selectionModel().select(modelIdx, QtCore.QItemSelectionModel.SelectCurrent)
                self.viewer1.myModel.updateCompareCell(index)
                modelIdx.row, modelIdx.column = x, y
                self.viewer1.table.dataChanged(modelIdx, modelIdx)
            else:
                self.viewer1.myModel.updateCompareCell(())
                self.viewer1.table.dataChanged(modelIdx, modelIdx)
            
            if x < len(self.viewer2.myModel.dataIn) and y < len(self.viewer2.myModel.dataIn[x]):
                self.viewer2.table.horizontalScrollBar().setValue(y)
                self.viewer2.table.verticalScrollBar().setValue(x)
                #self.viewer2.table.selectionModel().select(modelIdx, QtCore.QItemSelectionModel.SelectCurrent)
                modelIdx.row, modelIdx.column = x, y
                self.viewer2.myModel.updateCompareCell(index)
                self.viewer2.table.dataChanged(modelIdx, modelIdx)
            else:
                self.viewer2.myModel.updateCompareCell(())
                self.viewer2.table.dataChanged(modelIdx, modelIdx)
                    
            

def main():
    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    compare = gBCcompare()  # We set the form to be the viewer
    compare.show()  # Show the form
    sys.exit(app.exec_())  # and execute the app
    

if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function