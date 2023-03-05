import json
import os
import sys

dict = {}


def read_json(json_path):
    with open(json_path, 'rb') as f:
        params = json.load(f)

    return params


def write_json(json_path):
    params = read_json(json_path)
    