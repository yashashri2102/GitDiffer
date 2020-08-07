#!/usr/bin/python

from flask import Flask, jsonify, render_template
from subprocess import Popen, PIPE
import re

app = Flask(__name__)


@app.route('/')
def hello_world():
    file_data = get_file_content()
    diff_indexes, file_names = get_diff_file_index(file_data)
    diff_data = get_diff_data_with_file(diff_indexes, file_data, file_names)
    if not file_data:
        return "Could not load diff."
    return render_template('display.html', file_data=diff_data, file_names=file_names)


def get_file_content():
    import pdb;pdb.set_trace()

    with open(".diff.txt", "w+") as f:
        Popen(["git", "diff"], stdout=f, stderr=f)
        f.seek(0)
        return f.readlines()
    return "Could not load diff.1"


def get_diff_file_index(file_data):
    index_list = list()
    file_name = list()
    for index, line in enumerate(file_data):
        if line.lstrip().startswith('diff --git '):
            result = re.search('diff --git a/(.*)b/', line.lstrip())
            if result:
                file_name.append(result.group(1))
                index_list.append(index)
    print(index_list)
    return index_list, file_name


def get_diff_data_with_file(index_list, file_data, file_name):
    diff_data = list()
    for index in range(len(index_list) - 1):
        diff_data.append({
            'file_name': file_name[index],
            'diff_file_data': file_data[index_list[index]: index_list[index + 1]]})
    if file_data:
        diff_data.append({
            'file_name': file_name[-1],
            'diff_file_data': file_data[index_list[-1]: len(file_data)]})
    return diff_data


if __name__ == '__main__':
    app.run()

