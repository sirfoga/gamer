# !/usr/bin/python3
# coding: utf-8

# Copyright YYYY AUTHORS
#
# YOUR COPYRIGHT HERE (IF YOU WANT IT)


""" GAMER utils and tools """

import json
import os
import shutil
from datetime import datetime
from multiprocessing import Pool

from game.models import Game


def get_pretty_date(dt):
    return dt.strftime("%H:%M:%S")


def get_name_ext(path):
    """
    :param path: str
        Path of file/folder
    :return: tuple (str, str)
        Name of file, extension of file
    """

    return os.path.splitext(path)


def is_hidden(path):
    """
    :param path: str
        Path to file/folder
    :return: bool
        True iff path is hidden (starting with a dot)
    """

    name, extension = get_name_ext(path)
    return name.startswith(".")


def ls_recurse(path, include_hidden=False):
    """
    :param path: string
        Path to directory to get list of files and folders
    :param include_hidden: bool
        Whether to include hidden files in list.
    :return: list
        List of paths in given directory recursively.
    """

    lst = []
    for f in os.listdir(path):
        hidden_file = is_hidden(f)
        if (hidden_file and include_hidden) or (not hidden_file):
            lst.append(os.path.join(path, f))
            if os.path.isdir(os.path.join(path, f)):
                lst += ls_recurse(
                    os.path.join(path, f),
                    include_hidden=include_hidden
                )  # get list of files in directory
    return lst


def get_files(path, ending):
    """
    :param path: str
        Path to folder
    :param ending: str
        Ending of files to be selected
    :return: [] of str
        List of files found (recursively) not hidden
    """

    content = ls_recurse(path)
    return [
        f for f in content
        if f.endswith(ending) and os.path.isfile(f)
    ]


def get_folders(path):
    """
    :param path: str
        Path to folder
    :param ending: str
        Ending of files to be selected
    :return: [] of str
        List of files found (recursively) not hidden
    """

    return [
        f for f in os.listdir(path) if os.path.isdir(f)
    ]


def write_data_to_json(data, output_file):
    """
    :param data: list of {} or {}
        Data to write
    :param output_file: str
        Path to output file
    :return: void
        Saves output file as .json
    """

    with open(output_file, "w") as out:
        json.dump(
            data,  # data
            out,  # file handler
            indent=4, sort_keys=True  # pretty print
        )


def run_game(labels, additional_features, output_folder):
    output_filename = os.path.join(output_folder, "output_ml.dat")
    driver = Game(
        labels,
        output_filename=output_filename,
        manual_input=False,
        verbose=True
    )
    driver.run()

    output_filename = os.path.join(output_folder,
                                   "output_ml_additional.dat")
    driver.run_additional_labels(
        additional_features=additional_features,
        labels_file=os.path.join(
            os.getcwd(),
            "library",
            "additional_labels.dat"
        ),
        output_filename=output_filename
    )


def very_intensive_calc(big_num):
    """
    :param big_num: int
        Very big number
    :return: the input
        Makes some intensive calculations
    """

    for _ in range(big_num):
        _ * _
    return big_num


def threaded_function(thread_name, big_num, processes):
    """
    :param thread_name: str
        Name of thread currently running on
    :param big_num: int
        Very big int
    :param processes: int
        Number of sub-processes to handle
    :return: void
        Run function with multi-threading
    """

    print "\t", get_pretty_date(datetime.now()), "->", thread_name, \
        "THREAD ON"
    pool = Pool(processes=processes)
    _ = pool.map(
        very_intensive_calc,
        range(1, big_num)
    )
    pool.close()
    pool.join()
    print "\t", get_pretty_date(datetime.now()), "->", thread_name, \
        "THREAD OFF"


def name_of_folder(path):
    """
    :param path: str
        Path to folder
    :return: str
        Name of folder
    """

    return os.path.basename(path)


def move_folder(original_path, output_containing_folder):
    """
    :param original_path: str
        Path to folder to move
    :param output_containing_folder: str
        Path to output containing folder
    :return: void
        Moves folder tree to output folder
    """

    contents = os.listdir(original_path)
    folder_name = name_of_folder(original_path)
    out_folder = os.path.join(output_containing_folder, folder_name)
    for sub_dir in contents:
        dir_to_move = os.path.join(original_path, sub_dir)
        shutil.move(dir_to_move, out_folder)
