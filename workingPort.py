#!/usr/bin/python
# Import the Serial module
import serial;
import time

EOL = "\r";
SSC32_Port = '/dev/ttyUSB0'

panServo = 0;              # Servo in the base
LeftMStop = 1520;

tiltServo = 1;            
RightMStop = 1525;

PanChan = 2;                # Pan servo channel
PanHome = 150;
PanREnd = 2700;
PanLEnd = 800;

TiltChan = 3;                  # Tilt servo channel
TiltHome = 1430;
TiltUEnd = 500;
TiltDEnd = 1550;

class SSC32:
  def __init__(self):
    EOL = "\r";
    self.command = "";
    
    #   Open the port at 115200 Bps - defaults to 8N1
    self.ssc32 = serial.Serial(SSC32_Port, 115200);

  # Reads single characters until a CR is read
  def Response (self):
     ich = "";
     resp = "";

     while (ich <> '\r'):
        ich = self.ssc32.read(1);
        
        if (ich <> '\r'):
           resp = resp + ich;
     return resp;
        

  # Converts a servo position in degrees to uS for the SSC-32
  def To_Degrees (self, uS):
     result = 0;
     
     result = (uS - 1500) / 10;
     
     return result;

  # Converts an SSC-32 servo position in uS to degrees
  def To_uS (self, degrees):
     result = 0;
     
     result = (degrees * 10) + 1500;
     
     return result;


  #def panLR(position):
      

  def Send_Command (self, cmd, sendeol):
     
     result = self.ssc32.write (cmd);
     
     if (sendeol):
        self.ssc32.write (EOL);
     
     return result;

  def Send_EOL (self):

     result = self.ssc32.write(EOL);
     
     return result;


  def run(self):
    #   Send the version command
    command = "ver";
    self.Send_Command( command, False)
    self.Send_EOL ();

    #   Read the response
    inp = self.Response();

    #   Show what we got back

    while True:
        command = raw_input("> ")
        if command == "q":
            break
        else:
            print command
            self.Send_Command(command,True)
        time.sleep(.5)
    print inp;

    #   Close the port
    self.ssc32.close();

  def executeSingleCommand(self,command):
    self.Send_Command(command,True)

#test = SSC32()
#test.run()