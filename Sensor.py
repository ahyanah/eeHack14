import socket
import ast
import re
import csv

class Sensor:
   'Class for sensors'

   def __init__(self, ipAddress, port):
      self.ipAddress = ipAddress
      self.port = port
   
   def getMeasurements(self):
      data = self.getRawDataTCP(self.ipAddress, self.port, 'SEND_ALL_DATA')
     #implement interpret
      return data

   def getRawDataTCP(self, TCP_IP, TCP_PORT, REQUEST):

       BUFFER_SIZE = 1024 


       s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       s.connect((TCP_IP, TCP_PORT))
       s.send(REQUEST)
       data = s.recv(BUFFER_SIZE)
       s.close()

       #print data

       #print self._interpretRawData(data)
       return self._interpretRawData(data)


 


   def _interpretRawData(self,rawData):
       newData = rawData.translate(None, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ:=\' ')
       #print newData
       values = newData.split(',')
       #print values
       dictData = {"Light" : values[0], "Temperature" : values[1], "Sound" : values[2]}
       #print dictData
       return dictData
