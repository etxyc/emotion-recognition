from keras.applications.xception import Xception
from keras.layers import LSTM
from keras import Sequential
from keras.models import Model
from keras.layers import Dense, Flatten, Dropout, Input
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
class_num = 7
lr = 0.00001
decay = 0.0001
adam = Adam(lr=lr, decay=decay)


# Load dataset
train_data_path = "/dataset/train_data.npy"
train_label_path = "/dataset/train_labels_cate.npy"
val_data_path = "/dataset/val_data.npy"
val_label_path = "/dataset/val_labels_cate.npy"

x_train = load.load_dataset(train_data_path)
y_train = load.load_dataset(train_label_path)
x_val = load.load_dataset(val_data_path)
y_val = load.load_dataset(val_label_path)



#setup cnn
cate_input = Input(shape=(72, 72, 3))



vgg = Xception(include_top=False, weights='imagenet', input_shape=(72,72,3))
for layer in vgg.layers:
	layer.trainable = False

vgg_out_cate = vgg(cate_input)
vgg_out_cate = Dropout(0.5)(vgg_out_cate)
vgg_out_cate = Flatten()(vgg_out_cate)


cnn = Model(inputs=cate_input, outputs=vgg_out_cate)



#add LSTM to model

seq_input = Input(shape=(seq_length, 72, 72, 3))
seq_output = TimeDistributed(cnn)(seq_input)
lstm_output = LSTM(128, input_shape=(batch_size, seq_length, 1), return_sequences=True)(seq_output)
lstm_output = TimeDistributed(Dropout(0.5))(lstm_output)




# add FC
cate_output = TimeDistributed(Dense(class_num, activation='softmax'), name='cate_output')(lstm_output)


# train
model = Model(inputs=seq_input, outputs=cate_output)
print(model.summary())
model.compile(optimizer=adam, loss='categorical_crossentropy', metrics=['accuracy', util.recall, util.precision, util.f1])

# save the model
if not os.path.exists("./model"):
	os.makedirs("./model")

filepath = "./model/model.h5"
checkpoint = ModelCheckpoint(filepath, save_best_only=True)
callbacks_list = [checkpoint]


hist = model.fit(x=x_train, y=y_train, validation_data=(x_val, y_val), epochs=epoch, batch_size=batch_size, callbacks=callbacks_list)

print(hist.history)
