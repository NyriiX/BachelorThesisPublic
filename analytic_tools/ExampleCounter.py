import numpy as np
import pandas as pd

from configuration.Configuration import Configuration


def main():
    config = Configuration()

    # import datasets
    y_train = np.load(config.preprocessed_folder + "train_labels.npy")  # labels of the training data
    y_test = np.load(config.preprocessed_folder + "test_labels.npy")  # labels of the training data

    # get unqiue classes and the number of examples in each
    y_train_single, y_train_counts = np.unique(y_train, return_counts=True)
    y_test_single, y_test_counts = np.unique(y_test, return_counts=True)

    # create a dataframe
    x = np.stack((y_train_single, y_train_counts)).transpose()
    x = pd.DataFrame.from_records(x)

    y = np.stack((y_test_single, y_test_counts)).transpose()
    y = pd.DataFrame.from_records(y)

    x = x.merge(y, how='outer', on=0)
    x = x.rename(index=str, columns={0: 'Class', '1_x': 'Train', '1_y': 'Test'})

    # convert column types in order to be able to sum the values
    x['Train'] = pd.to_numeric(x['Train']).fillna(value=0).astype(int)
    x['Test'] = pd.to_numeric(x['Test']).fillna(value=0).astype(int)
    x['Total'] = x[['Test', 'Train']].sum(axis=1)
    x = x.set_index('Class')

    # print the information to console
    print('----------------------------------------------')
    print('Train and test data sets:')
    print('----------------------------------------------')
    print(x)
    print('\nTotal sum examples:', x['Total'].sum(axis=0))
    print('----------------------------------------------')

    print('\n\n')

    # repeat the process for the case base
    y_train = np.load(config.case_base_folder + "train_labels.npy")  # labels of the case base
    y_train_single, y_train_counts = np.unique(y_train, return_counts=True)

    x = np.stack((y_train_single, y_train_counts)).transpose()
    x = pd.DataFrame.from_records(x)
    x = x.rename(index=str, columns={0: 'Class', 1: 'Number of cases'})
    x['Number of cases'] = pd.to_numeric(x['Number of cases']).fillna(value=0).astype(int)
    x = x.set_index('Class')

    print('----------------------------------------------')
    print('Case base:')
    print('----------------------------------------------')
    print(x)
    print('\nTotal sum examples:', x['Number of cases'].sum(axis=0))
    print('----------------------------------------------\n')


# display the example distribution of the train and test dataset as well as the case case
if __name__ == '__main__':
    main()
