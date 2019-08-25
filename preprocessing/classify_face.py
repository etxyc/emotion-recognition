import glob, os
import math
import subprocess
from menpo.visualize import print_progress

from menpo.io import import_videos

import menpo.io as mio
from menpodetect.ffld2 import load_ffld2_frontal_face_detector

"""

Library to classfiy the faces by its coordinates

"""


def get_centre(A):
	coor = []
	left_sum = 0.0
	right_sum = 0.0

	for i in range(0,4):
		left_sum += A[i][0]
		right_sum += A[i][1]

	coor = [left_sum/4.0, right_sum/4.0]
	return coor

def get_distance(A, B):
	x = abs(A[0] - B[0])
	y = abs(A[1] - B[1])

	x = pow(x,2)
	y = pow(x,2)

	distance = math.sqrt(x + y)
	return distance

def main():
	# set the average location of left face and right face
	left_centre = [180.852, 286.917]
	right_centre = [158.152, 455.525]

	classify_dimen = 1 # 1 means classify by left and right, 0 means by up and down
	another_dimen = 1 - classify_dimen


	current_path = os.getcwd()

	folder_name = os.path.basename(current_path)

	uncropped_path = folder_name + "_uncropped"
	cropped_path = folder_name + "_cropped"


	detector = load_ffld2_frontal_face_detector()

	vv = mio.import_images(uncropped_path  + '/*.jpg')
	left_image = []
	right_image = []

	#make relative directory
	left_dir = cropped_path + "_left"
	right_dir = cropped_path + "_right"

	if not os.path.exists(left_dir):
		os.makedirs(left_dir)

	if not os.path.exists(right_dir):
		os.makedirs(right_dir)

	for cnt, im in enumerate(vv):
		name = '{0:05d}'.format(cnt+1)

		lns = detector(im)

		#if two faces exit, record coordinates, move the image to proper directory
		if im.landmarks.n_groups == 2:
			A_image = lns[0].points
			B_image = lns[1].points

			print(name)
			print("A")
			print(A_image)
			print(get_centre(A_image))
			print("B")
			print(B_image)
			print(get_centre(B_image))

			A_path = cropped_path + "/" + name + "_" + "0" + ".jpg"
			B_path = cropped_path + "/" + name + "_" + "1" + ".jpg"

			print(A_path)
			print(B_path)

			A_centre = get_centre(A_image)
			B_centre = get_centre(B_image)

			if A_centre[classify_dimen] <= B_centre[classify_dimen]:
				left_image.append(A_centre)
				right_image.append(B_centre)

				if os.path.isfile(A_path):
					subprocess.check_output("mv " + A_path + " " + left_dir, shell = True)
				if os.path.isfile(B_path):
					subprocess.check_output("mv " + B_path + " " + right_dir, shell = True)
			else:
				left_image.append(B_centre)
				right_image.append(A_centre)

				if os.path.isfile(B_path):
					subprocess.check_output("mv " + B_path + " " + left_dir, shell = True)
				if os.path.isfile(A_path):
					subprocess.check_output("mv " + A_path + " " + right_dir, shell = True)
		###################################################################################

		if im.landmarks.n_groups == 1:
			A_image = lns[0].points
			A_centre = get_centre(A_image)
			A_path = cropped_path + "/" + name + ".jpg"

			# calculate the distance to both left and right, move to the close one
			left_distance = get_distance(A_centre, left_centre)
			right_distance = get_distance(A_centre, right_centre)

			if left_distance <= right_distance:
				print("left")

				if os.path.isfile(A_path):
					subprocess.check_output("mv " + A_path + " " + left_dir, shell = True)
			else:
				print("right")
				if os.path.isfile(A_path):
					subprocess.check_output("mv " + A_path + " " + right_dir, shell = True)

		####################################################################################
	num = len(left_image)

	left_0 = 0.0
	left_1 = 0.0
	right_0 = 0.0
	right_1 = 0.0

	for limage in left_image:
		left_0 += limage[0]
		left_1 += limage[1]
	for rimage in right_image:
		right_0 += rimage[0]
		right_1 += rimage[1]

	left_0 = left_0/num
	left_1 = left_1/num
	right_0 = right_0/num
	right_1 = right_1/num


	left_str = str(left_0) + ", " + str(left_1)
	right_str = str(right_0) + ", " + str(right_1)

	print(left_str)
	print(right_str)

	with open("average_coor" + str(classify_dimen)  + ".txt", "w") as f:
		f.write(left_str + "\n")
		f.write(right_str + "\n")


	print("All Done")



if __name__ == "__main__":
	main()
