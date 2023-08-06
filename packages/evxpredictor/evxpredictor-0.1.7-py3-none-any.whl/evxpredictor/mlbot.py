import os
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import joblib
import numpy as np
from pkg_resources import resource_filename
import fire

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import tensorflow as tf

import logging
import tensorflow as tf
tf.get_logger().setLevel(logging.ERROR)
tf.autograph.set_verbosity(0)


class Evx:
  model_path = resource_filename(__name__, 'finalized_model.h5')  
  model_scaler_path = resource_filename(__name__, 'logscaler.gz')



  def __init__(self,*args):
  	pass

  @classmethod
  def loadmodel(cls):
    loaded_model = joblib.load(open(f'{cls.model_path}', 'rb'))
    return loaded_model


  @classmethod
  def prepareInput(cls,opening,closing,volume):
  	ask_ind = closing*volume/(opening + closing)
  	bid_ind = opening*volume/(opening + closing)
  	testdata = np.array([[ask_ind,bid_ind]])
  	scaler = joblib.load(f'{cls.model_scaler_path}')
  	testdata = scaler.transform(testdata)

  	return testdata


  @classmethod
  def buySignalGenerator(cls,opening,closing,volume,alpha):
    scalledInput = cls.prepareInput(opening,closing,volume)
    return (cls.loadmodel().predict(scalledInput) >= alpha).astype("int")[0][0]
    
  @classmethod
  def sellSignalGenerator(cls,opening,closing,volume,alpha):
    scalledInput = cls.prepareInput(opening,closing,volume)
    return (cls.loadmodel().predict(scalledInput) < alpha).astype("int")[0][0]



def signal(opening,closing,volume,alpha,sig):
  if sig == 'buy':
    try:
      return Evx.buySignalGenerator(opening,closing,volume,alpha=0.6494407)
    except Exception as e:
      print(e)
  elif sig == 'sell':
    try:
      return Evx.sellSignalGenerator(opening,closing,volume,alpha=0.6494407)
    except Exception as e:
      print(e)
  else:
    return f'{sig} is not a valid entry!'


if __name__ == '__main__':
  fire.Fire(signal)
