import pandas as pd
import numpy as np
from collections import namedtuple


def load_labeled_csv(filename, feature_cols, label_cols):
    """
    Loads a .csv file with labeled data into memory. CSV File has to contain
    samples in rows and features and labels in columns. The utility function
    then returns a named tuple with relevant information about data set.

    Arguments:
    ----------
        filename: string.
            Filename with .csv (str), e.g. 'test.csv'.
        feature_cols: list.
            Indices of columns with features, e.g. [0, 1].
        label_cols: list.
            Indices of columns with labels, e.g. [2, 3].

    Returns:
    --------
        data:   named tuple.
            data.features: array-like, shape=[# samples, # features].
                Features of the data set.
            data.labels: array-like, shape=[# samples, # labels].
                Labels of the data set.
            data.nb_features:   integer. 
                Number of features.
            data.nb_labels: integer.
                Number of labels.
            data.nb_samples: integer.
                Number of samples.
    """

    data = namedtuple('data_set', ['features', 'labels', 'nb_features',
                      'nb_labels', 'nb_samples'])

    raw_data = pd.read_csv(filename, skiprows=0).values
    
    data.features = raw_data[:, feature_cols]
    data.labels = raw_data[:, label_cols]

    data.nb_features = len(feature_cols)
    data.nb_labels = len(label_cols)
    data.nb_samples = raw_data.shape[0]

    return data


def make_log_df(nb_hidden_layers):
    """
    Utility function that prepares a Pandas DataFrame that may be used as a 
    log file to track training and validation losses and accuracies for a
    fully connected neural network with a specified number of hidden layers.

    Arguments:
    ----------
        nb_hidden_layers: integer.
            Number of hidden layers in fully connected neural network.

    Returns:
    --------
        log_df: pandas dataframe, shape=[, nb_layers + 8]
            Pandas df that serves as a log file.
    """

    # Make lists of column names to be included in df.
    units_hidden = ['# layer %i' %i for i in range(1, nb_hidden_layers + 1)]
    params = units_hidden + ['lr']
    train_cols = ['train_loss', 'train_acc2pc', 'train_acc1pc']
    val_cols = ['val_loss', 'val_acc2pc', 'val_acc1pc']
 
    # Merge lists of column names in one big list for df creation.
    cols =  params + ['epoch'] + train_cols + val_cols

    log_df = pd.DataFrame(columns=cols)

    return log_df


def make_hyper_param_str(hyper_params):
    """
    Takes a list of hyperparameters for a fully connected neural network, i.e. 
    the number of units per layer, the learning rate and the size of the mini-
    batches and turns them into an identifier string.

    Arguments:
    ----------
        hyper_params: list.
            List of hyperparameters of a fully connected neural network.
                layer_sizes: array-like, shape=[, # layers]
                    Number of units per layer, e.g. [32,16,8,4].
                learning_rate: float.
                    Learning rate used for backpropagation.
                mini_batch_size: integer.
                    Size of individual mini-batches used for backpropagation.

    Returns:
    --------
        hyper_param_str: string.
            String encoding all hyperparameter information.
    """

    layer_sizes, lr, mini_batch_size = hyper_params

    layer_sizes = str(layer_sizes)[1:-1].replace(" ", "")

    hyper_param_str = "nn=%s_lr=%.6E_mbs=%s" % (layer_sizes, lr, mini_batch_size)

    return hyper_param_str


def verbose_print(verbose, str_to_print):
    """
    Prints 'str_to_print' if verbose is True and nothing otherwise.

    Arguments:
    ----------
        verbose: boolean.
            If verbose=True, then print string, otherwise don't.
        str_to_print: string.
            String to print.
    """

    if verbose == True:

            print(str_to_print)


def nn_is_fully_trained(df, threshold):
    """
    Checks from df whether acc2pc on the validation set exceeds the given
    threshold, i.e. whether the network is fully trained. If yes, then returns
    True, otherwise False.

    Argument:
    ---------
        df: pandas dataframe, shape=[, nb_layers + 8].
            Pandas df log file obtained from backpropagation training.
        threshold: float, between 0 and 1.
            Percentage threshold for acc2pc on validation set for network to 
            stop learning.

    Returns:
    --------
        Boolean.
            True if accuracy achieved, False otherwise.
    """

    if df.loc[df.shape[0] - 1, 'val_acc2pc'] >= threshold:

        print('Neural network fully trained.')

        return True

    else:

        return False


def nn_does_not_learn(df):
    """
    Checks from df whether the NN does not learn, i.e. if the mean of the 
    accuracies on the validation set in the last three epochs is 0.
    If yes, then function returns True, False otherwise.

    Arguments:
    ----------
        df: pandas dataframe, shape=[, nb_layers + 8]
            Pandas df log file obtained from backpropagation training.

    Returns:
    --------
        Boolean.
            True if NN does not learn, False otherwise.
    """

    # Last epoch of training.
    last_ep = df.shape[0]

    if last_ep >= 3 and np.mean(df.loc[last_ep-3:last_ep , 'val_acc2pc']) <= 0:

        print('Neural network does not learn.')

        return True

    else: 

        return False

