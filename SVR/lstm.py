import gc
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import pickle
from sklearn.preprocessing import StandardScaler
from get_data import gen_input


import keras
from keras.models import Sequential
from keras.layers import Activation, Dense
from keras.layers import LSTM
from keras.layers import Dropout


x,y,scaler_speed, scaler_flow , scaler_occu = gen_input()


x_train = x[:-10]
x_test = x[-10:]
y_train = y[:-10][:,:1]
y_test = y[-10:][:,:1]

print (x_train.shape)
print (x_test.shape)
print (y_train.shape)
print (y_test.shape)

model = Sequential()

model.add(LSTM(units = 64, input_shape = (100,3), return_sequences = True))
model.add(LSTM( 64, return_sequences=False)) # SET HERE
# regressor.add(Dropout(0.2))
model.add(Dense(1))
model.compile(optimizer = 'adam', loss = 'mean_squared_error')
model.summary()

model.fit(x_train, y_train, epochs = 500, batch_size = 32)

with open('lstm.pickle','wb') as f:
    pickle.dump(model,f)

with open('lstm.pickle','rb') as f:
    model = pickle.load(f)

res=[]
for i in x_test:
    vec = np.array([i.tolist()])
    speed = model.predict(vec)
    res.append(scaler_speed.inverse_transform(speed.tolist()).tolist()[0][0])

# print (res)
x = list(range(len(y_test)))

y_true = [scaler_speed.inverse_transform(i.reshape(1,1)).tolist()[0][0] for i in y_test]
# print (y_true)
fig = plt.figure()
plt.plot(x,y_true,'r')
plt.plot(x,res,'b')
plt.show()
