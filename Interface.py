import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Element import *
from qtwidgets import AnimatedToggle
import platform
import serial
import math

os = platform.platform()[0].upper()
if os == 'M': #Mac
   ser = serial.Serial('/dev/cu.usbmodem14103', 512000, parity='E', stopbits=1, timeout=1)
elif os == 'W': #Windows
   ser = serial.Serial('COM3',512000,parity='E',stopbits=1,timeout=1)

class UserInterface(QWidget):
   def __init__(self):
      super().__init__()
      self.windowInit()

      self.currentStation = 0
      self.currentAngle = 0
      self.currentSpeed = 0

      self.substation = []
      self.maxSpeed = -1
      self.focusGoal = 3 
      self.goalPosition = -1
      self.goalSingleStation = -1
      self.goalMultiStation  = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
      self.goalMultiStationSize = 1
      self.goalMultiStationError = False

      self.background1 = Text(self, 0, '', 0, 0)
      self.background1.setSize(800, 750)
      self.background1.setStyle("background-color: {}".format(self.color.white))

      self.background2 = Text(self, 0, '', 475, 0)
      self.background2.setSize(325, 750)
      self.background2.object.setPixmap(QPixmap("Desktop/BaseSystemModule3/background.png")) if os == 'M' else self.background2.object.setPixmap(QPixmap("./background.png"))

      self.title = Text(self, 28, "         BASE SYSTEM         ", 50, 30)
      self.title.setFontSize(18) if os == 'W' else False
      self.title.setStyle("color: white; border-radius: 25; background-color: {}; padding: 10px".format(self.color.darkgray))
      
      self.logBorder = Text(self, 0, '', 36, 135)
      self.logBorder.setSize(400, 42)
      self.logBorder.setStyle("border-radius: 10; border: 3px solid rgb(0, 0, 150); background-color: rgba(255, 255, 255, 200); padding :5px")
      self.logTag = Text(self, 14, "     MESSAGE     ", 175, 125)
      self.logTag.setFontSize(8) if os == 'W' else False
      self.logTag.setStyle("color:white; background-color: {}; border-radius: 7; padding :3px".format(self.color.darkblue))
      self.log = Text(self, 15.5, "   PLEASE SELECT 10 SUB-STATIONS   ", 36, 140)
      self.log.setFontSize(10) if os == 'W' else False
      self.log.setSize(400, 40)
      self.log.normal()
      
      self.run = Button(self, 20, "RUN", 50, 670)
      self.run.setFontSize(12) if os == 'W' else False
      self.run.setSize(150, 40)
      self.run.setStyle("color:{}; background-color: {}; border-radius: 10; border: 4px solid {}".format(self.color.white, self.color.darkblue, self.color.darkblue))
      self.run.disable()

      self.home = Button(self, 20, "HOME", 250, 670)
      self.home.setFontSize(12) if os == 'W' else False
      self.home.setSize(150, 40)
      self.home.setStyle("color:{}; background-color: {}; border-radius: 10; border: 4px solid {}".format(self.color.white, self.color.lightgray, self.color.lightgray))
      self.home.ready = True

      self.speedBorder = Text(self, 0, '', 501, 40)
      self.speedBorder.setSize(275, 150)
      self.speedBorder.setStyle("border-radius: 15; border: 3px solid white")
      self.speedTag = Text(self, 14, "   SPEED   ", 597, 30)
      self.speedTag.setFontSize(9) if os == 'W' else False
      self.speedTag.setStyle("color:{}; background-color: white; border-radius: 7; border: 3px solid white".format(self.color.darkblue))
      self.maxSpeedText = Text(self, 15, "MAX SPEED\t\tRPM", 530, 70)
      self.maxSpeedText.setFontSize(9) if os == 'W' else False
      self.maxSpeedText.focus()
      self.maxSpeedText.object.setAlignment(Qt.AlignLeft)
      self.maxSpeedInput = InputBox(self, 15, 645, 68)
      self.maxSpeedInput.setPosition(635, 68) if os == 'W' else False
      self.maxSpeedInput.setFontSize(9) if os == 'W' else False
      self.maxSpeedInput.setSize(40, 25)
      self.maxSpeedInput.focus()
      self.nowSpeedText = Text(self, 15, "NOW SPEED\t0.00\tRPM", 530, 110)
      self.nowSpeedText.setFontSize(9) if os == 'W' else False
      self.nowSpeedText.object.setAlignment(Qt.AlignLeft)
      self.nowSpeedText.focus()
      self.topSpeedText = Text(self, 15, "TOP SPEED\t0.00\tRPM", 530, 150)
      self.topSpeedText.setFontSize(9) if os == 'W' else False
      self.topSpeedText.object.setAlignment(Qt.AlignLeft)
      self.topSpeedText.focus()

      self.goalBorder = Text(self, 0, '', 501, 220)
      self.goalBorder.setSize(275, 330)
      self.goalBorder.setStyle("border-radius: 15; border: 3px solid white")
      self.goalTag = Text(self, 14, "   GOAL   ", 602, 210)
      self.goalTag.setFontSize(9) if os == 'W' else False
      self.goalTag.setStyle("color:{}; background-color: white; border-radius: 7; border: 3px solid white".format(self.color.darkblue))
      
      self.goalPositionText = Text(self, 15, "ANGULAR\nPOSITION", 540, 253)
      self.goalPositionText.setFontSize(9) if os == 'W' else False
      self.goalPositionInput = InputBox(self, 16, 550, 298)
      self.goalPositionInput.setFontSize(9) if os == 'W' else False
      self.goalPositionInput.setSize(50, 25)
      self.goalDegree = Text(self, 12, "o", 605, 295)
      self.goalDegree.setFontSize(7) if os == 'W' else False
         
      self.goalSingleStationText = Text(self, 15, "SINGLE\nSTATION", 675, 253)
      self.goalSingleStationText.setFontSize(9) if os == 'W' else False
      self.goalSingleStationInput = InputBox(self, 18, 700, 298)
      self.goalSingleStationInput.setFontSize(9) if os == 'W' else False
      self.goalSingleStationInput.setSize(25, 25)
      self.goalSharp = Text(self, 15, "#", 685, 300)
      self.goalSharp.setFontSize(9) if os == 'W' else False

      self.goalMultiStationText = Text(self, 15, "MULTI STATION QUEUE", 552, 370)
      self.goalMultiStationText.setFontSize(9) if os == 'W' else False
      self.goalMultiStationText.focus()
      self.goalMultiStationInput = []
      for i in range(3):
         for j in range(5):
            self.goalMultiStationInput.append(InputBox(self, 18, 530+48*j, 400+48*i))
            self.goalMultiStationInput[-1].setFontSize(9) if os == 'W' else False
            self.goalMultiStationInput[-1].setSize(25, 25)
            self.goalMultiStationInput[-1].disable()
      
      self.goalMultiStationInput.append(InputBox(self, 18, 1000, 1000))
      self.goalMultiStationInput[-1].setSize(25, 25)
      self.goalMultiStationInput[-1].disable()

      self.goalMultiStationInput[0].enable()
      self.goalMultiStationInput[0].focus()

         
      self.goalLine1 = Text(self, 0, '', 640, 253)
      self.goalLine1.setSize(3, 92)
      self.goalLine1.setStyle("background-color: white; border: 3px solid white")
      self.goalLine2 = Text(self, 0, '', 524, 344)
      self.goalLine2.setSize(226, 3)
      self.goalLine2.setStyle("background-color: white; border: 3px solid white")


      self.endEffStatus = "DISABLE"
      self.endEffBorder = Text(self, 0, '', 501, 580)
      self.endEffBorder.setSize(275, 60)
      self.endEffBorder.setStyle("border-radius: 15; border: 3px solid white")
      self.endEffTag = Text(self, 14, "   END-EFFECTOR   ", 567, 570)
      self.endEffTag.setStyle("color:{}; background-color: white; border-radius: 7; border: 3px solid white".format(self.color.darkblue))
      self.endEffTag.setFontSize(9) if os == 'W' else False
      self.endEffText = Text(self, 16, "STATUS", 530, 605)
      self.endEffText.setStyle("color:white")
      self.endEffText.setFontSize(9) if os == 'W' else False
      self.endEffToggle = AnimatedToggle(self, checked_color="#44ccff", pulse_checked_color="#0099ccff", pulse_unchecked_color="#00ffffff")
      self.endEffToggle.move(599, 590)
      self.endEffToggle.resize(70, 50)
      self.endEffToggle.toggled.connect(self.endEffControl)
      self.endEffStatusText = Text(self, 16, "DISABLE", 675, 605)
      self.endEffStatusText.setFontSize(9) if os == 'W' else False
      self.endEffStatusText.setStyle("color:gray")

      self.mcuStatus = "DISCONNECT"
      self.mcuBorder = Text(self, 0, '', 501, 670)
      self.mcuBorder.setSize(275, 60)
      self.mcuBorder.setStyle("border-radius: 15; border: 3px solid white")
      self.mcuTag = Text(self, 14, "   MCU   ", 604, 660)
      self.mcuTag.setFontSize(9) if os == 'W' else False
      self.mcuTag.setStyle("color:{}; background-color: white; border-radius: 7; border: 3px solid white".format(self.color.darkblue))
      self.mcuText = Text(self, 16, "STATUS", 530, 695)
      self.mcuText.setFontSize(9) if os == 'W' else False
      self.mcuText.setStyle("color:white")
      self.mcuStatusText = Text(self, 15, "DISCONNECT", 665, 694)
      self.mcuStatusText.setFontSize(9) if os == 'W' else False
      self.mcuStatusText.setStyle("color:gray")
      self.mcuStatusText.setSize(100,20)
      self.mcuToggle = AnimatedToggle(self, checked_color="#44ccff", pulse_checked_color="#0099ccff", pulse_unchecked_color="#00ffffff")
      self.mcuToggle.move(599, 681)
      self.mcuToggle.resize(70, 50)
      self.mcuToggle.toggled.connect(self.mcuControl)
      self.mcuToggle.toggle()
      
      self.arrow = QLabel(self)
      self.arrow.move(40, 230)
      if(os == 'M'):
         self.arrowImage = QPixmap("Desktop/BaseSystemModule3/arrow.png")
      elif os == 'W':
         self.arrowImage = QPixmap("./arrow.png")
      self.arrowImage = self.arrowImage.scaled(390, 390, Qt.KeepAspectRatio)
      self.arrow.setPixmap( self.arrowImage.transformed(QTransform().rotate(0),Qt.SmoothTransformation) )
      self.arrow.setAlignment(Qt.AlignCenter)

      self.homeLine = Text(self, 0, '',233, 205)
      self.homeLine.setSize(5, 40)
      self.homeLine.setStyle("background-color: red; border: 3px solid red")
      
      self.station = Station(self, 35, 225, 200)

      self.timer=QTimer()
      self.timer.timeout.connect(self.showTime)
      self.timer.start(100)
      self.show()

   def windowInit(self):
      self.setFixedSize(800, 750)
      self.setWindowTitle("Base System")
      qr = self.frameGeometry()
      cp = QDesktopWidget().availableGeometry().center()
      qr.moveCenter(cp)
      self.move(qr.topLeft())
      self.color = Color()

   def showTime(self):
      # self.currentAngle += 1
      self.arrow.setPixmap( self.arrowImage.transformed(QTransform().rotate(self.currentAngle),Qt.SmoothTransformation) )

      focusMultiStationInput = False
      for i in range(15):
         if(self.goalMultiStationInput[i].focused):
            focusMultiStationInput = True

      if(self.goalPositionInput.focused and self.focusGoal != 1):
         self.goalSingleStationInput.unfocus()
         self.goalSingleStationText.unfocus()
         for i in range(15):
            self.goalMultiStationInput[i].unfocus()
         self.goalMultiStationText.unfocus()
         self.goalSharp.unfocus()
         self.goalPositionInput.focus()
         self.goalPositionText.focus()
         self.goalDegree.focus()
         self.focusGoal = 1

      elif(self.goalSingleStationInput.focused and self.focusGoal != 2):
         self.goalPositionInput.unfocus()
         self.goalPositionText.unfocus()
         for i in range(15):
            self.goalMultiStationInput[i].unfocus()
         self.goalMultiStationText.unfocus()
         self.goalDegree.unfocus()
         self.goalSingleStationInput.focus()
         self.goalSingleStationText.focus()
         self.goalSharp.focus()
         self.focusGoal = 2

      elif(focusMultiStationInput and self.focusGoal != 3):
         self.goalPositionInput.unfocus()
         self.goalPositionText.unfocus()
         self.goalSingleStationInput.unfocus()
         self.goalSingleStationText.unfocus()
         self.goalDegree.unfocus()
         self.goalSharp.unfocus()
         self.goalMultiStationInput[0].focus()
         self.goalMultiStationText.focus()
         self.focusGoal = 3

#-----------------------------------------------------------------------------------------------------------------

      self.log.normal()
      self.log.setText("HELLO")

      self.substation = self.station.selected

      if( len(self.station.selected) < 10):
         self.log.normal()
         self.log.setText("PLEASE SELECT {} SUB-STATIONS".format(10-len(self.station.selected)) )
      else:
         self.log.normal()
         self.log.setText("PLEASE INPUT MAX SPEED AND GOAL")
         

      msi = self.maxSpeedInput.getInput()
      if(msi.replace('.','',1).isdigit()):
         if(float(msi) > 10):
            self.log.error()
            self.log.setText("MAX SPEED CANNOT EXCEED 10 RPM")
            self.maxSpeed = -1
         elif(float(msi) < 5):
            self.log.error()
            self.log.setText("MAX SPEED CANNOT BELOW 5 RPM")
            self.maxSpeed = -1
         else:
            self.maxSpeed = msi
      else:
         if(msi != ''):
            if(msi[0] == '-'):
               self.log.error()
               self.log.setText("MAX SPEED CANNOT BE NEGATIVE")
               self.maxSpeed = -1
            else:
               self.log.error()
               self.log.setText("INPUT MAX SPEED NEED TO BE A NUMBER")
               self.maxSpeed = -1
      # print(self.maxSpeed)

      gpi = self.goalPositionInput.getInput()
      if(self.focusGoal == 1):
         if(gpi.replace('.','',1).isdigit()):
            if(float(gpi) >= 360):
               self.log.error()
               self.log.setText("POSITION NEED TO BE LESS THAN 360 DEGREE")
               self.goalPosition = -1
            else:
               self.goalPosition = gpi
         else:
            if(gpi != ''):
               if(gpi[0] == '-'):
                  self.log.error()
                  self.log.setText("POSITION CANNOT BE NEGATIVE")
                  self.goalPosition = -1
               else:
                  self.log.error()
                  self.log.setText("INPUT POSITION NEED TO BE A NUMBER")
                  self.goalPosition = -1
         # print(self.goalPosition)

      gssi = self.goalSingleStationInput.getInput()
      if(self.focusGoal == 2):
         if(gssi.isdigit()):
            if(int(gssi) < 1 or int(gssi) > 10):
               self.log.error()
               self.log.setText("INPUT STATION # BETWEEN 1-10")
               self.goalSingleStation = -1
            else:
               self.goalSingleStation = gssi
         else:
            if(gssi != ''):
               if(gssi[0] == '-'):
                  self.log.error()
                  self.log.setText("STATION # CANNOT BE NEGATIVE")
                  self.goalSingleStation = -1
               else:
                  self.log.error()
                  self.log.setText("STATION # NEED TO BE AN INTEGER")
                  self.goalSingleStation = -1
      # print(self.goalSingleStation)

      for i in range(self.goalMultiStationSize):
         gmsi = self.goalMultiStationInput[i].getInput()
         if(self.focusGoal == 3):
            if(gmsi.isdigit()):
               if(int(gmsi) < 1 or int(gmsi) > 10):
                  self.log.error()
                  self.log.setText("INPUT STATION # BETWEEN 1-10")
                  self.goalMultiStationError = True
                  self.goalMultiStation[i] = -1
               else:
                  self.goalMultiStationError = False
                  self.goalMultiStation[i] = int(gmsi) 
            else:
               if(gmsi != ''):
                  if(gmsi[0] == '-'):
                     self.log.error()
                     self.log.setText("STATION #  CANNOT BE NEGATIVE")
                     self.goalMultiStationError = True
                     self.goalMultiStation[i] = -1
                  else:
                     self.log.error()
                     self.log.setText("STATION # NEED TO BE AN INTEGER")
                     self.goalMultiStationError = True
                     self.goalMultiStation[i] = -1
               else:
                  if(i != self.goalMultiStationSize - 1):
                     self.goalMultiStation[i] = -1

      
            for i in range(min(self.goalMultiStationSize, 15)):
               if(self.goalMultiStation[i] != -1):
                  self.goalMultiStationInput[i+1].enable()
                  self.goalMultiStationInput[i+1].focus()
                  self.goalMultiStationSize = i+2
               else:
                  self.goalMultiStationInput[i+1].disable()
                  self.goalMultiStationSize = i+1

            for i in range(15):
               if(self.goalMultiStation[i] == -1):
                  self.goalMultiStationSize = i+1
                  break

            for i in range(self.goalMultiStationSize, 15):
               self.goalMultiStationInput[i].disable()

            # print(self.goalMultiStation, self.goalMultiStationSize)


#-----------------------------------------------------------------------------------------------------------------

      if(len(self.substation) == 10 and self.maxSpeed != -1 and msi != ''):
         self.run.ready = False
         if(self.focusGoal == 1):
            if(self.goalPosition != -1 and gpi != ''):
               self.run.ready = True              
         elif(self.focusGoal == 2):
            if(self.goalSingleStation != -1 and gssi != ''):
               self.run.ready = True
         elif(self.focusGoal == 3):
            if(self.goalMultiStationError == False and self.goalMultiStationSize > 1):
               self.run.ready = True
      else:
         self.run.ready = False

      if(self.run.ready):
         self.log.normal()
         self.log.setText("READY TO RUN")
         self.run.enable()
      else:
         self.run.disable()

      if(self.run.pressed):
         self.run.pressed = False
         if(self.run.ready and self.mcuStatus == "CONNECT"):
            self.home.disable()
            self.home.ready = False
            if(self.endEffStatus == "ENABLE"):
               self.mode_12() # Enable End-Effector
            elif(self.endEffStatus == "DISABLE"):
               self.mode_13() # Disable End-Effector
            
            if(self.focusGoal == 1):
               self.mode_5() # Set Goal Position
            elif(self.focusGoal == 2):
               self.mode_6() # Set Goal Single Station
            elif(self.focusGoal == 3):
               self.mode_7() # Set Goal Multi Station

            self.mode_4() # Set Max Speed

      if(self.home.pressed):
         self.home.pressed = False
         if(self.home.ready and self.mcuStatus == "CONNECT"):
            self.mode_14() # Set Home

#-----------------------------------------------------------------------------------------------------------------

   def endEffControl(self):
      if(self.endEffStatus == "DISABLE"):
         self.endEffStatus = "ENABLE"
         self.endEffStatusText.setStyle("color:{}".format(self.color.lightblue))
         if(self.mcuStatus == "CONNECT"):
            self.mode_12() # Enable End-Effector
      else:
         self.endEffStatus = "DISABLE"
         self.endEffStatusText.setStyle("color:gray")
         if(self.mcuStatus == "CONNECT"):
            self.mode_13() # Disable End-Effector
      self.endEffStatusText.setText(self.endEffStatus)

   def mcuControl(self):
      if(self.mcuStatus == "DISCONNECT"):
         self.mcuStatus = "CONNECT"
         self.mcuStatusText.setStyle("color:{}".format(self.color.lightblue))
         self.mode_2() # Connect MCU
      else:
         self.mcuStatus = "DISCONNECT"
         self.mcuStatusText.setStyle("color:gray")
         self.mode_3() # Disconnect MCU
      self.mcuStatusText.setText(self.mcuStatus)

   def checkSum(self,dataFrame):
      return (~(sum(dataFrame)%256))%256

   def serialWait(self):
      while(ser.in_waiting == 0):
         pass

   def mode_1(self):
      pass

   def mode_2(self):
      ser.write([146,109]) # 10010010 01101101
      self.serialWait()
      if(ser.read(2) == b'Xu'):
         print("Connect MCU")

   def mode_3(self):
      ser.write([147,108]) # 10010011 01101100
      self.serialWait()
      if(ser.read(2) == b'Xu'):
         print("Disconnect MCU")

   def mode_4(self):
      serialList = [148,0] # 10010100 00000000
      serialList.append(int(float(self.maxSpeed)*255/10)) # 8 bit (0-255) but 255 will equal to 11111111 which is blank (-1)
      serialList.append(self.checkSum(serialList))
      print(serialList)
      ser.write(serialList)
      self.serialWait()
      if(ser.read(2) == b'Xu'):
         print("Max Speed : ", self.maxSpeed)
         self.mode_8() # Go to Goal

   def mode_5(self):
      serialList = [149] # 10010101
      goalRad = int(float(self.goalPosition)*10000*math.pi/180)
      serialList.append(int(goalRad / 256)) # 1st 8 bit (0-255)
      serialList.append(int(goalRad % 256)) # 2nd 8 bit (0-255)
      serialList.append(self.checkSum(serialList))
      print(serialList)
      ser.write(serialList)
      self.serialWait()
      if(ser.read(2) == b'Xu'):
         print("Goal Position :", self.goalPosition)

   def mode_6(self):
      serialList = [150,0] # 10010110 00000000
      serialList.append(int(self.goalSingleStation)) # 1-10
      serialList.append(self.checkSum(serialList))
      ser.write(serialList)
      self.serialWait()
      if(ser.read(2) == b'Xu'):
         print("Goal Single Station :", self.goalSingleStation)

   def mode_7(self):
      serialList = [151] # 10010111 
      serialList.append(self.goalMultiStationSize-1)
      for i in range(self.goalMultiStationSize-1):
         serialList.append(int(self.goalMultiStation[i])) # 1-10
      serialList.append(self.checkSum(serialList))
      ser.write(serialList)
      self.serialWait()
      if(ser.read(2) == b'Xu'):
         print("Goal Multi Station :", self.goalMultiStation[:self.goalMultiStationSize-1])
      
   def mode_8(self):
      ser.write([152,103]) # 10011000 01100111
      self.serialWait()
      if(ser.read(2) == b'Xu'):
         print("RUN!! Go to Goal\n")
      self.serialWait()
      if(ser.read(2) == b'Fn'):
         print("FINISHED!! Reach Goal\n")

   def mode_9(self):
      return
      ser.write([153,102]) # 10011001 01100110
      self.serialWait()
      if(ser.read(2) == b'Xu'):
         print("Recieved Current Station")
      self.currentStation = ser.read(4)
      print(self.currentStation)
      

   def mode_10(self):
      return
      ser.write([154,101]) # 10011010 01100101
      self.serialWait()
      if(ser.read(2) == b'Xu'):
         print("Recieved Current Angle")
      self.currentAngle = ser.read(4)
      print(self.currentAngle)

   def mode_11(self):
      return
      ser.write([155,100]) # 10011011 01100100
      self.serialWait()
      if(ser.read(2) == b'Xu'):
         print("Recieved Current Speed")
      self.currentSpeed = ser.read(4)
      print(self.currentSpeed)

   def mode_12(self):
      ser.write([156,99]) # 10011100 01100011
      self.serialWait()
      if(ser.read(2) == b'Xu'):
         print("Enable End-Effector")

   def mode_13(self):
      ser.write([157,98]) # 10011101 01100010
      self.serialWait()
      if(ser.read(2) == b'Xu'):
         print("Disable End-Effector")

   def mode_14(self):
      ser.write([158,97]) # 10011110 01100001
      self.serialWait()
      if(ser.read(2) == b'Xu'):
         print("Set Home")


if __name__ == '__main__':
   app = QApplication(sys.argv)
   BaseSystem = UserInterface()
   sys.exit(app.exec_())