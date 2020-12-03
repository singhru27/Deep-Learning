import tensorflow as tf
import numpy as np
from functools import reduce
import csv
import random

##########DO NOT CHANGE EXCEPT BY RUJUL#####################
PAD_TOKEN = "*PAD*"
UNK_TOKEN = "*UNK*"
WINDOW_SIZE = 50
##########DO NOT CHANGE EXCEPT BY RUJUL#####################


def get_all_data(file):
    """
    Read and parse the train and test file line by line, then tokenize the sentences to build the train and test data separately.


    :param train_file: Path to the training file.
    :param test_file: Path to the test file.
    :return all_data: A list of lists, each list representing a tokenized sentence
    """
    # data = pd.read_csv(file)
    all_data = []
    with open(file) as csvfile:
        datareader = csv.reader(csvfile, delimiter=",")
        for row in datareader:
            all_data.append(row)
    dict = {}
    max_length = 0

    # Separating all punctuation in the dataset. Creating a list of words for each entry field for each datapoint
    all_data = all_data[2:]
    labels_list = []
    for i in range(len(all_data)):
        all_data[i][1] = str(all_data[i][1]).lower()
        all_data[i][2] = str(all_data[i][2]).lower()
        all_data[i][3] = str(all_data[i][3]).lower()

        all_data[i][2] = all_data[i][2].replace(".", " .")
        all_data[i][2] = all_data[i][2].replace(",", " ,")
        all_data[i][2] = all_data[i][2].replace("!", " !")
        all_data[i][2] = all_data[i][2].replace("?", " ?")
        all_data[i][2] = all_data[i][2].replace(")", " )")
        all_data[i][2] = all_data[i][2].replace("(", "( ")

        all_data[i][3] = all_data[i][3].replace(".", " .")
        all_data[i][3] = all_data[i][3].replace(",", " ,")
        all_data[i][3] = all_data[i][3].replace("!", " !")
        all_data[i][3] = all_data[i][3].replace("?", " ?")
        all_data[i][3] = all_data[i][3].replace(")", " )")
        all_data[i][3] = all_data[i][3].replace("(", "( ")

        all_data[i][1] = all_data[i][1].split(",")
        all_data[i][2] = all_data[i][2].split()
        all_data[i][3] = all_data[i][3].split()
        all_data[i][3].append(all_data[i][4])
        labels_list.append(all_data[i][0])
        all_data[i] = [
            all_data[i][1],
            all_data[i][2],
            all_data[i][3],
        ]
        # Creating a dictionary mapping words to word counts, to be used for UNKing later on
        for j in range(1, 4):
            for word in all_data[i][j]:
                if (word in dict) == False:
                    dict[word] = 0
                else:
                    dict[word] = dict[word] + 1
    # UNKing the words in the dataset
    for i in range(len(all_data)):
        for j in range(1, 4):
            for k in range(len(all_data[i][j])):
                if dict[all_data[i][j][k]] < 2:
                    all_data[i][j][k] = UNK_TOKEN
    return labels_list, all_data


def build_vocab(all_data):
    """
    Returns a dict mapping from words to IDs using the train data set
    param: all_data - List of sentences
    return: all_data - List of sentences converted to ID form
    return: vocab_didct - Dictionary mapping from words to ID
    """
    # Creating a vocabulary dictionary, mapping from words to their ids
    id_num = 0
    vocab_dict = {}
    for i in range(len(all_data)):
        for j in range(1, 4):
            for word in all_data[i][j]:
                if word not in vocab_dict:
                    vocab_dict[word] = id_num
                    id_num += 1
    return vocab_dict


def convert_to_id(all_data, vocab_dict):
    """
    Converts a list of tokenized sentences into a list of id lists
    param: all_data - List of sentences
    return: all_data - List of sentences converted to ID form
    return: vocab_didct - Dictionary mapping from words to ID
    """
    # Converting all words to their corresponding IDs
    for i in range(len(all_data)):
        for j in range(1, 4):
            word_list = []
            for word in all_data[i][j]:
                if word not in vocab_dict:
                    word_list.append(vocab_dict[UNK_TOKEN])
                else:
                    word_list.append(vocab_dict[word])
            all_data[i][j] = np.array(word_list)

    return all_data


def split_data(all_data):
    """
    Splits the entire set of data into a training set and a testing set
    Parameters:
        - all_data: The full dataset
    Returns:
        - train_data: The training dataset
        - test_data: The testing dataset
    """
    num_elements = len(all_data)
    train_percentage = 0.8
    test_percentage = 0.2
    random.shuffle(all_data)
    # Creating the train and test datasets, in list form
    num_in_train = int(train_percentage * num_elements)
    train_data = all_data[0:num_in_train]
    test_data = all_data[num_in_train:num_elements]
    return (train_data, test_data)


def pad_data(parsed_data):
    """
    Pads the dataset according to the window size
    Parameters:
        - all_data: The full dataset with all the text. Column 0 contains the average hours per course. Columns 1 -> 3 contains
          text entry for the three separate text entry fields
    Returns:
        - padded_data: The dataset shortened to window size. Sentences that are too short have been replaced with a padding token
    """

    for i in range(len(parsed_data)):
        # Skipping the first column, since it has the average hours (what we are trying to predict)
        for j in range(1, len(parsed_data[0])):
            parsed_data[i][j] = parsed_data[i][j][0:WINDOW_SIZE]
            parsed_data[i][j] = parsed_data[i][j] + [PAD_TOKEN] * (
                WINDOW_SIZE - len(parsed_data[i][j])
            )
    return parsed_data


def convert_to_numpy(data_id):
    """
    Converts data in list form to NumPy array
    Parameters:
        - data_id: Data in list form
    Returns:
        - data_text[1->3]: All the text
    """
    labels = np.array(data_id)[:, 0]
    data_id = data_id[1:]
    data_id = np.array(data_id)
    print(data_id.shape)
    text_1 = data_id[:, 1]
    text_2 = data_id[:, 2]
    text_3 = data_id[:, 3]
    return labels, text_1, text_2, text_3


def preprocess_data(filepath):
    pass


if __name__ == "__main__":
    (labels,) = get_all_data("2020-2019 Review Data.csv")
    all_data = pad_data(all_data)
    train_data, test_data = split_data(all_data)
    vocab_dict = build_vocab(train_data)
    train_data_id = convert_to_id(train_data, vocab_dict)
    test_data_id = convert_to_id(test_data, vocab_dict)
    train_labels, train_text1, train_text2, train_text3 = convert_to_numpy(
        train_data_id
    )
    print(train_text1.shape)
