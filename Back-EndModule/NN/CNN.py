import numpy as np
import matplotlib.pyplot as plt
import sys
from math import floor, sqrt, isnan
import decimal
import os
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, Conv2D, MaxPooling2D, Flatten, LSTM, Conv1D, GlobalAveragePooling1D, MaxPooling1D, GlobalMaxPooling1D, AveragePooling1D
from keras import regularizers
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split

def mathFilter(y):
    rng = range(1, len(y) - 1)
    res = []
    res.append(y[0])
    for j in rng:
        res.append((y[j - 1] / 4.0 + y[j] / 2.0 + y[j + 1] / 4.0))
    res.append(y[len(y) - 1])
    return res

def flooring(x):
    result = 0
    if not isnan(x):
        result = floor(decimal.Decimal(x))
    return result

def prepareData(path):
    X = np.array([])
    i = 0
    for subdir, dirs, files in os.walk(path):
        for file in files:
            print(file)
            data = np.fromfile(path + file)
            a = 0
            b = 200
            print(b)
            y = []

            for j in range(a, b):
                y.append(0.0 - flooring(data[j]))

            y = mathFilter(mathFilter(mathFilter(mathFilter(y))))
            #y = mathFilter(mathFilter(mathFilter(mathFilter(y))))
            #y = mathFilter(mathFilter(mathFilter(mathFilter(y))))
            #y = mathFilter(mathFilter(mathFilter(mathFilter(y))))
            print(len(y))
            X.append([np.array(y)])

    return np.array(X)
    
def prepareValues():
    labels = [
        "Coronary artery disease",      #0
        "Arterial hypertension",        #1
        "Acute MI",                     #2
        "Transient ischemic attack",    #3
        "Left ventricular hypertrophy", #4
        "Sinus node dysfunction",       #5
        "Earlier MI",                   #6
        "WPW",                          #7
        "AV block",                     #8
        "Bundle branch block",          #9
        "Normal"                        #10
    ]
    mlb = MultiLabelBinarizer()
    mlb.fit(labels)
    Y = np.array((
        
        mlb.transform((labels[0], labels[1])), 
        mlb.transform((labels[0], labels[1])), 
        mlb.transform((labels[2])), 
        mlb.transform((labels[2])), 
        mlb.transform((labels[2])),
        
        mlb.transform((labels[3])), 
        mlb.transform((labels[3])), 
        mlb.transform((labels[10])), 
        mlb.transform((labels[8])), 
        mlb.transform((labels[8])),
        
        mlb.transform((labels[8])), 
        mlb.transform((labels[10])), 
        mlb.transform((labels[10])), 
        mlb.transform((labels[10])), 
        mlb.transform((labels[3])),
        
        mlb.transform((labels[3])), 
        mlb.transform((labels[3])), 
        mlb.transform((labels[10])), 
        mlb.transform((labels[10])), 
        mlb.transform((labels[0], labels[1], labels[4])),
        
        mlb.transform((labels[0], labels[1], labels[4])), 
        mlb.transform((labels[0], labels[1], labels[4])), 
        mlb.transform((labels[6])), 
        mlb.transform((labels[6])), 
        mlb.transform((labels[5])),
        
        mlb.transform((labels[5])), 
        mlb.transform((labels[10])), 
        mlb.transform((labels[10])), 
        mlb.transform((labels[10])), 
        mlb.transform((labels[10])),
        
        mlb.transform((labels[10])), 
        mlb.transform((labels[10])), 
        mlb.transform((labels[10])), 
        mlb.transform((labels[10])), 
        mlb.transform((labels[0], labels[1], labels[4])),
        
        mlb.transform((labels[0], labels[1], labels[4])), 
        mlb.transform((labels[0], labels[1], labels[4])), 
        mlb.transform((labels[0], labels[1])), 
        mlb.transform((labels[0], labels[1])), 
        mlb.transform((labels[3])),
        
        mlb.transform((labels[3])), 
        mlb.transform((labels[10])), 
        mlb.transform((labels[10])), 
        mlb.transform((labels[0], labels[1], labels[4])), 
        mlb.transform((labels[0], labels[1], labels[4])),
        
        mlb.transform((labels[0], labels[1], labels[4])), 
        mlb.transform((labels[6])), 
        mlb.transform((labels[6])), 
        mlb.transform((labels[10])), 
        mlb.transform((labels[10])),
        
        mlb.transform((labels[10])), 
        mlb.transform((labels[10])), 
        mlb.transform((labels[10])), 
        mlb.transform((labels[6])), 
        mlb.transform((labels[6])),
        
        mlb.transform((labels[6])), 
        mlb.transform((labels[6])), 
        mlb.transform((labels[10])), 
        mlb.transform((labels[10])), 
        mlb.transform((labels[10])),
        
        mlb.transform((labels[10])), 
        mlb.transform((labels[2])), 
        mlb.transform((labels[2])), 
        mlb.transform((labels[2])), 
        mlb.transform((labels[10])),
        
        mlb.transform((labels[10])), 
        mlb.transform((labels[10])), 
        mlb.transform((labels[7])), 
        mlb.transform((labels[7])), 
        mlb.transform((labels[7])),
        
        mlb.transform((labels[7])), 
        mlb.transform((labels[0], labels[1], labels[4])), 
        mlb.transform((labels[0], labels[1], labels[4])), 
        mlb.transform((labels[6])), 
        mlb.transform((labels[6])),
    ))
    return Y

def main():
    path = "./../../DataSets/"
    X = np.array(prepareData(path))
    Y = prepareValues()

    (trainX, testX, trainY, testY) = train_test_split(X, Y, test_size=0.3, random_state=1349)

    model = Sequential()
    model.add(Conv1D(filters=200, kernel_size=3, activation='softmax', input_shape=(200, len(Y.shape[2]), )))
    model.add(Dense(100, activation='relu'))
    model.add(Conv1D(100, (3,), activation='softmax'))
    model.add(Dense(20, activation='relu'))
    model.add(Conv1D(20, (3,), activation='softmax'))
    model.add(Conv1D(10, (3,), activation='relu'))
    model.add(Conv1D(20, (3,), activation='softmax'))
    model.add(Dense(2, activation='relu'))
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    model.build()

    output = model.fit_generator((trainX, trainY), validation_data=(testX, testY), steps_per_epoch=len(trainX), epochs=18000, verbose=1)

    plt.style.use("ggplot")
    plt.figure()
    plt.plot(np.arange(0, 18000), output.history["loss"], label="train_loss")
    plt.plot(np.arange(0, 18000), output.history["val_loss"], label="val_loss")
    plt.plot(np.arange(0, 18000), output.history["acc"], label="train_acc")
    plt.plot(np.arange(0, 18000), output.history["val_acc"], label="val_acc")
    plt.title("Training Loss and Accuracy")
    plt.xlabel("Epoch #")
    plt.ylabel("Loss/Accuracy")
    plt.legend(loc="upper left")
    plt.savefig("plot")


if __name__ == "__main__":
    main()
