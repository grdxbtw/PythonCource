import logging
import argparse
import csv
import requests


logging.basicConfig(filename='file.log',
                    level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')

def explore_data(url_, filename):
    logging.info('Exploring the data provider site  and download a csv file with users ')
    response = requests.get(url_)
    if requests.status_codes == 200:
        with open(filename + '.csv', 'w', newline='') as file:
           file.write(response.content)





if __name__ == '__main__':
    url = 'https://randomuser.me/api/'

    parser = argparse.ArgumentParser()
    parser.add_argument('--destination_folder', required=True)
    parser.add_argument('--filename', default='output')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--gender')
    group.add_argument('--rows', type=int)
    parser.add_argument('log_level')
    args = parser.parse_args()

    explore_data(url, args.filename)


