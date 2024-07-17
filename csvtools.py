import os
import csv


def find_with_class(grade: str, directory: str = './records/csv') -> list:
    """Returns a list of all the files of a given class.

    Args:
        grade (str): The class.
        [optional] directory (str): The directory where records are kept.
            default: './records/csv'

    Returns:
        files: A list of all the csv files of the class.
    """
    files = []
    grade = grade.lower()
    for file_name in os.listdir(directory):
        if file_name.lower().startswith(grade):
            files.append(file_name)
    return files


def get_data(key: str) -> dict:
    pass
