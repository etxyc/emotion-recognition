import glob, os
import subprocess

"""
Library to remove wrongly cropped images.

"""

def remove_wrong():

	#find all the directory with possibly wrong cropped pictures

	output = subprocess.check_output("find . -type f -name '*_1.jpg' | sed -r 's|/[^/]+$||' |sort -u", shell = True)

	print("Output is:")
	directories = output.decode()
	directories = directories.split("\n")
	del directories[-1]
	print(directories)
	print(len(directories))

	total_number = len(directories)

	i = 0

	#for all those directories, move the wrong pictures to a new directory with the name of the origin one plus _second
	for directory in directories:
		subprocess.check_output("mkdir " + directory + "_second", shell = True)
		subprocess.check_output("mv " + directory + "/*_*.jpg " + directory + "_second", shell = True)
		subprocess.check_output("mv " + directory + "_second"  + "/*_0.jpg " + directory, shell = True)
		i += 1
		print(directory + " Finished")
		print(str(i) + "/" + str(total_number) + " Finished")

	print("All Done!")
