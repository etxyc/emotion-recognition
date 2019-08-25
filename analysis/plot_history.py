import matplotlib.pyplot as plt

"""
Library to plot the training history

"""


def plot_hist(history):
	"""
	Args: Keras Hitory Object

	"""
	print(history['val_cate_output_acc'])
	print(history['cate_output_acc'])


	plt.plot(history['cate_output_acc'][0:35])
	plt.plot(history['val_cate_output_acc'][0:35])
	plt.title('accuracy')
	plt.ylabel('accuracy')
	plt.xlabel('epoch')
	plt.legend(['train', 'validation'], loc='upper left')
	plt.show()


	plt.plot(history['VA_output_mean_squared_error'][0:35])
	plt.plot(history['val_VA_output_mean_squared_error'][0:35])
	plt.title('mse')
	plt.ylabel('mse')
	plt.xlabel('epoch')
	plt.legend(['train', 'validation'], loc='upper right')
	plt.show()
