#Program: Keras Trial.py
#Author: Sanjeev Naguleswaran 
#(adapted from https://machinelearningmastery.com/tutorial-first-neural-network-python-keras/)

#Example with Keras

from numpy import loadtxt
from keras import backend as K
import os

#function to switch backends - does not seem to work going from tensorflow ->theano
#In windows command prompt set "KERAS_BACKEND=theano"

def set_keras_backend(backend):

    if K.backend() != backend:
        os.environ['KERAS_BACKEND'] = backend
        import importlib; importlib.reload(K)
        assert K.backend() == backend

set_keras_backend("tensorflow")

from keras.models import Sequential
from keras.layers import Dense
# load the dataset
dataset = loadtxt('pima-indians-diabetes.csv', delimiter=',')
# split into input (X) and output (y) variables
X = dataset[:,0:8]
y = dataset[:,8]
# define the keras model
model = Sequential()
model.add(Dense(12, input_dim=8, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
# compile the keras model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# fit the keras model on the dataset
model.fit(X, y, epochs=150, batch_size=10, verbose=1)
# make class predictions with the model
predictions = model.predict_classes(X)
# summarize the first 5 cases
for i in range(5):
	print('%s => %d (expected %d)' % (X[i].tolist(), predictions[i], y[i]))