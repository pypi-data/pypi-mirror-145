import os
import sys
from random import shuffle


def get_features(args, accounts) -> list:
    """
    Split the features as evenly as possible
    :param args:
    :param accounts:
    :return:
    """
    # empty list to store feature paths
    all_features = []

    # find every feature file and put their paths in a list
    for directory in os.walk(args.feature_dir):
        for file in directory[2]:
            if file.endswith('.feature'):
                all_features.append(os.path.join(directory[0], file))

    # ugly math to separate features as evenly as possible
    inc = -(-len(all_features) // args.processes)  # weird, yucky
    features = [all_features[i:i + inc] for i in range(0, len(all_features), inc)]
    shuffle(features)

    # return a tuple grouping accounts and features
    return list(zip(accounts, features))


def get_features_with_general_accounts(args) -> list:
    # empty list to store feature paths
    all_features = [
        os.path.join(group[0], f)
        for group in os.walk(args.feature_dir)
        for f in group[2]
        if f.endswith('.feature')
    ]

    # ugly math to separate features as evenly as possible
    inc = -(-len(all_features) // args.processes)  # weird, yucky
    features = [all_features[i:i + inc] for i in range(0, len(all_features), inc)]
    shuffle(features)

    return list(zip(list(range(len(features))), features))
