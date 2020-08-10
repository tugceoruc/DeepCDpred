import keras
from keras.models import Sequential
from keras.layers import Dense, Activation,Dropout
from keras.utils.np_utils import to_categorical
from keras import regularizers,optimizers
from keras.callbacks import ModelCheckpoint,ReduceLROnPlateau
from keras.layers.normalization import BatchNormalization
import h5py
import numpy
import tensorflow as tf
from keras.backend import tensorflow_backend as K
import theano as T

root=''#path to the training data
features=[]
distance=[]


model=Sequential()
model.add(Dense(units=120,input_dim=733)) # First layer that accepts 733 features from the training data. It includes 120 neurons and selu is used as activation function. 
model.add(Activation('selu'))

model.add(Dense(units=50))
model.add(Activation('selu'))

model.add(Dense(units=30))
model.add(Activation('selu'))

model.add(Dense(units=30))
model.add(Activation('selu'))

model.add(Dense(units=30))
model.add(Activation('selu'))

model.add(Dense(units=30))
model.add(Activation('selu'))

model.add(Dense(units=30))
model.add(Activation('selu'))

model.add(Dense(units=30))
model.add(Activation('selu'))

model.add(Dense(units=1))
model.add(Activation('sigmoid'))

                                                                                                                                    
model.compile(loss='binary_crossentropy',optimizer='sgd',metrics=['accuracy']) # selection of loss function (binary cross-entropy), optimizer (sgd))

with h5py.File(root, 'r') as train_f:
    train=train_f['train_collection']
    features=train['features']
    distance=train['distance']

    distance=distance[0]
    labels=[]
    for dis in distance:
        if dis<=8.0:
            labels.append(1)
        else:
            labels.append(0)

    labels=numpy.matrix(labels)
    labels=labels.transpose()

    labels=numpy.rint(labels)
    features=numpy.transpose(features)
   

    Early_Stopping=keras.callbacks.EarlyStopping(monitor='val_loss', min_delta=0.0001, patience=40, verbose=1, mode='auto')                                                                                        

    Callbacks_List=[Early_Stopping]


    class_weight=[1,10]
    model.fit(features, labels, epochs=300, batch_size=32, validation_split=0.2, callbacks=Callbacks_List, class_weight=class_weight)
    model.save('model_name')

    
