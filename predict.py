from tensorflow.keras.models import load_model
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np
import math,os
import matplotlib.pyplot as plt

    

def main():

   epoch=1000
   b_size=20
   k=15
   
   workpath='../features'
   outdir  ='./result'
   os.system('mkdir '+ outdir)
  
   print('Loading training data ...')
   # load training dataset
   X_test = np.load(workpath + '/X_test_nor.npy')
   X_test = X_test.astype(np.float)


   
   prediction=[]
   for i in range(k): 
       
       # load trained model
       model_name ='./model/CNN/cnn_epoch_1000_fold_'+str(i+1)+'.h5'

       model = load_model(model_name)
       y_pred = model.predict(X_test)
       prediction=prediction+y_pred
       
       
   # save average predictions metric
   average_prediction=prediction /k
   
   with open(outdir+"/predcit.txt","w") as filename:
        filename1.write( 'The last predicted value is: '+str(average_prediction)  +'\n')

   filename.close()   

   print("The last predicted value is: {}".format(average_prediction))

if __name__ == '__main__':
    main()

