from keras.models import load_model
import load_dataset as load
import util
from sklearn.metrics import classification_report, accuracy_score
import numpy as np
np.set_printoptions(threshold=np.inf)

"""

Library to evaluate the emotion category models.

"""
def eval_cate(y_prob, y_val):

	"""
	to evaluate the emotion category models. print the classification report

	"""
	# Predict input data
	y_classes = y_prob.argmax(axis=-1)
	y_classes = y_classes.flatten()
	y_pred_cate = y_classes


	# Convert binary label to class numbers
	y_val = y_val.argmax(axis=-1)
	y_val = y_val.flatten()
	y_true_cate = y_val

	print(y_true_cate.shape)
	print(y_classes.shape)
	# Evaluate
	target_names = ['Neutral', 'Happiness', 'Sadness', 'Angry', 'Fear', 'Surprise', 'Disgust']

	class_report = classification_report(y_true_cate, y_pred_cate, target_names=target_names)
	print(class_report)
	acc = accuracy_score(y_true_cate, y_pred_cate)
	print(acc)




# Load the models
model = load_model("./model/model.h5", custom_objects={'recall': util.recall, 'precision': util.precision, 'f1': util.f1})

# Load data
val_data_path = "/dataset/val_data.npy"
val_label_path = "/dataset/val_labels_cate.npy"
x_val = load.load_dataset(val_data_path)
y_val = load.load_dataset(val_label_path)

# make prediction
y_prob = model.predict(x_val)

eval_cate(y_prob, y_val, model)
print("Done")
