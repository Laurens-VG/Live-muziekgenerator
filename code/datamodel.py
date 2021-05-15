"""File that creates the annotation for SuperCollider through the means of a machine learning model."""
# Author: Laurens Van Goethem, UGent

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPRegressor
from matplotlib.pyplot import axvline, axhline
from mir_main import get_min_max, translate
import csv


# Normalizes the data from deam
def normalize_data_deam(filename):
    df = pd.read_csv(filename)
    df = df.drop('first', 1).iloc[:, :]
    df_temp = df.drop('valence', 1).drop('arousal', 1)
    normalized_df = (df_temp - df_temp.min()) / (df_temp.max() - df_temp.min())
    normalized_df['valence'] = df['valence']
    normalized_df['arousal'] = df['arousal']
    normalized_df.to_csv('model_data/dataset_deam_norm.csv')


# Normalizes the data from supercollider
def normalize_data_super(filename):
    df = pd.read_csv(filename)
    df = df.drop('first', 1).iloc[:, :]
    normalized_df = (df - df.min()) / (df.max() - df.min())
    normalized_df.to_csv('model_data/dataset_super_norm.csv')


# Make scatter plot of the annotation
def graph_real_and_predicted(dataset, yhat, yhat2, fname=None):
    fig, ax = plt.subplots()
    axvline(5, color='0.7')
    axhline(5, color='0.7')
    plt.scatter(yhat, yhat2)  # , c=dataset2['scale']
    ticks = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    plt.xticks(ticks)
    plt.yticks(ticks)
    plt.axis('image')
    plt.tight_layout()
    plt.title("Emotional annotations 0")
    plt.xlabel("Valence")
    plt.ylabel("Arousal")
    # plt.show() # Turn off when trying to play music
    return fig


# Plots the comparison of mapped and predicted method
def plot_compare_mapped_and_pred():
    anno_path_pred = "model_data/anno_pred_supercollider.csv"
    anno_path_mapped = "features_data/anno_mapped_supercollider.csv"
    df = pd.read_csv(anno_path_pred)
    df_2 = pd.read_csv(anno_path_mapped)
    cutoff = None
    valence_1 = df['valence'].iloc[:cutoff]
    arousal_1 = df['arousal'].iloc[:cutoff]
    valence_2 = df_2['valence'].iloc[:cutoff]
    arousal_2 = df_2['arousal'].iloc[:cutoff]
    valence_diff = abs(valence_1 - valence_2)
    arousal_diff = abs(arousal_1 - arousal_2)
    plt.tight_layout()
    plt.title("Difference model valence")
    plt.xlabel("Difference")
    plt.ylabel("Total annotations")
    plt.hist(valence_diff)
    plt.show()
    plt.hist(arousal_diff, color='r')
    plt.tight_layout()
    plt.title("Difference model arousal")
    plt.xlabel("Difference")
    plt.ylabel("Total annotations")
    plt.show()
    tot_diff = np.sqrt(np.square(valence_diff) + np.square(arousal_diff))
    print("mean:")
    print(np.mean(tot_diff))
    print(tot_diff.mean)
    plt.hist(tot_diff)
    plt.tight_layout()
    plt.title("Difference model valence + arousal")
    plt.xlabel("Difference")
    plt.ylabel("Total annotations")
    plt.show()


# Makes a machine learning model
def model_sales_MLP(dataset, dataset_pred, hidden, print_coefs=True, max_iter=10000, type='valence', min=0, max=10):
    dataset = dataset.drop('first', 1)
    Xtrn = dataset.drop('valence', 1).drop('arousal', 1)
    Ytrn = dataset[type]
    Xval = dataset.drop('valence', 1).drop('arousal', 1)
    Yval = dataset[type]
    model = MLPRegressor(hidden, validation_fraction=0, solver='lbfgs', max_iter=max_iter).fit(Xtrn, Ytrn)
    coefs = model.coefs_
    yhat = model.predict(dataset_pred)
    for i in range(len(yhat)):
        if yhat[i] < min:
            yhat[i] = min
        if yhat[i] > max:
            yhat[i] = max
    yhatval = model.predict(Xval)
    loss = np.square(Yval - yhatval).mean()
    hiddens = coefs[0].T
    final_mlp = coefs[1].flatten()
    print(yhat)
    print("-------")
    print(yhatval)
    print("------")
    print("loss")
    print(loss)
    print("------")
    coefs = list(zip([dict(zip(X.columns, h)) for h in hiddens],
                     [['output mult:', m] for m in final_mlp.flatten()],
                     [['intercept:', i] for i in model.intercepts_[0]]))
    if print_coefs:
        for idx, c in enumerate(coefs):
            f1, o, i = c
            print('feature', idx, '=', f1['tempo'].round(2), '* brand +',
                  f1['scale'].round(2), '* d2c', '+', i[1].round(2))
        output = 'yhat = '
        for fidx, v in enumerate(final_mlp):
            output = output + str(v.round(2)) + ' * feat ' + str(fidx) + ' + '
        output = output + str(model.intercepts_[1][0].round(2))
        print(output)
    return model, yhat, coefs, loss, yhatval


# Writes annotation data to SuperCollider
def write_data_to_csv(valence, arousal):
    file = open('model_data/anno_pred_supercollider.csv', 'w', newline='')
    header = 'song_number valence arousal'
    header = header.split()
    with file:
        writer = csv.writer(file)
        writer.writerow(header)
        for i in range(len(valence)):
            to_append = f'{i} {valence[i]} {arousal[i]}'
            writer.writerow(to_append.split())


if __name__ == '__main__':
    # Normalize the data first if this has not been done yet
    # normalize_data_deam("model_data/dataset_deam.csv")
    # normalize_data_super("model_data/dataset_super.csv")

    # Read the two csv files with deam and supercollider data
    dataset = pd.read_csv('model_data/dataset_deam_norm.csv')
    dataset2 = pd.read_csv('model_data/dataset_super_norm.csv')

    # Choose what dataset to predict on
    # X = dataset.drop('valence', 1).drop('arousal', 1).drop('first', 1)
    X = dataset2.drop('first', 1)

    # Makes an MLP prediction
    number_of_hidden_layers = 50, 30
    minimum_anno = -100
    maxium_anno = 100
    model, yhat_vale, coefs, loss, yhatval_vale = model_sales_MLP(dataset, X, number_of_hidden_layers, 'valence',
                                                                  min=minimum_anno, max=maxium_anno)
    model2, yhat_arous, coefs2, loss2, yhatval_arous = model_sales_MLP(dataset, X, number_of_hidden_layers, 'arousal',
                                                                       min=minimum_anno, max=maxium_anno)

    # Normalize data
    min1 = min(yhatval_vale)
    max1 = max(yhatval_vale)
    min2 = min(yhatval_arous)
    max2 = max(yhatval_arous)
    for i in range(len(yhatval_vale)):
        yhatval_vale[i] = translate(yhatval_vale[i], 0, 10, min1, max1)
        yhatval_arous[i] = translate(yhatval_arous[i], 0, 10, min2, max2)
    min1 = min(yhat_vale)
    max1 = max(yhat_vale)
    min2 = min(yhat_arous)
    max2 = max(yhat_arous)
    for i in range(len(yhat_vale)):
        yhat_vale[i] = translate(yhat_vale[i], 0, 10, min1, max1)
        yhat_arous[i] = translate(yhat_arous[i], 0, 10, min2, max2)

    # Write and plot data
    # write_data_to_csv(yhat_vale, yhat_arous)

    # Plot data
    graph_real_and_predicted(dataset, yhat_vale, yhat_arous, 'neural_network')
    # graph_real_and_predicted(dataset, yhatval_vale, yhatval_arous, 'neural_network')
    # plot_compare_mapped_and_pred()
