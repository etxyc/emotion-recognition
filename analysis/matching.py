import numpy as np
import load_dataset as load
np.set_printoptions(threshold=np.inf)
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

"""
Library to visualize the distribution of emotion categories on valence and arousal space

"""
def vis_distribution():
	val_label_path_VA = "dataset/labels_VA.npy"
	val_label_path_cate = "dataset/labels_cate.npy"

	VA = load.load_dataset(val_label_path_VA)
	cate = load.load_dataset(val_label_path_cate)

	VA = VA.reshape(-1, VA.shape[-1])
	print(VA.shape)

	cate = cate.reshape(-1, cate.shape[-1])
	print(cate.shape)

	[rows, cols] = cate.shape

	VA_label = []
	color = []
	for i in range(rows):
		for j in range(cols):
			if cate[i, j] == 1:
				if j == 0:
					color.append('b')
					VA_label.append(VA[i])

				if j == 1:
					color.append('g')
					VA_label.append(VA[i])

				if j == 2:
					color.append('r')
					VA_label.append(VA[i])

				if j == 3:
					color.append('c')
					VA_label.append(VA[i])


				if j == 4:
					color.append('m')
					VA_label.append(VA[i])

				if j == 5:
					color.append('DarkOrange')
					VA_label.append(VA[i])

				if j == 6:
					color.append('k')
					VA_label.append(VA[i])


	VA_label = np.array(VA_label)
	plt.scatter(VA_label[:, 1], VA_label[:, 0], s=3, color=color, alpha=0.4)
	plt.ylim([-1, 1])
	plt.xlim([-1, 1])
	plt.xlabel("Valence")
	plt.ylabel("Arousal")
	plt.axhline(0, color='black')
	plt.axvline(0, color='black')

	plt.show()
