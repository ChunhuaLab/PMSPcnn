#!/usr/bin/env python3

# import required modules
import numpy as np
import pandas as pd
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.layers import Input, Dense, Dropout, Flatten
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Input, Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv1D, MaxPooling1D, AveragePooling1D
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
from tensorflow.keras.models import load_model
from tensorflow.keras import callbacks
from scipy import stats
from sklearn.model_selection import StratifiedKFold
import h5py
import os
import random




def build_model(dimension):
  
  input1 = Input(shape =((dimension,1)))

    # Set up 1dconv  model
  model_con1d = Conv1D(32,3,padding='same',activation='relu',kernel_initializer='he_normal')(input1)
  model_con1d = Conv1D(32,3,padding='same',activation='relu',kernel_initializer='lecun_uniform')(model_con1d)
  model_con1d = Dropout(0.2)(model_con1d)
 
  model_con1d = Conv1D(64,3,padding='same',activation='relu',kernel_initializer='lecun_uniform')(model_con1d)
  model_con1d = Conv1D(64,3,padding='same',activation='relu',kernel_initializer='lecun_uniform')(model_con1d)
  model_con1d = MaxPooling1D(3)(model_con1d)
  
  model_con1d = Conv1D(128,3,padding='same',activation='relu',kernel_initializer='lecun_uniform')(model_con1d)
  model_con1d = Conv1D(128,3,padding='same',activation='relu',kernel_initializer='lecun_uniform')(model_con1d)
  model_con1d = MaxPooling1D(3)(model_con1d)

  

  
  intermediate_output = Flatten()(model_con1d)
  model_final = Dropout(0.5)(intermediate_output)
  final_output = Dense(1,activation='linear')(model_final)  
  #
  # Set up model input and output
  Model_deep = Model(inputs = input1, outputs = final_output)
  
  

  return Model_deep


def cross_validate(X_direct, X_reverse, y_direct, y_reverse,label, epoch_size, k, b_size,outdir,dimension):
    """
    """
    assert len(X_direct) == len(X_reverse) and len(y_direct) == len(y_reverse) and len(X_direct) == len(y_direct)
    
    print('===============================================================')
    print('Cross-validating convolutional architecture epoch: ',  epoch_size)
    print('===============================================================')
    
   
    all_histories = []
    all_predictions = []
    mse=0
    rmse=0
    pccs=0
    PCC=[]
    
    # Regression stratification cross validation
        
    n=0
    kfold = StratifiedKFold(n_splits = k, shuffle=True, random_state =9)
    for train_index, validation_index in kfold.split(X_direct, label):
        X_direct_train, X_direct_validation = X_direct.iloc[train_index], X_direct.iloc[validation_index]
        X_reverse_train, X_reverse_validation = X_reverse.iloc[train_index], X_reverse.iloc[validation_index]
        y_direct_train, y_direct_validation = y_direct.iloc[train_index], y_direct.iloc[validation_index]
        y_reverse_train, y_reverse_validation = y_reverse.iloc[train_index], y_reverse.iloc[validation_index]
        
        X_train=np.concatenate((X_direct_train, X_reverse_train),axis=0)
        X_test =np.concatenate((X_direct_validation, X_reverse_validation),axis=0)
        Y_train=np.concatenate((y_direct_train, y_reverse_train),axis=0)
        Y_test=np.concatenate((y_direct_validation, y_reverse_validation),axis=0)
        
        
        n=n+1
        # checkpoint
        filepath=outdir + '/cnn_epoch_'+ str(epoch_size)+ '_fold_'+str( n ) + '.h5'
#        checkpoint = callbacks.ModelCheckpoint(filepath, monitor='val_loss', verbose=1, 
#                save_best_only=True, mode='min')
#        callbacks_list = [checkpoint]
        
        checkpoint = callbacks.ModelCheckpoint(filepath, monitor='val_loss', verbose=1, 
                save_best_only=True, mode='min')
        # reduce_on_plateau = callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=10)
        early_stopping = callbacks.EarlyStopping(monitor='val_loss', patience=80)
        callbacks_list = [checkpoint, early_stopping]
        
        
        
        # build a model
        
        Model_deep = build_model(dimension)
        adam = Adam(lr=0.0001)
        Model_deep.compile(optimizer=adam,loss='mse',metrics = ['mae'])
        
        print('The train_X shape is ',X_train.shape)
        
        # fit the model
        history = Model_deep.fit(X_train, Y_train, validation_data=(X_test, Y_test),callbacks=[checkpoint], epochs=epoch_size,batch_size=b_size)
        #history = Model_deep.fit(train_X, train_y, validation_data=(val_X, val_y), epochs=epoch,batch_size=b_size)

        # evaluate the model on the valitaion set
        all_histories.append(history)
        
        # load the best model for predictions
        best_model = load_model(filepath)
        predictions = best_model.predict(X_test)
        all_predictions.append(np.column_stack((predictions[:, 0], Y_test)))
        
        

def main():
    """
    """
    #outdir ='./test'
    outdir ='./last_model_epoch'
    workpath='../Q3211/feature_3211/aux_nor'
    
    #input_shape=(792,1)
    k = 5
    b_size=60
    
    # load training dataset
    X_direct = np.load(workpath + '/X_all_D_nor.npy')
    X_direct = pd.DataFrame(X_direct,dtype=float)
   
    X_reverse = np.load(workpath + '/X_all_R_nor.npy')
    X_reverse = pd.DataFrame(X_reverse,dtype=float)
   
    y_direct = np.load(workpath+'/Y_d.npy')
    y_direct = pd.DataFrame(y_direct,dtype=float)

    y_reverse = np.load(workpath+'/Y_R.npy')
    y_reverse = pd.DataFrame(y_reverse,dtype=float)

    
    label=np.load( 'label.npy')
    label=pd.DataFrame(label)

    shape=X_direct.shape[1]
    # instantiate the model
 
    epoch_size = 1000
    
    #for i in range(0,3):


    model = build_model(shape)
    #model.summary()
    # five-fold cross-validation
    cross_validate(X_direct, X_reverse, y_direct, y_reverse,label, epoch_size,k, b_size,outdir,shape)
    

    for i, p in enumerate(all_predictions):
         np.savetxt(os.path.join(outdir, 'conv_epoch_' + str(epoch_size) + '_fold_' + str(i + 1) + '_predictions.csv')
             , p, delimiter=',', fmt='%.3f')


if __name__ == '__main__':
    main()
