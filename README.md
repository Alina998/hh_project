# Проект 2. Поиск вакансий
## Задание
Напишите программу, которая будет получать информацию о вакансиях с платформы hh.ru в России, сохранять ее в файл и позволять удобно работать с ней: добавлять, фильтровать, удалять.
## Требования к реализации
1. Создать абстрактный класс для работы с API сервиса с вакансиями. Реализовать класс, наследующийся от абстрактного класса, для работы с платформой hh.ru. Класс должен уметь подключаться к API и получать вакансии.
2. Создать класс для работы с вакансиями. В этом классе самостоятельно определить атрибуты, такие как название вакансии, ссылка на вакансию, зарплата, краткое описание или требования и т. п. (всего не менее четырех атрибутов). Класс должен поддерживать методы сравнения вакансий между собой по зарплате и валидировать данные, которыми инициализируются его атрибуты.
Способами валидации данных может быть проверка, указана или нет зарплата. В этом случае выставлять значение зарплаты 0 или «Зарплата не указана» в зависимости от структуры класса.

3. Определить абстрактный класс, который обязывает реализовать методы для добавления вакансий в файл, получения данных из файла по указанным критериям и удаления информации о вакансиях. Создать класс для сохранения информации о вакансиях в JSON-файл. Дополнительно, по желанию, можно реализовать классы для работы с другими форматами, например с CSV- или Excel-файлом, с TXT-файлом.
Данный класс выступит в роли основы для коннектора, заменяя который (класс-коннектор), можно использовать в качестве хранилища одну из баз данных или удаленное хранилище со своей специфической системой обращений.

В случае если какие-то из методов выглядят не используемыми для работы с файлами, то не стоит их удалять. Они пригодятся для интеграции к БД. Сделайте заглушку в коде.

4. Создать функцию для взаимодействия с пользователем. Функция должна взаимодействовать с пользователем через консоль. Возможности этой функции должны быть следующими:
ввести поисковый запрос для запроса вакансий из hh.ru;
получить топ N вакансий по зарплате (N запрашивать у пользователя);
получить вакансии с ключевым словом в описании.
Помимо этого функционала, можно придумать дополнительные возможности, которые покажутся удобными.

5. Объединить все классы и функции в единую программу.
6. Покрыть описанный функционал тестами.