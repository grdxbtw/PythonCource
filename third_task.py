import logging
import argparse
import csv
import os.path
import shutil

import requests
from pprint import pprint
from datetime import datetime, timedelta


logging.basicConfig(filename='file.log',
                    level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')


def explore_data(url_, params, filename):
    """

    :param url_: url to download data about 5k user
    :param params: params to url
    :param filename: name of our file
    """
    logging.info('Exploring the data provider site  and download a csv file with users ')
    response = requests.get(url_, params=params)
    if response.status_code == 200:
        data = response.text
        with open(filename + '.csv', 'w', newline='', encoding='utf-8') as file:
            file.write(data)


def read_data(filename):
    """

    :param filename: name of our file
    :return: explored data(from given file) to our dict to work with
    """
    logging.info('reading explored data(from given file) to our dict to work with')

    with open(f'{filename}.csv', 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        data = list(csv_reader)
        # for row in csv_reader:
        #     data.append(row)
    return data


def give_filtered_data(filename, gender_=None, rows_=None):
    """
    :param filename: name of our file
    :param gender_: on of optional params given from console
    :param rows_: on of optional params given from console
    :return: return filtered data explored from our file
    """
    logging.info(' return filtered data explored from our file')
    data = read_data(filename)
    if gender_:
        filtered_data = list(filter(lambda x: x['gender'] == gender_, data))
        return filtered_data
    elif rows_:
        filtered_data = []
        counter = 0
        for f_data in data:
            if counter < rows_:
                filtered_data.append(f_data)
                counter += 1
            else:
                break
        return filtered_data
    else:
        return 'need params gender or rows'


def add_fields_to_file(file, rows):
    """
    :param rows: ew fields to our file
     :param file: name of our file
    :return rows
    """
    logging.info('add new fields to our file')
    for i, row in enumerate(rows, start=1):
        row['global_index'] = i
        row['current_time'] = datetime.now()

        match row['name.title']:
            case 'Mrs':
                row['name.title'] = 'missis'
            case 'Ms':
                row['name.title'] = 'miss'
            case 'Mr':
                row['name.title'] = 'mister'
            case 'Madame':
                row['name.title'] = 'mademoiselle'

        row['dob.date'] = datetime.strptime(row['dob.date'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%m/%d/%Y')
        row['registered.date'] = datetime.strptime(row['registered.date'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%m-%d-%Y/%H:%M:%S')

    with open(file + '.csv', 'w', newline='', encoding='utf-8') as file:
        csv_writer = csv.DictWriter(file)
        csv_writer.writerows(rows)

    logging.info("fields modified successfully.")
    return rows


def move_file_to_new_folder(destination_f):
    """
    :param destination_f: creating new destination folder

    """
    logging.info('creating new destination folder and move file to this folder')
    if not os.path.exists(destination_f):
        os.makedirs(destination_f)
        os.replace('third_task.py', destination_f)
        os.chdir(destination_f)


def parse_data(data):
    """

    :param data: explored data
    :return: structured data
    """
    logging.info('struct data')
    structured_data = {}
    for row in data:
        dob_date = datetime.strptime(row['dob.date'], '%m/%d/%Y')
        dob_decade = f"{dob_date.year // 10 * 10}-th"
        country = row['location.country']

        if dob_decade not in structured_data:
            structured_data[dob_decade] = {}
        if country not in structured_data[dob_decade]:
            structured_data[dob_decade][country] = []

        structured_data[dob_decade][country].append(row)

    return structured_data


def make_subfolders(structured_data):
    """

    :param structured_data: data structured by pattern
    """
    logging.info('make subfolders for each decades')
    for decade in structured_data.keys():
        os.makedirs(decade)


def store_data_to_folders(structured_data):
    """
    :param structured_data: data structured by pattern

    """
    logging.info("Storing data to folders")
    for decade, countries in structured_data.items():
        for country, rows in countries.items():
            folder = os.path.join(decade, country)
            os.makedirs(folder)

            filename = os.path.join(folder, f'max_age_{max(rows, key=lambda x: int(x["dob.age"]))["dob.age"]} \
            /_avg_registered_{sum(int(row["registered.age"]) for row in rows) / len(rows):.2f}\
            _popular_id_{max(rows, key=lambda x: x["id.name"])["id.name"]}.csv')
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = rows[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)


def parser_args():
    """

    :return: parse_args()
    """
    logging.info('parse ours args from console')
    parser = argparse.ArgumentParser()
    parser.add_argument('--destination_folder', required=True)
    parser.add_argument('--filename', default='output')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--gender')
    group.add_argument('--rows', type=int)
    parser.add_argument('log_level')
    return parser.parse_args()


def remove_data(structured_data):
    """

    :param year: data with year 1960>= should be removed
    :param structured_data: data structured by pattern
    :return: filtered data
    """
    logging.info('remove data with year - 1960')
    new_data = [row for row in structured_data if int(row['dob.data'][-4:]) < 1960]
    return new_data


def make_archive(destination_folder):
    logging.info('make archive')
    shutil.make_archive(destination_folder, 'zip', destination_folder)


if __name__ == '__main__':
    url = 'https://randomuser.me/api'
    params = {
        'results': 5000,
        'format': 'csv'
    }

    args = parser_args()
    # args.filename, args.gender 'down_data' 'male'
    explore_data(url, params, args.filename)
    pprint(give_filtered_data(args.filename, rows_=args.rows))
    # rows = give_filtered_data(args.filename, args.gender)
    # pprint(add_fields_to_file(args.filename, rows))
    # pprint(parse_data(rows))
    # struct_data = parse_data(rows)
    # make_subfolders(structured_data)
