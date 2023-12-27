from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl  

import time
import os
from pipeline import compute_score_for_app

StyleSheet = '''
#progressBar::chunk {
        background-color: #5DB1BB;
}
#comboBox {
        qproperty-alignment: AlignCenter;
}
'''

file_name = None
video_folder = "../voca/generated_animations"
lessons = []


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(859, 566)
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.centralwidget.setFont(font)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setStyleSheet("background-color: rgb(143, 212, 220);")
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 10, 861, 541))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setKerning(True)
        self.frame.setFont(font)
        self.frame.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.frame.setStyleSheet("")
        self.frame.setObjectName("frame")
        self.progressBar = QtWidgets.QProgressBar(self.frame)
        self.progressBar.setGeometry(QtCore.QRect(330, 390, 161, 21))
        self.progressBar.setCursor(QtGui.QCursor(QtCore.Qt.BusyCursor))
        self.progressBar.setStyleSheet("font: 75 bold 10pt \"Arial\";\n"
"color: rgb(26, 68, 94);\n"
"border-color: rgb(85, 85, 255);\n"
"background-color: rgb(255, 255, 255);\n"
"QProgressBar::chunk:progressBar {\n"
"background-color:rgb(255, 255, 255);\n"
"}\n"
"")
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setTextVisible(True)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setObjectName("progressBar")
        self.title = QtWidgets.QLabel(self.frame)
        self.title.setGeometry(QtCore.QRect(230, 40, 360, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(32)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setKerning(False)
        self.title.setFont(font)
        self.title.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        self.title.setStyleSheet("color: rgb(255, 255, 255);background-color: rgba(255,255,255,0);\n"
"font: 75 bold 32pt \"Arial\";")
        self.title.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.title.setFrameShadow(QtWidgets.QFrame.Raised)
        self.title.setLineWidth(1)
        self.title.setMidLineWidth(0)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setObjectName("title")
        self.feedButton_5 = QtWidgets.QPushButton(self.frame)
        self.feedButton_5.setGeometry(QtCore.QRect(290, 190, 251, 51))
        self.feedButton_5.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.feedButton_5.setAutoFillBackground(False)
        self.feedButton_5.setStyleSheet("font: 75 bold 18pt \"Arial\";\n"
"border-color: rgb(85, 85, 255);\n"
"color: rgb(143, 212, 220);\n"
"background-color: rgb(255, 255, 255);")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/Icon awesome-play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.feedButton_5.setIcon(icon)
        self.feedButton_5.setIconSize(QtCore.QSize(24, 26))
        self.feedButton_5.setDefault(False)
        self.feedButton_5.setFlat(False)
        self.feedButton_5.setObjectName("feedButton_5")
        self.feedButton_6 = QtWidgets.QPushButton(self.frame)
        self.feedButton_6.setGeometry(QtCore.QRect(290, 250, 251, 51))
        self.feedButton_6.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.feedButton_6.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.feedButton_6.setAutoFillBackground(False)
        self.feedButton_6.setStyleSheet("font: 75 bold 18pt \"Arial\";\n"
"border-color: rgb(85, 85, 255);\n"
"color: rgb(143, 212, 220);\n"
"background-color: rgb(255, 255, 255);")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/Icon open-media-record.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.feedButton_6.setIcon(icon1)
        self.feedButton_6.setIconSize(QtCore.QSize(24, 24))
        self.feedButton_6.setDefault(False)
        self.feedButton_6.setFlat(False)
        self.feedButton_6.setObjectName("feedButton_6")
        self.feedButton_7 = QtWidgets.QPushButton(self.frame)
        self.feedButton_7.setGeometry(QtCore.QRect(290, 310, 251, 51))
        self.feedButton_7.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.feedButton_7.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.feedButton_7.setAutoFillBackground(False)
        self.feedButton_7.setStyleSheet("font: 75 bold 18pt \"Arial\";\n"
"border-color: rgb(85, 85, 255);\n"
"color: rgb(143, 212, 220);\n"
"background-color: rgb(255, 255, 255);")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/Icon awesome-check.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.feedButton_7.setIcon(icon2)
        self.feedButton_7.setIconSize(QtCore.QSize(32, 32))
        self.feedButton_7.setDefault(False)
        self.feedButton_7.setFlat(False)
        self.feedButton_7.setObjectName("feedButton_7")
        self.feedButton_8 = QtWidgets.QPushButton(self.frame)
        self.feedButton_8.setGeometry(QtCore.QRect(550, 250, 51, 51))
        self.feedButton_8.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.feedButton_8.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.feedButton_8.setAutoFillBackground(False)
        self.feedButton_8.setStyleSheet("font: 75 bold 18pt \"Arial\";\n"
"border-color: rgb(85, 85, 255);\n"
"color: rgb(143, 212, 220);\n"
"background-color: rgb(255, 255, 255);\n"
"border-radius: 25px; ")
        self.feedButton_8.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/icons/Icon material-attach-file.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.feedButton_8.setIcon(icon3)
        self.feedButton_8.setIconSize(QtCore.QSize(32, 32))
        self.feedButton_8.setDefault(True)
        self.feedButton_8.setFlat(False)
        self.feedButton_8.setObjectName("feedButton_8")
        self.widget = QtWidgets.QWidget(self.frame)
        self.widget.setGeometry(QtCore.QRect(220, 40, 501, 481))
        self.widget.setStyleSheet("image: url(:/images/icons/imageedit_4_4021644950.png);\n"
"opacity: 50;")
        self.widget.setObjectName("widget")
        self.widget_2 = QtWidgets.QWidget(self.frame)
        self.widget_2.setGeometry(QtCore.QRect(110, 140, 201, 201))
        self.widget_2.setStyleSheet("image: url(:/images/icons/image (1).png);\n"
"background-color: rbga(255,255,255,0);")
        self.widget_2.setObjectName("widget_2")
        self.progressLabel = QtWidgets.QLabel(self.frame)
        self.progressLabel.setGeometry(QtCore.QRect(20, 420, 781, 31))
        self.progressLabel.setStyleSheet("font: 75 bold 12pt \"Arial\";background-color: rgba(255,255,255,0);\n"
"color: rgb(255, 255, 255);\n")
        self.progressLabel.setTextFormat(QtCore.Qt.AutoText)
        self.progressLabel.setScaledContents(False)
        self.progressLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.progressLabel.setObjectName("progressLabel")
        self.comboBox = QtWidgets.QComboBox(self.frame)
        self.comboBox.setEnabled(True)
        self.comboBox.setGeometry(QtCore.QRect(290, 130, 251, 51))
        self.comboBox.setStyleSheet("font: 75 bold 18pt \"Arial\";\n"
"border-color: rgb(85, 85, 255);\n"
"color: rgb(143, 212, 220);\n"
"background-color: rgb(255, 255, 255);")
        self.comboBox.setMinimumContentsLength(1)
        self.comboBox.setFrame(True)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.widget.raise_()
        self.widget_2.raise_()
        self.progressBar.raise_()
        self.title.raise_()
        self.feedButton_5.raise_()
        self.feedButton_6.raise_()
        self.feedButton_7.raise_()
        self.feedButton_8.raise_()
        self.progressLabel.raise_()
        self.comboBox.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionCredits = QtWidgets.QAction(MainWindow)
        self.actionCredits.setObjectName("actionCredits")
        self.actionRandom_Gen = QtWidgets.QAction(MainWindow)
        self.actionRandom_Gen.setObjectName("actionRandom_Gen")
        self.actionManual_Input = QtWidgets.QAction(MainWindow)
        self.actionManual_Input.setObjectName("actionManual_Input")

        self.opacity_effect = QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(0.2)
        self.widget.setGraphicsEffect(self.opacity_effect)
        self.comboBox.setEditable(True)
        line_edit = self.comboBox.lineEdit()
        line_edit.setAlignment(Qt.AlignCenter)
        line_edit.setReadOnly(True)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.feedButton_7.clicked.connect(self.evaluate)
        self.feedButton_5.clicked.connect(self.show_video)
        self.feedButton_8.clicked.connect(self.select_file)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Speech Therapy"))
        self.title.setToolTip(_translate("MainWindow", "Train your facial motions using AI"))
        self.title.setStatusTip(_translate("MainWindow", "Name of the program"))
        self.title.setText(_translate("MainWindow", "Speech Therapy"))
        self.feedButton_5.setText(_translate("MainWindow", "Watch Tutorial"))
        self.feedButton_6.setText(_translate("MainWindow", "Record Attempt"))
        self.feedButton_7.setText(_translate("MainWindow", "Evaluate"))
        self.progressLabel.setText(_translate("MainWindow", "Progress"))
        self.comboBox.setCurrentText(_translate("MainWindow", "Select Lesson"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Select Lesson"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionCredits.setText(_translate("MainWindow", "Credits"))
        self.actionRandom_Gen.setText(_translate("MainWindow", "Random Gen"))
        self.actionManual_Input.setText(_translate("MainWindow", "Manual Input"))
	
    def update_lessons(self, MainWindow):
        send_msg(self, "notify", "Fetching lessons..")
        self.comboBox.clear()
        for o in get_lessons(self):
            #o = o.capitalize() 
            self.comboBox.addItem(o) 
    
    def show_video(self):
        import cv2
        send_msg(self, "success", "Displaying Video")
        video_path = f"{video_folder}/{self.comboBox.currentText()}/video.mp4"
        print(video_path)
        cap = cv2.VideoCapture(video_path)
        cv2.namedWindow("Lesson", cv2.WINDOW_NORMAL)
        count = 0
        while(cap.isOpened()):
            # Capture frame-by-frame
            ret, frame = cap.read()
            if ret  == True:
                # Display the resulting frame
                cv2.imshow('video', frame)
                if cv2.waitKey(24) & 0xFF == ord('q'):
                    break
                if(count == 0):
                    cv2.waitKey(500)
                count += 1
            else:
                cv2.waitKey(500)
                break

        # When everything done, release the captureq
        cap.release()
        cv2.destroyAllWindows()

    def qt_video(self):
        send_msg(self, "success", "Displaying Video")
        video_path = f"{video_folder}/{self.comboBox.currentText()}/video.mp4"
        print(video_path)
        self._new_window = NewWindow(video_path)
        self._new_window.show()
        
    def select_file(self):
        global file_name
        #file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Single File', QtCore.QDir.rootPath() , '*.mp4')
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Open File", QtCore.QDir.rootPath(), "Videos (*.mp4 *.avi *.mkv *.flv *.mpeg *.mov)")
        send_msg(self, "success", "File Selected")
        #print(file_name)
        
    def evaluate(self):
        global file_name
        if file_name:
            compute_score_for_app(self, file_name, self.comboBox.currentText(), send_msg, set_progress)
        else:
            send_msg(self, "error", "Must select a file using browse")

class NewWindow(QtWidgets.QMainWindow):
    def __init__(self, video):
        super(NewWindow, self).__init__()
        #self._new_window = None
        self.setWindowTitle("Video Lesson")	
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()
        self.resize(640,480)
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(video)))
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.setCentralWidget(videoWidget)
        self.mediaPlayer.play()
        self.mediaPlayer.mediaStatusChanged.connect(self.statusChanged)

    def statusChanged(self, status):


        if status == QMediaPlayer.EndOfMedia:
            self.mediaPlayer.pause()
            time.sleep(5)
            self.mediaPlayer.setPosition(0)
            self.mediaPlayer.play()
            self.close()
        elif status == QMediaPlayer.BufferingMedia:
            print("detected")

def get_lessons(self):
    global lessons
    lessons = []
    try:
        lessons = os.listdir(video_folder)
        send_msg(self, "success", "Select your lesson")
    except Exception as e:
        send_msg(self, "error", "Lessons not found")
    return lessons
     
def send_msg(ui, type, msg):
    _translate = QtCore.QCoreApplication.translate
    if type == "notify":
        ui.progressLabel.setStyleSheet("color: #000000;font-weight: bold;background-color: rgba(255,255,255,0);")
    elif type == "error":
        ui.progressLabel.setStyleSheet("color: #A11515;font-weight: bold;background-color: rgba(255,255,255,0);")
    elif type == "success":
        ui.progressLabel.setStyleSheet("color: #33AA33;font-weight: bold;background-color: rgba(255,255,255,0);")
    elif type == "special":
        ui.progressLabel.setStyleSheet("color: #3a9fbf;font-weight: bold;background-color: rgba(255,255,255,0);")
    ui.progressLabel.setText(_translate("MainWindow", msg))

def set_progress(ui, value):
    ui.progressBar.setProperty("value", value)
    
def setup_program(ui, MainWindow):
    ui.update_lessons(MainWindow)
    MainWindow.activateWindow()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(StyleSheet)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    setup_program(ui, MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
