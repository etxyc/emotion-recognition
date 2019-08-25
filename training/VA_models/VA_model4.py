from keras.applications.vgg19 import VGG19
from keras.layers import LSTM
from keras import Sequential
from keras.layers import Dense, Flatten, Dropout
from keras.layers import TimeDistributed
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint
import numpy as np
from sklearn.model_selection import train_test_split
import load_dataset as load
import os
import util
np.set_printoptions(threshold=np.inf)
print(os.getcwd())

# set hyperparameters
seq_length = 60
batch_size = 2
epoch = 50
class_num = 2
lr = 0.0001
decay = 0.0001
adam = Adam(lr=lr, decay=decay)


# Load dataset
train_data_path = "/dataset/train_data.npy"
train_label_path = "/dataset/train_labels_VA.npy"
val_data_path = "/dataset/val_data.npy"
val_label_path = "/dataset/val_labels_VA.npy"

x_train = load.load_dataset(train_data_path)
y_train = load.load_dataset(train_label_path)
x_val = load.load_dataset(val_data_path)
y_val = load.load_dataset(val_label_path)


#setup vgg cnn
vgg = VGG19(include_top=False, weights='imagenet', input_shape=(72,72,3))
cnn = Sequential()
cnn.add(vgg)
cnn.add(Dropout(0.5))
cnn.add(Flatten())

#add LSTM to model
model = Sequential()
model.add(TimeDistributed(cnn, input_shape=(seq_length, 72, 72, 3), trainable=False))
model.add(LSTM(128, input_shape=(batch_size, seq_length, 1), return_sequences=True))
model.add(TimeDistributed(Dropout(0.5)))


# add FC
model.add(TimeDistributed(Dense(128)))
model.add(TimeDistributed(Dropout(0.5)))
model.add(TimeDistributed(Dense(class_num, activation='linear')))


# train
print(model.summary())
model.compile(optimizer=adam, loss='mse', metrics=[util.ccc, 'mse'])


# save the model
if not os.path.exists("./model"):
	os.makedirs("./model")

filepath = "./model/model.h5"
checkpoint = ModelCheckpoint(filepath, save_best_only=True)
callbacks_list = [checkpoint]


hist = model.fit(x=x_train, y=y_train, validation_data=(x_val, y_val), epochs=epoch, batch_size=batch_size, callbacks=callbacks_list)

print(hist.history)
