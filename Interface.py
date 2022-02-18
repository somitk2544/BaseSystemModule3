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
      self.maxSpeed = 0
      self.focusGoal = 3 
      self.goalPosition = 0
      self.goalSingleStation = 1
      self.goalMultiStation  = []

      self.background1 = Text(self, 0, '', 0, 0)
      self.background1.setSize(800, 750)
      self.background1.setStyle("background-color: {}".format(self.color.white))

      self.background2 = Text(self, 0, '', 475, 0)
      self.background2.setSize(325, 750)
      self.background2.object.setPixmap(QPixmap("/Users/Peace/Desktop/BaseSystemModule3/background.png")) 

      self.title = Text(self, 28, "         BASE SYSTEM         ", 50, 30)
      self.title.setStyle("color: white; border-radius: 25; background-color: {}; padding: 10px".format(self.color.darkgray))

      self.log = Text(self, 16, "   PLEASE SELECT 10 SUB-STATIONS   ", 36, 140)
      self.log.setSize(400, 40)
      self.log.setStyle("color:{}; border-radius: 10; border: 3px solid rgb(0, 0, 150); background-color: rgba(255, 255, 255, 200); padding :5px".format(self.color.darkgray))
      
      self.logTag = Text(self, 14, "     MESSAGE     ", 175, 125)
      self.logTag.setStyle("color:white; background-color: {}; border-radius: 7; padding :3px".format(self.color.darkblue))
      self.run = Button(self, 20, "RUN", 50, 670)
      self.run.setSize(150, 40)
      self.run.setStyle("color:{}; background-color: {}; border-radius: 10; border: 4px solid {}".format(self.color.white, self.color.darkblue, self.color.darkblue))

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

      if(self.goalPositionInput.submit):
         self.goalPositionInput.submit = False
         if( self.goalPositionInput.getInput().isnumeric() ):
            self.goalPosition = self.goalPositionInput.getInput()
         else:
            self.log.setText("INPUT NEED TO BE A NUMBER")
            # self.log.setStyle("color:red")
      if(self.goalSingleStationInput.submit):
         self.goalSingleStationInput.submit = False
         self.goalSingleStation = self.goalSingleStationInput.getInput()
      if(self.goalMultiStationInput[0].submit):
         self.goalMultiStationInput[0].submit = False
         self.goalMultiStation.append(int(self.goalMultiStationInput[0].getInput()))

      if(self.run.pressed):
         self.run.pressed = False
         if(self.focusGoal == 1):
            print("Goal Position :", self.goalPosition)
         elif(self.focusGoal == 2):
            print("Goal Single Station :", self.goalSingleStation)
         elif(self.focusGoal == 3):
            print("Goal Multi Station :", self.goalMultiStation)



      # if(self.mode == 1 or self.mode == 3 or self.mode == 5):
      #    # if( len(self.station.selected) < 10):
      #    if( len(self.station.selected) < 3):
      #       self.log.setText( "   PLEASE SELECT {} SUB-STATIONS   ".format(10-len(self.station.selected)) )
      #       self.maxSpeedInput.disable()
      #       self.goalPositionInput.disable()
      #       self.mode = 1
      #    else:
      #       if(self.mode == 1):
      #          self.mode = 2

      # if(self.mode == 2):
      #    self.log.setText( "   PLEASE INPUT MAX SPEED   ")
      #    self.mode = 3

      # if(self.mode == 3):
      #    self.maxSpeedInput.enable()
      #    if(self.maxSpeedInput.submit == True):
      #       self.maxSpeedInput.submit = False
      #       msi = self.maxSpeedInput.getInput()
      #       if(msi.isnumeric()):
      #          msi = int(msi)
      #          if(msi <= 10):
      #             self.maxSpeed = msi
      #             print("Max Speed :", self.maxSpeed)
      #             self.mode = 4
      #          else:
      #             self.log.setText( "   MAX SPEED CANNOT EXCEED 10 RPM   ")
      #             self.maxSpeedInput.clear()
      #       else:
      #          if(msi[0] == '-'):
      #             self.log.setText( "   MAX SPEED NEED CANNOT BE NEGATIVE   ")
      #             self.maxSpeedInput.clear()
      #          else:
      #             self.log.setText( "   MAX SPEED NEED TO BE A NUMBER   ")
      #             self.maxSpeedInput.clear()

      # if(self.mode == 4):
      #    self.log.setText( "   PLEASE INPUT GOAL POSITION   ")
      #    self.mode = 5
      
      # if(self.mode == 5):
      #    self.goalPositionInput.enable()

      # print(self.mode)




   def endEffControl(self):
      if(self.endEffStatus == "DISABLE"):
         self.endEffStatus = "ENABLE"
         self.endEffStatusText.setStyle("color:{}".format(self.color.lightblue))
      else:
         self.endEffStatus = "DISABLE"
         self.endEffStatusText.setStyle("color:gray")
      self.endEffStatusText.setText(self.endEffStatus)

   def mcuControl(self):
      if(self.mcuStatus == "DISCONNECT"):
         self.mcuStatus = "CONNECT"
         self.mcuStatusText.setStyle("color:{}".format(self.color.lightblue))
      else:
         self.mcuStatus = "DISCONNECT"
         self.mcuStatusText.setStyle("color:gray")
      self.mcuStatusText.setText(self.mcuStatus)


      
   

if __name__ == '__main__':
   app = QApplication(sys.argv)
   BaseSystem = UserInterface()
   sys.exit(app.exec_())