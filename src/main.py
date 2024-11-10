import json
import os.path
from abc import ABC, abstractmethod
from pathlib import Path

import requests


class Parser(ABC):
    """Родительский класс для работы с API HeadHunter"""

    @abstractmethod
    def load_vacancies(self, keyword):
        pass


class HH(Parser):
    """Класс для работы с API HeadHunter"""

    def __init__(self):
        """Инициализация объекта для отправки get-запроса"""
        self._url = 'https://api.hh.ru/vacancies'
        self._headers = {'User -Agent': 'HH-User -Agent'}
        self.params = {'text': '', 'page': 0, 'per_page': 100}
        self.vacancies = []

    def load_vacancies(self, keyword):
        """Метод отправки get-запроса на сайт Head Hunter"""
        self.params['text'] = keyword
        while self.params['page'] < 20:
            response = requests.get(self._url, headers=self._headers, params=self.params)
            if response.status_code != 200:
                print("Ошибка при запросе:", response.status_code)
                break
            vacancies = response.json().get('items', [])
            self.vacancies.extend(vacancies)
            self.params['page'] += 1


class Vacancy:
    def __init__(self, vacancies):
        self.result = []
        self.__filtered_data(vacancies)

    def __filtered_data(self, vacancies):
        for vacancy in vacancies:
            salary = vacancy.get("salary")
            if salary is None:
                self.result.append(self.__create_vacancy_dict(vacancy, 0, 0))
            elif salary["currency"] == 'RUR':
                from_salary = salary.get("from", 0)
                to_salary = salary.get("to", 0)
                self.result.append(self.__create_vacancy_dict(vacancy, from_salary, to_salary))

    def __create_vacancy_dict(self, vacancy, from_salary, to_salary):
        return {
            "name": vacancy["name"],
            "city": vacancy["area"]["name"],
            "salary": {"from": from_salary, "to": to_salary},
            "url": vacancy["alternate_url"],
            "description": vacancy["snippet"]["requirement"]
        }

    def __repr__(self):
        return str(self.result)


def get_top_vacancies(vacancies, number):
    """Функция вывода топ N вакансий по зарплате"""
    return vacancies[:number] if number > 0 else vacancies


def filter_vacancy(vacancies, keyword):
    """Функция получения вакансий с ключевым словом в описании"""
    return [vacancy for vacancy in vacancies if vacancy["description"] and keyword in vacancy["description"]]


class JSONSaver(ABC):
    """Абстрактный метод для сохранения информации о вакансиях в JSON-файл"""

    @abstractmethod
    def add_vacancy(self, stock_list):
        """Метод для сохранения данных о вакансиях в файл"""
        pass

    @abstractmethod
    def delete_vacancy(self, words_del):
        """Метод для удаления не нужного файла"""
        pass


class HHVacancy(JSONSaver):
    """Класс для сохранения информации о вакансиях в JSON-файл"""

    def __init__(self, file_name_save=str(Path(__file__).resolve().parent.parent) + "\\data\\fitting_vacancies.json"):
        """Инициализатор класса"""
        self.__file_name_save = file_name_save

    def get_file_name(self):
        return self.__file_name_save

    def add_vacancy(self, json_data):
        """Метод для сохранения данных о вакансиях в файл"""
        if json_data is None:
            print("Вакансий с такими критериями не найдено")
        else:
            if os.path.exists(self.get_file_name()):
                with open(self.get_file_name(), 'r', encoding="utf-8") as file:
                    data = json.load(file)
                for i in json_data:
                    if i not in data:
                        data.append(i)
                with open(self.get_file_name(), 'w', encoding="utf-8") as file:
                    json.dump(data, file, indent=4, ensure_ascii=False)
            else:
                with open(self.get_file_name(), 'w', encoding="utf-8") as file:
                    json.dump(json_data, file, indent=4, ensure_ascii=False)

    def delete_vacancy(self, words_del):
        """Метод для удаления не нужных данных из файла"""
        data_1 = []
        if os.path.exists(self.get_file_name()):
            with open(self.get_file_name(), 'r', encoding="utf-8") as file:
                data = json.load(file)
            for i in data:
                if words_del not in i['city'] and words_del not in i['name'] and words_del not in i['description']:
                    data_1.append(i)
            with open(self.get_file_name(), 'w', encoding="utf-8") as file:
                json.dump(data_1, file, indent=4, ensure_ascii=False)
            return data_1
        else:
            return 'Файла с таким названием не существует'

    def vacancy_from_file(self, words_sample):
        """Метод для выборки нужных данных из файла"""
        result_data = []
        if os.path.exists(self.get_file_name()):
            with open(self.get_file_name(), 'r', encoding="utf-8") as file:
                data = json.load(file)
            for i in data:
                if words_sample in i["description"] or words_sample == i['name'] or words_sample == i['city']:
                    result_data.append(i)
            return result_data
        else:
            return 'Файла с таким названием не существует'

    def full_data_from_file(self):
        """Метод для получения всех данных из файла"""
        if os.path.exists(self.get_file_name()):
            with open(self.get_file_name(), 'r', encoding="utf-8") as file:
                data = json.load(file)
            return data
        else:
            return "Файл пуст"


def user_interaction():
    hh_parser = HH()
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()

    hh_parser.load_vacancies(search_query)
    vacancies = hh_parser.vacancies
    vacancy_objects = Vacancy(vacancies)

    filtered_vacancies = []
    for word in filter_words:
        filtered_vacancies.extend(filter_vacancy(vacancy_objects.result, word))

    top_vacancies = get_top_vacancies(filtered_vacancies, top_n)

    print("Топ вакансий:", top_vacancies)  # Вывод отфильтрованных вакансий

    # Сохранение вакансий в JSON файл
    save_option = input("Хотите сохранить вакансии в файл? (да/нет): ").strip().lower()
    if save_option == 'да':
        hh_vacancy_saver = HHVacancy()
        hh_vacancy_saver.add_vacancy(top_vacancies)
        print("Вакансии успешно сохранены в файл:", hh_vacancy_saver.get_file_name())


if __name__ == "__main__":
    user_interaction()
