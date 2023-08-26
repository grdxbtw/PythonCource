from copy import deepcopy
from unittest.mock import MagicMock, patch, call
from copy import deepcopy
import pytest

from PythonCource.main import first_part_f_task, first_part_sec_task
from PythonCource.third_task import give_filtered_data
from PythonCource.fyle import Movie_data

RETURN_V = [
    {'gender': 'male', 'id.name': 'TFN'},
    {'gender': 'fds', 'id.name': 'TFN'},
    {'gender': 'female', 'id.name': 'TFN'}
]

Pair = {'Last_day_in_cinema': '2023-09-06',
  'Popularity': 3407.1,
  'Score': 8,
  'Title': 'Spider-Man: Across the Spider-Verse'}


@pytest.fixture
def movie_data_instance():
    return Movie_data(pages_numb=1)


def test_replaced_films_success(movie_data_instance):
    movie_data_instance.films_data = [{'genre_ids': [1, 2, 3]}]
    result = movie_data_instance.replaced_films()
    expected_result = [{'genre_ids': [22, 2, 3]}]
    assert result == expected_result


def test_replaced_films_no_genre_ids(movie_data_instance):
    movie_data_instance.films_data = [{'genre_ids': []}]
    result = movie_data_instance.replaced_films()
    expected_result = [{'genre_ids': []}]
    assert result == expected_result


@patch('PythonCource.third_task.read_data')
def test_give_filtered_data_in(mock_f):
    mock_f.return_value = deepcopy(RETURN_V)
    actual = give_filtered_data('filename', 'male')
    expected = [{'gender': 'male', 'id.name': 'TFN'}]
    assert actual == expected


@patch('PythonCource.third_task.read_data')
def test_give_filtered_data_elif(mock_f):
    mock_f.return_value = deepcopy(RETURN_V)
    actual = give_filtered_data('filename', rows_=2)
    expected = [
        {'gender': 'male', 'id.name': 'TFN'},
        {'gender': 'fds', 'id.name': 'TFN'}
    ]
    assert actual == expected


@patch('PythonCource.third_task.read_data')
def test_give_filtered_data_out(mock_f):
    mock_f.return_value = deepcopy(RETURN_V)
    actual = give_filtered_data('filename')
    expected = 'need params gender or rows'
    assert actual == expected


@pytest.mark.parametrize('input_p_1, input_p_2, expected', [(Pair,'filename.csv', None), (Pair,'filename', 'wrong file (need .csv)') ])
def test_write_to_file(movie_data_instance, input_p_1, input_p_2, expected):
    actual = movie_data_instance.write_to_file(input_p_1, input_p_2)
    assert actual == expected


def test_first_part_f_task():
    """
    test for main.first_part_f_task
    """
    input_param = [[0, 0], [1, 2], [1, 5]]
    actual = first_part_f_task(input_param)
    expected = 1
    assert actual == expected

