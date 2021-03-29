from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from qtpy.QtCore import Qt
import sys
import os
from glob import glob
import cv2
from PyQt5.QtGui import QPixmap, QIcon
import json
from datetime import datetime

os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"


class Ui_Geeks4LabelTool(object):
    
    def __init__(self):
        super(Ui_Geeks4LabelTool, self).__init__()
        self.viewer = PhotoViewer(self)
        self.counter = 0
        self.S_File = None
        self.img_path = None
        self.check_path = None
        self.img_idx = None
        self.labels = []
        self.flag = 0
        self.data = {
                "version": "1.0.0",
                "Created By": "4-Geeks",
                "date": "",
                "data": []
                }

    def setupUi(self, Geeks4LabelTool):
        Geeks4LabelTool.setObjectName("Geeks4LabelTool")
        Geeks4LabelTool.resize(1800, 984)

        # Create GridLayout
        self.gridLayoutWidget = QtWidgets.QWidget(Geeks4LabelTool)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 20, 1900, 984))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.gridLayoutWidget)
        self.verticalLayout_2.setContentsMargins(7, 5, 7, 7)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        # MenuBar BackGround
        self.frame_2 = QFrame(self.gridLayoutWidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 30))
        self.frame_2.setStyleSheet(u"background-color: rgb(34,37,49)")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)

        # Create MenuBar
        self.menubar = QtWidgets.QMenuBar(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.menubar.sizePolicy().hasHeightForWidth())
        self.menubar.setSizePolicy(sizePolicy)
        self.menubar.setMinimumSize(QtCore.QSize(10, 10))
        self.menubar.setMaximumSize(QtCore.QSize(800, 100))
        
        self.menubar.setStyleSheet("""
            QMenuBar {
                color: rgb(255,255,255);
            }

            QMenuBar::item {
                color: rgb(255,255,255);
            }

            QMenuBar::item::selected {
                color: rgb(255,255,255);
            }

            QMenu {
                color: rgb(200,200,200);
            }

            QMenu::item::selected {
                color: rgb(255,255,255);
            }
        """)

        font = self.menubar.font()
        font.setPointSize(12)
        self.menubar.setFont(font)
        ############################################## File #################################################
        actionFile = self.menubar.addMenu("&File")
        font = self.menubar.font()
        font.setPointSize(10)
        # File -> Open Dir
        openDirAct = QAction(QIcon('icons/open.png'), '&Open Dir', self.gridLayoutWidget)
        openDirAct.setStatusTip('Open New Directory')
        openDirAct.setFont(font)
        openDirAct.triggered.connect(self.show_dir)
        actionFile.addAction(openDirAct)
        # File -> Open File
        openFileAct = QAction(QIcon('icons/open.png'), '&Open File', self.gridLayoutWidget)
        openFileAct.setStatusTip('Open New File')
        openFileAct.setFont(font)
        openFileAct.triggered.connect(self.open_img)
        actionFile.addAction(openFileAct)
        # File -> Save Output File
        saveJason = QAction(QIcon('icons/save.ico'), '&Save Json', self.gridLayoutWidget)
        saveJason.setStatusTip('Save Jason')
        saveJason.setFont(font)
        saveJason.triggered.connect(self.save_path)
        actionFile.addAction(saveJason)
        # File -> Exit
        actionFile.addSeparator()
        exitAct = QAction(QIcon('icons/exit.webp'), '&Exit', self.gridLayoutWidget)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit Application')
        exitAct.setFont(font)
        exitAct.triggered.connect(qApp.quit)
        actionFile.addAction(exitAct)
        ############################################## File #################################################

        ############################################## View #################################################
        # actionFile = self.menubar.addMenu("&View")
        # actionFile.addAction("New")
        # actionFile.addAction("Open")
        # actionFile.addAction("Save")
        ############################################## View #################################################

        ############################################## Help #################################################
        actionFile = self.menubar.addMenu(("&Help"))
        # Help -> Save Image Label
        saveLabel = QAction(QIcon('icons/save.png'), '&Save Image Label            Ctrl+S', self.gridLayoutWidget)
        saveLabel.setStatusTip('Save Image Label')
        saveLabel.setFont(font)
        actionFile.addAction(saveLabel)
        # File -> Next Image
        nextImage = QAction(QIcon('icons/next.png'), '&Next Image                      Ctrl+F', self.gridLayoutWidget)
        nextImage.setStatusTip('Next Image')
        nextImage.setFont(font)
        actionFile.addAction(nextImage)
        # File -> Save Output File
        prevImage = QAction(QIcon('icons/prev.webp'), '&Previous Image                Ctrl+D', self.gridLayoutWidget)
        prevImage.setStatusTip('Previous Image')
        prevImage.setFont(font)
        actionFile.addAction(prevImage)
        ############################################## Help #################################################
        # MenuBar Layout
        self.verticalMenuLay = QtWidgets.QVBoxLayout(self.gridLayoutWidget)
        self.verticalMenuLay.setObjectName("verticalMenuLay")
        self.verticalMenuLay.addWidget(self.frame_2)
        self.verticalLayout_2.addLayout(self.verticalMenuLay)

        # Horizental Line to Seprate Menu Bar and GridLayout
        self.menuAndGridSep = QFrame(self.gridLayoutWidget)
        self.menuAndGridSep.setObjectName(u"menuAndGridSep")
        self.menuAndGridSep.setFrameShape(QFrame.HLine)
        self.menuAndGridSep.setFrameShadow(QFrame.Sunken)
        self.verticalLayout_2.addWidget(self.menuAndGridSep)

        # Set gridLayout_2
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")

        # For Stretching The Window
        Geeks4LabelTool.setLayout(self.verticalLayout_2)

        self.RlineLay = QtWidgets.QHBoxLayout()
        self.RlineLay.setObjectName("RlineLay")
        self.Rline = QtWidgets.QFrame(self.gridLayoutWidget)
        self.Rline.setFrameShape(QtWidgets.QFrame.VLine)
        self.Rline.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Rline.setObjectName("Rline")
        self.RlineLay.addWidget(self.Rline)

        # Text Widget
        self.textLay = QtWidgets.QVBoxLayout()
        self.textLay.setObjectName("textLay")
        self.textEdit = QtWidgets.QTextEdit(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setStyleSheet("color: rgb(255, 255, 255);")
        font = QtGui.QFont()
        font.setPointSize(16)
        self.textEdit.setFont(font)
        self.textEdit.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit.setMaximumSize(QtCore.QSize(300, 200))
        self.textEdit.setObjectName("textEdit")
        self.textLay.addWidget(self.textEdit, 0, QtCore.Qt.AlignTop)

        self.ButtonLay = QtWidgets.QHBoxLayout()
        self.ButtonLay.setObjectName("ButtonLay")

        # Prev Button
        self.prevButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.prevButton.sizePolicy().hasHeightForWidth())
        self.prevButton.setSizePolicy(sizePolicy)
        self.prevButton.setMaximumSize(QtCore.QSize(150, 30))
        self.prevButton.setStyleSheet("QPushButton:pressed{color: white} QPushButton{color: white}")
        font = QtGui.QFont()
        font.setPointSize(11)
        self.prevButton.setFont(font)
        # Shortcut (Ctrl + D) for "Prev Button"
        self.prev_shortcut = QShortcut(QtGui.QKeySequence("Ctrl+d"),Geeks4LabelTool)
        self.prevButton.setObjectName("prevButton")
        self.ButtonLay.addWidget(self.prevButton)
        
        # Save Button
        self.saveButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveButton.sizePolicy().hasHeightForWidth())
        self.saveButton.setSizePolicy(sizePolicy)
        self.saveButton.setMaximumSize(QtCore.QSize(150, 30))
        self.saveButton.setStyleSheet("QPushButton:pressed{color: white} QPushButton{color: white}")
        font = QtGui.QFont()
        font.setPointSize(11)
        self.saveButton.setFont(font)
        # Shortcut (Ctrl + S) for "Save Button"
        self.save_shortcut = QShortcut(QtGui.QKeySequence("Ctrl+s"),Geeks4LabelTool)
        self.saveButton.setObjectName("saveButton")
        self.ButtonLay.addWidget(self.saveButton)

        # Next Button
        self.nextButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nextButton.sizePolicy().hasHeightForWidth())
        self.nextButton.setSizePolicy(sizePolicy)
        self.nextButton.setMaximumSize(QtCore.QSize(150, 30))
        self.nextButton.setSizeIncrement(QtCore.QSize(0, 20))
        self.nextButton.setStyleSheet("QPushButton:pressed{color: white} QPushButton{color: white}")
        font = QtGui.QFont()
        font.setPointSize(11)
        self.nextButton.setFont(font)
        # Shortcut (Ctrl + F) for "Next Button"
        self.next_shortcut = QShortcut(QtGui.QKeySequence("Ctrl+f"),Geeks4LabelTool)
        self.nextButton.setObjectName("nextButton")
        self.ButtonLay.addWidget(self.nextButton)
        self.textLay.addLayout(self.ButtonLay)

        # ListBar Widget
        self.listWidget = QtWidgets.QListWidget(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        self.listWidget.setStyleSheet("QListWidget:pressed{color: white} QListWidget{color: white}")                
        self.listWidget.setMaximumSize(QtCore.QSize(300, 800))
        self.listWidget.setObjectName("listWidget")
        self.textLay.addWidget(self.listWidget)
        self.RlineLay.addLayout(self.textLay)
        self.gridLayout_2.addLayout(self.RlineLay, 0, 2, 1, 1)
        self.LlineLay = QtWidgets.QHBoxLayout()
        self.LlineLay.setObjectName("LlineLay")
        
        # 4Geeks Image
        self.geeksLayout = QtWidgets.QVBoxLayout()
        self.geeksLayout.setObjectName("geeksLayout")
        self.geekslabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.geekslabel.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(-10)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.geekslabel.sizePolicy().hasHeightForWidth())
        self.geekslabel.setSizePolicy(sizePolicy)
        self.geekslabel.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.geekslabel.setText("")
        self.geekslabel.setTextFormat(QtCore.Qt.AutoText)
        self.geekslabel.setPixmap(QtGui.QPixmap("icons/4geeks.png"))
        self.geekslabel.setObjectName("geekslabel")
        self.geeksLayout.addWidget(self.geekslabel)
        self.OpenLay = QtWidgets.QVBoxLayout()
        self.OpenLay.setObjectName("OpenLay")
        
        # Open Dir
        self.OpenDir = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.OpenDir.setMaximumSize(QtCore.QSize(120, 70))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(70)
        sizePolicy.setHeightForWidth(self.OpenDir.sizePolicy().hasHeightForWidth())
        self.OpenDir.setSizePolicy(sizePolicy)
        self.OpenDir.setStyleSheet("QToolButton:pressed{color: white} QToolButton{color: white}")
        font = QtGui.QFont()
        font.setPointSize(11)
        self.OpenDir.setFont(font)
        openDirIcon = QtGui.QPixmap("icons/open.png")
        self.OpenDir.setIcon(QtGui.QIcon(openDirIcon))
        self.OpenDir.setIconSize(QSize(64, 64))
        self.OpenDir.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.OpenDir.setObjectName("OpenDir")
        self.OpenLay.addWidget(self.OpenDir)
    
        # Open File
        self.OpenFile = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.OpenFile.setMaximumSize(QtCore.QSize(120, 70))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(70)
        sizePolicy.setHeightForWidth(self.OpenFile.sizePolicy().hasHeightForWidth())
        self.OpenFile.setSizePolicy(sizePolicy)
        self.OpenFile.setStyleSheet("QToolButton:pressed{color: white} QToolButton{color: white}")        
        font = QtGui.QFont()
        font.setPointSize(11)
        self.OpenFile.setFont(font)
        self.OpenFile.setAutoRepeat(False)
        self.OpenFile.setAutoExclusive(False)
        openFileIcon = QtGui.QPixmap("icons/open.png")
        self.OpenFile.setIcon(QtGui.QIcon(openFileIcon))
        self.OpenFile.setIconSize(QSize(64, 64))
        self.OpenFile.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.OpenFile.setObjectName("OpenFile")
        self.OpenLay.addWidget(self.OpenFile)

        # Save Json File
        self.SaveOutput = QtWidgets.QToolButton(self.gridLayoutWidget)
        self.SaveOutput.setMaximumSize(QtCore.QSize(120, 70))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(70)
        sizePolicy.setHeightForWidth(self.SaveOutput.sizePolicy().hasHeightForWidth())
        self.SaveOutput.setSizePolicy(sizePolicy)
        self.SaveOutput.setStyleSheet("QToolButton:pressed{color: white} QToolButton{color: white}")                
        font = QtGui.QFont()
        font.setPointSize(11)
        self.SaveOutput.setFont(font)
        self.SaveOutput.setAutoRepeat(False)
        self.SaveOutput.setAutoExclusive(False)
        saveJson = QtGui.QPixmap("icons/save.ico")
        self.SaveOutput.setIcon(QtGui.QIcon(saveJson))
        self.SaveOutput.setIconSize(QSize(40, 40))
        self.SaveOutput.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.SaveOutput.setObjectName("SaveOutput")
        self.OpenLay.addWidget(self.SaveOutput)

        # Spacer for OpenLay and add LlineLay to GridLayout
        spacerItem = QtWidgets.QSpacerItem(20, 35, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.OpenLay.addItem(spacerItem)
        self.geeksLayout.addLayout(self.OpenLay)
        self.LlineLay.addLayout(self.geeksLayout)
        self.Lline = QtWidgets.QFrame(self.gridLayoutWidget)
        self.Lline.setFrameShape(QtWidgets.QFrame.VLine)
        self.Lline.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Lline.setObjectName("Lline")
        self.LlineLay.addWidget(self.Lline)
        self.gridLayout_2.addLayout(self.LlineLay, 0, 0, 1, 1)

        # Image LayOut
        self.imgLay = QtWidgets.QVBoxLayout()
        self.imgLay.setObjectName("imgLay")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.viewer.setSizePolicy(sizePolicy)
        self.imgLay.addWidget(self.viewer)
        self.gridLayout_2.addLayout(self.imgLay, 0, 1, 1, 1)

        self.verticalLayout_2.addLayout(self.gridLayout_2)

        self.retranslateUi(Geeks4LabelTool)
        QtCore.QMetaObject.connectSlotsByName(Geeks4LabelTool)

        # Open Dir Click
        self.OpenDir.clicked.connect(self.show_dir)

        # Open File Click
        self.OpenFile.clicked.connect(self.open_img)

        # Listbar Item Selection
        self.listWidget.itemSelectionChanged.connect(self.ListBar)

        # Save Output Click 
        self.SaveOutput.clicked.connect(self.save_path)

        # Save Button Click 
        self.saveButton.clicked.connect(self.save_text)
        # Save Button Shortcut Key
        self.save_shortcut.activated.connect(self.save_text)

        # Next Button Click 
        self.nextButton.clicked.connect(self.next_image)
        # Next Button Shortcut Key
        self.next_shortcut.activated.connect(self.next_image)

        # Back Button Click 
        self.prevButton.clicked.connect(self.prev_image)
        # Back Button Shortcut Key
        self.prev_shortcut.activated.connect(self.prev_image)


    def retranslateUi(self, Geeks4LabelTool):
        _translate = QtCore.QCoreApplication.translate
        Geeks4LabelTool.setWindowTitle(_translate("Geeks4LabelTool", "textMe"))
        self.saveButton.setText(_translate("Geeks4LabelTool", "Save"))
        self.prevButton.setText(_translate("Geeks4LabelTool", "Back"))
        self.nextButton.setText(_translate("Geeks4LabelTool", "Next"))
        self.OpenDir.setText(_translate("Geeks4LabelTool", "Open Dir"))
        self.OpenFile.setText(_translate("Geeks4LabelTool", "Open File"))
        self.SaveOutput.setText(_translate("Geeks4LabelTool", "Save Output"))


    def open_img(self):
        self.openFileNameDialog()

    def openFileNameDialog(self):
        # Clear TextFile
        self.textEdit.clear()
        
        # Set Save Button Name to Save
        self.saveButton.setText("Save")

        dialog = QtWidgets.QFileDialog(None, windowTitle='Select File')
        dialog.setOptions(dialog.DontUseNativeDialog)
        # dialog.setStyleSheet("color: rgb(255, 255, 255);")
        fileName, _ = dialog.getOpenFileName(None,"Select File", "","All Files (*);;Iamges (*.jpg *.png) ", options=dialog.options())
        
        self.viewer.setPhoto(QtGui.QPixmap(fileName))
        self.img_path = fileName

        try:
            old_label = [(counter, item) for (counter, item) in enumerate(self.data['data']) if item["imagePath"] == f'{fileName}']
            self.textEdit.insertPlainText(old_label[0][1]['label'])
            self.check_path = old_label[0][1]["imagePath"]
            self.img_idx = old_label[0][0]
        except:
            pass


    def show_dir(self):
        # folderpath = QFileDialog.getExistingDirectory(Geeks4LabelTool, 'Select Folder',"./")
        # Geeks4LabelTool -> None
        dialog = QtWidgets.QFileDialog(None, windowTitle='Select Directory')
        dialog.setDirectory( __file__)
        dialog.setFileMode(dialog.Directory)
        dialog.setOptions(dialog.DontUseNativeDialog)
        # dialog.setStyleSheet("color: rgb(255, 255, 255);")

        if  dialog.exec_():
            folderpath = dialog.selectedFiles()[0]

            IMG_PATH = glob(str(folderpath) + '/*.jpg')
            IMG_PATH.extend(glob(str(folderpath) + '/*.png'))
            for item in IMG_PATH:
                self.listWidget.addItem(item)
        
        if self.flag == 0:
            self.listWidget.setCurrentRow(0)
            self.flag = 1
    

    def prev_image(self):
        self.labels = [self.listWidget.item(i).text() for i in range(self.listWidget.count())]
        label_idx = self.labels.index(self.img_path)

        if label_idx > 0:
            self.listWidget.setCurrentRow(label_idx-1)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("There Is No Item Left!")
            msg.setInformativeText('Move Forward')
            msg.setWindowTitle("Warning")
            msg.exec_()


    def next_image(self):
        self.labels = [self.listWidget.item(i).text() for i in range(self.listWidget.count())]
        label_idx = self.labels.index(self.img_path)

        if label_idx < len(self.labels)-1:
            self.listWidget.setCurrentRow(label_idx+1)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("There Is No Item Left!")
            msg.setInformativeText('Move Back')
            msg.setWindowTitle("Warning")
            msg.exec_()


    def ListBar(self):
        # Clear TextFile
        self.textEdit.clear()

        self.img_path = str(self.listWidget.selectedItems()[0].text())
        self.viewer.setPhoto(QtGui.QPixmap(self.img_path))

        # Set Save Button Name to Save
        self.saveButton.setText("Save")
        
        try:
            old_label = [(counter, item) for (counter, item) in enumerate(self.data['data']) if item["imagePath"] == f'{self.img_path}']
            self.textEdit.insertPlainText(old_label[0][1]['label'])
            self.check_path = old_label[0][1]["imagePath"]
            self.img_idx = old_label[0][0]
        except:
            pass


    def save_path(self):
        if self.counter ==0 or self.S_File[0] == '' :
            self.S_File = QtWidgets.QFileDialog.getSaveFileName(None,'Save Json File','./', "Json File (*.json)")
            self.S_File = list(self.S_File)

        if self.S_File[0] :
            if self.S_File[0].split('.')[-1] == 'json':
                with open(self.S_File[0], 'w', encoding="utf-8") as outfile:
                    self.data['date'] = str(datetime.now())
                    json.dump(self.data, outfile, indent=4, ensure_ascii = False)
            else:
                self.S_File[0] +=  '.json'
                with open(self.S_File[0], 'w', encoding="utf-8") as outfile:
                    self.data['date'] = str(datetime.now())
                    json.dump(self.data, outfile, indent=4, ensure_ascii = False)
  
        # Show Pop-Up
        if self.counter > 0:
            msg = QMessageBox()
            msg.setWindowTitle("Save Output") 
            msg.setText('Do You Want to Save The Output File Again?')
            msg.setIcon(QMessageBox.Question)
            msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
            
            msg.buttonClicked.connect(self.popup_button)
            x = msg.exec_()
        
        self.counter += 1

    def popup_button(self,i):
        if i.text() == '&OK':
            self.S_File = QtWidgets.QFileDialog.getSaveFileName(None,'SaveJsonFile','./', "Json File (*.json)")
            self.S_File = list(self.S_File)
        if self.S_File[0]:
            if self.S_File[0].split('.')[-1] == 'json':
                with open(self.S_File[0], 'w', encoding="utf-8") as outfile:
                    self.data['date'] = str(datetime.now())
                    json.dump(self.data, outfile, ensure_ascii = False, indent=4)
            else:
                self.S_File[0] += '.json'
                with open(self.S_File[0], 'w', encoding="utf-8") as outfile:
                    self.data['date'] = str(datetime.now())
                    json.dump(self.data, outfile, ensure_ascii = False, indent=4)
        else:
            pass


    def save_text(self):        
        text = self.textEdit.toPlainText()

        try:
        # if self.img_path:
            if self.check_path != self.img_path:
                img  = cv2.imread(self.img_path,0)
                
                self.data['data'].append({
                                        "imagePath": f"{self.img_path}",
                                        "imageHeight": img.shape[0],
                                        "imageWidth": img.shape[1],
                                        "label": f"{text}",
                                        })
                
                # Change Save Button Name to Done
                self.saveButton.setText("Done")
                self.check_path = self.img_path
            else:
                check_label = [(counter, item) for (counter, item) in enumerate(self.data['data']) if item["imagePath"] == f'{self.img_path}']
                # if self.img_idx is None:
                #     self.img_idx = check_label[0][0]
                
                # Change Save Button Name to Done
                self.saveButton.setText("Done")
                self.data['data'][check_label[0][0]]["label"] = text

            with open(self.S_File[0], 'w', encoding="utf-8") as outfile:
                json.dump(self.data, outfile, ensure_ascii = False, indent=4)

        except Exception as e :
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Please Create Your Output File")
            msg.setInformativeText('')
            msg.setWindowTitle("Error")
            msg.exec_()


class PhotoViewer(QtWidgets.QGraphicsView):
    photoClicked = QtCore.pyqtSignal(QtCore.QPoint)

    def __init__(self, parent):
        super(PhotoViewer, self).__init__()
        self._zoom = 0
        self._empty = True
        self._scene = QtWidgets.QGraphicsScene(self)
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self.setScene(self._scene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(34,37,49)))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

    def hasPhoto(self):
        return not self._empty

    def fitInView(self, scale=True):
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor*0.75, factor*0.75)
            self._zoom = 0

    def setPhoto(self, pixmap=None):
        self._zoom = 0
        if pixmap and not pixmap.isNull():
            self._empty = False
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
        else:
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())
        self.fitInView()

    def wheelEvent(self, event):
        if self.hasPhoto():
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0

    def toggleDragMode(self):
        if self.dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        elif not self._photo.pixmap().isNull():
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

    def mousePressEvent(self, event):
        if self._photo.isUnderMouse():
            self.photoClicked.emit(self.mapToScene(event.pos()).toPoint())
        super(PhotoViewer, self).mousePressEvent(event)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Geeks4LabelTool = QtWidgets.QWidget()
    ui = Ui_Geeks4LabelTool()
    ui.setupUi(Geeks4LabelTool)

    #BackGround Color
    Geeks4LabelTool.setStyleSheet("background-color: #1A1C27;") 

    Geeks4LabelTool.show()
    sys.exit(app.exec_())