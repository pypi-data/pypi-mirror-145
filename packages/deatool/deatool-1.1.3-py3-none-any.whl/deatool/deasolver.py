from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from deatool.MMODEL.CCR import MCCR
from deatool.MMODEL.DDF import MDDF
from deatool.MMODEL.SBM import MSBM
from deatool.MMODEL.CCR_pyomo import MCCR_pyomo
from deatool.MMODEL.DDF_pyomo import MDDF_pyomo
from deatool.MMODEL.SBM_pyomo import MSBM_pyomo
from deatool.QT5.Ui_table import Ui_Dialog
import pandas as pd
import os

class Tables(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.radioButton.setChecked(True)
        self.pushButton_1.clicked.connect(self.dataprocess)
        self.pushButton_2.clicked.connect(self.result)
        self.pushButton_3.clicked.connect(self.save)
        
        
    def initialize(self,df):
        # 设置表格行数和列数
        columns = df.columns
        rows = df.index
        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(len(columns))
        self.tableWidget.setHorizontalHeaderLabels(columns)
        for j in range(len(columns)):
            self.tableWidget.setColumnWidth(j, 100)
            for i in range(len(rows)):
                data = QTableWidgetItem(str(df.iloc[i][j]))
                self.tableWidget.setItem(i, j, data)
        self.tableWidget.setAlternatingRowColors(True)
    
    def final(self,df):
        columns = df.columns
        rows = df.index
        self.tableWidget_2.setRowCount(len(rows))
        self.tableWidget_2.setColumnCount(len(columns))
        self.tableWidget_2.setHorizontalHeaderLabels(columns)
        for j in range(len(columns)):
            self.tableWidget_2.setColumnWidth(j, 100)
            for i in range(len(rows)):
                data = QTableWidgetItem(str(df.iloc[i][j]))
                self.tableWidget_2.setItem(i, j, data)
        self.tableWidget_2.setAlternatingRowColors(True)
    
    def dataprocess(self):
        try:
            openfile_name = QFileDialog.getOpenFileName(self,'选择文件','','Excel files(*.xlsx , *.xls)')
            global path_openfile_name
            path_openfile_name = openfile_name[0]
            self.df=pd.read_excel(path_openfile_name)
            self.initialize(self.df)
        except:
            self.printf('Error:数据读取有误，请检查数据。')
        
    def result(self):
        data = self.df.copy()
        try:
            self.input_cols = list(self.df.columns.values[1:int(self.lineEdit.text())+1])
            self.output_cols = list(self.df.columns.values[int(self.lineEdit.text())+1:int(self.lineEdit.text())+int(self.lineEdit_2.text())+1])
            if self.lineEdit_3.text() == '若无可不填写':
                self.un_output_cols = []
            else:
                self.un_output_cols = list(self.df.columns.values[int(self.lineEdit.text())+int(self.lineEdit_2.text())+1:
                    int(self.lineEdit.text())+int(self.lineEdit_2.text())+int(self.lineEdit_3.text())+1])
            self.printf('-------------------------------------')
            self.printf('投入为{}'.format(self.input_cols))
            self.printf('产出为{}'.format(self.output_cols))
            self.printf('非期望产出为{}'.format(self.un_output_cols))
            self.key = self.comboBox.currentText() 
            vv = self.comboBox_3.currentText() 
            dd = self.comboBox_2.currentText()
            self.printf('正在计算结果，请稍后')
            if self.radioButton.isChecked():
                if self.key == 'CCR模型':
                    if self.un_output_cols == []:
                        self.printf('您选择的模型是CCR模型 没有非期望产出')
                    else:
                        self.printf('您选择的模型是CCR模型 有非期望产出')
                    model = MCCR(data=data, input_cols = self.input_cols, output_cols = self.output_cols,un_output_cols = self.un_output_cols, vv = vv )
                    self.res = model.res()
                elif self.key == 'DDF模型':
                    if self.un_output_cols == []:
                        self.printf('您选择的模型是DDF模型,没有非期望产出')
                    else:
                        self.printf('您选择的模型是DDF模型,有非期望产出')
                    model = MDDF(data=data, input_cols = self.input_cols, output_cols = self.output_cols,un_output_cols = self.un_output_cols, vv = vv, dd = dd)
                    self.res = model.res()
                elif self.key == 'SBM模型':
                    if self.un_output_cols == []:
                        self.printf('您选择的模型是SBM模型,没有非期望产出')
                    else:
                        self.printf('您选择的模型是SBM模型,有非期望产出')
                    model = MSBM(data=data, input_cols = self.input_cols, output_cols = self.output_cols,un_output_cols = self.un_output_cols, vv = vv )
                    self.res = model.res()
                self.printf('计算已结束')
                self.printf('-------------------------------------')
                self.final(self.res)
            else:
                if self.radioButton_2.isChecked():
                    status = 'cplex'
                elif self.radioButton_3.isChecked():
                    status = 'glpk'
                self.printf('您选择的求解器为{}'.format(status))
                if self.key == 'CCR模型':
                    if self.un_output_cols == []:
                        self.printf('您选择的模型是CCR模型,没有非期望产出')
                    else:
                        self.printf('您选择的模型是CCR模型,有非期望产出')
                    model = MCCR_pyomo(data=data, input_cols = self.input_cols, output_cols = self.output_cols,un_output_cols = self.un_output_cols, vv = vv, solver = status)
                    self.res = model.res()
                elif self.key == 'DDF模型':
                    if self.un_output_cols == []:
                        self.printf('您选择的模型是DDF模型,没有非期望产出')
                    else:
                        self.printf('您选择的模型是DDF模型,有非期望产出')
                    model = MDDF_pyomo(data=data, input_cols = self.input_cols, output_cols = self.output_cols,un_output_cols = self.un_output_cols, vv = vv, dd = dd, solver = status)
                    self.res = model.res()
                elif self.key == 'SBM模型':
                    if self.un_output_cols == []:
                        self.printf('您选择的模型是SBM模型,没有非期望产出')
                    else:
                        self.printf('您选择的模型是SBM模型,有非期望产出')
                    model = MSBM_pyomo(data=data, input_cols = self.input_cols, output_cols = self.output_cols,un_output_cols = self.un_output_cols, vv = vv, solver = status )
                    self.res = model.res()
                self.printf('计算已结束')
                self.printf('-------------------------------------')
                self.final(self.res)
        except:
            self.printf('出错，请检查步骤是否正确')
            self.printf('可能的原因有:')
            self.printf('1.数据格式设置有误,请参照正确设置方式;')
            self.printf('2.您的系统没有该求解器,请重新选取。')
            self.printf('-------------------------------------')
    
    def save(self):
        path = os.path.split(path_openfile_name)[0]
        self.res.to_excel(path+r'\结果_{}.xlsx'.format(self.key), index=False)
        
# 运行界面
    def printf(self, mes):
        self.textBrowser.append(mes)  # 在指定的区域显示提示信息
        self.cursot = self.textBrowser.textCursor()
        self.textBrowser.moveCursor(self.cursot.End)