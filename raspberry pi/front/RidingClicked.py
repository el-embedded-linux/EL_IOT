import platform
from BackCam import *
if platform.system()=='Linux':
    import FrontCam
    import SpeedMeter
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# 주행다이얼로그
class RidingClicked(QDialog):
    def __init__(self):
        super().__init__()
        self.formSetting()

    def formSetting(self):
        self.setStyleSheet("background-color:rgb(41,41,41)")

        self.cameraLabel = QLabel(self)
        self.heartRateImage = QMovie("Images/heart.gif", QByteArray(), self)
        self.heartRateScreen = QLabel(self)
        self.heartRate = QLabel(self)
        self.distance = QLabel(self)
        self.direction = QLabel(self)
        self.speed = QLabel(self)
        self.backButton = QPushButton(self)

        self.cameraLabel.setGeometry(0,0,800,480)
        self.heartRateScreen.setGeometry(15,20,80,80)
        self.heartRate.setGeometry(100,10,150,100)
        self.distance.setGeometry(430, 35, 60, 20)
        self.direction.setGeometry(430, 55, 60, 40)
        self.speed.setGeometry(510,10,280,100)
        self.backButton.setGeometry(712,428,70,30)

        self.heartRateScreen.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.heartRateScreen.setAlignment(Qt.AlignCenter)
        self.distance.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.direction.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.cameraLabel.setStyleSheet("background-color:rgba(255,0,0,0)")
        self.heartRate.setStyleSheet("background-color:rgba(255,255,255,0);color:white;font:bold 80px Arial;")
        self.heartRateScreen.setStyleSheet("background-color:rgba(255,255,255,0)")
        self.distance.setStyleSheet("background-color:rgba(255,255,255,0);color:white;font:bold 16px Arial;")
        self.direction.setStyleSheet("background-color:rgba(255,255,255,0);")
        self.speed.setStyleSheet("background-color:rgba(255,255,255,0);color:white;font:bold 80px Arial;")
        self.backButton.setText("Quit")
        self.backButton.setStyleSheet("font:bold 14px Arial; color:rgb(41,41,41); border:0px; border-radius:5px; background-color:rgb(106,230,197); outline:0px;")
        self.backButton.clicked.connect(self.quit)

        if platform.system() == 'Linux':
            SpeedMeter.speedmeter.callback = self.speedUpdate #콜백함수 등록
            SpeedMeter.speedmeter.start_b() #테스트용 쓰레드 시작

        backcam.frameUpdate = self.frameUpdate #영상 라벨 전달
        if platform.system()=='Linux':
            self.frontCamera = FrontCam.FrontCam() #카메라 객체 생성 & 녹화 시작

        self.heartRateImage.setCacheMode(QMovie.CacheAll)
        self.heartRateImage.setSpeed(120)
        self.heartRateScreen.setMovie(self.heartRateImage)
        self.heartRateImage.start()

        self.fontEffect(self.speed)
        self.fontEffect(self.heartRate)
        self.speedUpdate('10')
        self.showFullScreen()

    def fontEffect(self, item):
        effect = QGraphicsDropShadowEffect()
        effect.setBlurRadius(10)
        effect.setColor(QColor("black"))
        effect.setOffset(1,1)
        item.setGraphicsEffect(effect)

    def heartRateUpdate(self, data):
        if int(data) < 10:
            dataOutput = '0' + data
        else:
            dataOutput = data

        self.heartRate.setText(dataOutput)   #심박수 완료 후 변경

    def navUpdate(self, distance, direction):      #네비 테스트 완료 후 변경, 이미지 넣어야 함
        if direction == 'right':
            img = QPixmap('Images/sunny.png')
        elif direction == 'left':
            img = QPixmap('Images/cloudy.png')
        elif direction == 'uturn':
            img = QPixmap('Images/rainny.png')
        else :
            img = QPixmap('Images/sunny.png')
        self.distance.setText(str(distance)+'m')
        self.direction.setPixmap(img)

    def speedUpdate(self, data): #속도 데이터 수신 콜백함수
        if int(data) < 10 :
            dataOutput = '0' + data
            self.navUpdate(100, 'right')  # 네비 완료 후 변경
        else :
            dataOutput = data
            self.navUpdate(10, 'left')  # 네비 완료 후 변경

        self.heartRateUpdate(data)      #심박수 완료 후 변경
        self.speed.setText(dataOutput+"km/h")

    def frameUpdate(self):
        self.cameraLabel.clear() # Label을 clear하여 paintEvent가 실행되도록 함

    def paintEvent(self, QPaintEvent):
        painter = QPainter(self)
        if backcam.image != None:
            painter.drawImage(0,0,backcam.image) # 카메라객체에 가장 최근 프레임을 그림


    def quit(self):
        self.heartRateImage.stop()
        if platform.system()=='Linux':
            SpeedMeter.speedmeter.stop()
            self.frontCamera.stop()
        backcam.stop()
        self.close()
