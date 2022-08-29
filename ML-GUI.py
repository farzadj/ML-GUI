import sys
import time
import os
import io
import seaborn as sns
import pandas as pd
from PyQt5.QtWidgets import QApplication, QTableView, QFileDialog, QListWidgetItem, QWidget
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib
from matplotlib.ticker import FormatStrFormatter
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as Navi
from matplotlib.figure import Figure
import platform
import sip
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler,StandardScaler, RobustScaler
import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.optimizers import Adam, SGD
from sklearn.metrics import mean_absolute_error,mean_squared_error
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dropout
from sklearn.metrics import classification_report,confusion_matrix,plot_confusion_matrix
from sklearn.model_selection import GridSearchCV
from tensorflow.keras.wrappers.scikit_learn import KerasClassifier, KerasRegressor
from sklearn.model_selection import KFold
from CSV_2 import Ui_SecondWindow
import joblib
import pickle
random_seed = 1


class MatplotlibCanvas(FigureCanvasQTAgg):
    def __init__(self,parent=None, dpi = 120):
        fig = Figure(dpi = dpi)
        fig.subplots_adjust(bottom=0.25,left=0.2)
        self.axes = fig.add_subplot(111)
        super(MatplotlibCanvas,self).__init__(fig)
        #fig.tight_layout()

class pandasModel(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None



class Ui_MainWindow(object):
    def open_window(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_SecondWindow()
        self.ui.setupUi(self.window)
        self.window.show()
        self.ui.pushButton_13.clicked.connect(self.add_HL)
        self.ui.pushButton_14.clicked.connect(self.del_HL)
        self.ui.pushButton_16.clicked.connect(self.add_NEU)
        self.ui.pushButton_15.clicked.connect(self.del_NEU)
        self.ui.pushButton_22.clicked.connect(self.add_BAT)
        self.ui.pushButton_21.clicked.connect(self.del_BAT)
        self.ui.pushButton_24.clicked.connect(self.add_EPO)
        self.ui.pushButton_23.clicked.connect(self.del_EPO)
        self.ui.pushButton_28.clicked.connect(self.add_LR)
        self.ui.pushButton_26.clicked.connect(self.del_LR)
        self.ui.pushButton_25.clicked.connect(self.add_EPS)
        self.ui.pushButton_27.clicked.connect(self.del_EPS)

        self.ui.pushButton_18.clicked.connect(self.add_AF)
        self.ui.pushButton_17.clicked.connect(self.del_AF)
        self.ui.pushButton_30.clicked.connect(self.add_OP)
        self.ui.pushButton_29.clicked.connect(self.del_OP)
        self.ui.pushButton_20.clicked.connect(self.add_LF)
        self.ui.pushButton_19.clicked.connect(self.del_LF)
        self.ui.pushButton_11.clicked.connect(self.grid_S)
        self.ui.pushButton_111.clicked.connect(self.training)
        self.ui.pushButton_12.clicked.connect(self.apply_GS)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1190, 870)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_1.setGeometry(QtCore.QRect(130, 10, 75, 23))
        self.pushButton_1.setAutoFillBackground(False)
        self.pushButton_1.setObjectName("pushButton_1")
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setEnabled(True)
        self.label_1.setGeometry(QtCore.QRect(20, 10, 101, 16))
        self.label_1.setAutoFillBackground(True)
        self.label_1.setObjectName("label_1")
        self.listWidget_1 = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_1.setGeometry(QtCore.QRect(370, 30, 101, 171))
        self.listWidget_1.setObjectName("listWidget_1")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(395, 10, 47, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 191, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 60, 287, 13))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 100, 201, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(495, 5, 201, 170))
        self.label_5.setObjectName("label_5")
        self.comboBox_1 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_1.setGeometry(QtCore.QRect(40, 240, 141, 22))
        self.comboBox_1.setObjectName("comboBox_222")
        self.comboBox_222 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_222.setGeometry(QtCore.QRect(40, 210, 141, 22))
        self.comboBox_222.setObjectName("comboBox_222")
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(220, 240, 141, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(20, 240, 31, 16))
        self.label_6.setObjectName("label_666")
        self.label_666 = QtWidgets.QLabel(self.centralwidget)
        self.label_666.setGeometry(QtCore.QRect(20, 210, 31, 16))
        self.label_666.setObjectName("label_666")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(200, 240, 16, 16))
        self.label_7.setObjectName("label_7")
        self.comboBox_3 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_3.setGeometry(QtCore.QRect(460, 240, 81, 22))
        self.comboBox_3.setObjectName("comboBox_3")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(380, 240, 71, 20))
        self.label_8.setObjectName("label_8")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(210, 10, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_333 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_333.setGeometry(QtCore.QRect(290, 10, 60, 23))
        self.pushButton_333.setObjectName("pushButton_333")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(20, 120, 101, 16))
        self.label_9.setObjectName("label_9")
        self.label_99 = QtWidgets.QLabel(self.centralwidget)
        self.label_99.setGeometry(QtCore.QRect(20, 140, 151, 16))
        self.label_99.setObjectName("label_99")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(560, 240, 75, 23))
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(22, 329, 631, 491))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 280, 631, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBox_4 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_4.setGeometry(QtCore.QRect(850, 30, 81, 22))
        self.comboBox_4.setObjectName("comboBox_4")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(720, 30, 121, 22))
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(720, 10, 71, 16))
        self.label_10.setObjectName("label_10")
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(850, 10, 71, 16))
        self.label_14.setObjectName("label_14")
        self.comboBox.setObjectName("comboBox")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(940, 30, 131, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_9 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_9.setGeometry(QtCore.QRect(1080, 30, 81, 23))
        self.pushButton_9.setAutoFillBackground(False)
        self.pushButton_9.setObjectName("pushButton_9")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(780, 120, 47, 13))
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(920, 120, 47, 13))
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(1020, 90, 201, 216))
        self.label_13.setObjectName("label_13")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(720, 140, 61, 23))
        self.pushButton_2.setAutoFillBackground(False)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(870, 140, 61, 23))
        self.pushButton_5.setAutoFillBackground(False)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(790, 140, 61, 23))
        self.pushButton_6.setAutoFillBackground(False)
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(940, 140, 61, 23))
        self.pushButton_7.setAutoFillBackground(False)
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setGeometry(QtCore.QRect(1040, 140, 111, 23))
        self.pushButton_8.setAutoFillBackground(False)
        self.pushButton_8.setObjectName("pushButton_8")
        self.listWidget_2 = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_2.setGeometry(QtCore.QRect(720, 180, 131, 171))
        self.listWidget_2.setObjectName("listWidget_2")
        self.listWidget_3 = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_3.setGeometry(QtCore.QRect(870, 180, 131, 171))
        self.listWidget_3.setObjectName("listWidget_3")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(690, 90, 481, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(690, 815, 481, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(680, 100, 20, 726))
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setGeometry(QtCore.QRect(1160, 100, 20, 726))
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(1070, 480, 61, 22))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        self.label_15.setGeometry(QtCore.QRect(720, 380, 71, 16))
        self.label_15.setObjectName("label_15")
        self.pushButton_10 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_10.setGeometry(QtCore.QRect(790, 400, 81, 23))
        self.pushButton_10.setAutoFillBackground(False)
        self.pushButton_10.setObjectName("pushButton_10")
        self.label_16 = QtWidgets.QLabel(self.centralwidget)
        self.label_16.setGeometry(QtCore.QRect(900, 380, 101, 50))
        self.label_16.setObjectName("label_16")
        self.comboBox_5 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_5.setGeometry(QtCore.QRect(1050, 400, 101, 22))
        self.comboBox_5.setObjectName("comboBox_5")
        self.label_17 = QtWidgets.QLabel(self.centralwidget)
        self.label_17.setGeometry(QtCore.QRect(1050, 380, 71, 16))
        self.label_17.setObjectName("label_17")
        self.label_18 = QtWidgets.QLabel(self.centralwidget)
        self.label_18.setGeometry(QtCore.QRect(720, 445, 101, 31))
        self.label_18.setObjectName("label_18")
        self.label_19 = QtWidgets.QLabel(self.centralwidget)
        self.label_19.setGeometry(QtCore.QRect(830, 460, 71, 16))
        self.label_19.setObjectName("label_19")
        self.label_20 = QtWidgets.QLabel(self.centralwidget)
        self.label_20.setGeometry(QtCore.QRect(790, 440, 81, 41))
        self.label_20.setObjectName("label_20")
        self.comboBox_6 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_6.setGeometry(QtCore.QRect(720, 480, 61, 22))
        self.comboBox_6.setObjectName("comboBox_6")
        self.lineEdit_22 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_22.setGeometry(QtCore.QRect(790, 480, 61, 22))
        self.lineEdit_22.setObjectName("lineEdit_22")
        self.comboBox_8 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_8.setGeometry(QtCore.QRect(860, 480, 61, 22))
        self.comboBox_8.setObjectName("comboBox_8")
        self.label_21 = QtWidgets.QLabel(self.centralwidget)
        self.label_21.setGeometry(QtCore.QRect(870, 440, 81, 41))
        self.label_21.setObjectName("label_21")
        self.label_22 = QtWidgets.QLabel(self.centralwidget)
        self.label_22.setGeometry(QtCore.QRect(930, 440, 81, 41))
        self.label_22.setObjectName("label_22")
        self.comboBox_9 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_9.setGeometry(QtCore.QRect(930, 480, 61, 22))
        self.comboBox_9.setObjectName("comboBox_9")
        self.label_23 = QtWidgets.QLabel(self.centralwidget)
        self.label_23.setGeometry(QtCore.QRect(1070, 440, 81, 41))
        self.label_23.setObjectName("label_23")
        self.comboBox_10 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_10.setGeometry(QtCore.QRect(1000, 480, 61, 22))
        self.comboBox_10.setObjectName("comboBox_10")
        self.label_24 = QtWidgets.QLabel(self.centralwidget)
        self.label_24.setGeometry(QtCore.QRect(1000, 440, 81, 41))
        self.label_24.setObjectName("label_24")
        self.comboBox_11 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_11.setGeometry(QtCore.QRect(720, 400, 61, 22))
        self.comboBox_11.setObjectName("comboBox_11")
        self.pushButton_11 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_11.setGeometry(QtCore.QRect(880, 540, 81, 23))
        self.pushButton_11.setAutoFillBackground(False)
        self.pushButton_11.setObjectName("pushButton_11")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(830, 580, 211, 23))
        self.progressBar.setMaximum(0)
        self.progressBar.setProperty("value", -1)
        self.progressBar.setObjectName("progressBar")
        self.label_25 = QtWidgets.QLabel(self.centralwidget)
        self.label_25.setGeometry(QtCore.QRect(710, 615, 251, 256))
        self.label_25.setObjectName("label_25")
        self.pushButton_12 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_12.setGeometry(QtCore.QRect(1070, 680, 81, 23))
        self.pushButton_12.setAutoFillBackground(False)
        self.pushButton_12.setObjectName("pushButton_12")
        self.label_26 = QtWidgets.QLabel(self.centralwidget)
        self.label_26.setGeometry(QtCore.QRect(990, 640, 81, 41))
        self.label_26.setObjectName("label_26")
        self.comboBox_12 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_12.setGeometry(QtCore.QRect(990, 680, 71, 22))
        self.comboBox_12.setObjectName("comboBox_12")
        self.comboBox_13 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_13.setGeometry(QtCore.QRect(910, 680, 71, 22))
        self.comboBox_13.setObjectName("comboBox_13")
        self.label_27 = QtWidgets.QLabel(self.centralwidget)
        self.label_27.setGeometry(QtCore.QRect(910, 640, 81, 41))
        self.label_27.setObjectName("label_27")
        self.pushButton_13 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_13.setGeometry(QtCore.QRect(1070, 710, 81, 23))
        self.pushButton_13.setAutoFillBackground(False)
        self.pushButton_13.setObjectName("pushButton_13")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(640, 220, 51, 61))
        self.checkBox.setObjectName("checkBox_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 680, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuFile_2 = QtWidgets.QMenu(self.menubar)
        self.menuFile_2.setObjectName("menuFile_2")
        self.menuFile_3 = QtWidgets.QMenu(self.menubar)
        self.menuFile_3.setObjectName("menuFile_3")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionBox = QtWidgets.QAction(MainWindow)
        self.actionBox.setObjectName("actionBox")
        self.actionScatter = QtWidgets.QAction(MainWindow)
        self.actionScatter.setObjectName("actionScatter")
        self.actionModel = QtWidgets.QAction(MainWindow)
        self.actionModel.setObjectName("actionModel")
        self.actionModel_2 = QtWidgets.QAction(MainWindow)
        self.actionModel_2.setObjectName("actionModel_2")
        self.actionExpert = QtWidgets.QAction(MainWindow)
        self.actionExpert.setObjectName("actionExpert")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile_2.addAction(self.actionBox)
        self.menuFile_2.addAction(self.actionScatter)
        self.menuFile_3.addAction(self.actionExpert)
        self.menuFile_3.addAction(self.actionModel)
        self.menuFile_3.addAction(self.actionModel_2)
        self.menubar.addAction(self.menuFile_2.menuAction())
        self.menubar.addAction(self.menuFile_3.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


        self.filename = ''
        #self.df = []
        self.actionOpen.triggered.connect(self.getFile)
        self.pushButton_1.clicked.connect(self.getFile)
        self.pushButton_3.clicked.connect(self.show_table)
        self.pushButton_333.clicked.connect(self.combine)
        self.pushButton_9.clicked.connect(self.apply_filter)
        self.pushButton_10.clicked.connect(self.split)
        self.listWidget_1.itemClicked.connect(self.describe)
        self.comboBox_1.activated.connect(self.plot_para)
        self.comboBox_2.activated.connect(self.plot_para)
        self.comboBox_3.activated.connect(self.plot_para)
        self.comboBox_4.activated.connect(self.check)
        self.comboBox_12.activated.connect(self.check)
        self.pushButton_4.clicked.connect(self.update)
        self.pushButton_2.clicked.connect(self.add_input)
        self.pushButton_5.clicked.connect(self.add_output)
        self.pushButton_6.clicked.connect(self.del_input)
        self.pushButton_7.clicked.connect(self.del_output)
        self.pushButton_8.clicked.connect(self.create_dataset)
        self.pushButton_11.clicked.connect(self.q_bar)
        self.pushButton_12.clicked.connect(self.plot_result)
        self.pushButton_13.clicked.connect(self.compare)
        self.pushButton_3.setEnabled(False)
        self.pushButton_333.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        self.pushButton_9.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        self.pushButton_5.setEnabled(False)
        self.pushButton_8.setEnabled(False)
        self.pushButton_10.setEnabled(False)
        self.actionScatter.setEnabled(False)
        self.actionBox.setEnabled(False)
        self.actionModel.setEnabled(False)
        self.actionExpert.setEnabled(False)
        self.lineEdit.setEnabled(False)
        self.comboBox_11.setEnabled(False)
        self.comboBox_5.setEnabled(False)
        self.comboBox_6.setVisible(False)
        self.lineEdit_22.setVisible(False)
        self.comboBox_8.setVisible(False)
        self.comboBox_9.setVisible(False)
        self.comboBox_10.setVisible(False)
        self.lineEdit_2.setVisible(False)
        self.label_18.setVisible(False)
        self.label_20.setVisible(False)
        self.label_21.setVisible(False)
        self.label_22.setVisible(False)
        self.label_23.setVisible(False)
        self.label_24.setVisible(False)
        self.pushButton_11.setVisible(False)
        self.progressBar.setVisible(False)
        self.label_26.setVisible(False)
        self.comboBox_12.setVisible(False)
        self.label_27.setVisible(False)
        self.comboBox_13.setVisible(False)
        self.pushButton_12.setVisible(False)
        self.pushButton_13.setVisible(False)
        self.checkBox.setVisible(False)
        self.label_666.setVisible(False)
        self.comboBox_222.setVisible(False)


        self.actionExit.triggered.connect(MainWindow.close)
        self.actionScatter.triggered.connect(self.scatter)
        self.actionBox.triggered.connect(self.box_plot)
        self.actionModel.triggered.connect(self.save_model)
        self.actionModel_2.triggered.connect(self.load_my_model)
        self.actionExpert.triggered.connect(self.open_window)
        self.actionExpert.triggered.connect(self.enable)

    def enable(self):
        self.pushButton_11.setEnabled(False)
        self.pushButton_12.setEnabled(False)
        self.pushButton_13.setEnabled(False)

    def combine(self):
        import os
        self.filename = QFileDialog.getOpenFileName(filter="csv (*.csv)")[0]
        if self.filename:
            base_name = os.path.basename(self.filename)
            self.Title = "Combined CSV ({})".format(os.path.splitext(base_name)[0])
            self.pushButton_3.setEnabled(True)
            self.pushButton_333.setEnabled(True)
            self.pushButton_4.setEnabled(True)
            self.pushButton_9.setEnabled(True)
            self.pushButton_2.setEnabled(True)
            self.pushButton_5.setEnabled(True)
            self.checkBox.setVisible(True)
            self.actionScatter.setEnabled(True)
            self.actionBox.setEnabled(True)
            if self.listWidget_1:
                self.listWidget_1.clear()
                self.listWidget_2.clear()
                self.listWidget_3.clear()
                self.comboBox_1.clear()
                self.comboBox_222.clear()
                self.comboBox_2.clear()
                self.comboBox_3.clear()
                self.comboBox.clear()
                self.comboBox_4.clear()
                self.lineEdit.clear()
            self.df_new = pd.read_csv(self.filename, encoding='utf-8')
            self.df = pd.concat([self.df, self.df_new],ignore_index=True)
            self.print_info()
            self.plot_para()
            self.check()

    def apply_GS(self):
        self.confusion_1=[]
        self.df_ML = pd.DataFrame()
        try:
            self.X_data = self.X_test
            self.y_data = self.y_test
        except:
            if self.scaler:
                self.X_data = self.scaler.fit_transform(self.X_data.reshape(-1, self.listWidget_2.count()))
            else:
                pass
        if self.ui.listWidget_6.findItems('binary_crossentropy', Qt.MatchExactly):
            self.predictions = (self.model.predict(self.X_data) > 0.5).astype("int32")
            for i in range(self.y_data.shape[1]):
                globals()['self.pre_%s' % i] = []
                globals()['self.Y_%s' % i] = []
                globals()['self.Y_%s_%s' % (i, i)] = []
                for j in range(self.predictions.shape[0]):
                    if self.y_data.shape[1] == 1:
                        globals()['self.pre_%s' % i].append(self.predictions[j])
                        globals()['self.Y_%s' % i].append(self.y_data[j][i])
                        globals()['self.Y_%s_%s' % (i, i)].append(self.y_data[j][i])
                    else:
                        globals()['self.pre_%s' % i].append(self.predictions[j][i])
                        globals()['self.Y_%s' % i].append(self.y_data[j][i])
                        globals()['self.Y_%s_%s' % (i, i)].append(self.y_data[j][i])
                self.df_ML['pre_%s' % i] = globals()['self.pre_%s' % i]
                self.df_ML['Y_%s' % i] = globals()['self.Y_%s' % i]
                self.df_ML['Y_%s_%s' % (i, i)] = globals()['self.Y_%s_%s' % (i, i)]
            try:
                self.X_data = self.X_test_2
            except:
                pass
            for i in range(self.X_data.shape[1]):
                globals()['self.X_%s' % i] = []
                for j in range(self.X_data.shape[0]):
                    globals()['self.X_%s' % i].append(self.X_data[j][i])
                self.df_ML[self.listWidget_2.item(i).text()] = globals()['self.X_%s' % i]
            self.df_ML.columns = self.df_ML.columns.str.strip()
            self.predictions = (self.model.predict(self.X_test) > 0.5).astype("int32")
            self.label_25.setText("Confusion matrix:\n{}".format(confusion_matrix(self.y_test, self.predictions))
                                    + "\nClassification report:\n{}".format(
                classification_report(self.y_test, self.predictions)))
            self.predictions = (self.model.predict(self.X_test) > 0.5).astype("int32")
            self.confusion_1 = confusion_matrix(self.y_test, self.predictions)
        elif self.ui.listWidget_6.findItems('categorical_crossentropy', Qt.MatchExactly):
            self.predictions = np.argmax(self.model.predict(self.X_data), axis=-1)
            for i in range(self.y_data.shape[1]):
                globals()['self.pre_%s' % i] = []
                globals()['self.Y_%s' % i] = []
                globals()['self.Y_%s_%s' % (i, i)] = []
                for j in range(self.predictions.shape[0]):
                    if self.y_data.shape[1] == 1:
                        globals()['self.pre_%s' % i].append(self.predictions[j])
                        globals()['self.Y_%s' % i].append(self.y_data[j][i])
                        globals()['self.Y_%s_%s' % (i, i)].append(self.y_data[j][i])
                    else:
                        globals()['self.pre_%s' % i].append(self.predictions[j][i])
                        globals()['self.Y_%s' % i].append(self.y_data[j][i])
                        globals()['self.Y_%s_%s' % (i, i)].append(self.y_data[j][i])
                self.df_ML['pre_%s' % i] = globals()['self.pre_%s' % i]
                self.df_ML['Y_%s' % i] = globals()['self.Y_%s' % i]
                self.df_ML['Y_%s_%s' % (i, i)] = globals()['self.Y_%s_%s' % (i, i)]
            try:
                self.X_data = self.X_test_2
            except:
                pass
            for i in range(self.X_data.shape[1]):
                globals()['self.X_%s' % i] = []
                for j in range(self.X_data.shape[0]):
                    globals()['self.X_%s' % i].append(self.X_data[j][i])
                self.df_ML[self.listWidget_2.item(i).text()] = globals()['self.X_%s' % i]
            self.df_ML.columns = self.df_ML.columns.str.strip()
            self.predictions = np.argmax(self.model.predict(self.X_test), axis=-1)
            self.label_25.setText("Confusion matrix:\n{}".format(confusion_matrix(self.y_test, self.predictions))
                                    + "\nClassification report:\n{}".format(
                classification_report(self.y_test, self.predictions)))
            self.predictions = np.argmax(self.model.predict(self.X_test), axis=-1)
            self.confusion_1 = confusion_matrix(self.y_test, self.predictions)
        else:
            self.predictions = self.model.predict(self.X_data)
            for i in range(self.y_data.shape[1]):
                globals()['self.pre_%s' % i] = []
                globals()['self.Y_%s' % i] = []
                globals()['self.Y_%s_%s' % (i, i)] = []
                for j in range(self.predictions.shape[0]):
                    if self.y_data.shape[1] == 1:
                        globals()['self.pre_%s' % i].append(self.predictions[j])
                        globals()['self.Y_%s' % i].append(self.y_data[j][i])
                        globals()['self.Y_%s_%s' % (i, i)].append(self.y_data[j][i])
                    else:
                        globals()['self.pre_%s' % i].append(self.predictions[j][i])
                        globals()['self.Y_%s' % i].append(self.y_data[j][i])
                        globals()['self.Y_%s_%s' % (i, i)].append(self.y_data[j][i])
                self.df_ML['pre_%s' % i] = globals()['self.pre_%s' % i]
                self.df_ML['Y_%s' % i] = globals()['self.Y_%s' % i]
                self.df_ML['Y_%s_%s' % (i, i)] = globals()['self.Y_%s_%s' % (i, i)]
            try:
                self.X_data = self.X_test_2
            except:
                pass
            for i in range(self.X_data.shape[1]):
                globals()['self.X_%s' % i] = []
                for j in range(self.X_data.shape[0]):
                    globals()['self.X_%s' % i].append(self.X_data[j][i])
                self.df_ML[self.listWidget_2.item(i).text()] = globals()['self.X_%s' % i]
            self.df_ML.columns = self.df_ML.columns.str.strip()
            try:
                self.label_25.setText("Best score: %e" % self.grid_result.best_score_)
            except:
                self.label_25.setText("Training score: {}".format("{:e}".format(self.training_score))
                                      + "\nTest score: {}".format("{:e}".format(self.test_score)))
        self.label_26.setVisible(True)
        self.comboBox_12.setVisible(True)
        self.pushButton_12.setVisible(True)
        self.pushButton_13.setVisible(True)
        self.comboBox_13.setVisible(True)
        self.label_27.setVisible(True)
        self.comboBox_12.clear()
        self.comboBox_13.clear()
        self.comb12 = []
        for i in range(self.listWidget_2.count()):
            self.comb12.append(self.listWidget_2.item(i).text())
        self.comboBox_12.addItems(self.comb12)
        self.comboBox_12.addItem("None")
        self.comb13 = []
        for i in range(self.listWidget_3.count()):
            self.comb13.append(self.listWidget_3.item(i).text())
        self.comboBox_13.addItems(self.comb13)
        self.actionModel.setEnabled(True)
        try:
            if self.confusion_1.any():
                self.conf_plot()
        except:
            self.ML_plot()
        self.pushButton_12.setEnabled(True)
        self.pushButton_13.setEnabled(True)


    def scaling(self):
        if self.ui.comboBox_17.currentText() == "MinMax":
            self.scaler = MinMaxScaler()
            self.X_train = []
            self.X_test = []
            self.X_train = self.scaler.fit_transform(self.X_train_1)
            self.X_test = self.scaler.transform(self.X_test_1)
        elif self.ui.comboBox_17.currentText() == "Standard":
            self.scaler = StandardScaler()
            self.X_train = []
            self.X_test = []
            self.X_train = self.scaler.fit_transform(self.X_train_1)
            self.X_test = self.scaler.transform(self.X_test_1)
        elif self.ui.comboBox_17.currentText() == "Robust":
            self.scaler = RobustScaler()
            self.X_train = []
            self.X_test = []
            self.X_train = self.scaler.fit_transform(self.X_train_1)
            self.X_test = self.scaler.transform(self.X_test_1)
        else:
            self.scaler = None
            self.X_train = []
            self.X_test = []
            self.X_train = self.X_train_1
            self.X_test = self.X_test_1


    def baseline_model(self):
        def create_model(learning_rate=0.001, units_1=10, units_2=10,units_3=10,units_4=10,units_5=10,activ='relu', loss='mse', momentum=0, epsilon= 1e-7, hidden_layer = 1):
            self.Grid_model = Sequential()
            Units_list = [units_1,units_2,units_3,units_4,units_5]
            for i in range(hidden_layer):
                self.Grid_model.add(Dense(units=Units_list[i], activation=activ))
            if self.ui.listWidget_6.findItems("binary_crossentropy", Qt.MatchExactly):
                self.Grid_model.add(Dense(units=self.y_data.shape[1], activation='sigmoid'))
            elif self.ui.listWidget_6.findItems("categorical_crossentropy", Qt.MatchExactly):
                self.Grid_model.add(Dense(units=self.y_data.shape[1], activation='softmax'))
            else:
                self.Grid_model.add(Dense(units=self.y_data.shape[1]))
            if self.ui.listWidget_11.findItems("Adam", Qt.MatchExactly):
                opt = Adam(learning_rate=learning_rate, epsilon=epsilon)
            else:
                opt = SGD(learning_rate=learning_rate, momentum=momentum)
            self.Grid_model.compile(loss=loss, optimizer=opt)
            return self.Grid_model
        return create_model


    def wrap(self):
        self.wrap_model = KerasRegressor(build_fn=self.baseline_model(), batch_size=16, epochs=50, verbose=1)
        if self.ui.checkBox_3.isChecked() and self.ui.lineEdit_10.text():
            self.cv = KFold(n_splits=int(float(self.ui.lineEdit_10.text())), shuffle=False, random_state=None)
        else:
            self.cv = None
        self.grid = GridSearchCV(estimator=self.wrap_model, param_grid=self.param_grid, cv=self.cv)
        if self.ui.checkBox_4.isChecked() and self.ui.lineEdit_100.text():
            self.early_stop = EarlyStopping(monitor='val_loss', mode='min', verbose=1,
                                            patience=int(float(self.ui.lineEdit_100.text())))
            self.grid_result = self.grid.fit(self.X_train, self.y_train, validation_data=(self.X_test, self.y_test), callbacks=[self.early_stop])
        else:
            self.grid_result = self.grid.fit(self.X_train, self.y_train)
        self.model = self.grid

    def training(self):
        self.ui.progressBar.setVisible(False)
        if self.ui.listWidget_3 and self.ui.listWidget_4 and self.ui.listWidget_5 and self.ui.listWidget_6 and self.ui.listWidget_7 and self.ui.listWidget_8 and self.ui.listWidget_11:
            self.NEU ={'self.NEU_1' : [],'self.NEU_2' : [],'self.NEU_3' : [],'self.NEU_4' : [],'self.NEU_5' : []}
            A=str(self.ui.listWidget_4.item(0).text())
            B = A.split(',')
            C =[int(float(item)) for item in B]
            for i in range(len(C)):
                self.NEU[f'self.NEU_{i+1}'] = C[i]
            if len(C) ==  int(float(self.ui.listWidget_3.item(0).text())):
                if self.ui.listWidget_4.count() == 1:
                    if self.ui.checkBox.isChecked() and self.ui.listWidget_11.findItems("Adam", Qt.MatchExactly):
                        hidden_layer=int(float(self.ui.listWidget_3.item(0).text()))
                        units_1=self.NEU['self.NEU_1']
                        units_2=self.NEU['self.NEU_2']
                        units_3=self.NEU['self.NEU_3']
                        units_4=self.NEU['self.NEU_4']
                        units_5=self.NEU['self.NEU_5']
                        activ=self.ui.listWidget_5.item(0).text()
                        loss = self.ui.listWidget_6.item(0).text()
                        batch_size = int(float(self.ui.listWidget_7.item(0).text()))
                        epochs = int(float(self.ui.listWidget_8.item(0).text()))
                        learning_rate = float(self.ui.listWidget_9.item(0).text())
                        epsilon = float(self.ui.listWidget_10.item(0).text())
                    elif self.ui.checkBox.isChecked() and self.ui.listWidget_11.findItems("SGD", Qt.MatchExactly):
                        hidden_layer=int(float(self.ui.listWidget_3.item(0).text()))
                        units_1=self.NEU['self.NEU_1']
                        units_2=self.NEU['self.NEU_2']
                        units_3=self.NEU['self.NEU_3']
                        units_4=self.NEU['self.NEU_4']
                        units_5=self.NEU['self.NEU_5']
                        activ=self.ui.listWidget_5.item(0).text()
                        loss = self.ui.listWidget_6.item(0).text()
                        batch_size = int(float(self.ui.listWidget_7.item(0).text()))
                        epochs = int(float(self.ui.listWidget_8.item(0).text()))
                        learning_rate = float(self.ui.listWidget_9.item(0).text())
                        momentum = float(self.ui.listWidget_10.item(0).text())
                    else:
                        hidden_layer=int(float(self.ui.listWidget_3.item(0).text()))
                        units_1=self.NEU['self.NEU_1']
                        units_2=self.NEU['self.NEU_2']
                        units_3=self.NEU['self.NEU_3']
                        units_4=self.NEU['self.NEU_4']
                        units_5=self.NEU['self.NEU_5']
                        activ=self.ui.listWidget_5.item(0).text()
                        loss = self.ui.listWidget_6.item(0).text()
                        batch_size = int(float(self.ui.listWidget_7.item(0).text()))
                        epochs = int(float(self.ui.listWidget_8.item(0).text()))
                        learning_rate = 0.001
                        momentum = 0
                        epsilon = 1e-07
                self.scaling()
                self.model_2 = Sequential()
                Units_list = [units_1,units_2,units_3,units_4,units_5]
                for i in range(hidden_layer):
                    self.model_2.add(Dense(units=Units_list[i], activation=activ))
                if self.ui.listWidget_6.findItems("binary_crossentropy", Qt.MatchExactly):
                    self.model_2.add(Dense(units=self.y_data.shape[1], activation='sigmoid'))
                elif self.ui.listWidget_6.findItems("categorical_crossentropy", Qt.MatchExactly):
                    self.model_2.add(Dense(units=self.y_data.shape[1], activation='softmax'))
                else:
                    self.model_2.add(Dense(units=self.y_data.shape[1]))
                if self.ui.listWidget_11.findItems("Adam", Qt.MatchExactly):
                    opt = Adam(learning_rate=learning_rate, epsilon=epsilon)
                else:
                    opt = SGD(learning_rate=learning_rate, momentum=momentum)
                self.model_2.compile(loss=loss, optimizer=opt)
                if self.ui.checkBox_4.isChecked() and self.ui.lineEdit_100.text():
                    self.early_stop = EarlyStopping(monitor='val_loss', mode='min', verbose=1,
                                                    patience=int(float(self.ui.lineEdit_100.text())))
                    self.model_2.fit(self.X_train, self.y_train, validation_data=(self.X_test, self.y_test),
                                                     callbacks=[self.early_stop],batch_size=int(float(self.ui.listWidget_7.item(0).text())),epochs = int(float(self.ui.listWidget_8.item(0).text())))
                else:
                    self.model_2.fit(self.X_train, self.y_train,batch_size=int(float(self.ui.listWidget_7.item(0).text())),epochs = int(float(self.ui.listWidget_8.item(0).text())))
                self.model = self.model_2
                self.ui.progressBar.setMinimum(0)
                self.ui.progressBar.setMaximum(100)
                self.ui.progressBar.setValue(100)
                self.ui.progressBar.setVisible(True)
                self.training_score = self.model.evaluate(self.X_train, self.y_train, verbose=0,
                                              batch_size=int(float(self.ui.listWidget_7.item(0).text())))
                self.test_score = self.model.evaluate(self.X_test, self.y_test, verbose=0,
                                          batch_size=int(float(self.ui.listWidget_7.item(0).text())))
                if self.ui.checkBox_3.isChecked() and self.ui.lineEdit_10.text():
                    self.ui.textBrowser.setText("..................For using Kfold feature start a Gridsearch!..................")
                else:
                    self.ui.textBrowser.clear()
                self.ui.pushButton_12.setEnabled(True)
            else:
                pass
        else:
            pass


    def grid_S(self):
        try:
            self.grid_result.best_params_['loss']=[]
        except:
            pass
        try:
            self.grid_result.best_params_['activ']=[]
        except:
            pass
        if self.ui.listWidget_3 and self.ui.listWidget_4 and self.ui.listWidget_5 and self.ui.listWidget_6 and self.ui.listWidget_7 and self.ui.listWidget_8 and self.ui.listWidget_11:
            self.ui.progressBar.setVisible(False)
            if self.ui.listWidget_4.count() == int(float(self.ui.listWidget_3.item(0).text())):
                self.HL = []
                self.NEU ={'self.NEU_1' : [],'self.NEU_2' : [],'self.NEU_3' : [],'self.NEU_4' : [],'self.NEU_5' : []}
                self.AF = []
                self.OP = []
                self.LF = []
                self.BAT = []
                self.EPO = []
                self.LR = []
                self.EPS = []
                self.MOM = []

                for i in range(self.ui.listWidget_3.count()):
                    self.HL.append(int(float(self.ui.listWidget_3.item(i).text())))
                for i in range(self.ui.listWidget_4.count()):
                    A=str(self.ui.listWidget_4.item(i).text())
                    B = A.split(',')
                    C =[int(float(item)) for item in B]
                    self.NEU[f'self.NEU_{i+1}'] = C
                for i in range(self.ui.listWidget_7.count()):
                    self.BAT.append(int(float(self.ui.listWidget_7.item(i).text())))
                for i in range(self.ui.listWidget_8.count()):
                    self.EPO.append(int(float(self.ui.listWidget_8.item(i).text())))
                for i in range(self.ui.listWidget_9.count()):
                    self.LR.append(float(self.ui.listWidget_9.item(i).text()))
                for i in range(self.ui.listWidget_10.count()):
                    self.EPS.append(float(self.ui.listWidget_10.item(i).text()))
                for i in range(self.ui.listWidget_5.count()):
                    self.AF.append(self.ui.listWidget_5.item(i).text())
                for i in range(self.ui.listWidget_11.count()):
                    self.OP.append(self.ui.listWidget_11.item(i).text())
                for i in range(self.ui.listWidget_6.count()):
                    self.LF.append(self.ui.listWidget_6.item(i).text())

                if self.ui.listWidget_4.count() == 1:
                    if self.ui.checkBox.isChecked() and self.ui.listWidget_11.findItems("Adam", Qt.MatchExactly):
                        self.param_grid = dict(hidden_layer=self.HL, units_1=self.NEU['self.NEU_1'], activ=self.AF,
                                           loss = self.LF, batch_size = self.BAT, epochs = self.EPO, learning_rate = self.LR,
                                           epsilon = self.EPS)
                    elif self.ui.checkBox.isChecked() and self.ui.listWidget_11.findItems("SGD", Qt.MatchExactly):
                        self.param_grid = dict(hidden_layer=self.HL, units_1=self.NEU['self.NEU_1'], activ=self.AF,loss = self.LF, batch_size = self.BAT, epochs = self.EPO, learning_rate = self.LR, momentum = self.EPS)
                    else:
                        self.param_grid = dict(hidden_layer=self.HL, units_1=self.NEU['self.NEU_1'], activ=self.AF,
                                           loss = self.LF, batch_size = self.BAT, epochs = self.EPO)
                elif self.ui.listWidget_4.count() == 2:
                    if self.ui.checkBox.isChecked() and self.ui.listWidget_11.findItems("Adam", Qt.MatchExactly):
                        self.param_grid = dict(hidden_layer=self.HL, units_1=self.NEU['self.NEU_1'], units_2=self.NEU['self.NEU_2'], activ=self.AF,
                                           loss = self.LF, batch_size = self.BAT, epochs = self.EPO, learning_rate = self.LR,
                                           epsilon = self.EPS)
                    elif self.ui.checkBox.isChecked() and self.ui.listWidget_11.findItems("SGD", Qt.MatchExactly):
                        self.param_grid = dict(hidden_layer=self.HL, units_1=self.NEU['self.NEU_1'], units_2=self.NEU['self.NEU_2'],
                                               activ=self.AF,loss = self.LF, batch_size = self.BAT, epochs = self.EPO, learning_rate = self.LR, momentum = self.EPS)
                    else:
                        self.param_grid = dict(hidden_layer=self.HL, units_1=self.NEU['self.NEU_1'], units_2=self.NEU['self.NEU_2'], activ=self.AF,
                                           loss = self.LF, batch_size = self.BAT, epochs = self.EPO)
                elif self.ui.listWidget_4.count() == 3:
                    if self.ui.checkBox.isChecked() and self.ui.listWidget_11.findItems("Adam", Qt.MatchExactly):
                        self.param_grid = dict(hidden_layer=self.HL, units_1=self.NEU['self.NEU_1'], units_2=self.NEU['self.NEU_2'], units_3=self.NEU['self.NEU_3']
                                               , activ=self.AF,
                                           loss = self.LF, batch_size = self.BAT, epochs = self.EPO, learning_rate = self.LR,
                                           epsilon = self.EPS)
                    elif self.ui.checkBox.isChecked() and self.ui.listWidget_11.findItems("SGD", Qt.MatchExactly):
                        self.param_grid = dict(hidden_layer=self.HL, units_1=self.NEU['self.NEU_1'], units_2=self.NEU['self.NEU_2'], units_3=self.NEU['self.NEU_3'],
                                               activ=self.AF,loss = self.LF, batch_size = self.BAT, epochs = self.EPO, learning_rate = self.LR, momentum = self.EPS)
                    else:
                        self.param_grid = dict(hidden_layer=self.HL, units_1=self.NEU['self.NEU_1'], units_2=self.NEU['self.NEU_2'], units_3=self.NEU['self.NEU_3'],
                                               activ=self.AF,
                                           loss = self.LF, batch_size = self.BAT, epochs = self.EPO)
                elif self.ui.listWidget_4.count() == 4:
                    if self.ui.checkBox.isChecked() and self.ui.listWidget_11.findItems("Adam", Qt.MatchExactly):
                        self.param_grid = dict(hidden_layer=self.HL, units_1=self.NEU['self.NEU_1'], units_2=self.NEU['self.NEU_2'], units_3=self.NEU['self.NEU_3'],
                                               units_4=self.NEU['self.NEU_4'], activ=self.AF,
                                           loss = self.LF, batch_size = self.BAT, epochs = self.EPO, learning_rate = self.LR,
                                           epsilon = self.EPS)
                    elif self.ui.checkBox.isChecked() and self.ui.listWidget_11.findItems("SGD", Qt.MatchExactly):
                        self.param_grid = dict(hidden_layer=self.HL, units_1=self.NEU['self.NEU_1'], units_2=self.NEU['self.NEU_2'], units_3=self.NEU['self.NEU_3'],
                                               units_4=self.NEU['self.NEU_4'],
                                               activ=self.AF,loss = self.LF, batch_size = self.BAT, epochs = self.EPO, learning_rate = self.LR, momentum = self.EPS)
                    else:
                        self.param_grid = dict(hidden_layer=self.HL, units_1=self.NEU['self.NEU_1'], units_2=self.NEU['self.NEU_2'], units_3=self.NEU['self.NEU_3'],
                                               units_4=self.NEU['self.NEU_4'], activ=self.AF,
                                           loss = self.LF, batch_size = self.BAT, epochs = self.EPO)
                elif self.ui.listWidget_4.count() == 5:
                    if self.ui.checkBox.isChecked() and self.ui.listWidget_11.findItems("Adam", Qt.MatchExactly):
                        self.param_grid = dict(hidden_layer=self.HL, units_1=self.NEU['self.NEU_1'], units_2=self.NEU['self.NEU_2'], units_3=self.NEU['self.NEU_3'],
                                               units_4=self.NEU['self.NEU_4'], units_5=self.NEU['self.NEU_5'], activ=self.AF,
                                           loss = self.LF, batch_size = self.BAT, epochs = self.EPO, learning_rate = self.LR,
                                           epsilon = self.EPS)
                    elif self.ui.checkBox.isChecked() and self.ui.listWidget_11.findItems("SGD", Qt.MatchExactly):
                        self.param_grid = dict(hidden_layer=self.HL, units_1=self.NEU['self.NEU_1'], units_2=self.NEU['self.NEU_2'], units_3=self.NEU['self.NEU_3'],
                                               units_4=self.NEU['self.NEU_4'], units_5=self.NEU['self.NEU_5'],
                                               activ=self.AF,loss = self.LF, batch_size = self.BAT, epochs = self.EPO, learning_rate = self.LR, momentum = self.EPS)
                    else:
                        self.param_grid = dict(hidden_layer=self.HL, units_1=self.NEU['self.NEU_1'], units_2=self.NEU['self.NEU_2'], units_3=self.NEU['self.NEU_3'],
                                               units_4=self.NEU['self.NEU_4'], units_5=self.NEU['self.NEU_5'], activ=self.AF,
                                           loss = self.LF, batch_size = self.BAT, epochs = self.EPO)
                self.scaling()
                self.baseline_model()
                self.wrap()
                self.ui.progressBar.setMinimum(0)
                self.ui.progressBar.setMaximum(100)
                self.ui.progressBar.setValue(100)
                self.ui.progressBar.setVisible(True)
                self.ui.textBrowser.setText(
                    "Best: %e using %s" % (self.grid_result.best_score_, self.grid_result.best_params_))
                means = self.grid_result.cv_results_['mean_test_score']
                stds = self.grid_result.cv_results_['std_test_score']
                params = self.grid_result.cv_results_['params']
                for mean, stdev, param in zip(means, stds, params):
                    self.ui.textBrowser.append("%e with: %r" % (mean, param))
                print("Best: %e using %s" % (self.grid_result.best_score_, self.grid_result.best_params_))
                self.ui.pushButton_12.setEnabled(True)
            else:
                pass
        else:
            pass


    def add_LF(self):
        if self.ui.listWidget_6.findItems(self.ui.comboBox_13.currentText(), Qt.MatchExactly):
            pass
        elif self.ui.comboBox_13.currentText():
            self.item_inp = self.ui.comboBox_13.currentText()
            self.ui.listWidget_6.addItem(self.item_inp)
        else:
            pass

    def del_LF(self):
        self.item_inp_del = self.ui.listWidget_6.currentRow()
        self.ui.listWidget_6.takeItem(self.item_inp_del)

    def add_OP(self):
        if self.ui.listWidget_11.findItems(self.ui.comboBox_14.currentText(), Qt.MatchExactly) or self.ui.listWidget_11:
            pass
        elif self.ui.comboBox_14.currentText():
            self.item_inp = self.ui.comboBox_14.currentText()
            self.ui.listWidget_11.addItem(self.item_inp)
        else:
            pass

    def del_OP(self):
        self.item_inp_del = self.ui.listWidget_11.currentRow()
        self.ui.listWidget_11.takeItem(self.item_inp_del)

    def add_AF(self):
        if self.ui.listWidget_5.findItems(self.ui.comboBox_12.currentText(), Qt.MatchExactly):
            pass
        elif self.ui.comboBox_12.currentText():
            self.item_inp = self.ui.comboBox_12.currentText()
            self.ui.listWidget_5.addItem(self.item_inp)
        else:
            pass

    def del_AF(self):
        self.item_inp_del = self.ui.listWidget_5.currentRow()
        self.ui.listWidget_5.takeItem(self.item_inp_del)

    def add_HL(self):
        if self.ui.listWidget_3.findItems(self.ui.comboBox_32.currentText(), Qt.MatchExactly):
            pass
        elif self.ui.comboBox_32.currentText():
            self.item_inp = self.ui.comboBox_32.currentText()
            self.ui.listWidget_3.addItem(self.item_inp)
            self.ui.pushButton_13.setEnabled(False)
        else:
            pass

    def del_HL(self):
        if self.ui.listWidget_3:
            self.item_inp_del = self.ui.listWidget_3.currentRow()
            self.ui.listWidget_3.takeItem(self.item_inp_del)
            if not self.ui.listWidget_3:
                self.ui.pushButton_13.setEnabled(True)

    def add_NEU(self):
        if self.ui.lineEdit_3.text():
            self.item_inp = self.ui.lineEdit_3.text()
            self.ui.listWidget_4.addItem(self.item_inp)
            self.ui.lineEdit_3.clear()
        else:
            pass

    def del_NEU(self):
        self.item_inp_del = self.ui.listWidget_4.currentRow()
        self.ui.listWidget_4.takeItem(self.item_inp_del)

    def add_BAT(self):
        if self.ui.listWidget_7.findItems(self.ui.lineEdit_6.text(), Qt.MatchExactly):
            pass
        elif self.ui.lineEdit_6.text():
            self.item_inp = self.ui.lineEdit_6.text()
            self.ui.listWidget_7.addItem(self.item_inp)
            self.ui.lineEdit_6.clear()
        else:
            pass

    def del_BAT(self):
        self.item_inp_del = self.ui.listWidget_7.currentRow()
        self.ui.listWidget_7.takeItem(self.item_inp_del)

    def add_EPO(self):
        if self.ui.listWidget_8.findItems(self.ui.lineEdit_7.text(), Qt.MatchExactly):
            pass
        elif self.ui.lineEdit_7.text():
            self.item_inp = self.ui.lineEdit_7.text()
            self.ui.listWidget_8.addItem(self.item_inp)
            self.ui.lineEdit_7.clear()
        else:
            pass

    def del_EPO(self):
        self.item_inp_del = self.ui.listWidget_8.currentRow()
        self.ui.listWidget_8.takeItem(self.item_inp_del)

    def add_LR(self):
        if self.ui.listWidget_9.findItems(self.ui.lineEdit_8.text(), Qt.MatchExactly):
            pass
        elif self.ui.lineEdit_8.text():
            self.item_inp = self.ui.lineEdit_8.text()
            self.ui.listWidget_9.addItem(self.item_inp)
            self.ui.lineEdit_8.clear()
        else:
            pass

    def del_LR(self):
        self.item_inp_del = self.ui.listWidget_9.currentRow()
        self.ui.listWidget_9.takeItem(self.item_inp_del)

    def add_EPS(self):
        if self.ui.listWidget_10.findItems(self.ui.lineEdit_9.text(), Qt.MatchExactly):
            pass
        elif self.ui.lineEdit_9.text():
            self.item_inp = self.ui.lineEdit_9.text()
            self.ui.listWidget_10.addItem(self.item_inp)
            self.ui.lineEdit_9.clear()
        else:
            pass

    def del_EPS(self):
        self.item_inp_del = self.ui.listWidget_10.currentRow()
        self.ui.listWidget_10.takeItem(self.item_inp_del)


    def load_my_model(self):
            self.loadfilename = QFileDialog.getOpenFileName(filter="h5 (*.h5)")[0]
            if self.loadfilename:
                base_name = os.path.basename(self.loadfilename)
                self.name = os.path.splitext(base_name)[0]
                self.model = load_model(self.loadfilename)
                try:
                    self.scaler = pickle.load(open(f'{self.name}_scaler.pkl', 'rb'))
                    scaler_info = f"Scaler function was loaded as {self.name}_scaler.pkl"
                except:
                    scaler_info = "Warning! Please load the scaler function."
                self.messagebox_1 = QtWidgets.QMessageBox()
                self.messagebox_1.setIcon(QtWidgets.QMessageBox.Information)
                self.messagebox_1.setWindowTitle("Load Model")
                self.messagebox_1.setText(f"{base_name} was loaded\n\n{scaler_info}")
                stream = io.StringIO()
                self.model.summary(print_fn=lambda x: stream.write(x + '\n'))
                summary_string = stream.getvalue()
                stream.close()
                self.messagebox_1.setDetailedText(f"{summary_string}\n\nInput shape = {self.model.input_shape}")
                self.messagebox_1.setStandardButtons(QtWidgets.QMessageBox.Ok)
                self.messagebox_1.exec_()
                self.label_26.setVisible(True)
                self.comboBox_12.setVisible(True)
                self.pushButton_12.setVisible(True)
                self.pushButton_13.setVisible(True)
                self.comboBox_13.setVisible(True)
                self.label_27.setVisible(True)
                self.comboBox_12.clear()
                self.comboBox_13.clear()
                self.comb12 = []
                for i in range(self.listWidget_2.count()):
                    self.comb12.append(self.listWidget_2.item(i).text())
                self.comboBox_12.addItems(self.comb12)
                self.comboBox_12.addItem("None")
                self.comb13 = []
                for i in range(self.listWidget_3.count()):
                    self.comb13.append(self.listWidget_3.item(i).text())
                self.comboBox_13.addItems(self.comb13)
                self.actionModel.setEnabled(True)

    def save_model(self):
        self.savefilename = QFileDialog.getSaveFileName(None, "", "", "h5 (*.h5)")[0]
        if self.savefilename:
            base_name = os.path.basename(self.savefilename)
            self.name = os.path.splitext(base_name)[0]
            try:
                self.model.save(self.name + ".h5")
                pickle.dump(self.scaler, open(f'{self.name}_scaler.pkl', 'wb'))
                self.messagebox_1 = QtWidgets.QMessageBox()
                self.messagebox_1.setIcon(QtWidgets.QMessageBox.Information)
                self.messagebox_1.setWindowTitle("Save Model")
                self.messagebox_1.setText(f"Model was saved as {self.name}.h5\n\nScaler function was saved as {self.name}_scaler.pkl")
                self.messagebox_1.setStandardButtons(QtWidgets.QMessageBox.Ok)
                self.messagebox_1.exec_()
            except:
                with open(f'{self.name}.pkl', 'wb') as f:
                    pickle.dump(self.grid_result.cv_results_, f)
                    self.messagebox_1 = QtWidgets.QMessageBox()
                    self.messagebox_1.setIcon(QtWidgets.QMessageBox.Information)
                    self.messagebox_1.setWindowTitle("Save Model")
                    self.messagebox_1.setText(f"Gridsearch results were saved as Gridsearch_{self.name}.pkl")
                    self.messagebox_1.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    self.messagebox_1.exec_()

    def compare(self):
        self.df_ML = pd.DataFrame()
        try:
            self.X_data = self.X_test
            self.y_data = self.y_test
        except:
            if self.scaler:
                self.X_data = self.scaler.fit_transform(self.X_data.reshape(-1, self.listWidget_2.count()))
            else:
                pass
        try:
            if self.grid_result.best_params_['loss'] == 'binary_crossentropy':
                self.predictions = (self.model.predict(self.X_data) > 0.5).astype("int32")
                for i in range(self.y_data.shape[1]):
                    globals()['self.pre_%s' % i] = []
                    globals()['self.Y_%s' % i] = []
                    globals()['self.Y_%s_%s' % (i, i)] = []
                    for j in range(self.predictions.shape[0]):
                        if self.y_data.shape[1] == 1:
                            globals()['self.pre_%s' % i].append(self.predictions[j])
                            globals()['self.Y_%s' % i].append(self.y_data[j][i])
                            globals()['self.Y_%s_%s' % (i, i)].append(self.y_data[j][i])
                        else:
                            globals()['self.pre_%s' % i].append(self.predictions[j][i])
                            globals()['self.Y_%s' % i].append(self.y_data[j][i])
                            globals()['self.Y_%s_%s' % (i, i)].append(self.y_data[j][i])
                    self.df_ML['pre_%s' % i] = globals()['self.pre_%s' % i]
                    self.df_ML['Y_%s' % i] = globals()['self.Y_%s' % i]
                    self.df_ML['Y_%s_%s' % (i, i)] = globals()['self.Y_%s_%s' % (i, i)]
                try:
                    self.X_data = self.X_test_2
                except:
                    pass
                for i in range(self.X_data.shape[1]):
                    globals()['self.X_%s' % i] = []
                    for j in range(self.X_data.shape[0]):
                        globals()['self.X_%s' % i].append(self.X_data[j][i])
                    self.df_ML[self.listWidget_2.item(i).text()] = globals()['self.X_%s' % i]
                self.df_ML.columns = self.df_ML.columns.str.strip()
            elif self.grid_result.best_params_['loss'] == 'categorical_crossentropy':
                self.predictions = np.argmax(self.model.predict(self.X_data), axis=-1)
                for i in range(self.y_data.shape[1]):
                    globals()['self.pre_%s' % i] = []
                    globals()['self.Y_%s' % i] = []
                    globals()['self.Y_%s_%s' % (i, i)] = []
                    for j in range(self.predictions.shape[0]):
                        if self.y_data.shape[1] == 1:
                            globals()['self.pre_%s' % i].append(self.predictions[j])
                            globals()['self.Y_%s' % i].append(self.y_data[j][i])
                            globals()['self.Y_%s_%s' % (i, i)].append(self.y_data[j][i])
                        else:
                            globals()['self.pre_%s' % i].append(self.predictions[j][i])
                            globals()['self.Y_%s' % i].append(self.y_data[j][i])
                            globals()['self.Y_%s_%s' % (i, i)].append(self.y_data[j][i])
                    self.df_ML['pre_%s' % i] = globals()['self.pre_%s' % i]
                    self.df_ML['Y_%s' % i] = globals()['self.Y_%s' % i]
                    self.df_ML['Y_%s_%s' % (i, i)] = globals()['self.Y_%s_%s' % (i, i)]
                try:
                    self.X_data = self.X_test_2
                except:
                    pass
                for i in range(self.X_data.shape[1]):
                    globals()['self.X_%s' % i] = []
                    for j in range(self.X_data.shape[0]):
                        globals()['self.X_%s' % i].append(self.X_data[j][i])
                    self.df_ML[self.listWidget_2.item(i).text()] = globals()['self.X_%s' % i]
                self.df_ML.columns = self.df_ML.columns.str.strip()
            elif self.grid_result.best_params_['activ']:
                self.predictions = self.model.predict(self.X_data)
                for i in range(self.y_data.shape[1]):
                    globals()['self.pre_%s' % i] = []
                    globals()['self.Y_%s' % i] = []
                    globals()['self.Y_%s_%s' % (i, i)] = []
                    for j in range(self.predictions.shape[0]):
                        if self.y_data.shape[1] == 1:
                            globals()['self.pre_%s' % i].append(self.predictions[j])
                            globals()['self.Y_%s' % i].append(self.y_data[j][i])
                            globals()['self.Y_%s_%s' % (i, i)].append(self.y_data[j][i])
                        else:
                            globals()['self.pre_%s' % i].append(self.predictions[j][i])
                            globals()['self.Y_%s' % i].append(self.y_data[j][i])
                            globals()['self.Y_%s_%s' % (i, i)].append(self.y_data[j][i])
                    self.df_ML['pre_%s' % i] = globals()['self.pre_%s' % i]
                    self.df_ML['Y_%s' % i] = globals()['self.Y_%s' % i]
                    self.df_ML['Y_%s_%s' % (i, i)] = globals()['self.Y_%s_%s' % (i, i)]
                try:
                    self.X_data = self.X_test_2
                except:
                    pass
                for i in range(self.X_data.shape[1]):
                    globals()['self.X_%s' % i] = []
                    for j in range(self.X_data.shape[0]):
                        globals()['self.X_%s' % i].append(self.X_data[j][i])
                    self.df_ML[self.listWidget_2.item(i).text()] = globals()['self.X_%s' % i]
                self.df_ML.columns = self.df_ML.columns.str.strip()
        except:
            try:
                if self.ui.listWidget_6.findItems('binary_crossentropy', Qt.MatchExactly):
                    self.predictions = (self.model.predict(self.X_data) > 0.5).astype("int32")
                    for i in range(self.y_data.shape[1]):
                        globals()['self.pre_%s' % i] = []
                        globals()['self.Y_%s' % i] = []
                        globals()['self.Y_%s_%s' % (i, i)] = []
                        for j in range(self.predictions.shape[0]):
                            if self.y_data.shape[1] == 1:
                                globals()['self.pre_%s' % i].append(self.predictions[j])
                                globals()['self.Y_%s' % i].append(self.y_data[j][i])
                                globals()['self.Y_%s_%s' % (i, i)].append(self.y_data[j][i])
                            else:
                                globals()['self.pre_%s' % i].append(self.predictions[j][i])
                                globals()['self.Y_%s' % i].append(self.y_data[j][i])
                                globals()['self.Y_%s_%s' % (i, i)].append(self.y_data[j][i])
                        self.df_ML['pre_%s' % i] = globals()['self.pre_%s' % i]
                        self.df_ML['Y_%s' % i] = globals()['self.Y_%s' % i]
                        self.df_ML['Y_%s_%s' % (i, i)] = globals()['self.Y_%s_%s' % (i, i)]
                    try:
                        self.X_data = self.X_test_2
                    except:
                        pass
                    for i in range(self.X_data.shape[1]):
                        globals()['self.X_%s' % i] = []
                        for j in range(self.X_data.shape[0]):
                            globals()['self.X_%s' % i].append(self.X_data[j][i])
                        self.df_ML[self.listWidget_2.item(i).text()] = globals()['self.X_%s' % i]
                    self.df_ML.columns = self.df_ML.columns.str.strip()
                elif self.ui.listWidget_6.findItems('categorical_crossentropy', Qt.MatchExactly):
                    self.predictions = np.argmax(self.model.predict(self.X_data), axis=-1)
                    for i in range(self.y_data.shape[1]):
                        globals()['self.pre_%s' % i] = []
                        globals()['self.Y_%s' % i] = []
                        globals()['self.Y_%s_%s' % (i, i)] = []
                        for j in range(self.predictions.shape[0]):
                            if self.y_data.shape[1] == 1:
                                globals()['self.pre_%s' % i].append(self.predictions[j])
                                globals()['self.Y_%s' % i].append(self.y_data[j][i])
                                globals()['self.Y_%s_%s' % (i, i)].append(self.y_data[j][i])
                            else:
                                globals()['self.pre_%s' % i].append(self.predictions[j][i])
                                globals()['self.Y_%s' % i].append(self.y_data[j][i])
                                globals()['self.Y_%s_%s' % (i, i)].append(self.y_data[j][i])
                        self.df_ML['pre_%s' % i] = globals()['self.pre_%s' % i]
                        self.df_ML['Y_%s' % i] = globals()['self.Y_%s' % i]
                        self.df_ML['Y_%s_%s' % (i, i)] = globals()['self.Y_%s_%s' % (i, i)]
                    try:
                        self.X_data = self.X_test_2
                    except:
                        pass
                    for i in range(self.X_data.shape[1]):
                        globals()['self.X_%s' % i] = []
                        for j in range(self.X_data.shape[0]):
                            globals()['self.X_%s' % i].append(self.X_data[j][i])
                        self.df_ML[self.listWidget_2.item(i).text()] = globals()['self.X_%s' % i]
                    self.df_ML.columns = self.df_ML.columns.str.strip()
                elif self.ui.listWidget_6.findItems('mse', Qt.MatchExactly) or self.ui.listWidget_6.findItems('mae', Qt.MatchExactly):
                    self.predictions = self.model.predict(self.X_data)
                    for i in range(self.y_data.shape[1]):
                        globals()['self.pre_%s' % i] = []
                        globals()['self.Y_%s' % i] = []
                        globals()['self.Y_%s_%s' % (i, i)] = []
                        for j in range(self.predictions.shape[0]):
                            if self.y_data.shape[1] == 1:
                                globals()['self.pre_%s' % i].append(self.predictions[j])
                                globals()['self.Y_%s' % i].append(self.y_data[j][i])
                                globals()['self.Y_%s_%s' % (i, i)].append(self.y_data[j][i])
                            else:
                                globals()['self.pre_%s' % i].append(self.predictions[j][i])
                                globals()['self.Y_%s' % i].append(self.y_data[j][i])
                                globals()['self.Y_%s_%s' % (i, i)].append(self.y_data[j][i])
                        self.df_ML['pre_%s' % i] = globals()['self.pre_%s' % i]
                        self.df_ML['Y_%s' % i] = globals()['self.Y_%s' % i]
                        self.df_ML['Y_%s_%s' % (i, i)] = globals()['self.Y_%s_%s' % (i, i)]
                    try:
                        self.X_data = self.X_test_2
                    except:
                        pass
                    for i in range(self.X_data.shape[1]):
                        globals()['self.X_%s' % i] = []
                        for j in range(self.X_data.shape[0]):
                            globals()['self.X_%s' % i].append(self.X_data[j][i])
                        self.df_ML[self.listWidget_2.item(i).text()] = globals()['self.X_%s' % i]
                    self.df_ML.columns = self.df_ML.columns.str.strip()
            except:
                if self.comboBox_9.currentText() != 'binary_crossentropy':
                    self.predictions = self.model.predict(self.X_data)
                    for i in range(self.y_data.shape[1]):
                        globals()['self.pre_%s' % i] = []
                        globals()['self.Y_%s' % i] = []
                        globals()['self.Y_%s_%s' % (i, i)] = []
                        for j in range(self.predictions.shape[0]):
                            if self.y_data.shape[1] == 1:
                                globals()['self.pre_%s' % i].append(self.predictions[j])
                                globals()['self.Y_%s' % i].append(self.y_data[j][i])
                                globals()['self.Y_%s_%s' % (i, i)].append(self.y_data[j][i])
                            else:
                                globals()['self.pre_%s' % i].append(self.predictions[j][i])
                                globals()['self.Y_%s' % i].append(self.y_data[j][i])
                                globals()['self.Y_%s_%s' % (i, i)].append(self.y_data[j][i])
                        self.df_ML['pre_%s' % i] = globals()['self.pre_%s' % i]
                        self.df_ML['Y_%s' % i] = globals()['self.Y_%s' % i]
                        self.df_ML['Y_%s_%s' % (i, i)] = globals()['self.Y_%s_%s' % (i, i)]
                    try:
                        self.X_data = self.X_test_2
                    except:
                        pass
                    for i in range(self.X_data.shape[1]):
                        globals()['self.X_%s' % i] = []
                        for j in range(self.X_data.shape[0]):
                            globals()['self.X_%s' % i].append(self.X_data[j][i])
                        self.df_ML[self.listWidget_2.item(i).text()] = globals()['self.X_%s' % i]
                    self.df_ML.columns = self.df_ML.columns.str.strip()
                else:
                    self.predictions = (self.model.predict(self.X_data) > 0.5).astype("int32")
                    for i in range(self.y_data.shape[1]):
                        globals()['self.pre_%s' % i] = []
                        globals()['self.Y_%s' % i] = []
                        globals()['self.Y_%s_%s' % (i, i)] = []
                        for j in range(self.predictions.shape[0]):
                            if self.y_data.shape[1] == 1:
                                globals()['self.pre_%s' % i].append(self.predictions[j])
                                globals()['self.Y_%s' % i].append(self.y_data[j][i])
                                globals()['self.Y_%s_%s' % (i, i)].append(self.y_data[j][i])
                            else:
                                globals()['self.pre_%s' % i].append(self.predictions[j][i])
                                globals()['self.Y_%s' % i].append(self.y_data[j][i])
                                globals()['self.Y_%s_%s' % (i, i)].append(self.y_data[j][i])
                        self.df_ML['pre_%s' % i] = globals()['self.pre_%s' % i]
                        self.df_ML['Y_%s' % i] = globals()['self.Y_%s' % i]
                        self.df_ML['Y_%s_%s' % (i, i)] = globals()['self.Y_%s_%s' % (i, i)]
                    try:
                        self.X_data = self.X_test_2
                    except:
                        pass
                    for i in range(self.X_data.shape[1]):
                        globals()['self.X_%s' % i] = []
                        for j in range(self.X_data.shape[0]):
                            globals()['self.X_%s' % i].append(self.X_data[j][i])
                        self.df_ML[self.listWidget_2.item(i).text()] = globals()['self.X_%s' % i]
                    self.df_ML.columns = self.df_ML.columns.str.strip()

        plt.clf()
        try:
            self.verticalLayout.removeWidget(self.canv)
            self.horizontalLayout.removeWidget(self.toolbar)
            sip.delete(self.canv)
            sip.delete(self.toolbar)
            self.canv = None
        except:
            pass
        self.canv = MatplotlibCanvas(self)
        self.toolbar = Navi(self.canv, self.centralwidget)
        self.horizontalLayout.addWidget(self.toolbar)
        self.verticalLayout.addWidget(self.canv)
        self.canv.axes.cla()
        self.ax = self.canv.axes
        self.xlabel = self.comboBox_13.currentIndex()
        self.color_1 = self.comboBox_12.currentIndex()
        self.ylabel = self.comboBox_13.currentText()
        self.title_plot = ""
        self.ax1 = self.XY_dataset.plot.scatter(x=self.comboBox_12.currentText(),
                                           y=self.comboBox_13.currentText(),ax=self.ax,legend=None,
                                           title=self.title_plot,xlabel=self.comboBox_12.currentText(),
                                           ylabel=self.ylabel)
        self.ax2 = self.df_ML.plot.scatter(x=self.df_ML.columns[(self.color_1 - len(self.X_data[0]))],
                                           y=self.df_ML.columns[(self.xlabel * 3)], ax=self.ax1, legend=None,
                                           title=self.title_plot, xlabel=self.comboBox_12.currentText(),
                                           ylabel=self.ylabel,c='r')
        self.ax.legend(["True values", "Predicted values"])
        self.ax.tick_params(axis='x', labelrotation=60)
        self.canv.draw()

    def plot_result(self):
        self.confusion_1=[]
        self.df_ML = pd.DataFrame()
        try:
            self.X_data = self.X_test
            self.y_data = self.y_test
        except:
            if self.scaler:
                self.X_data = self.scaler.fit_transform(self.X_data.reshape(-1, self.listWidget_2.count()))
            else:
                pass
        try:
            if self.grid_result.best_params_['loss'] == 'binary_crossentropy':
                self.predictions = (self.model.predict(self.X_data) > 0.5).astype("int32")
                for i in range(self.y_data.shape[1]):
                    globals()['self.pre_%s' % i] = []
                    globals()['self.Y_%s' % i] = []
                    globals()['self.Y_%s_%s' % (i, i)] = []
                    for j in range(self.predictions.shape[0]):
                        if self.y_data.shape[1] == 1:
                            globals()['self.pre_%s' % i].append(self.predictions[j])
                            globals()['self.Y_%s' % i].append(self.y_data[j][i])
                            globals()['self.Y_%s_%s' % (i, i)].append(self.y_data[j][i])
                        else:
                            globals()['self.pre_%s' % i].append(self.predictions[j][i])
                            globals()['self.Y_%s' % i].append(self.y_data[j][i])
                            globals()['self.Y_%s_%s' % (i, i)].append(self.y_data[j][i])
                    self.df_ML['pre_%s' % i] = globals()['self.pre_%s' % i]
                    self.df_ML['Y_%s' % i] = globals()['self.Y_%s' % i]
                    self.df_ML['Y_%s_%s' % (i, i)] = globals()['self.Y_%s_%s' % (i, i)]
                try:
                    self.X_data = self.X_test_2
                except:
                    pass
                for i in range(self.X_data.shape[1]):
                    globals()['self.X_%s' % i] = []
                    for j in range(self.X_data.shape[0]):
                        globals()['self.X_%s' % i].append(self.X_data[j][i])
                    self.df_ML[self.listWidget_2.item(i).text()] = globals()['self.X_%s' % i]
                self.df_ML.columns = self.df_ML.columns.str.strip()
                self.predictions = (self.model.predict(self.X_test) > 0.5).astype("int32")
                self.confusion_1 = confusion_matrix(self.y_test, self.predictions)
            elif self.grid_result.best_params_['loss'] == 'categorical_crossentropy':
                self.predictions = np.argmax(self.model.predict(self.X_data), axis=-1)
                for i in range(self.y_data.shape[1]):
                    globals()['self.pre_%s' % i] = []
                    globals()['self.Y_%s' % i] = []
                    globals()['self.Y_%s_%s' % (i, i)] = []
                    for j in range(self.predictions.shape[0]):
                        if self.y_data.shape[1] == 1:
                            globals()['self.pre_%s' % i].append(self.predictions[j])
                            globals()['self.Y_%s' % i].append(self.y_data[j][i])
                            globals()['self.Y_%s_%s' % (i, i)].append(self.y_data[j][i])
                        else:
                            globals()['self.pre_%s' % i].append(self.predictions[j][i])
                            globals()['self.Y_%s' % i].append(self.y_data[j][i])
                            globals()['self.Y_%s_%s' % (i, i)].append(self.y_data[j][i])
                    self.df_ML['pre_%s' % i] = globals()['self.pre_%s' % i]
                    self.df_ML['Y_%s' % i] = globals()['self.Y_%s' % i]
                    self.df_ML['Y_%s_%s' % (i, i)] = globals()['self.Y_%s_%s' % (i, i)]
                try:
                    self.X_data = self.X_test_2
                except:
                    pass
                for i in range(self.X_data.shape[1]):
                    globals()['self.X_%s' % i] = []
                    for j in range(self.X_data.shape[0]):
                        globals()['self.X_%s' % i].append(self.X_data[j][i])
                    self.df_ML[self.listWidget_2.item(i).text()] = globals()['self.X_%s' % i]
                self.df_ML.columns = self.df_ML.columns.str.strip()
                self.predictions = np.argmax(self.model.predict(self.X_test), axis=-1)
                self.confusion_1 = confusion_matrix(self.y_test, self.predictions)
            elif self.grid_result.best_params_['activ']:
                self.predictions = self.model.predict(self.X_data)
                for i in range(self.y_data.shape[1]):
                    globals()['self.pre_%s' % i] = []
                    globals()['self.Y_%s' % i] = []
                    globals()['self.Y_%s_%s' % (i, i)] = []
                    for j in range(self.predictions.shape[0]):
                        if self.y_data.shape[1] == 1:
                            globals()['self.pre_%s' % i].append(self.predictions[j])
                            globals()['self.Y_%s' % i].append(self.y_data[j][i])
                            globals()['self.Y_%s_%s' % (i, i)].append(self.y_data[j][i])
                        else:
                            globals()['self.pre_%s' % i].append(self.predictions[j][i])
                            globals()['self.Y_%s' % i].append(self.y_data[j][i])
                            globals()['self.Y_%s_%s' % (i, i)].append(self.y_data[j][i])
                    self.df_ML['pre_%s' % i] = globals()['self.pre_%s' % i]
                    self.df_ML['Y_%s' % i] = globals()['self.Y_%s' % i]
                    self.df_ML['Y_%s_%s' % (i, i)] = globals()['self.Y_%s_%s' % (i, i)]
                try:
                    self.X_data = self.X_test_2
                except:
                    pass
                for i in range(self.X_data.shape[1]):
                    globals()['self.X_%s' % i] = []
                    for j in range(self.X_data.shape[0]):
                        globals()['self.X_%s' % i].append(self.X_data[j][i])
                    self.df_ML[self.listWidget_2.item(i).text()] = globals()['self.X_%s' % i]
                self.df_ML.columns = self.df_ML.columns.str.strip()
        except:
            try:
                if self.ui.listWidget_6.findItems('binary_crossentropy', Qt.MatchExactly):
                    self.predictions = (self.model.predict(self.X_data) > 0.5).astype("int32")
                    for i in range(self.y_data.shape[1]):
                        globals()['self.pre_%s' % i] = []
                        globals()['self.Y_%s' % i] = []
                        globals()['self.Y_%s_%s' % (i, i)] = []
                        for j in range(self.predictions.shape[0]):
                            if self.y_data.shape[1] == 1:
                                globals()['self.pre_%s' % i].append(self.predictions[j])
                                globals()['self.Y_%s' % i].append(self.y_data[j][i])
                                globals()['self.Y_%s_%s' % (i, i)].append(self.y_data[j][i])
                            else:
                                globals()['self.pre_%s' % i].append(self.predictions[j][i])
                                globals()['self.Y_%s' % i].append(self.y_data[j][i])
                                globals()['self.Y_%s_%s' % (i, i)].append(self.y_data[j][i])
                        self.df_ML['pre_%s' % i] = globals()['self.pre_%s' % i]
                        self.df_ML['Y_%s' % i] = globals()['self.Y_%s' % i]
                        self.df_ML['Y_%s_%s' % (i, i)] = globals()['self.Y_%s_%s' % (i, i)]
                    try:
                        self.X_data = self.X_test_2
                    except:
                        pass
                    for i in range(self.X_data.shape[1]):
                        globals()['self.X_%s' % i] = []
                        for j in range(self.X_data.shape[0]):
                            globals()['self.X_%s' % i].append(self.X_data[j][i])
                        self.df_ML[self.listWidget_2.item(i).text()] = globals()['self.X_%s' % i]
                    self.df_ML.columns = self.df_ML.columns.str.strip()
                    self.predictions = (self.model.predict(self.X_test) > 0.5).astype("int32")
                    self.confusion_1 = confusion_matrix(self.y_test, self.predictions)
                elif self.ui.listWidget_6.findItems('categorical_crossentropy', Qt.MatchExactly):
                    self.predictions = np.argmax(self.model.predict(self.X_data), axis=-1)
                    for i in range(self.y_data.shape[1]):
                        globals()['self.pre_%s' % i] = []
                        globals()['self.Y_%s' % i] = []
                        globals()['self.Y_%s_%s' % (i, i)] = []
                        for j in range(self.predictions.shape[0]):
                            if self.y_data.shape[1] == 1:
                                globals()['self.pre_%s' % i].append(self.predictions[j])
                                globals()['self.Y_%s' % i].append(self.y_data[j][i])
                                globals()['self.Y_%s_%s' % (i, i)].append(self.y_data[j][i])
                            else:
                                globals()['self.pre_%s' % i].append(self.predictions[j][i])
                                globals()['self.Y_%s' % i].append(self.y_data[j][i])
                                globals()['self.Y_%s_%s' % (i, i)].append(self.y_data[j][i])
                        self.df_ML['pre_%s' % i] = globals()['self.pre_%s' % i]
                        self.df_ML['Y_%s' % i] = globals()['self.Y_%s' % i]
                        self.df_ML['Y_%s_%s' % (i, i)] = globals()['self.Y_%s_%s' % (i, i)]
                    try:
                        self.X_data = self.X_test_2
                    except:
                        pass
                    for i in range(self.X_data.shape[1]):
                        globals()['self.X_%s' % i] = []
                        for j in range(self.X_data.shape[0]):
                            globals()['self.X_%s' % i].append(self.X_data[j][i])
                        self.df_ML[self.listWidget_2.item(i).text()] = globals()['self.X_%s' % i]
                    self.df_ML.columns = self.df_ML.columns.str.strip()
                    self.predictions = np.argmax(self.model.predict(self.X_test), axis=-1)
                    self.confusion_1 = confusion_matrix(self.y_test, self.predictions)
                elif self.ui.listWidget_6.findItems('mse', Qt.MatchExactly) or self.ui.listWidget_6.findItems('mae', Qt.MatchExactly):
                    self.predictions = self.model.predict(self.X_data)
                    for i in range(self.y_data.shape[1]):
                        globals()['self.pre_%s' % i] = []
                        globals()['self.Y_%s' % i] = []
                        globals()['self.Y_%s_%s' % (i, i)] = []
                        for j in range(self.predictions.shape[0]):
                            if self.y_data.shape[1] == 1:
                                globals()['self.pre_%s' % i].append(self.predictions[j])
                                globals()['self.Y_%s' % i].append(self.y_data[j][i])
                                globals()['self.Y_%s_%s' % (i, i)].append(self.y_data[j][i])
                            else:
                                globals()['self.pre_%s' % i].append(self.predictions[j][i])
                                globals()['self.Y_%s' % i].append(self.y_data[j][i])
                                globals()['self.Y_%s_%s' % (i, i)].append(self.y_data[j][i])
                        self.df_ML['pre_%s' % i] = globals()['self.pre_%s' % i]
                        self.df_ML['Y_%s' % i] = globals()['self.Y_%s' % i]
                        self.df_ML['Y_%s_%s' % (i, i)] = globals()['self.Y_%s_%s' % (i, i)]
                    try:
                        self.X_data = self.X_test_2
                    except:
                        pass
                    for i in range(self.X_data.shape[1]):
                        globals()['self.X_%s' % i] = []
                        for j in range(self.X_data.shape[0]):
                            globals()['self.X_%s' % i].append(self.X_data[j][i])
                        self.df_ML[self.listWidget_2.item(i).text()] = globals()['self.X_%s' % i]
                    self.df_ML.columns = self.df_ML.columns.str.strip()
            except:
                if self.comboBox_9.currentText() != 'binary_crossentropy':
                    self.predictions = self.model.predict(self.X_data)
                    for i in range(self.y_data.shape[1]):
                        globals()['self.pre_%s' % i] = []
                        globals()['self.Y_%s' % i] = []
                        globals()['self.Y_%s_%s' % (i, i)] = []
                        for j in range(self.predictions.shape[0]):
                            if self.y_data.shape[1] == 1:
                                globals()['self.pre_%s' % i].append(self.predictions[j])
                                globals()['self.Y_%s' % i].append(self.y_data[j][i])
                                globals()['self.Y_%s_%s' % (i, i)].append(self.y_data[j][i])
                            else:
                                globals()['self.pre_%s' % i].append(self.predictions[j][i])
                                globals()['self.Y_%s' % i].append(self.y_data[j][i])
                                globals()['self.Y_%s_%s' % (i, i)].append(self.y_data[j][i])
                        self.df_ML['pre_%s' % i] = globals()['self.pre_%s' % i]
                        self.df_ML['Y_%s' % i] = globals()['self.Y_%s' % i]
                        self.df_ML['Y_%s_%s' % (i, i)] = globals()['self.Y_%s_%s' % (i, i)]
                    try:
                        self.X_data = self.X_test_2
                    except:
                        pass
                    for i in range(self.X_data.shape[1]):
                        globals()['self.X_%s' % i] = []
                        for j in range(self.X_data.shape[0]):
                            globals()['self.X_%s' % i].append(self.X_data[j][i])
                        self.df_ML[self.listWidget_2.item(i).text()] = globals()['self.X_%s' % i]
                    self.df_ML.columns = self.df_ML.columns.str.strip()
                else:
                    self.predictions = (self.model.predict(self.X_data) > 0.5).astype("int32")
                    for i in range(self.y_data.shape[1]):
                        globals()['self.pre_%s' % i] = []
                        globals()['self.Y_%s' % i] = []
                        globals()['self.Y_%s_%s' % (i, i)] = []
                        for j in range(self.predictions.shape[0]):
                            if self.y_data.shape[1] == 1:
                                globals()['self.pre_%s' % i].append(self.predictions[j])
                                globals()['self.Y_%s' % i].append(self.y_data[j][i])
                                globals()['self.Y_%s_%s' % (i, i)].append(self.y_data[j][i])
                            else:
                                globals()['self.pre_%s' % i].append(self.predictions[j][i])
                                globals()['self.Y_%s' % i].append(self.y_data[j][i])
                                globals()['self.Y_%s_%s' % (i, i)].append(self.y_data[j][i])
                        self.df_ML['pre_%s' % i] = globals()['self.pre_%s' % i]
                        self.df_ML['Y_%s' % i] = globals()['self.Y_%s' % i]
                        self.df_ML['Y_%s_%s' % (i, i)] = globals()['self.Y_%s_%s' % (i, i)]
                    try:
                        self.X_data = self.X_test_2
                    except:
                        pass
                    for i in range(self.X_data.shape[1]):
                        globals()['self.X_%s' % i] = []
                        for j in range(self.X_data.shape[0]):
                            globals()['self.X_%s' % i].append(self.X_data[j][i])
                        self.df_ML[self.listWidget_2.item(i).text()] = globals()['self.X_%s' % i]
                    self.df_ML.columns = self.df_ML.columns.str.strip()
                    self.predictions = (self.model.predict(self.X_test) > 0.5).astype("int32")
                    self.confusion_1 = confusion_matrix(self.y_test, self.predictions)
        try:
            if self.confusion_1.any():
                self.conf_plot()
        except:
            self.ML_plot()

    def conf_plot(self):
        plt.clf()
        try:
            self.verticalLayout.removeWidget(self.canv)
            self.horizontalLayout.removeWidget(self.toolbar)
            sip.delete(self.canv)
            sip.delete(self.toolbar)
            self.canv = None
        except:
            pass
        self.canv = MatplotlibCanvas(self)
        self.toolbar = Navi(self.canv, self.centralwidget)
        self.horizontalLayout.addWidget(self.toolbar)
        self.verticalLayout.addWidget(self.canv)
        self.canv.axes.cla()
        self.ax = self.canv.axes
        self.heat = sns.heatmap(confusion_matrix(self.y_test, self.predictions), annot=True, ax=self.ax)
        self.heat.set(xlabel='Predicted label', ylabel='True label')
        # self.confusion = plot_confusion_matrix(self.model, self.X_test, self.y_test, ax=self.ax) #only supports classifiers
        self.canv.draw()


    def ML_plot(self):
        plt.clf()
        try:
            self.verticalLayout.removeWidget(self.canv)
            self.horizontalLayout.removeWidget(self.toolbar)
            sip.delete(self.canv)
            sip.delete(self.toolbar)
            self.canv = None
        except:
            pass
        self.canv = MatplotlibCanvas(self)
        self.toolbar = Navi(self.canv, self.centralwidget)
        self.horizontalLayout.addWidget(self.toolbar)
        self.verticalLayout.addWidget(self.canv)
        self.canv.axes.cla()
        self.ax = self.canv.axes
        self.kind = 'scatter'
        self.xlabel = self.comboBox_13.currentIndex()
        self.color_1 = self.comboBox_12.currentIndex()
        self.ylabel = self.comboBox_13.currentText()
        self.title_plot = ""
        self.ind_Y =len(self.y_data[0])
        self.XX = self.df_ML.columns[(self.xlabel*3)+1]
        self.YY = self.df_ML.columns[(self.xlabel*3)+2]
        if self.comboBox_12.currentText() != 'None':
            self.ax1 = self.df_ML.plot(x=self.XX, y=self.YY, ax=self.ax, legend=None, title=self.title_plot, color='r')
            self.ax2 = self.df_ML.plot.scatter(x=self.df_ML.columns[(self.xlabel*3)+1],
                            y=self.df_ML.columns[(self.xlabel*3)],ax=self.ax1,legend=None,title=self.title_plot,xlabel=self.ylabel,
                            ylabel="Prediction of"+" "+self.ylabel,
                            c=self.df_ML.columns[(self.color_1 - len(self.X_data[0]))], s=10, cmap='jet')
            self.ax.tick_params(axis='x', labelrotation=60)
            self.canv.draw()
        else:
            self.ax1 = self.df_ML.plot(x=self.XX, y=self.YY, ax=self.ax, legend=None, title=self.title_plot, color='r')
            self.ax2 = self.df_ML.plot.scatter(x=self.df_ML.columns[(self.xlabel*3)+1],
                            y=self.df_ML.columns[(self.xlabel*3)],ax=self.ax1,legend=None,title=self.title_plot,xlabel=self.ylabel,
                            ylabel="Prediction of"+" "+self.ylabel)
            self.ax.tick_params(axis='x', labelrotation=60)
            self.canv.draw()


    def q_bar(self):
        if self.lineEdit_2.text() and self.lineEdit_22.text() != '':
            self.progressBar.setVisible(True)
            # time.sleep(2)
            self.train()
        else:
            pass


    def train(self):
        try:
            self.ui.listWidget_6.clear()
        except:
            pass
        self.X_train = []
        self.X_test = []
        self.scaler = MinMaxScaler()
        self.X_train = self.scaler.fit_transform(self.X_train_1)
        self.X_test = self.scaler.transform(self.X_test_1)
        self.model_1 = Sequential()
        self.add_layer()
        if self.comboBox_9.currentText() == 'binary_crossentropy':
            self.model_1.add(Dense(units=self.y_data.shape[1], activation='sigmoid'))
        else:
            self.model_1.add(Dense(units=self.y_data.shape[1]))
        self.opt = Adam(learning_rate=0.001)
        self.model_1.compile(optimizer=self.opt, loss=self.comboBox_9.currentText())
        self.model_1.fit(x=self.X_train, y=self.y_train, validation_data=(self.X_test, self.y_test),
                batch_size=int(self.comboBox_10.currentText()),
                epochs=int(self.lineEdit_2.text()), verbose=1)
        self.model = self.model_1
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(100)
        self.training_score = self.model.evaluate(self.X_train, self.y_train, verbose=0, batch_size=int(self.comboBox_10.currentText()))
        self.test_score = self.model.evaluate(self.X_test, self.y_test, verbose=0, batch_size=int(self.comboBox_10.currentText()))
        if self.comboBox_9.currentText() == 'binary_crossentropy':
            self.predictions = (self.model.predict(self.X_test) > 0.5).astype("int32")
            self.label_25.setText("Confusion matrix:\n{}".format(confusion_matrix(self.y_test, self.predictions))
                                  + "\nClassification report:\n{}".format(classification_report(self.y_test, self.predictions)))
        else:
            self.label_25.setText("Training score: {}".format("{:e}".format(self.training_score))
                                + "\nTest score: {}".format("{:e}".format(self.test_score)))
        self.label_26.setVisible(True)
        self.comboBox_12.setVisible(True)
        self.pushButton_12.setVisible(True)
        self.pushButton_13.setVisible(True)
        self.comboBox_13.setVisible(True)
        self.label_27.setVisible(True)
        self.comboBox_12.clear()
        self.comboBox_13.clear()
        self.comb12 = []
        for i in range(self.listWidget_2.count()):
            self.comb12.append(self.listWidget_2.item(i).text())
        self.comboBox_12.addItems(self.comb12)
        self.comboBox_12.addItem("None")
        self.comb13 = []
        for i in range(self.listWidget_3.count()):
            self.comb13.append(self.listWidget_3.item(i).text())
        self.comboBox_13.addItems(self.comb13)
        self.actionModel.setEnabled(True)



    def add_layer(self):
        for _ in range(int(self.comboBox_6.currentText())):
            self.model_1.add(Dense(units=int(float(self.lineEdit_22.text())),
                                     activation=self.comboBox_8.currentText()))

    def split(self):
        self.X_data =self.df[self.l1].values
        self.y_data =self.df[self.l2].values
        self.X_train_1, self.X_test_1, self.y_train, self.y_test = train_test_split\
            (self.X_data, self.y_data, test_size=float(self.comboBox_11.currentText()), random_state=42)
        self.label_16.setText("X train: {}".format(self.X_train_1.shape)
                              + "\nX test: {}".format(self.X_test_1.shape)
                              + "\nY train: {}".format(self.y_train.shape)
                              + "\nY test: {}".format(self.y_test.shape))
        self.comboBox_5.clear()
        self.comboBox_5.addItems(["ANN"])
        self.comboBox_5.setEnabled(True)
        self.comboBox_6.setVisible(True)
        self.lineEdit_22.setVisible(True)
        self.comboBox_8.setVisible(True)
        self.comboBox_9.setVisible(True)
        self.comboBox_10.setVisible(True)
        self.lineEdit_2.setVisible(True)
        self.label_18.setVisible(True)
        self.label_20.setVisible(True)
        self.label_21.setVisible(True)
        self.label_22.setVisible(True)
        self.label_23.setVisible(True)
        self.label_24.setVisible(True)
        self.pushButton_11.setVisible(True)
        self.actionExpert.setEnabled(True)
        self.comboBox_6.clear()
        self.lineEdit_22.clear()
        self.comboBox_8.clear()
        self.comboBox_9.clear()
        self.comboBox_10.clear()
        self.lineEdit_2.clear()
        self.comboBox_6.addItems(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
        self.comboBox_8.addItems(["relu", "sigmoid", "tanh", "elu"])
        self.comboBox_9.addItems(["mse", "mae", "binary_crossentropy"])
        self.comboBox_10.addItems(["1", "2", "4", "8", "16", "32", "64", "128", "256", "512", "1024", "2048"])
        self.X_test_2 = self.X_test_1

    def create_dataset(self):
        self.l1 = []
        self.l2 = []
        for i in range(self.listWidget_2.count()):
            self.l1.append(self.listWidget_2.item(i).text())
        for i in range(self.listWidget_3.count()):
            self.l2.append(self.listWidget_3.item(i).text())
        self.X_data =self.df[self.l1].values
        self.y_data =self.df[self.l2].values
        self.X_dataset =self.df[self.l1]
        self.y_dataset =self.df[self.l2]
        self.label_13.setText("Input dataset: {}".format(self.X_data.shape)
                              + "\nOutput dataset: {}".format(self.y_data.shape))
        self.comboBox_11.setEnabled(True)
        self.pushButton_10.setEnabled(True)
        self.progressBar.setVisible(False)
        self.comboBox_11.clear()
        self.comboBox_11.addItems(["0.1", "0.2", "0.3", "0.4", "0.5"])
        self.XY_dataset = pd.concat([self.X_dataset, self.y_dataset], axis=1, join='inner')

    def add_input(self):
       self.item_in = QListWidgetItem(self.listWidget_1.currentItem())
       if self.listWidget_2.findItems(self.listWidget_1.currentItem().text(), Qt.MatchExactly):
           pass
       else:
           self.listWidget_2.addItem(self.item_in)
       self.check()

    def add_output(self):
       self.item_out = QListWidgetItem(self.listWidget_1.currentItem())
       if self.listWidget_3.findItems(self.listWidget_1.currentItem().text(), Qt.MatchExactly):
           pass
       else:
           self.listWidget_3.addItem(self.item_out)
       self.check()

    def del_input(self):
       self.item_in_del = self.listWidget_2.currentRow()
       self.listWidget_2.takeItem(self.item_in_del)
       self.check()

    def del_output(self):
       self.item_out_del = self.listWidget_3.currentRow()
       self.listWidget_3.takeItem(self.item_out_del)
       self.check()

    def apply_filter(self):
        self.f_col = self.comboBox.currentText()
        self.filter = self.comboBox_4.currentText()
        self.txt = self.lineEdit.text()
        if self.filter == "<":
            if self.txt:
                self.df = self.df[self.df[self.f_col] < float(self.txt)]
        elif self.filter == ">":
            if self.txt:
                self.df = self.df[self.df[self.f_col] > float(self.txt)]
        elif self.filter == "=":
            if self.txt:
                self.df = self.df[self.df[self.f_col] == float(self.txt)]
        elif self.filter == "drop":
            self.df = self.df.drop([self.f_col], axis=1)
        elif self.filter == "drop NaN":
            self.df = self.df.dropna()

        if self.listWidget_1:
            self.listWidget_1.clear()
            self.listWidget_2.clear()
            self.listWidget_3.clear()
            self.comboBox_1.clear()
            self.comboBox_2.clear()
            self.comboBox_3.clear()
            self.comboBox.clear()
            self.comboBox_4.clear()
            self.lineEdit.clear()
        self.print_info()
        self.plot_para()
        self.check()

    def check(self):
        if self.comboBox_4.currentText() == "drop NaN":
            self.lineEdit.setEnabled(False)
            self.comboBox.setEnabled(False)
        elif self.comboBox_4.currentText() == "drop":
            self.lineEdit.setEnabled(False)
        else:
            self.lineEdit.setEnabled(True)
            self.comboBox.setEnabled(True)
        if self.listWidget_2 and self.listWidget_3:
            self.pushButton_8.setEnabled(True)
        else:
            self.pushButton_8.setEnabled(False)
        if self.comboBox_12.currentText() == 'None':
            self.pushButton_13.setEnabled(False)
        else:
            self.pushButton_13.setEnabled(True)



    def plot_para(self):
        self.X = self.comboBox_1.currentText()
        self.Y = self.comboBox_2.currentText()
        self.s_sample = self.comboBox_3.currentText()

    def update(self):
        if self.checkBox.isChecked():
            self.ax = self.canv.axes
            self.plot_fig()
        else:
            plt.clf()
            try:
                self.verticalLayout.removeWidget(self.canv)
                self.horizontalLayout.removeWidget(self.toolbar)
                sip.delete(self.canv)
                sip.delete(self.toolbar)
                self.canv = None
            except:
                pass
            self.canv = MatplotlibCanvas(self)
            self.toolbar = Navi(self.canv, self.centralwidget)
            self.horizontalLayout.addWidget(self.toolbar)
            self.verticalLayout.addWidget(self.canv)
            self.canv.axes.cla()
            self.ax = self.canv.axes
            self.plot_fig()

    def box_plot(self):
        self.plot_para()
        plt.clf()
        try:
            self.verticalLayout.removeWidget(self.canv)
            self.horizontalLayout.removeWidget(self.toolbar)
            sip.delete(self.canv)
            sip.delete(self.toolbar)
            self.canv = None
        except:
            pass
        self.canv = MatplotlibCanvas(self)
        self.toolbar = Navi(self.canv, self.centralwidget)
        self.horizontalLayout.addWidget(self.toolbar)
        self.verticalLayout.addWidget(self.canv)
        self.canv.axes.cla()
        self.ax = self.canv.axes

        self.kind = 'box'
        self.xlabel = self.comboBox_1.currentText()
        self.ylabel = self.comboBox_2.currentText()
        self.title_plot = ""
        # self.ax.yaxis.set_major_formatter(FormatStrFormatter('%.2e'))
        # self.ax.xaxis.set_major_formatter(FormatStrFormatter('%.2e'))
        self.X = None
        self.df.plot(kind=self.kind,x=self.X,y=self.Y,ax=self.ax,legend=None,xlabel=self.xlabel,
                            ylabel=self.ylabel,title=self.title_plot)
        self.ax.tick_params(axis='x', labelrotation=60)
        self.canv.draw()


    def scatter(self):
        self.plot_para()
        plt.clf()
        try:
            self.verticalLayout.removeWidget(self.canv)
            self.horizontalLayout.removeWidget(self.toolbar)
            sip.delete(self.canv)
            sip.delete(self.toolbar)
            self.canv = None
        except:
            pass
        self.canv = MatplotlibCanvas(self)
        self.toolbar = Navi(self.canv, self.centralwidget)
        self.horizontalLayout.addWidget(self.toolbar)
        self.verticalLayout.addWidget(self.canv)

        self.canv.axes.cla()
        self.ax = self.canv.axes
        self.xlabel = self.comboBox_1.currentText()
        self.ylabel = self.comboBox_2.currentText()
        self.c_color = self.comboBox_222.currentText()
        self.title_plot = ""
        if self.comboBox_222.currentText() == 'None':
            self.df.plot.scatter(x=self.X,y=self.Y,ax=self.ax,legend=None,xlabel=self.xlabel,
                            ylabel=self.ylabel,title=self.title_plot)
        else:
            self.df.plot.scatter(x=self.X,y=self.Y,ax=self.ax,legend=None,xlabel=self.xlabel,
                            ylabel=self.ylabel,title=self.title_plot,
                     c=self.c_color,
                     s=5, cmap='jet')
        self.ax.tick_params(axis='x', labelrotation=60)
        self.canv.draw()
        self.label_666.setVisible(True)
        self.comboBox_222.setVisible(True)

    def plot_fig(self):
        self.plot_para()
        self.kind = 'line'
        self.xlabel = self.comboBox_1.currentText()
        self.ylabel = self.comboBox_2.currentText()
        self.title_plot = ""
        # self.ax.yaxis.set_major_formatter(FormatStrFormatter('%.2e'))
        # self.ax.xaxis.set_major_formatter(FormatStrFormatter('%.2e'))
        if self.comboBox_1.currentText() == self.comboBox_2.currentText():
            self.kind = 'hist'
            self.X = None
            self.title_plot = "Histogram of {}".format(self.xlabel)
            self.df.plot(kind=self.kind, x=self.X, y=self.Y, ax=self.ax, legend=None, xlabel=self.xlabel,
                           ylabel=self.ylabel, title=self.title_plot, bins=20)
            self.ax.tick_params(axis='x', labelrotation=60)
            self.canv.draw()
        elif ((self.comboBox_1.currentText() == self.cols[0] or self.comboBox_1.currentText() == self.cols[1] or
                    self.comboBox_1.currentText() == self.cols[2] or self.comboBox_1.currentText() == self.cols[3]) and
                (self.comboBox_2.currentText() == self.cols[0] or self.comboBox_2.currentText() == self.cols[1] or
                    self.comboBox_2.currentText() == self.cols[2] or self.comboBox_2.currentText() == self.cols[3])):
            self.kind = 'scatter'
            self.xlabel = self.comboBox_1.currentText()
            self.ylabel = self.comboBox_2.currentText()
            self.title_plot = ""
            self.df.plot(kind=self.kind, x=self.X, y=self.Y, ax=self.ax, legend=None, xlabel=self.xlabel,
                     ylabel=self.ylabel, title=self.title_plot)
            self.ax.tick_params(axis='x', labelrotation=60)
            self.canv.draw()
        else:
            for row in range(int(self.s_sample)):
                self.df_1 = self.df.iloc[[row+1]]
                self.df_1 = self.df[(self.df[self.cols[0]] == float(self.df.iloc[[row+1]][self.cols[0]].values)) & (
                self.df[self.cols[1]] == float(self.df.iloc[[row+1]][self.cols[1]].values)) & (
                self.df[self.cols[2]] == float(self.df.iloc[[row+1]][self.cols[2]].values)) & (
                self.df[self.cols[3]] == float(self.df.iloc[[row+1]][self.cols[3]].values))]
                self.df_1.plot(kind=self.kind,x=self.X,y=self.Y,ax=self.ax,legend=None,xlabel=self.xlabel,
                               ylabel=self.ylabel,title=self.title_plot)
            self.canv.draw()


    def show_table(self):
        self.model_Table = pandasModel(self.df)
        self.view = QTableView()
        self.view.setModel(self.model_Table)
        self.view.resize(800, 600)
        self.view.show()

    def getFile(self):
        import os
        self.filename = QFileDialog.getOpenFileName(filter="csv (*.csv)")[0]
        if self.filename:
            base_name = os.path.basename(self.filename)
            self.Title = os.path.splitext(base_name)[0]
            self.pushButton_3.setEnabled(True)
            self.pushButton_333.setEnabled(True)
            self.pushButton_4.setEnabled(True)
            self.pushButton_9.setEnabled(True)
            self.pushButton_2.setEnabled(True)
            self.pushButton_5.setEnabled(True)
            self.checkBox.setVisible(True)
            self.actionScatter.setEnabled(True)
            self.actionBox.setEnabled(True)
            if self.listWidget_1:
                self.listWidget_1.clear()
                self.listWidget_2.clear()
                self.listWidget_3.clear()
                self.comboBox_1.clear()
                self.comboBox_222.clear()
                self.comboBox_2.clear()
                self.comboBox_3.clear()
                self.comboBox.clear()
                self.comboBox_4.clear()
                self.lineEdit.clear()
            self.readData()

    def get_panda_info(self):
        self.row = len(self.df)
        self.col = len(self.df.columns)
        self.elements = self.df.size
        self.cols = self.df.columns


    def describe(self):
        self.get_panda_info()
        self.CR = self.listWidget_1.currentRow()
        self.label_5.setText(str(self.df[self.cols[self.CR]].describe().transpose()))



    def print_info(self):
        self.get_panda_info()
        self.label_3.setText("CSV file name: {}".format(self.Title))
        self.label_2.setText("Number of rows: {}".format(self.row))
        self.label_4.setText("Number of columns: {}".format(self.col))
        self.label_9.setText("N. of elements: {}".format(self.elements))
        self.label_99.setText("NaN elements: {}".format(self.df.isnull().values.any()))
        for i in range(len(self.cols)):
            self.item = QListWidgetItem(self.cols[i])
            self.listWidget_1.addItem(self.item)
        self.comboBox_222.addItem('None')
        for i in range(len(self.cols)):
            self.item_combo = self.cols[i]
            self.comboBox_1.addItem(self.item_combo)
            self.comboBox_222.addItem(self.item_combo)
            self.comboBox_2.addItem(self.item_combo)
            self.comboBox.addItem(self.item_combo)
        for j in range(1,11):
            self.item_s = str(j)
            self.comboBox_3.addItem(self.item_s)
        self.listWidget_1.setCurrentRow(0)
        self.comboBox_4.addItems(["=", ">", "<", "drop", "drop NaN"])
        self.describe()


    def readData(self):
        self.df = pd.read_csv(self.filename, encoding='utf-8')
        self.print_info()
        self.plot_para()
        self.check()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", " "))
        self.pushButton_1.setText(_translate("MainWindow", "Open"))
        self.label_1.setText(_translate("MainWindow", "Open the .CSV file:"))
        self.label.setText(_translate("MainWindow", "Columns"))
        self.label_2.setText(_translate("MainWindow", "Number of rows: "))
        self.label_3.setText(_translate("MainWindow", "CSV file name:"))
        self.label_4.setText(_translate("MainWindow", "Number of columns:"))
        self.label_5.setText(_translate("MainWindow", ""))
        self.label_6.setText(_translate("MainWindow", "X:"))
        self.label_666.setText(_translate("MainWindow", "C:"))
        self.label_7.setText(_translate("MainWindow", "Y:"))
        self.label_8.setText(_translate("MainWindow", "N. of samples:"))
        self.pushButton_3.setText(_translate("MainWindow", "Show"))
        self.label_9.setText(_translate("MainWindow", "Number of samples:"))
        self.label_99.setText(_translate("MainWindow", "NaN elements:"))
        self.pushButton_4.setText(_translate("MainWindow", "Plot  X-Y"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuFile_2.setTitle(_translate("MainWindow", "Plot"))
        self.menuFile_3.setTitle(_translate("MainWindow", "ML"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionBox.setText(_translate("MainWindow", "Box Y"))
        self.actionScatter.setText(_translate("MainWindow", "Scatter X-Y"))
        self.actionModel.setText(_translate("MainWindow", "Save Model"))
        self.actionModel_2.setText(_translate("MainWindow", "Load Model"))
        self.actionExpert.setText(_translate("MainWindow", "Expert"))
        self.label_10.setText(_translate("MainWindow", "Column:"))
        self.label_14.setText(_translate("MainWindow", "Filter:"))
        self.pushButton_9.setText(_translate("MainWindow", "Apply Filter"))
        self.label_11.setText(_translate("MainWindow", "Input"))
        self.label_12.setText(_translate("MainWindow", "Output"))
        self.label_13.setText(_translate("MainWindow", ""))
        self.pushButton_2.setText(_translate("MainWindow", "Add"))
        self.pushButton_333.setText(_translate("MainWindow", "Add"))
        self.pushButton_5.setText(_translate("MainWindow", "Add"))
        self.pushButton_6.setText(_translate("MainWindow", "Delete"))
        self.pushButton_7.setText(_translate("MainWindow", "Delete"))
        self.pushButton_8.setText(_translate("MainWindow", "Create Dataset"))
        self.label_15.setText(_translate("MainWindow", "Test size:"))
        self.pushButton_10.setText(_translate("MainWindow", "Split"))
        self.label_16.setText(_translate("MainWindow", ""))
        self.label_17.setText(_translate("MainWindow", "Model:"))
        self.label_18.setText(_translate("MainWindow", "N. of hidden \n"
                                                       "layers:"))
        self.label_19.setText(_translate("MainWindow", " "))
        self.label_20.setText(_translate("MainWindow", "N. of neurons \n"
                                                       "for each layer:"))
        self.label_21.setText(_translate("MainWindow", "Activation \n"
                                                       "function:"))
        self.label_22.setText(_translate("MainWindow", "Loss\n"
                                                       "function:"))
        self.label_23.setText(_translate("MainWindow", "Epochs:"))
        self.label_24.setText(_translate("MainWindow", "Batch size:"))
        self.pushButton_11.setText(_translate("MainWindow", "Start training"))
        self.label_25.setText(_translate("MainWindow", ""))
        self.pushButton_12.setText(_translate("MainWindow", "Plot result"))
        self.label_26.setText(_translate("MainWindow", "Marker colors \n"
                                                       "column:"))
        self.label_27.setText(_translate("MainWindow", "Predicted \n"
                                                       "output"))
        self.pushButton_13.setText(_translate("MainWindow", "Compare"))
        self.checkBox.setText(_translate("MainWindow", "Hold\n On"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
