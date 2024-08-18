import os
import csv
from models import Students


def find_with_class(grade: str, directory: str = './records/csv') -> list:
    """Returns a list of all the files of a given class.

    Args:
        grade (str): The class.
        [optional] directory (str): The directory where records are kept.
            default: './records/csv'

    Returns:
        files (list): A list of all the csv files of the class.
    """
    files = []
    grade = grade.lower()
    for file_name in os.listdir(directory):
        if file_name.lower().startswith(grade):
            files.append(file_name)
    return files


def get_data(file_names: list | tuple, student: Students) -> dict:
    admn_no = student.admn_no
    processed_data = {
        '${ADMN_NO}': admn_no, '${STUDENT_NAME}': student.name,
        '$T{SCHOLASTIC_AREAS_TABLE}':
            {
                'Subjects': [],
                'Marks': [],
                'Grades': []
            }
    }
    for file_name in file_names:
        with open('./records/csv/'+file_name, 'r') as file:
            data = list(csv.reader(file))
            headers = data[0]
            locator_col = None
            for i in range(len(headers)):
                if headers[i] == 'Admn. No.':
                    locator_col = i
                    break
            if not locator_col:
                return 0
            processed_data['$T{SCHOLASTIC_AREAS_TABLE}']['Subjects'] = headers[locator_col+1:]
            for row in data:
                if row[locator_col] == admn_no:
                    for i in range(locator_col+1, len(headers)):
                        mark = row[i]
                        processed_data['$T{SCHOLASTIC_AREAS_TABLE}']['Marks'].append(mark)
                        processed_data['$T{SCHOLASTIC_AREAS_TABLE}']['Grades'].append('No grade')

            return processed_data
