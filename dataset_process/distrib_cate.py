import tensorflow as tf
import scipy.ndimage as ndimage
import numpy as np
import scipy.misc as misc
import os
import cv2
import matplotlib.pyplot as plt


"""
Library to load images and create npy dataset, i.e. traing, validation, testing

"""

np.set_printoptions(threshold=np.inf)
UNCATE = 15
HEAD = 99
SEQ_LEN = 60



def read_image(file_name):
	"""
	load image
 	Args: the path of images
	return: np array

	"""
	image = cv2.imread(file_name)
	image = cv2.resize(image, (72, 72))
	image = image / 255.0 * 2.0 - 1.0
	#print(image)
	return image

def read_dir(dir_path):
	"""
	read the images in one directory, and matching the label_seq
	Args: directory to Load
	return: data and labels

	"""
	# read annotation file into dict
	# get a list of all the image files
	images = os.listdir(dir_path)
	images.sort()

	# read image file, get ndarray
	img_list = []
	for image in images:
		image_path = dir_path + "/" + image
		img_arr = read_image(image_path)
		img_list.append(img_arr)

	# load label list
	print("Loading: " + dir_path)
	name = dir_path.split("/")[-1]
	name = name.split(".mp4")[0]
	anno_name = "AU_" + name + ".txt"
	anno_path = "./annotation/category/" + anno_name

	emotion = [HEAD]

	with open(anno_path) as f:
		for line in f:
			first_process = line.split(":")
			if first_process[1] == " N/A\n":
				emotion.append(UNCATE)
			else:

				second_process = first_process[1].split(",")
				third_process = [value for value in second_process if value != "1"]
				third_process = [value for value in third_process if value != "1\n"]

				for i in range(0, 8):
					if third_process[i] == "true" or third_process[i] == " true":
						emotion.append(i)

	# append both image and label
	# prepare sequence
	img_sample = []
	labels = []
	f = 0
#	print(images)
	while img_list:
		img_seq = []
		label_seq = []
		for i in range(0, SEQ_LEN):
			if not img_list:
				break
			else:
				img_seq.append(img_list.pop(0))
				frame_num = images[f].split(".jpg")[0]
				frame_num = int(frame_num.split("_")[0])

				emo_label = [0, 0, 0, 0, 0, 0, 0]
				emo_label[emotion[frame_num]] = 1
				label_seq.append(emo_label)
				f += 1

		if len(img_seq) == SEQ_LEN:
			new_seq = np.array(img_seq)
			img_sample.append(new_seq)
			new_labels = np.array(label_seq)
			labels.append(new_labels)

	img_sample = np.array(img_sample)
	labels = np.array(labels)

	return img_sample, labels

def cate_distribution(labels):
	"""
	calculate the distribution of emotion categories
	Args: emtion labels

	Return: number of emotions in a list
	"""
	[rows, cols] = labels.shape
	items = []
	for i in range(rows):
		for j in range(cols):
			if labels[i, j] == 1:
				items.append(j)
	return items


def read_all_dir():
	"""
	load and calculate the emotion distribution for one directory
	Returns: data and labels
	"""
	current_path = os.getcwd()
	dir_list = os.listdir("./dataset/training")

	samples, labels = read_dir(current_path + "/dataset/training/" + dir_list.pop(0))

	for dire in dir_list:
		dire = current_path + "/dataset/training/" + dire
		img_sample, label = read_dir(dire)
		if img_sample.shape[0] > 0:
			samples = np.append(samples, img_sample, axis=0)
			labels = np.append(labels, label, axis=0)

	print(samples.shape)
	print(labels.shape)

	labels = labels.reshape(-1, labels.shape[-1])
	print(labels.shape)

	items = cate_distribution(labels)

	emotions = ("Neutral", "Happiness", "Sadness", "Angry", "Fear", "Surprise", "Disgust")
	print(items)

	freq = []
	for i in range(0, 7):
		freq.append(items.count(i))


	y_pos = np.arange(len(emotions))
	plt.bar(y_pos, freq, align='center', alpha=0.5)
	plt.xticks(y_pos, emotions)
	plt.ylabel("No. of frames")
	plt.title("Emotion categories distribution")

	plt.show()
	return samples, labels

def main():
	read_all_dir()


if __name__ == "__main__":
	main()
