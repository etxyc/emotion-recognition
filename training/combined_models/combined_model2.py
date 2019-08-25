from keras.applications.vgg16 import VGG16
from keras.layers import LSTM
from keras import Sequential
from keras.models import Model
from keras.layers import Dense, Flatten, Input, Dropout
from keras.layers import TimeDistributed
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint
import numpy as np
from sklearn.model_selection import train_test_split
import load_dataset as load
import os
import util_cate as util1
import util_VA as util2
np.set_printoptions(threshold=np.inf)
print(os.getcwd())

# set hyperparameters
batch_size = 2
epoch = 50
lr = 0.00001
decay = 0.00001
seq_length = 60
cate_num = 7
VA_num = 2
adam = Adam(lr=lr, decay=decay)

# Load dataset
train_data_path = "/dataset/train_data.npy"
train_label_path_VA = "/dataset/train_labels_VA.npy"
train_label_path_cate = "/dataset/train_labels_cate.npy"
val_data_path = "/dataset/val_data.npy"
val_label_path_VA = "/dataset/val_labels_VA.npy"
val_label_path_cate = "/dataset/val_labels_cate.npy"


x_train = load.load_dataset(train_data_path)
x_val = load.load_dataset(val_data_path)
y_VA_train = load.load_dataset(train_label_path_VA)
y_VA_val = load.load_dataset(val_label_path_VA)
y_cate_train = load.load_dataset(train_label_path_cate)
y_cate_val = load.load_dataset(val_label_path_cate)


# set cnn
cate_input = Input(shape=(72, 72, 3))
vgg = VGG16(include_top=False, weights='imagenet', input_shape=(72,72,3))
for layer in vgg.layers:
	layer.trainable = False

vgg_out_cate = vgg(cate_input)
vgg_out_cate = Dropout(0.5)(vgg_out_cate)
vgg_out_cate = Flatten()(vgg_out_cate)

cnn = Model(inputs=cate_input, outputs=vgg_out_cate)


# set RNN
seq_input = Input(shape=(seq_length, 72, 72, 3))
seq_output = TimeDistributed(cnn)(seq_input)
lstm_output = LSTM(128, input_shape=(batch_size, seq_length, 1), return_sequences=True)(seq_output)
lstm_output = TimeDistributed(Dropout(0.5))(lstm_output)


# define 2 dense and timedistributed for each mode



cate_output = TimeDistributed(Dense(cate_num, activation='softmax'), name='cate_output')(lstm_output)




VA_output = TimeDistributed(Dense(VA_num, activation='linear'), name='VA_output')(lstm_output)


# train
model = Model(inputs=seq_input, outputs=[cate_output, VA_output])
print(model.summary())
model.compile(optimizer=adam, loss={'cate_output': 'categorical_crossentropy', 'VA_output': 'mse'}, loss_weights={'cate_output': 0.33, 'VA_output': 1.0}, metrics={'cate_output': ['accuracy', util1.f1], 'VA_output': [util2.ccc, 'mse']})



# save the model
if not os.path.exists("./model"):
	os.makedirs("./model")

filepath = "./model/model.h5"
checkpoint = ModelCheckpoint(filepath, save_best_only=True)
callbacks_list = [checkpoint]


hist = model.fit(x=x_train, y={'cate_output': y_cate_train, 'VA_output': y_VA_train},validation_data=(x_val, {'cate_output': y_cate_val, 'VA_output': y_VA_val}), epochs=epoch, batch_size=batch_size, callbacks=callbacks_list)


print(hist.history)


#model.save_weights("./model/model.h5")
#model_json = model.to_json()
#with open("./model/model.json", "w") as json_file:
#	json_file.write(model_json)
#print("Model Saved")
