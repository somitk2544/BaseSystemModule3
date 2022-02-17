from select import select
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import math

#-------------------------------------------------------#

class Color():
   def __init__(self):
      self.white     = "rgb(255, 255, 255)"
      self.darkgray  = "rgb(48,  55,  60 )" 
      self.darkblue  = "rgb(10,  20,  150)"
      self.lightgray = "rgb(68,  75,  80 )" 
      self.lightblue = "rgb(0,   255, 255)"
      self.red       = "rgb(252, 3,   48 )"

#-------------------------------------------------------#

class Text():
   def __init__(self, window, fontSize, word, posX, posY):
      self.object = QLabel(window)
      self.object.setText(word)
      self.object.setFont(QFont("Arial", fontSize))
      self.object.move(posX, posY)
      self.object.setAlignment(Qt.AlignCenter)
      
   def setPosition(self, posX, posY):
      self.object.move(posX, posY)

   def setSize(self, sizeX, sizeY):
      self.object.resize(sizeX, sizeY)

   def setStyle(self, style):
      self.object.setStyleSheet(style)

   def setText(self, text):
      self.object.setText(text)

#-------------------------------------------------------#

class Button():
   def __init__(self, window, fontSize, word, posX, posY):
      self.object = QPushButton(window)
      self.object.setText(word)
      self.object.setFont(QFont("Arial", fontSize))
      self.object.move(posX, posY)
      self.object.clicked.connect(self.buttonClick)
      self.pressed = False
      
   def setPosition(self, posX, posY):
      self.object.move(posX, posY)

   def setSize(self, sizeX, sizeY):
      self.object.resize(sizeX, sizeY)

   def setStyle(self, style):
      self.object.setStyleSheet(style)

   def buttonClick(self):
      # self.object.setText("Clicked!!")
      self.pressed = not self.pressed
      print(self.pressed)

#-------------------------------------------------------#

class InputBox():
   def __init__(self, window, fontSize, posX, posY):
      self.object = QLineEdit(window)
      self.object.setFont(QFont("Arial", fontSize))
      self.object.move(posX, posY)
      self.object.returnPressed.connect(self.pressEnter)
      self.object.setAlignment(Qt.AlignCenter)
      self.submit = False
      self.disable()

   def setPosition(self, posX, posY):
      self.object.move(posX, posY)

   def setSize(self, sizeX, sizeY):
      self.object.resize(sizeX, sizeY)

   def pressEnter(self):
      self.submit = True
      # print(self.object.text())
      # self.object.setText("")
   
   def clear(self):
      self.object.setText('')

   def disable(self):
      # self.clear()
      self.object.setReadOnly(True)
      self.object.setStyleSheet("color: rgb(48,  55,  60 ); background-color : rgba(0, 0, 0, 70); border : 0px solid rgb(255, 255, 255); border-radius: 7px")

   def enable(self):
      self.object.setReadOnly(False)
      self.object.setStyleSheet("color: rgb(48,  55,  60 ); background-color : rgba(255, 255, 255, 255); border : 0px solid rgb(255, 255, 255); border-radius: 7px")
      
   def getInput(self):
      return self.object.text()

#-------------------------------------------------------#

class Station:
   def __init__(self, window, posX, posY, radius):
      self.selected = []
      self.circle = QPushButton(window)
      self.radius = radius
      self.centerX = posX + radius
      self.centerY = posY + radius
      self.circle.setGeometry(posX, posY, 2*self.radius, 2*self.radius)
      self.circle.setStyleSheet("border-radius : {}; border : 4px solid rgb(252, 3, 48)".format(self.radius))
      self.substation = []
      for i in range(72):
         degree = i*5 - 90
         x = self.radius * math.cos(math.radians(degree)) + self.centerX - 7
         y = self.radius * math.sin(math.radians(degree)) + self.centerY - 7
         self.substation.append(Button(window, 0, '', x, y))
         self.substation[i].setSize(14, 14)
         self.substation[i].setStyle("background-color: white ; border-radius: 7; border: 2px solid rgb(252, 3, 48)")
         self.substation[i].object.clicked.connect(self.selectSubstation)

   def selectSubstation(self):
      for i in range(72):
         if(self.substation[i].pressed):
            self.substation[i].pressed = False
            if(i not in self.selected):
               if(len(self.selected) < 10):
                  self.selected.append(i)
                  self.selected.sort()
                  self.substation[i].setStyle("background-color: black ; border-radius: 7; border: 2px solid black")
                  print(self.selected)
            else:
               self.selected.remove(i)
               self.substation[i].setStyle("background-color: white ; border-radius: 7; border: 2px solid rgb(252, 3, 48)")
               print(self.selected)

#-------------------------------------------------------#