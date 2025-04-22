import pyxel  
from math import *
from colorutils import *
from PIL import Image
import PyxelUniversalFont as puf
data = [0,1,1,1,2,3,3,3,4,5]
map0 = Image.open("CARP_RES/map.png")
num = 0
pain=["ffffff","a3ff9f","3faefb","000000","888888"]
pain2 = []
for c in pain:
	pain2.append(int(c,16))
print(pain2)
writer = puf.Writer("IniSans-VGvnZ.otf")
class App:
	def __init__(self):
		pyxel.init(526,700)
		self.num = 0
		pain2.extend([0xff0000,0xffff00,0x00ff00,0x0000ff,0xff00ff])
		pyxel.colors.from_list(pain2)
		pyxel.run(self.update, self.draw)
	def update(self):
		pass

		
	def draw(self):
		def drawoverlay(img):
			if img != 0:
				map = Image.open("r"+str(img)+".png")
				for x in range(map.size[0]):
					for y in range(map.size[1]):
						if map.getpixel((x,y))[-1]>200:
							pyxel.pset(x,y,5+img-1)
		def drawMap(map):	
			for x in range(map.size[0]):
				for y in range(map.size[1]):
					d = 10000
					bc = 1
					c = list(map.getpixel((x,y)))
					c.pop(-1)
					for i in range(len(pain)):
						dis = dist(hex_to_rgb(pain[i]),c)
						if dis < 5:
							bc = i
							break
						if dis < d:
							d = dis
							bc = i
					pyxel.pset(x,y,bc)
		if pyxel.frame_count < 1 :
			drawMap(map0)
			
		#pyxel.mouse(True)
		pyxel.rect(0,20,100,40,0)
		writer.draw(0,20,str(2016+self.num),40,3)
		if pyxel.btnp(pyxel.KEY_RIGHT):
			self.num+=1
			drawoverlay(data[self.num])
		if pyxel.btnp(pyxel.KEY_LEFT):
			self.num-=1
			drawMap(map0)
			for I in range(self.num):
				drawoverlay(data[I])
		if pyxel.btnp(pyxel.KEY_0):
			self.num=0
			drawMap(map0)
			drawoverlay(data[self.num])
			
		

		

				
		

App()