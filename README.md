# Unittest. Тесты для проекта [Yatube v2](https://github.com/AnnaBerk/hw03_forms)

### Описание
Покрытие тестами проекта Yatube из спринта 4 Питон-разработчика бекенда Яндекс.Практикум. Все что нужно, это покрыть тестами проект, в учебных целях.

### Функционал
Тестирование моделей
- Протестированы модели приложения posts в Yatube

Тестирование URLs
- Проверка доступности страниц и названия шаблонов приложения Posts проекта Yatube. Проверка учитывает права доступа

Тестирование Views
- Тесты, которые проверяют, что во view-функциях используются правильные html-шаблоны

Тестирование Views
- Проверка словаря context, передаваемого в шаблон при вызове

Тестирование Forms
- при отправке валидной формы со страницы создания поста
- при отправке валидной формы со страницы редактирования поста

### Установка
Клонировать репозиторий:
```bash
git clone git@github.com:AnnaBerk/hw04_tests.git
```
Перейти в папку с проектом:
```bash
cd hw04_tests
```
Установить виртуальное окружение для проекта:
```bash
python -m venv venv
```
Активировать виртуальное окружение для проекта:

для OS Lunix и MacOS
```bash
source venv/bin/activate
```
для OS Windows
```bash
source venv/Scripts/activate
```
Установить зависимости:
```bash
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
Выполнить миграции на уровне проекта:
```bash
cd yatube
python3 manage.py makemigrations
python3 manage.py migrate
```
Запускаем тесты:
```bash
python3 manage.py test
```

