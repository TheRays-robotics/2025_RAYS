import pyxel	
import serial
import numpy
import re
from random import randint as ran
from time import sleep,time
from math import dist,atan2,degrees,radians,sin,cos,dist
import PyxelUniversalFont as puf
from PIL import Image, ImageFile
readFromsSerial = 0
useolddataformat = 1
xbee = 0
so=6
tnum = 10
batnum = 90
starttime = time()
def lerp(pos1,pos2, t):
	x1 = pos1[0]
	y1 = pos1[1]
	x2 = pos2[0]
	y2 = pos2[1]
	return [x1 + (x2 - x1) * t, y1 + (y2 - y1) * t]
def val(value, istart, istop, ostart, ostop):
	return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))
def clamp(n, minn, maxn):
	return max(min(maxn, n), minn)
def angle_between(a, b):
	angle = degrees(atan2(a[1] - b[1], b[0] - a[0]))
	if angle < 0:
		angle += 360
	return radians(180-angle)
def tline(ps1,ps2,th,col):
	angl = angle_between(ps1,ps2)
	pyxel.tri(ps1[0]+cos(angl+radians(90))*(th),ps1[1]+sin(angl+radians(90))*(th),ps1[0]+cos(angl+radians(270))*(th),ps1[1]+sin(angl+radians(270))*(th),ps2[0]+cos(angl+radians(90))*(th),ps2[1]+sin(angl+radians(90))*(th),col)
	pyxel.tri(ps1[0]+cos(angl+radians(270))*(th),ps1[1]+sin(angl+radians(270))*(th),ps2[0]+cos(angl+radians(90))*(th),ps2[1]+sin(angl+radians(90))*(th),ps2[0]+cos(angl+radians(270))*(th),ps2[1]+sin(angl+radians(270))*(th),col)
	pyxel.circ(ps1[0],ps1[1],th,col)
	pyxel.circ(ps2[0],ps2[1],th,col)
def CatmullRomSpline(P0, P1, P2, P3, a, nPoints=30):
	"""
	P0, P1, P2, and P3 should be (x,y) point pairs that define the Catmull-Rom spline.
	nPoints is the number of points to include in this curve segment.
	"""
	# Convert the points to numpy so that we can do array multiplication
	P0, P1, P2, P3 = map(numpy.array, [P0, P1, P2, P3])

	# Calculate t0 to t4
	alpha = a
	def tj(ti, Pi, Pj):
		xi, yi = Pi
		xj, yj = Pj
		return ( ( (xj-xi)**2 + (yj-yi)**2 )**0.5 )**alpha + ti

	t0 = 0
	t1 = tj(t0, P0, P1)
	t2 = tj(t1, P1, P2)
	t3 = tj(t2, P2, P3)

	# Only calculate points between P1 and P2
	t = numpy.linspace(t1,t2,nPoints)

	# Reshape so that we can multiply by the points P0 to P3
	# and get a point for each value of t.
	t = t.reshape(len(t),1)

	A1 = (t1-t)/(t1-t0)*P0 + (t-t0)/(t1-t0)*P1
	A2 = (t2-t)/(t2-t1)*P1 + (t-t1)/(t2-t1)*P2
	A3 = (t3-t)/(t3-t2)*P2 + (t-t2)/(t3-t2)*P3

	B1 = (t2-t)/(t2-t0)*A1 + (t-t0)/(t2-t0)*A2
	B2 = (t3-t)/(t3-t1)*A2 + (t-t1)/(t3-t1)*A3

	C	= (t2-t)/(t2-t1)*B1 + (t-t1)/(t2-t1)*B2
	return C

def CatmullRomChain(P:list,alpha,rang):
	
	""" P.insert(0,[P[0][0]-P[1][0],P[0][1]-P[1][1]])
	P.append([P[-1][0]-P[-2][0],P[-1][1]-P[-2][1]])"""
	P.insert(0,P[0])
	P.append(P[-1])
	sz = len(P)

	# The curve C will contain an array of (x,y) points.
	C = []
	for i in range(sz-3):
		c = CatmullRomSpline(P[i], P[i+1], P[i+2], P[i+3],alpha)
		C.extend(c)
		ç=[]
		for cç in C:
			ç.append([cç[0],clamp(cç[1],low(rang),high(rang))])

	return ç
if readFromsSerial==0:
	txt = open("txt.txt")
	linesoftxt = txt.readlines()
def scanr(id):
	out=[]
	for l in linesoftxt:
		if l[0]==id:
			out.append(float((l.replace(id,""))))
	return(out)
def high(list):
	hig = -9999999
	for l in list:
		if l > hig:
			hig = l
	return(hig)
def low(list):
	lo = 9999999
	for l in list:
		if l < lo:
			lo = l
	return(lo)
def conv(num,ç):
	if ç ==0: 
		return((num))
		#return((num)/(9.81*996.25))
	else:
		return(num)
#load image resourses 
if True:
	img = Image.open("FLOAT_RES/descend.png")
	descendpyres =[]
	for xx in range(img.size[0]):
		for yy in range(img.size[1]):
			if not img.getpixel((xx,yy))[3] == 0:
				descendpyres.append([xx,yy])
	img = Image.open("FLOAT_RES/data.png")
	datapyres =[]
	for xx in range(img.size[0]):
		for yy in range(img.size[1]):
			if not img.getpixel((xx,yy))[3] == 0:
				datapyres.append([xx,yy])
	img = Image.open("FLOAT_RES/mystery.png")
	pyres =[]
	for xx in range(img.size[0]):
		for yy in range(img.size[1]):
			if not img.getpixel((xx,yy))[3] == 0:
				pyres.append([xx,yy])
	initpyres =[]
	img = Image.open("FLOAT_RES/init.png")
	for xx in range(img.size[0]):
		for yy in range(img.size[1]):
			if not img.getpixel((xx,yy))[3] == 0:
				initpyres.append([xx,yy])
def pymg(xx,yy,so,co):
	for ip in so:
		pyxel.pset(ip[0]+xx-9-10,ip[1]+yy-15-6,co)

			
ts = []
ds = []
points = []
if readFromsSerial == 0:
	ts = scanr("t")
	ds = scanr("d")

else:
	ser = serial.Serial(('/dev/ttyACM0','/dev/ttyUSB0')[xbee], 9600)
	print("connected")

writer = puf.Writer("IniSans-VGvnZ.otf")
class App:#shrimp!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	def __init__(self):
		pyxel.init(1200, 600,title="The Rays Float")
		tc = pyxel.colors.to_list()
		tc.append(0x008cff)
		tc.append(0x36ca14)
		pyxel.colors.from_list(tc)
		pyxel.colors[15] = 0xff0000
		pyxel.colors[14] = 0x707070
		self.curpro = 0
		self.cp=1
		self.usepr = 0
		self.store = []
		self.ß=0
		self.issmooth = 1
		self.points = []
		self.starttime = starttime
		self.nextFrameIsFreeze=0
		self.prof = []

		points = []
		global newdata
		def newdata():
			ts.clear()
			ds.clear()
			if useolddataformat == 1:
				while True:
					chrs = str(ser.readline().decode(encoding="utf-8")).replace('\n',"")
					if "end" in chrs:
						break
					elif "d" in chrs:
							ds.append(float(chrs.replace("d","")))
					elif "t" in chrs and not "a" in chrs:
							ts.append(float(chrs.replace("t","")))
			else:
				while True:
					chrs = str(ser.readline().decode(encoding="utf-8")).replace('\n',"").replace("\r","")
					print(chrs)
					#ds.append(float(chrs.replace("d","")))
					if "end" in chrs:
						break
					elif "  " in chrs:
						colontime = chrs.split("  ")[1].split(":")
						ts.append(float(colontime[0])*3600+(float(colontime[1]))*60+(float(colontime[2])))
						ds.append(float(chrs.split("  ")[2].replace("d","")))
			points.clear()
			self.points.clear()
			for p in range(len(ts)):
				points.append((ts[p],ds[p]))
				self.points.append((ts[p],ds[p]))
				"""if self.issmooth == 1:
					self.store.clear()
					for p in range(len(ts)):
						self.store.append((ts[p],ds[p]))
					points.clear()
					points.extend(CatmullRomChain(self.store,0,ds))"""
			self.prof.append([[],[]])
			self.prof[-1][0].extend(ts)
			self.prof[-1][1].extend(ds)
			
		if readFromsSerial==1:
			if xbee==0 and 1==1:
				newdata()
		if True:
			points = []
			for i in range(len(ts)):
				points.append((ts[i],ds[i]))
			if len(points) != 0:
				points = CatmullRomChain(points,0,ds)
		pyxel.run(self.update, self.draw)
		
		
	def update(self):
		pass
	
		
	def draw(self):
		pyxel.cls(0)
		if pyxel.btn(pyxel.KEY_0):
			print(self.curpro)
		#self.curpro = (self.curpro+ pyxel.mouse_wheel)%len(self.prof)
		#self.starttime=time()
		if readFromsSerial == 1 and pyxel.btnp(pyxel.KEY_D):
				ser.write("D".encode())
				#squimble
		if self.nextFrameIsFreeze==1:
			self.nextFrameIsFreeze = 0
			ser.reset_input_buffer()
			self.curpro += 1
			newdata()
			if self.issmooth == 0:
					points.clear()
					for i in range(len(ts)):
						points.append([ts[i],ds[i]])
			else:
					self.store.clear()
					for p in range(len(ts)):
						self.store.append((ts[p],ds[p]))
					points.clear()
					points.extend(CatmullRomChain(self.store,0,ds))
		for i in range(1000-70):
			if ((val(i+70,70,1000,(low(ts)),(high(ts))))) % 5 < (0.07):
				pyxel.line(i+70,550,i+70,20,7)
				if not ((val(i+70,70,1000,conv(low(ts),0),conv(high(ts),0))) == conv(low(ts),0) or (val(i+70,70,1000,conv(low(ts),0),conv(high(ts),0))) ==conv(high(ts),0)):
					writer.draw(i+70, 570, str(int(val(i+70,70,1000,conv(low(ts),0),conv(high(ts),0)))), 9+so, 7)
		for i in range(550):
			if (val(i,20,550,conv(low(ds),0),conv(high(ds),0))) % 0.5 < 0.006:
				pyxel.line(1000,i,70,i,7)
				if not ((val(i,20,550,low(ds),high(ds))) < low(ds)+0.1 or (val(i,20,550,low(ds),high(ds))) > high(ds)-0.1):
					writer.draw(25, i, str(int((val(i,20,550,conv(low((ds)),self.usepr),conv(high(ds),self.usepr)))*10)/10), 8+so, 7)

		#pyxel.line(800,0,800,600,8)
		
		tline((1002,0),(1002,600),2,8)
		tline((70,0),(70,600),2,8)
		tline((70,0),(70,600),2,8)
		tline((1200,552),(25,552),2,5)
		tline((22,0),(22,600),1,8)
		tline((22,20),(70,20),1,8)
		#print(self.usepr)
		writer.draw(25, 20, str(conv(low(ds),self.usepr))+["m","kpa"][self.usepr], 8+(((self.usepr+1)%2)*3)+so, 7)
		writer.draw(25, 555, str(conv(high(ds),self.usepr)).split(".")[0]+"."+str(conv(high(ds),self.usepr)).split(r".")[1%len(str(conv(high(ds),self.usepr)).split(r"."))][-1]+(("m","kpa")[self.usepr]), 8+(((self.usepr+1)%2)*3)+so, 7)
		writer.draw(70, 570, str(low(ts))+"s", 11+so, 7)
		writer.draw(1000, 570, str(high(ts))+"s", 11+so, 7)
		#side pannel

		pyxel.line(1068,40,1068,1000,7)
		pyxel.line(1004,40,1200,40,7)
		pyxel.line(1004,20,1200,20,7)
		writer.draw(1075,43,("DEPTH(m)","PRESURE(kpa)")[self.usepr],13+so,3)
		writer.draw(1006,3,"Team Number:"+str(tnum),13+so,3)
		writer.draw(1006, 23, "FPS:"+str(int(pyxel.frame_count/(time()-self.starttime))), 13+so, 3)
		writer.draw(1006,43,"TIME(s)",12+so,3)
		self.ß = 0
		for t in ts:
			self.ß =self.ß+ 1
			if self.ß < 44: 
				writer.draw(1006,50+(self.ß*11),str(t)[0:9],6+so,3)
			elif self.ß == 44:
				writer.draw(1006,50+(self.ß*11),"...",6+so,3)
		self.ß = 0
		for t in ds:
			self.ß =self.ß+1 
			if self.ß < 44: 
				writer.draw(1075,50+(self.ß*11),str(conv(t,self.usepr)).split(".")[0]+"."+str(conv(t,self.usepr)).split(r".")[1][-1]+(("m","kpa")[self.usepr]),6+so,3)
			elif self.ß == 44:
				writer.draw(1006,50+(self.ß*11),"...",6+so,3)
		#left buttons
		for i in range(len(self.prof)):
			if pyxel.mouse_x < 20 and clamp(pyxel.mouse_y,(i*20),(i*20)+20) == pyxel.mouse_y and not self.prof[i]==[[],[]]:
				self.curpro = i
				ds.clear()
				ds.extend(self.prof[i][1])
				
				ts.clear()
				ts.extend(self.prof[i][0])
				
				points.clear()
				self.points.clear()
				for p in range(len(ts)):
					points.append((ts[p],ds[p]))
					self.points.append((ts[p],ds[p]))
				if self.issmooth == 1:
					self.store.clear()
					for p in range(len(ts)):
						self.store.append((ts[p],ds[p]))
					
					points.clear()
					points.extend(CatmullRomChain(self.store,0,ds))
			if self.curpro == i:
				pyxel.rect(0,(i*20)+1,20,20,2)
			writer.draw(8,(i*20)+5,str(i+1),9+so,7)
			pyxel.line(0,(i*20)+20,20,(i*20)+20,7)
		#top line
		writer.draw(70,0,"Rays Float 2025",13+so,11)
		pyxel.rect(400,0,60,20,14)
		pyxel.rect(400+(self.usepr*30),0,30,20,13)
		writer.draw(400+(self.usepr*30)+10+(self.usepr*-9),4,("M","KPA")[self.usepr],10+so,7)
		pyxel.rect(600,0,60,20,14)
		pyxel.rect(600+(self.issmooth*30),0,30,20,13)
		writer.draw(600+(self.issmooth*30)+10+(self.issmooth*-5),4,("L","CR")[self.issmooth],10+so,7)
		if pyxel.mouse_y < 20:
			if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x == clamp(pyxel.mouse_x,400+(self.usepr*30),430+(self.usepr*30)):
				self.usepr = (self.usepr+1)%2
			if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x == clamp(pyxel.mouse_x,600+(self.issmooth*30),630+(self.issmooth*30)):
				self.issmooth = (self.issmooth+1)%2
				if self.issmooth == 0:
					points.clear()
					for i in range(len(ts)):
						points.append([ts[i],ds[i]])
				else:
					self.store.clear()
					for p in range(len(ts)):
						self.store.append((ts[p],ds[p]))
					points.clear()
					points.extend(CatmullRomChain(self.store,0,ds))
		for i in range(len(points)-1):
			tline((val(points[i][0],low(ts),high(ts),70,1000),(val(points[i][1],low(ds),high(ds),20,550))),((val(points[i+1][0],low(ts),high(ts),70,1000),(val(points[i+1][1],low(ds),high(ds),20,550)))),2,7)
			pass
		for p in self.points:
			pyxel.circ(val(p[0],low(ts),high(ts),70,1000),(val(p[1],low(ds),high(ds),20,550)),3,15) 
		pyxel.mouse(True)
		if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and clamp(pyxel.mouse_x,23,1000) == pyxel.mouse_x and 19<pyxel.mouse_y:
			pyxel.line(pyxel.mouse_x,0,pyxel.mouse_x,600,5)
			pyxel.line(0,pyxel.mouse_y,1000,pyxel.mouse_y,8)
			writer.draw(pyxel.mouse_x+10,pyxel.mouse_y,str(int(conv(val(pyxel.mouse_y,20,550,low(ds),high(ds)),self.usepr)*100)/100)+("m","kpa")[self.usepr],11+so,8)		 
			writer.draw(pyxel.mouse_x+10,pyxel.mouse_y+15,str(int(val(pyxel.mouse_x,70,1000,low(ts),high(ts))*1)/1)+"s",11+so,5)
		pyxel.circ(1135,576,20,15)
		pyxel.circ(1178,576,20,17)
		pyxel.circ(1090,576,20,16)
		#writer.draw(1150,570,"GO",11+so,7)
		#writer.draw(1100-7,570,"Data",11+so,0)
		pymg(1135,576,descendpyres,7)
		pymg(1090,576,datapyres,7)
		pymg(1178,576,initpyres,7)
		if not pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
			self.cp =1
		if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and self.cp == 1:
			self.cp = 0 
			if dist((1135,576),(pyxel.mouse_x+0.1,pyxel.mouse_y+0.1)) <= 20:
					pyxel.circ(1135,576,20,0)
					ser.write("D".encode())
			if dist((1178,576),(pyxel.mouse_x+0.1,pyxel.mouse_y+0.1)) <= 20:
					pyxel.circ(1178,576,20,0)
					ser.write("I".encode())
			if dist((1090,576),(pyxel.mouse_x+0.1,pyxel.mouse_y+0.1)) <= 20:
				pyxel.cls(0)
				writer.draw(300,300,"Collecting serial data...",20+so,9)
				self.nextFrameIsFreeze=1
App()