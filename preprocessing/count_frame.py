from os import listdir
"""
Script to calculate thhe overall category distribution at early stage

"""
#Load file names
files = listdir("../../Annotation_Data")
frameStat = [0,0,0,0,0,0,0]

#for all files
for txtFile in files:
	#open file
	with open("../../Annotation_Data/" + txtFile) as f:

		#for all lines in file
		for line in f:
			#pre-process data
			firstProcess = line.split(":")
			if firstProcess[1] != " N/A\n":
				emotions = firstProcess[1].split(",")
				secProcess = [value for value in emotions if value != "1"]
				secProcess = [value for value in secProcess if value != "1\n"]

				print(secProcess)

				#for all emotions, record the frames
				for i in range(0,7):
					if secProcess[i] == "true" or secProcess[i] == " true":
						frameStat[i] += 1

#output result
print(frameStat)
