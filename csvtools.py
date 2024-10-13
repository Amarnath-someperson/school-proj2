import os
import csv
from models import Students


def find_with_class(grade: str, directory: str = './records/csv') -> list:
    """Returns a list of all the files of a given class.

    Args:
        grade (str): The class.
        directory (str): The directory where records are kept.
            default: './records/csv'

    Returns:
        files (list): A list of all the csv files of the class.
    """
    files = []
    grade = grade.lower()

    for file_name in os.listdir(directory):
        if file_name.lower().startswith(grade) or file_name.lower().startswith('0'+grade):
            files.append(file_name)
    return files


def get_data(file_names: list | tuple, student: Students) -> list:
    """Returns a list with data of the student gathered from all csv files. 
    Each element in the list is a dictionary with the variables from the 
    template docx file as keys, and their replacements as values.

    Args:
        file_names (list | tuple): the files to search for the student's
            records.
        student (Students): the student whose records are to be searched.

    Raises:
        Exception (Exception): thrown if no admission number column is found.
        e (Exception): any error thrown when trying to find subjects and their max. marks.

    Returns:
        list: the list with all the reports of the student from records/csv.
    """
    admn_no = student.admn_no
    processed_data_list = []
    for file_name in file_names:
        processed_data = {
            '${ADMN_NO}': admn_no, '${STUDENT_NAME}': student.name,
            '${CLASS}': str(student.grade), '${CLASS_DIV}': student.div,
            '${ROLL_NO}': str(student.roll_no),
            '$T{SCHOLASTIC_AREAS_TABLE}':
            {
                'Subject': [],
                'Mark': [],
                'Percentage (%)': [],
                'Grade': []
            },
            '${PERCENTAGE}': -1
        }
        with open('./records/csv/'+file_name, 'r') as file:
            data = list(csv.reader(file))
            headers = data[0]
            locator_col = None

            for i in range(len(headers)):
                if 'admn' in headers[i].lower() and 'no' in headers[i].lower():
                    locator_col = i
                    break
            if locator_col is None:
                raise RuntimeError(
                    f"A column with admission numbers was not found in file ./records/csv/{file_name}")

            subject_totals = []
            subjects = []

            for i in headers[locator_col+1:]:
                split_col_name = i.partition('(')
                try:
                    subjects.append(split_col_name[0].strip())
                    subject_totals.append(
                        int(split_col_name[2].removesuffix(')')))
                except Exception as e:
                    raise e

            processed_data['$T{SCHOLASTIC_AREAS_TABLE}']['Subject'] = subjects

            # sum of all the percentages obtained by the student, for average calc.
            percent_sum = 0

            for row in data:
                if row == []:
                    continue  # for extra rows with no data
                if row[locator_col] == admn_no:
                    for i in range(locator_col+1, len(headers)):
                        mark = row[i]
                        processed_data['$T{SCHOLASTIC_AREAS_TABLE}']['Mark'].append(
                            mark)
                        percent = int(mark)/subject_totals[i-locator_col-1]*100
                        percent_sum += percent
                        processed_data['$T{SCHOLASTIC_AREAS_TABLE}']['Percentage (%)'].append(
                            str(percent))
                        processed_data['$T{SCHOLASTIC_AREAS_TABLE}']['Grade'].append(
                            'No grade')

            processed_data['${PERCENTAGE}'] = str(
                percent_sum/len(subject_totals))
            processed_data['${ACAD_SESSION}'] = file_name[3:5] + \
                '-' + file_name[5:7]
            processed_data['${EXAM_NAME}'] = file_name[7:10]
            if len(processed_data['$T{SCHOLASTIC_AREAS_TABLE}']['Mark']) == 0:
                sub_len = len(
                    processed_data['$T{SCHOLASTIC_AREAS_TABLE}']['Subject'])
                na_list = ['N/A' for i in range(sub_len)]
                processed_data['$T{SCHOLASTIC_AREAS_TABLE}']['Mark'] = na_list
                processed_data['$T{SCHOLASTIC_AREAS_TABLE}']['Grade'] = na_list
                processed_data['$T{SCHOLASTIC_AREAS_TABLE}']['Percentage (%)'] = na_list
            processed_data_list.append(processed_data)

    return processed_data_list
