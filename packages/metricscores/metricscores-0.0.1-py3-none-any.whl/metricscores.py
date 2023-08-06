# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 21:44:59 2022

@author: sarathbabu
"""

from pandas import DataFrame
from sklearn import metrics
from statistics import sqrt

def regressionscores(y_true,y_pred,x_true=[]):
    """Calculates MSE,RMSE,R2,MAE,MAPE in %,MedianAE,MSLE,RMSLE and Max Error.
    For Adjusted R2, Please input x as a Dataframe.
    By Default, x is inputed as empty list."""
    mse=metrics.mean_squared_error(y_true,y_pred)
    rmse=sqrt(mse)
    r2=metrics.r2_score(y_true,y_pred)
    mae=metrics.mean_absolute_error(y_true,y_pred)
    mdae=metrics.median_absolute_error(y_true,y_pred)
    max_e=metrics.max_error(y_true,y_pred)
    msle=metrics.mean_squared_log_error(y_true,y_pred)
    rmsle=sqrt(msle)
    
    if len(x_true)>0:
        degrees_of_freedom_of_samples=len(x_true)-1
        degrees_of_freedom_of_samples_with_predictors=len(x_true)-x_true.shape[1]-1

        adj_r2=(1-r2)*(degrees_of_freedom_of_samples/degrees_of_freedom_of_samples_with_predictors)
        adj_r2=1-adj_r2
    else:
        adj_r2='Provide non empty Input Dataframe'
        

    if 'mean_absolute_percentage_error' in dir(metrics):
        mape=metrics.mean_absolute_percentage_error(y_true,y_pred)
        mape=round(mape*100,2)
        mape=f'{mape:.2f}%'
    else:
        mape='MAPE not available in sklearn'
        
    return DataFrame(zip(['mean squared error','root mean squared error','r2',\
                          'adjusted r2','mean absolute error','mean absolute percentage error',\
                          'median absolute error','mean squared log error',\
                        'root mean squared log error','max error'],\
                        [mse,rmse,r2,adj_r2,mae,mape,mdae,msle,rmsle,max_e]),columns=['metrics','values'])