import matplotlib
matplotlib.use('Agg')

from keras.applications import VGG16
from keras.models import load_model
from vis.utils import utils
from keras import activations
from vis.visualization import visualize_activation
import util_cate
import util_VA
from matplotlib import pyplot as plt
import numpy as np



"""
Library to visualise images that can maximumly activate the the last fully connected layer.

"""

# load the model
model = load_model("./model/model.h5", custom_objects={'recall': util_cate.recall, 'precision': util_cate.precision, 'f1': util_cate.f1, 'ccc': util_VA.ccc})

# Utility to search for last fully connected layer index by name.
layer_idx = utils.find_layer_idx(model, 'cate_output')

# Swap softmax with linear
model.layers[layer_idx].activation = activations.linear
model = utils.apply_modifications(model, custom_objects={'recall': util_cate.recall, 'precision': util_cate.precision, 'f1': util_cate.f1, 'ccc': util_VA.ccc})



# generate images
plt.rcParams['figure.figsize'] = (18, 6)

# Specify the filter_indices for the class to visualise, for example 2 is the class sadness
img = visualize_activation(model, layer_idx, filter_indices=2, max_iter=500)
print(img.shape)

for i in range(0, 60):
	image = img[i]
	plt.imshow(image)
	name = str(i) + ".png"
	plt.savefig(name)
