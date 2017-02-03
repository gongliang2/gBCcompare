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
        
        self.viewer1 = gBCviewer()
        self.viewer2 = gBCviewer()
        self.hLayout2.addWidget(self.viewer1)
        self.hLayout2.addWidget(self.viewer2)

        self.pb_compare.clicked.connect(self.tryCompare)
        
        self.viewer1.syncScrollbar4Compare = self.synchScrollbar
        self.viewer2.syncScrollbar4Compare = self.synchScrollbar
        
        
    def tryCompare(self):
        if self.viewer1.data2View and self.viewer2.data2View:
            model1 = compareTableModel(self)
            model1.update(self.viewer1.data2View, self.viewer1.cb_diff.isChecked())
            model1.dataAnother = self.viewer2.data2View
            model2 = compareTableModel(self)
            model2.update(self.viewer2.data2View, self.viewer2.cb_diff.isChecked())
            model2.dataAnother = self.viewer1.data2View
            self.viewer1.myModel = model1
            self.viewer2.myModel = model2
            self.viewer1.table.setModel(model1)
            self.viewer2.table.setModel(model2)
            
    def synchScrollbar(self):
        if self.viewer1.table and self.viewer2.table:
            self.viewer1.table.verticalScrollBar().valueChanged.connect(self.viewer2.table.verticalScrollBar().setValue)
            self.viewer2.table.verticalScrollBar().valueChanged.connect(self.viewer1.table.verticalScrollBar().setValue)
            self.viewer1.table.horizontalScrollBar().valueChanged.connect(self.viewer2.table.horizontalScrollBar().setValue)
            self.viewer2.table.horizontalScrollBar().valueChanged.connect(self.viewer1.table.horizontalScrollBar().setValue)
        

def main():
    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    compare = gBCcompare()  # We set the form to be the viewer
    compare.show()  # Show the form
    sys.exit(app.exec_())  # and execute the app
    

if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function