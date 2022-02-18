import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Element import *
from qtwidgets import AnimatedToggle

class UserInterface(QWidget):
   def __init__(self):
      super().__init__()
      self.windowInit()

      self.angle = 0
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
      self.background2.object.setPixmap(QPixmap("/Users/Peace/Desktop/BaseSystemModule3/background.png")) 

      self.title = Text(self, 28, "         BASE SYSTEM         ", 50, 30)
      self.title.setStyle("color: white; border-radius: 25; background-color: {}; padding: 10px".format(self.color.darkgray))

      
      self.logBorder = Text(self, 0, '', 36, 135)
      self.logBorder.setSize(400, 42)
      self.logBorder.setStyle("border-radius: 10; border: 3px solid rgb(0, 0, 150); background-color: rgba(255, 255, 255, 200); padding :5px")
      self.logTag = Text(self, 14, "     MESSAGE     ", 175, 125)
      self.logTag.setStyle("color:white; background-color: {}; border-radius: 7; padding :3px".format(self.color.darkblue))
      self.log = Text(self, 15.5, "   PLEASE SELECT 10 SUB-STATIONS   ", 36, 140)
      self.log.setSize(400, 40)
      self.log.normal()
      
      self.run = Button(self, 20, "RUN", 50, 670)
      self.run.setSize(150, 40)
      self.run.setStyle("color:{}; background-color: {}; border-radius: 10; border: 4px solid {}".format(self.color.white, self.color.darkblue, self.color.darkblue))
      self.run.disable()

      self.home = Button(self, 20, "HOME", 250, 670)
      self.home.setSize(150, 40)
      self.home.setStyle("color:{}; background-color: {}; border-radius: 10; border: 4px solid {}".format(self.color.white, self.color.lightgray, self.color.lightgray))

      self.speedBorder = Text(self, 0, '', 501, 40)
      self.speedBorder.setSize(275, 150)
      self.speedBorder.setStyle("border-radius: 15; border: 3px solid white")
      self.speedTag = Text(self, 14, "   SPEED   ", 597, 30)
      self.speedTag.setStyle("color:{}; background-color: white; border-radius: 7; border: 3px solid white; padding :0px".format(self.color.darkblue))
      self.maxSpeedText = Text(self, 15, "MAX SPEED\t\tRPM", 530, 70)
      self.maxSpeedText.focus()
      self.maxSpeedText.object.setAlignment(Qt.AlignLeft)
      self.maxSpeedInput = InputBox(self, 15, 645, 68)
      self.maxSpeedInput.setSize(40, 25)
      self.maxSpeedInput.focus()
      self.nowSpeedText = Text(self, 15, "NOW SPEED\t0.00\tRPM", 530, 110)
      self.nowSpeedText.object.setAlignment(Qt.AlignLeft)
      self.nowSpeedText.focus()
      self.topSpeedText = Text(self, 15, "TOP SPEED\t0.00\tRPM", 530, 150)
      self.topSpeedText.object.setAlignment(Qt.AlignLeft)
      self.topSpeedText.focus()

      self.goalBorder = Text(self, 0, '', 501, 220)
      self.goalBorder.setSize(275, 330)
      self.goalBorder.setStyle("border-radius: 15; border: 3px solid white")
      self.goalTag = Text(self, 14, "   GOAL   ", 602, 210)
      self.goalTag.setStyle("color:{}; background-color: white; border-radius: 7; border: 3px solid white; padding :0px".format(self.color.darkblue))
      
      self.goalPositionText = Text(self, 15, "ANGULAR\nPOSITION", 540, 253)
      self.goalPositionInput = InputBox(self, 16, 550, 298)
      self.goalPositionInput.setSize(50, 25)
      self.goalDegree = Text(self, 12, "o", 605, 295)
         
      self.goalSingleStationText = Text(self, 15, "SINGLE\nSTATION", 675, 253)
      self.goalSingleStationInput = InputBox(self, 18, 700, 298)
      self.goalSingleStationInput.setSize(25, 25)
      self.goalSharp = Text(self, 15, "#", 685, 300)

      self.goalMultiStationText = Text(self, 15, "MULTI STATION QUEUE", 552, 370)
      self.goalMultiStationText.focus()
      self.goalMultiStationInput = []
      for i in range(3):
         for j in range(5):
            self.goalMultiStationInput.append(InputBox(self, 18, 530+48*j, 400+48*i))
            self.goalMultiStationInput[-1].setSize(25, 25)
            self.goalMultiStationInput[-1].disable()

      self.goalMultiStationInput[0].enable()
      self.goalMultiStationInput[0].focus()

      
   
      
      self.goalLine1 = Text(self, 0, '', 640, 258)
      self.goalLine1.setSize(3, 87)
      self.goalLine1.setStyle("color:{}; background-color: white; border: 3px solid white; padding :0px".format(self.color.darkblue))
      self.goalLine2 = Text(self, 0, '', 524, 344)
      self.goalLine2.setSize(226, 3)
      self.goalLine2.setStyle("color:{}; background-color: white; border: 3px solid white; padding :0px".format(self.color.darkblue))


      self.endEffStatus = "DISABLE"
      self.endEffBorder = Text(self, 0, '', 501, 580)
      self.endEffBorder.setSize(275, 60)
      self.endEffBorder.setStyle("border-radius: 15; border: 3px solid white")
      self.endEffTag = Text(self, 14, "   END-EFFECTOR   ", 567, 570)
      self.endEffTag.setStyle("color:{}; background-color: white; border-radius: 7; border: 3px solid white; padding :0px".format(self.color.darkblue))
      self.endEffText = Text(self, 16, "STATUS", 530, 605)
      self.endEffText.setStyle("color:white")
      self.endEffToggle = AnimatedToggle(self, checked_color="#44ccff", pulse_checked_color="#cc99ccff")
      self.endEffToggle.move(599, 590)
      self.endEffToggle.resize(70, 50)
      self.endEffToggle.toggled.connect(self.endEffControl)
      self.endEffStatusText = Text(self, 16, "DISABLE", 675, 605)
      self.endEffStatusText.setStyle("color:gray")

      self.mcuStatus = "DISCONNECT"
      self.mcuBorder = Text(self, 0, '', 501, 670)
      self.mcuBorder.setSize(275, 60)
      self.mcuBorder.setStyle("border-radius: 15; border: 3px solid white")
      self.mcuTag = Text(self, 14, "   MCU   ", 604, 660)
      self.mcuTag.setStyle("color:{}; background-color: white; border-radius: 7; border: 3px solid white; padding :0px".format(self.color.darkblue))
      self.mcuText = Text(self, 16, "STATUS", 530, 695)
      self.mcuText.setStyle("color:white")
      self.mcuToggle = AnimatedToggle(self, checked_color="#44ccff", pulse_checked_color="#cc99ccff")
      self.mcuToggle.move(599, 681)
      self.mcuToggle.resize(70, 50)
      self.mcuToggle.toggled.connect(self.mcuControl)
      self.mcuStatusText = Text(self, 15, "DISCONNECT", 665, 695)
      self.mcuStatusText.setStyle("color:gray")

      self.arrow = QLabel(self)
      self.arrow.move(40, 225)
      self.arrowImage = QPixmap("/Users/Peace/Desktop/BaseSystemModule3/arrow.png")
      self.arrowImage = self.arrowImage.scaled(390, 390, Qt.KeepAspectRatio)
      self.arrow.setPixmap( self.arrowImage.transformed(QTransform().rotate(0),Qt.SmoothTransformation) )
      self.arrow.setAlignment(Qt.AlignCenter)

      # self.pie = QLabel(self)
      # self.pie.move(35, 220)
      # self.pieImage = QPixmap("/Users/Peace/Desktop/BaseSystemModule3/pie.png")
      # self.pieImage = self.pieImage.scaled(400, 400, Qt.KeepAspectRatio)
      # self.pie.setPixmap( self.pieImage )
      # self.pie.setAlignment(Qt.AlignCenter)

      self.station = Station(self, 35, 220, 200)

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
      self.angle += 1
      self.arrow.setPixmap( self.arrowImage.transformed(QTransform().rotate(self.angle),Qt.SmoothTransformation) )

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

      elif(self.goalMultiStationInput[0].focused and self.focusGoal != 3):
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

      # if( len(self.station.selected) < 10):
      if( len(self.station.selected) < 3):
         self.log.normal()
         # self.log.setText( "   PLEASE SELECT {} SUB-STATIONS   ".format(10-len(self.station.selected)) )
         self.log.setText( "PLEASE SELECT {} SUB-STATIONS".format(3-len(self.station.selected)) )
      else:
         self.log.normal()
         self.log.setText( "PLEASE INPUT MAX SPEED AND GOAL".format(3-len(self.station.selected)) )
         

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
                  self.log.setText("STATION #  CANNOT BE NEGATIVE")
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

      
      for i in range(min(self.goalMultiStationSize, 14)):
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

      self.goalMultiStationInput[14].disable()

      print(self.goalMultiStation, self.goalMultiStationSize)







      if(len(self.substation) == 3 and self.maxSpeed != -1 and msi != ''):
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



            
      # if(len(self.substation) == 3 and self.maxSpeed != -1 and msi != ''):
      #    if(self.focusGoal == 1):
      #       if(self.goalPosition != -1 and gpi != ''):
      #          self.log.normal()
      #          self.log.setText("READY TO RUN")
      #          self.run.enable()
      #          self.run.ready = True
      #       else:
      #          self.run.disable()
      #          self.run.ready = False
      # else:
      #    self.run.disable()
      #    self.run.ready = False

      if(self.run.pressed):
         self.run.pressed = False
         if(self.run.ready):
            self.home.disable()
            self.home.ready = False
            if(self.focusGoal == 1):
               print("Goal Position :", self.goalPosition)
            elif(self.focusGoal == 2):
               print("Goal Single Station :", self.goalSingleStation)
            elif(self.focusGoal == 3):
               print("Goal Multi Station :", self.goalMultiStation[:self.goalMultiStationSize-1])

            print("Max Speed : ", self.maxSpeed)
            print()
   
               # self.home.enable()
               # self.home.ready = True
         # elif(self.focusGoal == 2):
         #    if(self.goalSingleStation != -1):
         #       print("Goal Single Station :", self.goalSingleStation)
         # elif(self.focusGoal == 3):
         #    if(self.goalMultiStation != []):
         #       print("Goal Multi Station :", self.goalMultiStation)

#-----------------------------------------------------------------------------------------------------------------

   def endEffControl(self):
      if(self.endEffStatus == "DISABLE"):
         self.endEffStatus = "ENABLE"
         self.endEffStatusText.setStyle("color:{}".format(self.color.lightblue))
         print("Enable End-Effector")
      else:
         self.endEffStatus = "DISABLE"
         self.endEffStatusText.setStyle("color:gray")
         print("Disable End-Effector")
      self.endEffStatusText.setText(self.endEffStatus)

   def mcuControl(self):
      if(self.mcuStatus == "DISCONNECT"):
         self.mcuStatus = "CONNECT"
         self.mcuStatusText.setStyle("color:{}".format(self.color.lightblue))
         print("Connect MCU")
      else:
         self.mcuStatus = "DISCONNECT"
         self.mcuStatusText.setStyle("color:gray")
         print("Disconnect MCU")
      self.mcuStatusText.setText(self.mcuStatus)


      
   

if __name__ == '__main__':
   app = QApplication(sys.argv)
   BaseSystem = UserInterface()
   sys.exit(app.exec_())