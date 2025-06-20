import matplotlib.pyplot as plt
import numpy as np
import sys
import glob
from time import sleep
import serial
import re
def serial_ports():#scan for ports
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result
def getport():#wait for Serial conection

    print("no devices, waiting")
    print(len(serial_ports()))
    if len(serial_ports()) > 0:
        return(serial_ports()[0])
getport()
#dev = USBSerial(port = 'COM6', baudrate = 9600, Timeout = 3, open = True)
dev = serial.Serial("COM6")
all_numbers = []
if True:#gerating a list of numbers
    for i in range(10000):
        ii = str(i)

        all_numbers.append(ii)
    for i in range(101):
         all_numbers.append("0"+str(i))
    for o in range(20):
        ii = "100"
        for i in range(o):
            ii =  "0" +ii
        all_numbers.append(ii)
    for o in range(20):
        ii = "10"
        for i in range(o):
            ii =  "0" +ii
        all_numbers.append(ii)
    remov = "[xyac'b]"
ss  = ""#string stoarge
stp = "88,2,78,"
stp1 ="2,4,6,"
stp2 = "2,67,4,9,"
stp3 ="2,4,6,8,"
#stp stands for "string to parse"
num = 0
x = 0
y = 0
while True:
    
    SerLine = str(dev.read_all())
    if len(SerLine)>5:
        print(SerLine)
    
    if "x" in SerLine:
        x = 1
        stp = SerLine

    if "y" in SerLine:
        y = 1
        stp1 = SerLine

            
    if x + y == 2:
        break

print(stp)
print(stp1)
ps =[]
ps1 = []
ps2 =[]
ps3 = []
# parsed string = ps
a = 0

for c in stp:   
            if c == ",":
                ss = re.sub(remov,'',ss)
                if len(ss) > 0:
                    if ss in all_numbers or ss[0] =="0":
                        ps.append(int(ss)/1000)
                ss = ''
            else:
                ss = ss + c
#spliting the string in to ints
for c in stp1:
          
            if c == ",":
                ss = re.sub(remov,'',ss)
                if len(ss) > 0:
                    if ss in all_numbers or ss[0] =="0":
                        ps1.append(int(ss))
                ss = ''
            else:
                ss = ss + c
#spliting the string in to ints
a +=1
if len(ps1)>len(ps):
     ps1.remove(ps1[-1])
if len(ps)>len(ps1):
     ps.remove(ps[-1])
depth = []
for point in ps:
    depth.append(-1*((point * 6894.75729)/(1000 * 9.81)))

xp = np.array(ps1)
yp = np.array(depth)

fig = plt.figure("Profile 1")
fig.patch.set_facecolor('#333333')
ax = plt.gca()
ax.set_xlabel('Time (seconds)', color='#aaff00') 
ax.set_ylabel('Depth (Meters)',color='#aaff00')

ax.set_facecolor('#333333')
plt.plot(xp,yp,c='#aaff00')
plt.show()
#displaying the data
num =0
#                                    doing the same thing again
while True:
            SerLine = str(dev.read_all())
            if "a" in SerLine:
                num += 1
                stp2 = SerLine
            if "c" in SerLine:
                num += 1
                stp3 = SerLine
            if num ==2 :
                 break
print(stp2)
print(stp3)
for c in stp2:   
            if c == ",":
                ss = re.sub(remov,'',ss)
                if len(ss) > 0:
                    if (ss in all_numbers or ss[0] =="0") and len(ss) < 6 :
                        ps2.append(int(ss)/1000)
                ss = ''
            else:
                ss = ss + c

for c in stp3:
          
            if c == ",":
                ss = re.sub(remov,'',ss)
                if len(ss) > 0:
                    if ss in all_numbers or ss[0] =="0":
                        ps3.append(int(ss))
                ss = ''
            else:
                ss = ss + c
for i in ps3:
     if i == 0:
          ps3.remove(i)
if len(ps3)>len(ps2):
     ps3.remove(ps3[-1])
if len(ps2)>len(ps3):
     ps2.remove(ps2[-1])
depth1 = []
for point in ps2:
    depth1.append(-1*((point * 6894.75729)/(1000 * 9.81)))

xp1 = np.array(ps3)

yp1 = np.array(depth1)
print(ps2)
print(ps3)
print(depth1)
print(xp1)
print(yp1)
fig = plt.figure("Profile 2")
fig.patch.set_facecolor('#333333')
ax = plt.gca()
ax.set_xlabel('Time (seconds)', color='#aaff00') 
ax.set_ylabel('Depth (Meters)',color='#aaff00')

ax.set_facecolor('#333333')
plt.plot(xp1,yp1,c='#aaff00')
plt.show()
