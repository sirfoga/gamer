# !/usr/bin/python3
# coding: utf-8

# Copyright YYYY AUTHORS
#
# YOUR COPYRIGHT HERE (IF YOU WANT IT)


""" Utils and tools """

import json


def get_pretty_date(dt):
    return dt.strftime("%H:%M:%S")


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
