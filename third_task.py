import logging
import argparse
import csv
import requests
from pprint import pprint


logging.basicConfig(filename='file.log',
                    level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')

def explore_data(url_, params, filename):
    logging.info('Exploring the data provider site  and download a csv file with users ')
    response = requests.get(url_, params=params)
    if response.status_code == 200:
        data = response.text
        with open(filename + '.csv', 'w', newline='', encoding='utf-8') as file:
            file.write(data)

def read_data(filename):
    data = []
    with open(f'{filename}.csv', 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file, delimiter=',', quotechar='\'')
        for row in csv_reader:
            data.append(row)
    return data


if __name__ == '__main__':
    url = 'https://randomuser.me/api'
    params = {
        'results': 5000,
        'format': 'csv'
    }

    # parser = argparse.ArgumentParser()
    # parser.add_argument('--destination_folder', required=True)
    # parser.add_argument('--filename', default='output')
    #
    # group = parser.add_mutually_exclusive_group()
    # group.add_argument('--gender')
    # group.add_argument('--rows', type=int)
    # parser.add_argument('log_level')
    # args = parser.parse_args()

    # args.filename
    explore_data(url, params, 'down_data')
    pprint(read_data('down_data'))

