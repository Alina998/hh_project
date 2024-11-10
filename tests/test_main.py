import json
import os
import unittest
from unittest.mock import patch

from src.main import HH, HHVacancy, Vacancy, filter_vacancy, get_top_vacancies


class TestHHParser(unittest.TestCase):

    @patch('requests.get')
    def test_load_vacancies_success(self, mock_get):
        # Настройка mock-ответа
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'items': [
                {
                    'name': 'Программист',
                    'area': {'name': 'Москва'},
                    'salary': {'from': 100000, 'to': 150000, 'currency': 'RUR'},
                    'alternate_url': 'http://example.com',
                    'snippet': {'requirement': 'Знание Python'}
                }
            ]
        }

        parser = HH()
        parser.load_vacancies('Программист')
        self.assertEqual(parser.vacancies[0]['name'], 'Программист')

    @patch('requests.get')
    def test_load_vacancies_error(self, mock_get):
        mock_get.return_value.status_code = 404
        parser = HH()
        parser.load_vacancies('Программист')
        self.assertEqual(len(parser.vacancies), 0)


class TestVacancy(unittest.TestCase):

    def test_filtered_data(self):
        vacancies_data = [
            {
                'name': 'Программист',
                'area': {'name': 'Москва'},
                'salary': {'from': 100000, 'to': 150000, 'currency': 'RUR'},
                'alternate_url': 'http://example.com',
                'snippet': {'requirement': 'Знание Python'}
            },
            {
                'name': 'Тестировщик',
                'area': {'name': 'Санкт-Петербург'},
                'salary': None,
                'alternate_url': 'http://example.com',
                'snippet': {'requirement': 'Знание тестирования'}
            }
        ]
        vacancy_obj = Vacancy(vacancies_data)
        self.assertEqual(len(vacancy_obj.result), 2)
        self.assertEqual(vacancy_obj.result[0]['salary']['from'], 100000)
        self.assertEqual(vacancy_obj.result[1]['salary']['from'], 0)


class TestHHVacancy(unittest.TestCase):

    def setUp(self):
        self.file_name = 'test_vacancies.json'
        self.hh_vacancy = HHVacancy(self.file_name)

    def tearDown(self):
        if os.path.exists(self.file_name):
            os.remove(self.file_name)

    def test_add_vacancy(self):
        vacancies = [{'name': 'Программист', 'city': 'Москва', 'description': 'Знание Python'}]
        self.hh_vacancy.add_vacancy(vacancies)

        with open(self.file_name, 'r', encoding='utf-8') as file:
            data = json.load(file)

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'Программист')

    def test_delete_vacancy(self):
        vacancies = [{'name': 'Программист', 'city': 'Москва', 'description': 'Знание Python'}]
        self.hh_vacancy.add_vacancy(vacancies)
        self.hh_vacancy.delete_vacancy('Программист')

        with open(self.file_name, 'r', encoding='utf-8') as file:
            data = json.load(file)

        self.assertEqual(len(data), 0)

    def test_vacancy_from_file(self):
        vacancies = [{'name': 'Программист', 'city': 'Москва', 'description': 'Знание Python'}]
        self.hh_vacancy.add_vacancy(vacancies)
        result = self.hh_vacancy.vacancy_from_file('Python')

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'Программист')

    def test_full_data_from_file(self):
        vacancies = [{'name': 'Программист', 'city': 'Москва', 'description': 'Знание Python'}]
        self.hh_vacancy.add_vacancy(vacancies)
        result = self.hh_vacancy.full_data_from_file()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'Программист')


def test_filter_vacancy():
    vacancies = [
        {'description': 'Требования 1'},
        {'description': 'Требования 2'},
        {'description': None}
    ]
    filtered = filter_vacancy(vacancies, 'Требования 1')
    assert len(filtered) == 1
    assert filtered[0]['description'] == 'Требования 1'


def test_get_top_vacancies():
    vacancies = [
        {'name': 'Вакансия 1'},
        {'name': 'Вакансия 2'},
        {'name': 'Вакансия 3'}
    ]
    top_vacancies = get_top_vacancies(vacancies, 2)
    assert len(top_vacancies) == 2
    assert top_vacancies[0]['name'] == 'Вакансия 1'
    assert top_vacancies[1]['name'] == 'Вакансия 2'


if __name__ == '__main__':
    unittest.main()
