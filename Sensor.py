import myTCP
import socket
import ast

class Sensor:
   'Class for sensors'

   def __init__(self, ipAddress, port):
      self.ipAddress = ipAddress
      self.port = port
   
   def getMeasurements(self):
      rawData = self.getRawDataTCP(self.ipAddress, self.port, 'SEND_ALL_DATA')
     #implement interpret
      return self._interpretRawData(rawData)

   def getRawDataTCP(self, TCP_IP, TCP_PORT, REQUEST):

       BUFFER_SIZE = 1024 


       s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       s.connect((TCP_IP, TCP_PORT))
       s.send(REQUEST)
       data = s.recv(BUFFER_SIZE)
       s.close()

       return data


   def _interpretRawData(rawData):
      # Raw data is a stringified dict: i.e. rawData = "{"Temperature" : 123, ... }"
      # Use the following to convert evaluate string safely into a dict.
      return ast.literal_eval(rawData)