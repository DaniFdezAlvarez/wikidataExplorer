__author__ = 'Dani'

import os


def rel_path_to_file(rel_path, base_file):
    """
    Ir receives a relative path and the path to the file in which it was written (base_file).
    It returns the absolute path obtained from calculating a rel_path from base_file.
    Example:

    base_file: /root/something/project/test/a_test.py
    real_path: ../files/a_file.txt

    result ---> /root/something/project/files/a_file.txt

    """
    steps_behind = max(rel_path.count("../"),
                       rel_path.count("..\\"))

    dir_target = os.path.dirname(base_file)
    while steps_behind != 0:
        if dir_target[-1] in ['/', '\\']:
            dir_target = dir_target[:-1]
        dir_target = os.path.dirname(dir_target)
        steps_behind -= 1

    path_forward = rel_path.replace("../", "").replace("..\\", "")

    # print os.path.normpath(os.path.join(dir_target, path_forward))
    return os.path.normpath(os.path.join(dir_target, path_forward))
