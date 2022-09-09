import sys
import cv2
import math
import numpy as np

def readFile(fname):
    f = open(fname, "r")
    img = f.read().rstrip()
    clean = img.splitlines()
    arr = []
    for i in clean:
        if i[0] == '#':
            clean.remove(i)
    
    type = clean[0]
    arr.append(type)
    dim = clean[1]
    arr.append(dim)
    dlst = dim.split(" ")
    w = int(dlst[0])
    h = int(dlst[1])
    m = clean[2]
    arr.append(m)
    for i in range(3,len(clean),1):
        ls = clean[i].rstrip().split(" ")
        for j in ls:
            if(j.isnumeric()):
                arr.append(j)
    
    #print(arr)
    print(len(clean))
    f.close()
    print(len(clean))
    return type, w, h, arr,m

def createFile(img,width,height,maxColor,ptype):
    ppm = []
    ppm.append(ptype)
    ppm.append(str(width) + " " + str(height))
    ppm.append(str(maxColor))
    
    for i in img:
        ppm.append(str(i))
        
    f = open("grey.ppm","w")
    for i in ppm:
        f.write(str(i) + "\n")
    f.close()        
    showImage("grey.ppm")

def showImage(path):
    img  = cv2.imread(path)
    cv2.imshow("the image",img)
    cv2.waitKey(0)    
    cv2.destroyAllWindows()

def showFile (path,t, w, h, dta):
    print ("This file is of type: " + t)
    print ("Its dimensions are: " + str(w) + ", " + str(h))
    print("Its max color is: " + dta)
    print ("And it looks like this:")
    print ()
    showImage(path)
    print()

#-----------------------------------------------GreyScale-------------------------------------------
#single Channel
def singleR(img,width,height,maxColor):
    arr = []
    for i in range(3,len(img),3):
        arr.append(round(int(img[i])))
    createFile(arr, width, height, maxColor,"P2")

def singleG(img,width,height,maxColor):
    arr = []
    for i in range(3,len(img),3):
        arr.append(round(int(img[i + 1])))
    createFile(arr, width, height, maxColor,"P2")
    
def singleB(img,width,height,maxColor):
    arr = []
    for i in range(3,len(img),3):
        arr.append(round(int(img[i + 2])))
    createFile(arr, width, height, maxColor,"P2")
    
    
#average
def average(img,width,height,maxColor):
    arr = []
    for i in range(3,len(img),3):
        arr.append(round(((int(img[i])) + (int(img[i+1])) + (int(img[i+2])))/3))
    print(arr)
    createFile(arr, width, height, maxColor,"P2")
    
def weighted(img,width,height,maxColor):
    arr = []
    for i in range(3,len(img),3):
        red = ((int(img[i]) * 0.299))
        green = ((int(img[i+1]) * 0.587))
        blue = ((int(img[i]) * 0.114))
        arr.append(round(red + green + blue))
    #print(arr)
    createFile(arr, width, height, maxColor,"P2")
    

#----------------------------------Scaling----------------------------------------
def nnScale(img,width,height,width2,height2,maxColor):
   temp = [0] * (width2 * height2)
   #print(len(temp))
   #apply greyscaling before scaling 
   weighted(img, width, height, maxColor)
   type,width,height,img,maxColor = readFile("grey.ppm")
   
   x_ratio = width / width2
   y_ratio = height / height2
   del img[:3]
   for i in range (height2):
       for j in range (width2):
           px = math.floor(j * x_ratio)
           py = math.floor(i * y_ratio)
           temp[(i * width2) + j] = int(img[int((py*width) +px)])
  
   #print(temp)
   createFile(temp, width2, height2, maxColor, "P2")
 
            

def main():
    if len(sys.argv) == 2:
        type,width,height,img,maxColor = readFile(sys.argv[1])
        showFile (sys.argv[1],type,width,height,maxColor)
        #average(img, width, height, maxColor)
        #weighted(img, width, height, maxColor)
        nnScale(img,width,height,300,300,maxColor)
        
        
    else:
        print("Usage: pbmview filename")


if __name__ == "__main__":
    main()