import random
import pandas as pd
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
# tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
# tf.get_logger().setLevel('ERROR')

import tensorflow as tf

from keras import Sequential
from keras.layers import  Activation
import tensorflow.keras.backend as K
from keras.layers import Dense,Dropout
from sklearn.model_selection import train_test_split

import warnings
warnings.filterwarnings('ignore')
pd.set_option('max_columns', None)
random.seed(42)
#--------------------------------------------------

stv=pd.read_csv('data/sales_train_validation.csv')
cal=pd.read_csv('data/calendar.csv')
ss = pd.read_csv('data/sample_submission.csv')

stv_df = stv.drop(['item_id', 'dept_id', 'cat_id', 'store_id', 'state_id'], axis=1).set_index('id').T
stv_df['d'] = stv_df.index

df = pd.merge(cal, stv_df, left_on='d', right_on='d', how='left')


def event_detector(x):
    if x == None:
        return 0
    else:
        return 1


drp = ['wm_yr_wk', 'weekday', 'year', 'd', 'event_type_1', 'event_type_2']

#we will use these columns
cols_x = ['wday', 'month', 'event_name_1', 'event_name_2','snap_CA', 'snap_TX', 'snap_WI']


# process events to binary
df = df.drop(drp, axis=1)
df['event_name_1'] = df['event_name_1'].apply(lambda x: event_detector(x))
df['event_name_2'] = df['event_name_2'].apply(lambda x: event_detector(x))

ddf = df[(pd.to_datetime(df['date']) < '2016-04-25')&(pd.to_datetime(df['date']) >= '2015-06-19')].drop('date', axis=1)
#valid_df = df[(pd.to_datetime(df['date']) >= '2016-04-25')&(pd.to_datetime(df['date']) < '2016-05-23')].drop('date', axis=1)
eval_df = df[pd.to_datetime(df['date']) >= '2016-04-25'].drop('date', axis=1)

X_ddf = ddf[cols_x]
y_ddf = ddf.drop(cols_x, axis=1)



X_train, X_valid, y_train, y_valid = train_test_split(
         X_ddf, y_ddf, test_size=0.33, random_state=42,shuffle=False)

X_eval=eval_df[cols_x]
y_eval=eval_df.drop(cols_x, axis=1)

EarlyStopping = tf.keras.callbacks.EarlyStopping(restore_best_weights=True)
# model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
#     filepath='best_model.pkl',
#     save_weights_only=True,
#     monitor='val_loss',
#     mode='min',
#     save_best_only=True)

def rmse(y_true, y_pred):
    return K.sqrt(K.mean(K.square(y_pred -y_true)))

epochs=1
batch_size = 512
verbose = 1
validation_split = 0.2
input_dim = X_train.shape[1]
n_out = y_train.shape[1]

model = Sequential([
                Dense(256, input_shape=(input_dim,)),
                Activation('relu'),
                Dropout(0.2),
                Dense(128),
                Activation('relu'),
                Dropout(0.2),
                Dense(n_out),
                Activation('relu'),
                    ])

model.compile(loss='mse',
                 optimizer='adam',
                 metrics=['mse', rmse])
hist = model.fit(X_train, y_train,validation_data=[X_valid,y_valid],
                         batch_size = batch_size, epochs = epochs,
                         callbacks = [EarlyStopping],
                         verbose=verbose, validation_split=validation_split)

cust_object={ 'rmse': rmse}

model.save('models/model.h5')
score = model.evaluate(X_valid, y_valid, verbose=verbose)
print("\nTest score:", score)

model=tf.keras.models.load_model('models/model.h5',custom_objects=cust_object)
y_pred=model.predict(X_eval)



