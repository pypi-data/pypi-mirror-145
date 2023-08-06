"""General Utilities"""

import os
import errno


def standardize_path(path):
    std_path = os.path.expandvars(path)
    std_path = os.path.expanduser(std_path)
    return std_path

def ensure_exists(path):
    std_path = standardize_path(path)
    if not os.path.exists(std_path):
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), std_path)
    return std_path

def ensure_file(path):
    std_path = ensure_exists(path)
    if not os.path.isfile(std_path):
        raise IsADirectoryError(
            errno.EISDIR, os.strerror(errno.EISDIR), std_path)
    return std_path

def ensure_dir(path):
    std_path = ensure_exists(path)
    if not os.path.isdir(std_path):
        raise NotADirectoryError(
            errno.ENOTDIR, os.strerror(errno.ENOTDIR), std_path)
    return std_path
