"""
In this file, you should implement the forward calculation of the basic RNN model and the RNN model with GRUs. 
Please use the provided interface. The arguments are explained in the documentation of the two functions.
"""

import numpy as np
from scipy.special import expit as sigmoid

def rnn(wt_h, wt_x, bias, init_state, input_data):
    """
    RNN forward calculation.
    inputs:
        wt_h: shape [hidden_size, hidden_size], weight matrix for hidden state transformation
        wt_x: shape [input_size, hidden_size], weight matrix for input transformation
        bias: shape [hidden_size], bias term
        init_state: shape [hidden_size], the initial state of the RNN
        input_data: shape [batch_size, time_steps, input_size], input data of `batch_size` sequences, each of
                    which has length `time_steps` and `input_size` features at each time step. 
    outputs:
        outputs: shape [batch_size, time_steps, hidden_size], outputs along the sequence. The output at each 
                 time step is exactly the hidden state
        final_state: the final hidden state
    """

    batch_size, time_steps, _ = np.shape(input_data)
    hidden_size = np.shape(bias)
    outputs = np.zeros((batch_size,time_steps,hidden_size[0]))

    nsteps = np.shape(input_data)[1] # number of time steps

    for ii in range(nsteps):
        init_state = np.tanh(np.dot(init_state,wt_h)+np.dot(input_data[:,ii,:],wt_x)+bias)
        outputs[:,ii,:] = init_state

    final_state = outputs[:, -1, :]
    
    ##################################################################################################
    # Please implement the basic RNN here. You don't need to considier computational efficiency.     #
    ##################################################################################################


    return outputs, final_state


def gru(wtu_h, wtu_x, biasu, wtr_h, wtr_x, biasr, wtc_h, wtc_x, biasc, init_state, input_data):
    """
    RNN forward calculation.

    inputs:
        wtu_h: shape [hidden_size, hidden_size], weight matrix for hidden state transformation for u gate
        wtu_x: shape [input_size, hidden_size], weight matrix for input transformation for u gate
        biasu: shape [hidden_size], bias term for u gate
        wtr_h: shape [hidden_size, hidden_size], weight matrix for hidden state transformation for r gate
        wtr_x: shape [input_size, hidden_size], weight matrix for input transformation for r gate
        biasr: shape [hidden_size], bias term for r gate
        wtc_h: shape [hidden_size, hidden_size], weight matrix for hidden state transformation for candidate
               hidden state calculation
        wtc_x: shape [input_size, hidden_size], weight matrix for input transformation for candidate
               hidden state calculation
        biasc: shape [hidden_size], bias term for candidate hidden state calculation
        init_state: shape [hidden_size], the initial state of the RNN
        input_data: shape [batch_size, time_steps, input_size], input data of `batch_size` sequences, each of
                    which has length `time_steps` and `input_size` features at each time step. 
    outputs:
        outputs: shape [batch_size, time_steps, hidden_size], outputs along the sequence. The output at each 
                 time step is exactly the hidden state
        final_state: the final hidden state
    """

    batch_size, time_steps, _ = np.shape(input_data)
    hidden_size = np.shape(biasc)
    outputs = np.zeros((batch_size,time_steps,hidden_size[0]))

    nsteps = np.shape(input_data)[1]

    for ii in range(nsteps):
        u = sigmoid(np.dot(init_state,wtu_h)+np.dot(input_data[:,ii,:],wtu_x)+biasu)
        r = sigmoid(np.dot(init_state,wtr_h)+np.dot(input_data[:,ii,:],wtr_x)+biasr)

        h_hat = np.tanh(np.dot(input_data[:,ii,:],wtc_x)+np.dot((r*init_state),wtc_h)+biasc)
        init_state = u*init_state+(1-u)*h_hat
        outputs[:,ii,:] = init_state

    final_state = outputs[:,-1,:]
    ##################################################################################################
    # Please implement an RNN with GRU here. You don't need to considier computational efficiency.   #
    ##################################################################################################
       
    
    return outputs, final_state

