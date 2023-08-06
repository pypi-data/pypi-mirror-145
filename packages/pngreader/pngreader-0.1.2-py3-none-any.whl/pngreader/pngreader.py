import os
import cv2
import numpy as np
import math
from PIL import Image
import sys
import zlib
def ReadPngHexWithCv(filename):#
	img = cv2.imread(filename)
	return img
def WritePngHexWithCv(filename,Hex):#
	cv2.imwrite(filename,Hex,[int(cv2.IMWRITE_PNG_COMPRESSION),9])
def CvReadToString(object):
	isEncryption = False
	if object[-1][-1][-1] == 253:
		isEncryption = True
	charlist = []
	object_ = list(object)
	for item in object_:
		item = list(item)
		for items in item:
			items = list(items)
			if items[0] == 255:
				if items[1] != 255:
					ch = int(str(list(items)[1])+str(list(items)[2]))
					charlist.append(chr(ch))
			else:
				for moreitem in items:
					if moreitem != 253 and moreitem != 255:
						charlist.append(chr(moreitem))
					else:
						pass
	if isEncryption == True:
		charlist = charlist[::-1]
	return charlist
def operation(object,isEncryption=False,isChinese=True):#
	object_ = int(len(object)/3)+1
	object_ = int(math.sqrt(object_))+1
	MainList = []
	count = 0
	templist=[]
	for item in object:
		if count < 3:
			count += 1
			if item > 255:
				if isChinese == True:
					if len(templist) != 3:
						for i in range(3-len(templist)):
							templist.append(255)
						MainList.append(templist)
					templist = []
					lenstr = str(item)
					second = lenstr[:2]
					third = lenstr[2:]
					templist=[255,int(second),int(third)]
					MainList.append(templist)
					templist=[]
					count = 0
			else:
				templist.append(item)
		else:
			if item > 255:
				if isChinese == True:
					templist = []
					lenstr = str(item)
					second = lenstr[:2]
					third = lenstr[2:]
					templist=[255,int(second),int(third)]
					MainList.append(templist)
					templist = []
					count = 0
			else:
				MainList.append(templist)
				count = 1
				templist = [item]
	if len(templist) != 3:
		for i in range(3-len(templist)):
			templist.append(255)
		MainList.append(templist)
	if [object[-3],object[-2],object[-1]] not in MainList and [object[-2],object[-1],255] not in MainList and [object[-1],255,255] not in MainList:
		MainList.append([object[-3],object[-2],object[-1]])
	OutList = [[]]
	countOUT = 0
	for item in MainList:
		if countOUT < object_+1:
			OutList[-1].append(item)
			countOUT+=1
		else:
			countOUT=1
			OutList.append([item])
	count=0
	Len = len(OutList[0])
	for i in range(len(OutList)):
		get = OutList[i]
		lenth = len(get)
		if lenth != Len:
			print('[!] Find Not Alignment array')
			OutList[i] = get+[[255,255,255]]*(Len-lenth)
	for i in OutList:
		for d in i:
			if len(d)!=3:
				print('[!] Find Not Alignment array in L-',d)
				OutList[OutList.index(i)][OutList[OutList.index(i)].index(d)] = d+[255]*(3-len(d))
	out = np.array(OutList,dtype = 'uint8')
	if isEncryption == True:
		out[-1][-1][-1]=253
	return out
def ReadFileASCII(filename,isEncryption=False):#
	ASCIIlist=[]
	with open(filename,'r',encoding='utf-8') as File:
		Filehex = File.read()
		out = Filehex.encode()
		print(len(out))
		c = zlib.compress(out)
		print(len(c))
	for item in Filehex:
		ASCIIlist.append(ord(item))
	if isEncryption == True:
		ASCIIlist = ASCIIlist[::-1]
	return ASCIIlist
def  ReASCII(object):#
	Relist = []
	for item in object:
		Relist.append(chr(item))
	return ''.join(Relist)
def MakePng(filename,isEncryption=False,isChinese=True):#
	firstData=ReadFileASCII(filename,isEncryption)
	secondDATA = operation(firstData,isEncryption,isChinese)
	WritePngHexWithCv(filename.split('.')[0]+'.png',secondDATA)
	return filename.split('.')[0]+'.png'
def ReadPng(filename):#
	get = ReadPngHexWithCv(filename)
	getready = CvReadToString(get)
	string = ''.join(getready)
	return string
