# -*- coding: UTF-8 -*-

import sys

from PySide import QtGui
from PySide import QtCore

import datetime, codecs, platform, time
import pandas as pd
from pandas import DataFrame, Series
from textanalysis import *

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent = None ):
        super(MainWindow, self).__init__(parent)

        self.filename = ''

        widget1   =  QtGui.QWidget()
        vbox1     =  QtGui.QVBoxLayout(widget1)
        self.le1  =  QtGui.QLineEdit()
        self.le2 = QtGui.QLineEdit()
        self.le3 = QtGui.QLineEdit()
        self.le_outputfilename= QtGui.QLineEdit()
        self.le_outputfilename.setText("output_making_")

        self.btn_open = QtGui.QPushButton("file_open(*.xlsx)")
        self.btn_open.clicked.connect(self.menu_file_open)

        self.combo_field = QtGui.QComboBox()
        self.combo_field.addItems(['',''])

        self.combo_sep = QtGui.QComboBox()
        self.combo_sep.addItems([',',' ','|','/'])

        self.te1  =  QtGui.QTextEdit()
        self.te1.setTextColor("#ffffff")
        self.te1.setStyleSheet("QTextEdit { background-color: #000000; border: 1px solid #ffffff; }")

        btn1      =  QtGui.QPushButton( "making (*.net, *.vec, *.csv)" )
        btn1.clicked.connect(self.making_net)


        self.form_layout = QtGui.QFormLayout()
        self.form_layout.addRow(u'파  일', self.btn_open)
        self.form_layout.addRow(u'필  드', self.combo_field)
        self.form_layout.addRow(u'구분자', self.combo_sep)
        self.form_layout.addRow(u'출력파일', self.le_outputfilename)
        self.groupBox = QtGui.QGroupBox("Option")
        self.groupBox.setLayout(self.form_layout)


        vbox1.addWidget(self.groupBox)
        vbox1.addWidget(btn1)
        vbox1.addWidget(self.te1)

        #self.layout(vbox1)

        self.setCentralWidget(widget1)

        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
        self.setGeometry(50,50,500,500) #x,y 폭, 높이
        self.setWindowTitle(u"co-word(공기어 분석하여 분석용 파일 생성해줌(*.net, *.vec, *.csv)")

    def making_net(self):
        print ">>> making_net()"

        if self.filename != '':
            f1 = self.filename
            f2 = self.combo_field.currentText()
            f3 = self.combo_sep.currentText()
            f4 = self.le_outputfilename.text()
            try :
                making_pajek_netfile_from_excelfile(filename      = f1,
                                                fieldname     = f2,
                                                sep           = f3,
                                                pajekfilename = f4,
                                                cutoffn       = 0,
                                                option={'no': 1})
                txt = self.te1.toPlainText()
                #self.te1.setTextColor("#aaffaa")
                filenamelist = ">>> %s\n>>> %s\n>>> %s\n"%(f4+'.net', f4+'.vec', f4+'.csv')
                self.te1.setText(">>> File Saved !!!\n" + filenamelist + '\n' + txt)
                #self.te1.setTextColor("#ffffff")

            except AttributeError as error :
                e = ">>> %s" %(error)
                txt = self.te1.toPlainText()
                #self.te1.setTextColor("#ff0000")
                self.te1.setText(e + '\n' + txt )
                #self.te1.setTextColor("#ffffff")

        else:
            txt = self.te1.toPlainText()
            self.te1.setTextColor("#ff0000")
            self.te1.setText(">>> Enter Excel file format !!! " + '\n' + txt )
            self.te1.setTextColor("#ffffff")

    def menu_file_open(self):
        print ">>>menu_file_open"

        FILENAME, _ = QtGui.QFileDialog.getOpenFileName(self,
                                                        'Open News data file (excell file format)',
                                                        './',
                                                        "Files(*.xlsx);;Files2(*.xls);;All Files(*.*)"
                                                        )  # 필터none:
        if FILENAME:
            self.filename = FILENAME
            # 파일이름 지정해주기
            self.btn_open.setText(self.filename)

            # 필드명 업데이트하기
            xls1 = pd.ExcelFile(FILENAME)
            sheet = xls1.sheet_names
            df  = xls1.parse(sheet[0])
            df1 = df.fillna('*')
            # combo box 내용 지정하기

            # 현재 콤보내의 내용을 삭제하는 방법법
            self.combo_field.clear()
            self.combo_field.addItems(df1.columns.tolist())
            self.combo_field.setCurrentIndex(0)
        else:
            return False


def main1():

    app = QtGui.QApplication(sys.argv)
    w1  = MainWindow()
    w1.show()

    sys.exit(app.exec_())



if __name__ == '__main__':
    main1()
   
   
 