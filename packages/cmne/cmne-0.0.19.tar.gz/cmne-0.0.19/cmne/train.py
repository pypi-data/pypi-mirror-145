#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# @authors   Christoph Dinh <christoph.dinh@brain-link.de>
#            John G Samuelson <johnsam@mit.edu>
# @version   1.0
# @date      April, 2018
# @copyright Copyright (c) 2018-2022, authors of CMNE. All rights reserved.
# @license   MIT
# @brief     Methods to train the LSTM model
# ---------------------------------------------------------------------------

#%%
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import datetime

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM

from keras.callbacks import TensorBoard

from .settings import Settings
from .data import Data
from .data import generate_lstm_batches


def train(
    settings: Settings,
    data: Data,
    minibatch_size: int=30,
    steps_per_ep: int=25,
    num_epochs: int=100,
    lstm_look_back: int=80,
    num_units: int=1280,
    idx: int=None,
    verbose: bool=False
) -> str:
    """
    Train the LSTM model.

    Args:
        settings: Settings object
        data: Data object
        minibatch_size: Size of the minibatches
        steps_per_ep: Number of steps per epoch
        num_epochs: Number of epochs
        lstm_look_back: Number of time steps to look back
        num_units: Number of units in the LSTM layer
        idx: selection of the training epochs, if None all epochs are used
    
    Returns:
        model_name: Name of the trained model
    """    
    
    ###################################################################################################
    # The Script
    ###################################################################################################
    
    num_features_in = data.inv_op()['nsource']
    num_labels_out = num_features_in
    
    # TensorBoard Callback
    tbCallBack = TensorBoard(log_dir=settings.tb_log_dir(), histogram_freq=1, write_graph=True, write_images=True)

    #time_steps_in = lstm_look_back
    # create the Data Generator
    data_generator = generate_lstm_batches(epochs=data.train_epochs(idx=idx), inverse_operator=data.inv_op(), lambda2=data.lambda2(), method=data.method(), look_back=lstm_look_back, batch_size=minibatch_size)
    
    # create LSTM model
    model = None
    model = Sequential()
    model.add(LSTM(num_units, activation='tanh', return_sequences=False, input_shape=(lstm_look_back,num_features_in)))
    model.add(Dense(num_labels_out, activation='linear'))
    
    # compile the model
    model.compile(loss = 'mean_squared_error', optimizer = 'adam')
    
    # Train - fit the model :D
    fitting_result = model.fit_generator(data_generator, steps_per_epoch = steps_per_ep, epochs = num_epochs, verbose=1, callbacks=[tbCallBack], validation_data=None, class_weight=None, workers=1)
    
    # # let's get some predictions
    # test_predict = model.predict(test_features)
    
    
    ###################################################################################################
    # Save Results
    ###################################################################################################
    
    date_stamp = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')

    fname_model = settings.results_models_path() + '/model_' + settings.modality() + '_nu_' + str(num_units) +'_lb_' + str(lstm_look_back) + '_' + date_stamp + '.h5'
    fname_training_loss = settings.results_training_path() + '/loss_' + settings.modality() + '_nu_' + str(num_units) +'_lb_' + str(lstm_look_back) + '_' + date_stamp + '.txt'
    fname_result_fig = settings.results_img_path() + '/loss_' + settings.modality() + '_nu_' + str(num_units) +'_lb_' + str(lstm_look_back) + '_' + date_stamp + '.png'
    
    history_losses = fitting_result.history['loss']
    
    # save model
    model.save(fname_model)
    
    # # plot the data
    if verbose:
        print('Testing Prediction',test_predict)
        print('Testing Reference',test_labels)
    
    # save loss
    np.savetxt(fname_training_loss, fitting_result.history['loss'])
    
    # save data plot
    plt.figure()
    plt.plot(fitting_result.history['loss'])
    plt.xlabel('Minibatch number')
    plt.ylabel('Loss')
    plt.title('Minibatch run vs. Training loss')
    #axes = plt.gca()
    #axes.set_xlim([xmin,xmax])
    #axes.set_ylim([0,1.2])
    fig = plt.gcf()
    fig.set_size_inches(8, 6)
    plt.savefig(fname_result_fig, dpi=300)
    
    # plot data
    if verbose:
        plt.show()

    return fname_model