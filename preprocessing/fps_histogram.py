import subprocess
from os import listdir
import matplotlib.pyplot as plt
import numpy as np

"""
Library to calculate the fps distribution

"""

def fps_distri():

	files = listdir(".")
	#print(len(files))

	mp4List = []
	for fileName in files:
		if fileName.endswith(".mp4"):
			mp4List.append(fileName)

	#print(len(mp4List))

	fpsList = []

	for videoFile in mp4List:
		fps_check = subprocess.check_output('ffprobe ' + videoFile +' 2>&1 | grep fps',shell=True)
		fps_check = str(fps_check, 'utf-8')
		fps = float(fps_check.split(' fps')[0].split(',')[-1][1:])
		fpsList.append(fps)
		print(fps)

	print("No. of vidoes: " + str(len(fpsList)))
	figure = plt.hist(fpsList)
	plt.title("Frame Rate")
	plt.xlabel("Frames per Seconds")

	plt.show()
