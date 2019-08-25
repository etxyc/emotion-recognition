import numpy as np
"""
Function to load the npy file into np array for Keras usage

"""
def load_dataset(path):
	"""
	Args: path of the npy file
	Return: the np arrays
	"""
	print("Loading:" + path)
	return np.load(path)
