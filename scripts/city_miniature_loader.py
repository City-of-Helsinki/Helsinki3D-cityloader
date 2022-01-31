import site
import sys
sys.path.append(site.getusersitepackages())
import math
import requests
import zipfile36
from remotezip import RemoteZip as RemoteZip
import os
import shutil

originx = 25490000
originy = 6668000
origincode = 668490

originxid = math.floor(originx/2000)
originyid = math.floor(originy/2000)

leftx = int(sys.argv[4])
lefty = int(sys.argv[5])

rightx = int(sys.argv[6])
righty = int(sys.argv[7])

leftxid = math.floor(leftx/2000)
leftyid = math.floor(lefty/2000)

rightxid = math.floor(rightx/2000)
rightyid = math.floor(righty/2000)

leftdeltax = leftxid-originxid
leftdeltay = leftyid-originyid

rightdeltax = rightxid-originxid
rightdeltay = rightyid-originyid
lod = sys.argv[8]

#250m
#668490a1 = 7 1
xoffset = 7
yoffset = 1
originxid250 = math.floor(originx/250)
originyid250 = math.floor(originy/250)

leftxid250 = math.floor(leftx/250)
leftyid250 = math.floor(lefty/250)

rightxid250 = math.floor(rightx/250)
rightyid250 = math.floor(righty/250)

leftdeltax250 = leftxid250-originxid250
leftdeltay250 = leftyid250-originyid250

rightdeltax250 = rightxid250-originxid250
rightdeltay250 = rightyid250-originyid250
if os.path.isdir(sys.argv[2]+"/../../src_3d_files/"):
	shutil.rmtree(sys.argv[2]+"/../../src_3d_files/")
for x in range(leftdeltax,rightdeltax+1):
    for y in range(leftdeltay,rightdeltay+1):
        tilecode = str(origincode + x*2 + y*2000)+"x2"
        url = "http://3d.hel.ninja/data/mesh/Helsinki3D-MESH_2017_OBJ_2km-250m_ZIP/Helsinki3D_2017_OBJ_"+tilecode+".zip"
        downloadabletiles = []
        for x2 in range(0,8):
            for y2 in range(0,8):
                coordx = x*2000+x2*250
                coordy = y*2000+y2*250
                isinbounds = (coordx <= (rightdeltax250)*250 and coordx >= (leftdeltax250)*250 and coordy <= (rightdeltay250)*250 and coordy >= (leftdeltay250)*250)
                if (isinbounds):
                    downloadabletiles.append("Tile_+"+str(x*8+x2+xoffset).zfill(3)+"_+"+str(y*8+y2+yoffset).zfill(3))
        print("\nDownloading " + str(downloadabletiles)+"...\n")
        with RemoteZip(url) as zip:
            for zip_info in zip.infolist():
                for downloadabletile in downloadabletiles:
                    if lod in zip_info.filename and downloadabletile in zip_info.filename and ".obj" in zip_info.filename:
                        zip.extract(zip_info.filename,sys.argv[2]+"/../../src_3d_files/")
            
            